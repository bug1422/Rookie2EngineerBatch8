from datetime import date, datetime, timezone
from sqlalchemy import func
from sqlalchemy.orm import Session, aliased, joinedload
from core.exceptions import NotFoundException
from enums.assignment.state import AssignmentState

from models.asset import Asset
from models.category import Category
from schemas.query.filter.assignment import AssignmentFilter, HomeAssignmentFilter
from schemas.assignment import AssignmentRead, AssignmentUpdate, AssignmentStateUpdate, AssignmentUpdateResponse, AssignmentUserReadByUID
from schemas.asset import AssetRead
from schemas.shared.paginated_response import PaginatedResponse, PaginationMeta
from models.assignment import Assignment
from models.user import User
from schemas.query.sort.sort_type import SortAssignmentBy, SortDirection, SortHomeAssignmentBy
from core.logging_config import get_logger
from schemas.user import UserRead
from schemas.asset import AssetHistory
from models.request import Request

logger = get_logger(__name__)

class AssignmentRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_assignments_paginated(self, assignment_filter: AssignmentFilter, current_user: UserRead) -> PaginatedResponse[AssignmentRead]:
        # Use aliased() to create distinct aliases for the User table
        # Create aliases for the User table
        AssignedToUser = aliased(User)
        AssignedByUser = aliased(User)
        
        query = self.db.query(Assignment)\
            .join(Asset, Assignment.asset_id == Asset.id)\
            .join(AssignedToUser, Assignment.assigned_to_id == AssignedToUser.id, isouter=True)\
            .join(AssignedByUser, Assignment.assigned_by_id == AssignedByUser.id, isouter=True)\
            .filter(
                    Assignment.assignment_state != AssignmentState.RETURNED
                )\
            .filter(
                Assignment.assigned_to_user.has(User.location == current_user.location)
            )
        
        if assignment_filter.state:
            query = query.filter(Assignment.assignment_state == assignment_filter.state)
        
        if assignment_filter.assign_date:
            query = query.filter(Assignment.assign_date == assignment_filter.assign_date)
        
        if assignment_filter.asset_id:
            query = query.filter(Assignment.asset_id == assignment_filter.asset_id)
        
        if assignment_filter.search:
            query = query.filter(
                (Asset.asset_code.ilike(f"%{assignment_filter.search}%"))
                | (Asset.asset_name.ilike(f"%{assignment_filter.search}%"))
                | (AssignedToUser.username.ilike(f"%{assignment_filter.search}%"))
            )
        
        if assignment_filter.sort_by:
            if assignment_filter.sort_by == SortAssignmentBy.ID:
                query = query.order_by(
                    Assignment.id.asc()
                    if assignment_filter.sort_direction == SortDirection.ASC
                    else Assignment.id.desc()
                )
            elif assignment_filter.sort_by == SortAssignmentBy.ASSET_CODE:
                query = query.order_by(
                    Asset.asset_code.asc()
                    if assignment_filter.sort_direction == SortDirection.ASC
                    else Asset.asset_code.desc()
                )
            elif assignment_filter.sort_by == SortAssignmentBy.ASSET_NAME:
                query = query.order_by(
                    Asset.asset_name.asc()
                    if assignment_filter.sort_direction == SortDirection.ASC
                    else Asset.asset_name.desc()
                )
            elif assignment_filter.sort_by == SortAssignmentBy.ASSIGNED_TO:
                query = query.order_by(
                    AssignedToUser.username.asc()
                    if assignment_filter.sort_direction == SortDirection.ASC
                    else AssignedToUser.username.desc()
                )
            elif assignment_filter.sort_by == SortAssignmentBy.ASSIGNED_BY:
                query = query.order_by(
                    AssignedByUser.username.asc()
                    if assignment_filter.sort_direction == SortDirection.ASC
                    else AssignedByUser.username.desc()
                )
            elif assignment_filter.sort_by == SortAssignmentBy.ASSIGN_DATE:
                query = query.order_by(
                    Assignment.assign_date.asc()
                    if assignment_filter.sort_direction == SortDirection.ASC
                    else Assignment.assign_date.desc()
                )
            elif assignment_filter.sort_by == SortAssignmentBy.STATE:
                query = query.order_by(
                    Assignment.assignment_state.asc()
                    if assignment_filter.sort_direction == SortDirection.ASC
                    else Assignment.assignment_state.desc()
                )
            elif assignment_filter.sort_by == SortAssignmentBy.UPDATED_AT:
                query = query.order_by(
                    Assignment.updated_at.asc()
                    if assignment_filter.sort_direction == SortDirection.ASC
                    else Assignment.updated_at.desc()
                )

        total = query.count()
        total_pages = (total + assignment_filter.size - 1) // assignment_filter.size

        assignments = (
            query.offset((assignment_filter.page - 1) * assignment_filter.size)
            .limit(assignment_filter.size)
            .all()
        )

        # Map Assignment models to AssignmentRead DTOs
        assignment_reads = [
            AssignmentRead(
                id=assignment.id,
                assign_date=assignment.assign_date.date(),
                assignment_state=assignment.assignment_state,
                asset_id=assignment.asset_id,
                assigned_to_id=assignment.assigned_to_id,
                assigned_by_id=assignment.assigned_by_id,
                assigned_to_username=assignment.assigned_to_user.username,
                assigned_by_username=assignment.assigned_by_user.username,
                assignment_note=assignment.assignment_note,
                asset=AssetRead.model_validate(assignment.asset, from_attributes=True)
            )
            for assignment in assignments
        ]
        return PaginatedResponse(
            data=assignment_reads,  # Return DTOs instead of models
            meta=PaginationMeta(
                total=total,
                total_pages=total_pages,
                page=assignment_filter.page,
                page_size=assignment_filter.size,
            ),
        )

    def get_assignment_by_id(self, assignment_id: int) -> Assignment:
        return ( 
                self.db.query(Assignment)
                .options(
                    joinedload(Assignment.assigned_to_user),
                    joinedload(Assignment.assigned_by_user),
                    joinedload(Assignment.asset).joinedload(Asset.category)
                )
                .filter(Assignment.id == assignment_id)
                .first()
            )
    
    def update_assignment(
        self, assignment_id: int, assignment_update: AssignmentUpdate, assigned_by_id: int
    ) -> AssignmentUpdateResponse:
        """Update an existing assignment."""
        existing_assignment = self.db.query(Assignment).filter(Assignment.id == assignment_id).first()
        if not existing_assignment:
            raise NotFoundException(f"Assignment with ID {assignment_id} not found")
            
        # Update only the fields that were provided in the update
        for key, value in assignment_update.model_dump(exclude_unset=True).items():
            setattr(existing_assignment, key, value)
        
        # Ensure we always update the assigned_by_id by the current admin
        existing_assignment.assigned_by_id = assigned_by_id    
        existing_assignment.updated_at = datetime.now(timezone.utc)
        self.db.commit()
        self.db.refresh(existing_assignment)
        return existing_assignment
    

    def get_user_assignments_paginated(
        self, pagination: HomeAssignmentFilter, end_date: date, user_id: int
    ) -> PaginatedResponse[AssignmentUserReadByUID]:
        """
        Get all assignments for a user where assign_date <= current date
        and assignment_state is ACCEPTED or WAITING_FOR_ACCEPTANCE
        """
        query = (
            self.db.query(Assignment)
            .join(Asset, Assignment.asset_id == Asset.id)
            .join(Category, Asset.category_id == Category.id)
            .filter(
                Assignment.assigned_to_id == user_id,
                Assignment.assignment_state.notin_([AssignmentState.DECLINED, AssignmentState.RETURNED]),
                func.date(Assignment.assign_date) <= end_date,
            )
        )
        if pagination.sort_by:
            if pagination.sort_by == SortHomeAssignmentBy.ASSET_CODE:
                query = query.order_by(
                    Asset.asset_code.asc()
                    if pagination.sort_direction == SortDirection.ASC
                    else Asset.asset_code.desc()
                )
            elif pagination.sort_by == SortHomeAssignmentBy.ASSET_NAME:
                query = query.order_by(
                    Asset.asset_name.asc()
                    if pagination.sort_direction == SortDirection.ASC
                    else Asset.asset_name.desc()
                )
            elif pagination.sort_by == SortHomeAssignmentBy.CATEGORY:
                query = query.order_by(
                    Category.category_name.asc()
                    if pagination.sort_direction == SortDirection.ASC
                    else Category.category_name.desc()
                )
            elif pagination.sort_by == SortHomeAssignmentBy.STATE:
                query = query.order_by(
                    Assignment.assignment_state.asc()
                    if pagination.sort_direction == SortDirection.ASC
                    else Assignment.assignment_state.desc()
                )
            elif pagination.sort_by == SortHomeAssignmentBy.ASSIGN_DATE:
                query = query.order_by(
                    Assignment.assign_date.asc()
                    if pagination.sort_direction == SortDirection.ASC
                    else Assignment.assign_date.desc()
                )

        total = query.count()
        total_pages = (total + pagination.size - 1) // pagination.size

        assignments = (
            query.offset((pagination.page - 1) * pagination.size)
            .limit(pagination.size)
            .all()
        )

        assignment_reads = [
            AssignmentUserReadByUID(
                id=assignment.id,
                assign_date=assignment.assign_date.date(),
                assignment_note=assignment.assignment_note,
                assignment_state=assignment.assignment_state,
                asset=AssetRead.model_validate(assignment.asset, from_attributes=True),
                assigned_to_user=UserRead.model_validate(assignment.assigned_to_user, from_attributes=True),
                assigned_by_user=UserRead.model_validate(assignment.assigned_by_user, from_attributes=True),
            )
            for assignment in assignments
        ]

        return PaginatedResponse(
            data=assignment_reads,
            meta=PaginationMeta(
                total=total,
                total_pages=total_pages,
                page=pagination.page,
                page_size=pagination.size,
            ),
        )

    def update_assignment_state(
        self, assignment_id: int, assignment: AssignmentStateUpdate
    ) -> Assignment:
        """
        Update an assignment's state by ID.
        """
        assignment_model = self.db.query(Assignment).filter(
            Assignment.id == assignment_id
        ).first()
        if not assignment_model:
            logger.error(f"Assignment {assignment_id} not found")
            raise NotFoundException(detail="Assignment not found")
        
        assignment_model.assignment_state = assignment.assignment_state
        self.db.commit()
        self.db.refresh(assignment_model)
        return assignment_model

    def create_assignment(self, assignment: Assignment) -> Assignment:
        """
        Save an assignment to the database
        
        Args:
            assignment: The assignment object to save
            
        Returns:
            Assignment: The saved assignment with ID
        """
        self.db.add(assignment)
        self.db.commit()
        self.db.refresh(assignment)
        return assignment
        
    def delete_assignment(self, assignment: Assignment) -> None:
        """
        Delete an assignment by ID.
        """
        self.db.delete(assignment)
        self.db.commit()
        
    def is_asset_available(self, asset_id: int) -> bool:
        """Check if an asset is available for assignment"""
        # An asset is available if it doesn't have any active assignments
        active_assignments = self.db.query(Assignment).filter(
            Assignment.asset_id == asset_id,
            Assignment.assignment_state.in_([
                AssignmentState.WAITING_FOR_ACCEPTANCE,
                AssignmentState.ACCEPTED
            ])
        ).count()
        
        return active_assignments == 0

    def get_assignment_by_id_no_join(self, assignment_id: int) -> Assignment:
        return self.db.query(Assignment).filter(Assignment.id == assignment_id).first()
    
    def get_assignment_history(self, asset_id: int, filter: AssignmentFilter) -> PaginatedResponse[AssetHistory]:
        # Create aliases for the User table to avoid conflicts
        from sqlalchemy.orm import aliased
        AssignedToUser = aliased(User)
        AssignedByUser = aliased(User)
        
        query = (
            self.db.query(Assignment)
            .join(Asset, Assignment.asset_id == Asset.id)
            .join(AssignedToUser, Assignment.assigned_to_id == AssignedToUser.id)
            .join(AssignedByUser, Assignment.assigned_by_id == AssignedByUser.id)
            .outerjoin(Request, Assignment.id == Request.assignment_id)
            .filter(
                Assignment.asset_id == asset_id,  # Filter by asset_id (required)
                Assignment.assignment_state.in_([
                    AssignmentState.ACCEPTED,
                    AssignmentState.RETURNED
                ])
            )
            .order_by(Assignment.created_at.desc())  # Sort from latest to oldest
        )
        
        total = query.count()
        total_pages = (total + filter.size - 1) // filter.size

        assignments = (
            query.offset((filter.page - 1) * filter.size)
            .limit(filter.size)
            .all()
        )
        
        # Create AssetHistory objects for each assignment
        asset_history = [
            AssetHistory(
                id=assignment.id,
                assign_date=assignment.assign_date.date(),  # Convert datetime to date
                assigned_to=assignment.assigned_to_user.username,
                assigned_by=assignment.assigned_by_user.username,
                return_date=assignment.requests.return_date.date() if assignment.requests and assignment.requests.return_date else None
            )
            for assignment in assignments  # Iterate over each assignment
        ]
        
        return PaginatedResponse(
            data=asset_history,
            meta=PaginationMeta(
                total=total,
                total_pages=total_pages,
                page=filter.page,
                page_size=filter.size,
            ),
        )
