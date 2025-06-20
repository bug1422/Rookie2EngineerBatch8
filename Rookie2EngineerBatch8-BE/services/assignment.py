from datetime import date
from sqlalchemy.orm import Session
from core.exceptions import BusinessException, PermissionDeniedException, ValidationException, NotFoundException
from core.logging_config import get_logger
from enums.asset.state import AssetState
from enums.assignment.state import AssignmentState
from enums.shared.location import Location
from enums.user.status import Status
from repositories.assignment import AssignmentRepository
from schemas.assignment import AssignmentCreate, AssignmentRead, AssignmentUpdate, AssignmentStateUpdate, AssignmentUpdateResponse, AssignmentReadDetail, AssignmentReadSimple
from schemas.query.filter.assignment import AssignmentFilter
from schemas.shared.paginated_param import PaginationParams
from schemas.shared.paginated_response import PaginatedResponse
from schemas.assignment import AssignmentUserReadByUID
from schemas.asset import AssetRead, AssetUpdate
from schemas.user import UserRead
from services.asset import AssetService
from services.user import UserService
from schemas.asset import AssetHistory

logger = get_logger(__name__)


class AssignmentService:
    def __init__(self, db: Session):
        self.repository = AssignmentRepository(db)

    def read_assignments_paginated(self, assignment_filter: AssignmentFilter, current_user: UserRead) -> PaginatedResponse[AssignmentRead]:
        assignments = self.repository.get_assignments_paginated(assignment_filter, current_user)
        return assignments

    def read_assignment(self, assignment_id: int, current_user: UserRead) -> AssignmentReadDetail:
        assignment = self.repository.get_assignment_by_id_no_join(assignment_id)

        if not assignment:
            raise NotFoundException(detail=f"Assignment with id {assignment_id} not found")

        related_asset = AssetService(self.repository.db).read_asset(assignment.asset_id, current_user.location)
        if not related_asset:
            raise NotFoundException(detail=f"Asset with id {assignment.asset_id} in this assignment not found")

        # if related_asset.asset_location != current_user.location:
        #     raise BusinessException(detail="You don't have permission to view assignment from other location")

        user_service = UserService(self.repository.db)

        assignee = user_service.read_user(assignment.assigned_to_id)
        if not assignee:
            raise NotFoundException(detail=f"User with id {assignment.assigned_to_id} in this assignment not found")

        assigner = user_service.read_user(assignment.assigned_by_id)
        if not assigner:
            raise NotFoundException(detail=f"User with id {assignment.assigned_by_id} in this assignment not found")

        return AssignmentReadDetail(
            assignment=AssignmentReadSimple(
                id=assignment.id,
                assign_date=assignment.assign_date,
                assignment_state=assignment.assignment_state,
                assignment_note=assignment.assignment_note
            ),
            assigned_to_user=UserRead.model_validate(assignee, from_attributes=True),
            assigned_by_user=UserRead.model_validate(assigner, from_attributes=True),
            asset=AssetRead.model_validate(related_asset, from_attributes=True)
        )

    def edit_assignment(
        self, assignment_id: int, assignment_update: AssignmentUpdate, current_admin: UserRead
    ) -> AssignmentRead:
        assignment = self.repository.get_assignment_by_id_no_join(assignment_id)
        if not assignment:
            raise NotFoundException(f"Assignment with ID {assignment_id} not found.")

        self.validate_assigned_user(assignment_update.assigned_to_id, current_admin.location)

        try:
            updated_assignment = self.repository.update_assignment(assignment_id, assignment_update, current_admin.id)
        except Exception as e:
            raise ValidationException(f"Failed to update assignment: {str(e)}")

        return updated_assignment

    def get_user_assignments_until_current_date(
        self, pagination: PaginationParams, current_user: UserRead
    ) -> PaginatedResponse[AssignmentUserReadByUID]:
        """
        Get all assignments for a user until current date.
        Users can only view their own assignments unless they are admin.
        Only show assignments that are not declined or returned.
        """
        user_id = current_user.id

        current_date = date.today()
        assignments = self.repository.get_user_assignments_paginated(
            pagination, current_date, user_id
        )
        return assignments

    def update_assignment_state(
        self, assignment_id: int, assignment_update: AssignmentStateUpdate, user_id: int, user_location: Location
    ) -> AssignmentUpdateResponse:
        """
        Update an assignment's state by ID.
        """
        assignment = self.repository.get_assignment_by_id(assignment_id)
        if not assignment:
            logger.error(f"Assignment {assignment_id} not found")
            raise NotFoundException(detail="Assignment not found")
        if assignment.assigned_to_id != user_id:
            logger.error(
                f"User {user_id} attempted to update assignment {assignment_id} assigned to user {assignment.assigned_to_id}"
            )
            raise PermissionDeniedException(
                detail="You can only update your own assignments"
            )
        if assignment.assignment_state in [AssignmentState.DECLINED, AssignmentState.ACCEPTED, AssignmentState.RETURNED]:
            logger.error(
                f"User {user_id} attempted to update assignment {assignment_id} that is already {assignment.assignment_state}"
            )
            raise PermissionDeniedException(
                detail="You can only update assignments that are waiting for acceptance"
            )
        updated_assignment = self.repository.update_assignment_state(
            assignment_id, assignment_update
        )

        # If the assignment is declined, update the asset state to "Available"
        if assignment_update.assignment_state == AssignmentState.DECLINED:
            logger.info(
                f"Assignment {assignment_id} declined, updating asset {assignment.asset_id} to Available state"
            )
            asset_service = AssetService(self.repository.db)
            asset = asset_service.read_asset(assignment.asset_id,user_location)
            asset_update = AssetUpdate(asset_state=AssetState.AVAILABLE)
            asset_service.repository.update_asset(asset.id, asset_update)
        return updated_assignment

    def create_assignment(self, assignment: AssignmentCreate, assigned_by_id: int, current_user: UserRead) -> AssignmentRead:
        """Create a new assignment

        Args:
            assignment: The assignment to create with all required fields
            assigned_by_id: ID of the user creating the assignment

        Returns:
            AssignmentRead: The created assignment with all related data

        Raises:
            NotFoundException: If user or asset is not found
            BusinessException: If asset is not available or assign date is invalid
        """
        # Check if assigned user exists
        user_service = UserService(self.repository.db)
        try:
            assigned_user = user_service.read_user(assignment.assigned_to_id)
        except NotFoundException:
            raise NotFoundException(f"User with ID {assignment.assigned_to_id} not found")

        # Check if asset exists
        asset_service = AssetService(self.repository.db)
        asset = asset_service.repository.get_asset_by_id(assignment.asset_id)
        if not asset:
            raise NotFoundException(f"Asset with ID {assignment.asset_id} not found")

        # Check if asset is available for assignment
        if not self.repository.is_asset_available(assignment.asset_id):
            raise BusinessException(detail=f"Asset with ID {assignment.asset_id} is not available for assignment")

        # Create the assignment object
        from models.assignment import Assignment
        db_assignment = Assignment(
            asset_id=assignment.asset_id,
            assigned_to_id=assignment.assigned_to_id,
            assigned_by_id=assigned_by_id,
            assign_date=assignment.assign_date,
            assignment_state=AssignmentState.WAITING_FOR_ACCEPTANCE,
            assignment_note=assignment.assignment_note
        )

        # Save to database through repository
        try:
            db_assignment = self.repository.create_assignment(db_assignment)

            # Update asset state to "Assigned" immediately after creating assignment
            logger.info(f"Assignment {db_assignment.id} created, updating asset {db_assignment.asset_id} to Assigned state")
            asset_service = AssetService(self.repository.db)
            asset_update = AssetUpdate(asset_state=AssetState.ASSIGNED)
            asset_service.repository.update_asset(db_assignment.asset_id, asset_update)
            logger.info(f"Asset {db_assignment.asset_id} state updated to Assigned")

            # Get usernames and asset for the response
            user_service = UserService(self.repository.db)
            assigned_to = user_service.read_user(db_assignment.assigned_to_id)
            assigned_by = user_service.read_user(db_assignment.assigned_by_id)

            # Get updated asset info (with new state)
            asset = asset_service.read_asset(db_assignment.asset_id, current_user.location)

            # Create response with all required fields
            response = AssignmentRead(
                id=db_assignment.id,
                asset_id=db_assignment.asset_id,
                assigned_to_id=db_assignment.assigned_to_id,
                assigned_by_id=db_assignment.assigned_by_id,
                assign_date=db_assignment.assign_date.date(),
                assignment_state=db_assignment.assignment_state,
                assignment_note=db_assignment.assignment_note,
                assigned_to_username=assigned_to.username,
                assigned_by_username=assigned_by.username,
                asset=AssetRead.model_validate(asset, from_attributes=True)
            )

            return response

        except Exception as e:
            self.repository.db.rollback()
            logger.error(f"Error creating assignment: {str(e)}")
            raise BusinessException(detail=f"Failed to create assignment: {str(e)}")

    def delete_assignment(self, assignment_id: int, location: Location) -> None:
        """
        Delete an assignment by ID.
        """
        assignment = self.repository.get_assignment_by_id(assignment_id)

        if not assignment:
            logger.error(f"Assignment {assignment_id} not found")
            raise NotFoundException(detail="Assignment not found")

        if location != assignment.asset.asset_location:
            logger.error(f"Assignment {assignment_id} is not in the same location as the user")
            raise BusinessException(
            detail="You can only delete assignments that are in the same location as you"
            )

        if assignment.assignment_state in [AssignmentState.ACCEPTED, AssignmentState.RETURNED]:
            logger.error(f"Assignment {assignment_id} is {assignment.assignment_state} and cannot be deleted")
            raise BusinessException(
            detail="You can only delete assignments that are 'Waiting for acceptance' or 'Declined'"
            )

        # Change asset state to Available
        asset_service = AssetService(self.repository.db)
        asset = asset_service.read_asset(assignment.asset_id, location)
        asset_update = AssetUpdate(asset_state=AssetState.AVAILABLE)
        asset_service.repository.update_asset(asset.id, asset_update)
        logger.info(f"Asset {asset.id} state updated to Available after deleting assignment {assignment_id}")

        self.repository.delete_assignment(assignment)
        

    def validate_assigned_user(self, user_id: int | None, admin_location: Location) -> None:
        if not user_id:
            return

        assigned_user = UserService(self.repository.db).read_user(user_id)

        if assigned_user.location != admin_location:
            raise ValidationException(
                f"User with ID {user_id} belongs to {assigned_user.location.value} location, but assignment is for {admin_location.value} location"
            )

        if assigned_user.status != Status.ACTIVE:
            raise ValidationException(f"User with ID {user_id} is not active (current status: {assigned_user.status.value})")

    def validate_asset(self, asset_id: int | None, admin_location: Location) -> None:
        if not asset_id:
            return

        asset = AssetService(self.repository.db).read_asset(asset_id, admin_location)

        if asset.asset_state != AssetState.AVAILABLE:
            raise ValidationException(
                f"Asset with ID {asset_id} is not available (current state: {asset.asset_state.value})"
            )
            
    def get_assignment_history(self, asset_id: int, filter: AssignmentFilter, current_user: UserRead) -> PaginatedResponse[AssetHistory]:
        # Validate that asset_id is provided
        if not filter.asset_id:
            raise ValidationException("Asset ID is required for assignment history")
        
        assignments = self.repository.get_assignment_history(asset_id, filter)
        return assignments
