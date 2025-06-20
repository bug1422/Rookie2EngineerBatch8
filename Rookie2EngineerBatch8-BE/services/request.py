from datetime import datetime
import logging
from sqlmodel import Session
from core.exceptions import BusinessException, NotFoundException
from core.logging_config import get_logger
from enums.asset.state import AssetState
from enums.assignment.state import AssignmentState
from enums.request.state import RequestState
from repositories.asset import AssetRepository
from repositories.assignment import AssignmentRepository
from repositories.request import RequestReturningRepository
from schemas.asset import AssetUpdate
from schemas.assignment import AssignmentStateUpdate
from schemas.request import RequestCreate, RequestRead, RequestUpdate
from models.request import Request
from schemas.user import UserRead
from services.assignment import AssignmentService
from schemas.shared.paginated_response import PaginatedResponse
from schemas.query.filter.request import RequestFilter

logger = get_logger(__name__)

class RequestReturningService:
    def __init__(self, db: Session):
        self.repository = RequestReturningRepository(db)
        self.assignment_service = AssignmentService(db)
        self.assignment_repository = AssignmentRepository(db)
        self.asset_repository = AssetRepository(db)
        
    def create_request_returning(self, request_data: RequestCreate, request_by: UserRead) -> RequestRead:
        """Create a new request."""
        db_request = Request(
            assignment_id=request_data.assignment_id,
            requested_by_id=request_by.id,
            request_state=RequestState.WAITING_FOR_RETURNING
        )
        
        # Check if assignment valid
        assignment = self.assignment_service.read_assignment(
            request_data.assignment_id,
            request_by
        )
        
        if assignment.assignment.assignment_state != AssignmentState.ACCEPTED:
            raise BusinessException(
                detail="Assignment is not in accepted state to return"
            )
        
        # Check if request already exists for the assignment
        if self.check_request_exist_by_assignment_id(
                request_data.assignment_id
            ):
            raise BusinessException(
                detail="Request already exists for this assignment with waiting for returning state.",
            )
        
        try:
            db_request_respone = self.repository.create_request_returning(db_request)
        except Exception as e:
            logging.error(f"Error creating request: {e}")
            raise BusinessException(
                detail=str(e),
            )
        
        # Convert the database response to a RequestRead schema
        response = RequestRead(
            assignment_id=db_request_respone.assignment_id,
            requested_by_id=db_request_respone.requested_by_id,
            return_date=db_request_respone.return_date,
            request_state=db_request_respone.request_state,
            id=db_request_respone.id
        )
        return response
    
    def check_request_exist_by_assignment_id(self, assignment_id: int) -> bool:
        """
        Check if a request exists for the given assignment_id with WAITING_FOR_RETURNING state.
        
        Args:
            assignment_id: The ID of the assignment to check
            
        Returns:
            bool: True if a waiting request exists, False otherwise
        """
        db_request = self.repository.get_request_by_assignment_id(assignment_id)
        
        # Check if request exists and has WAITING_FOR_RETURNING state
        return db_request is not None and db_request.request_state == RequestState.WAITING_FOR_RETURNING
    
    def create_request_returning_by_staff(self, request_data: RequestCreate, request_by: UserRead) -> RequestRead:
        """
        Create a new request by user.
        
        Args:
            request_data: Request creation data containing assignment_id
            request_by: Current user making the request
            
        Returns:
            RequestRead: The created request details
            
        Raises:
            BusinessException: If user is not the assignee or request already exists
        """
        # Get assignment to validate user is the assignee
        assignment = self.assignment_service.repository.get_assignment_by_id_no_join(
            request_data.assignment_id
        )
        
        if not assignment:
            raise BusinessException(
                detail=f"Assignment with id {request_data.assignment_id} not found"
            )
            
        # Check if current user is the assignee
        if assignment.assigned_to_id != request_by.id:
            raise BusinessException(
                detail="You can only create return requests for your own assignments"
            )
        
        # Use existing admin method after validation
        return self.create_request_returning(request_data, request_by)


    def read_requests_paginated(self, filter: RequestFilter, current_user: UserRead) -> PaginatedResponse[RequestRead]:
        requests = self.repository.get_requests_paginated(filter, current_user)
        return requests

    
        
    def update_request(self, request_id: int, request_update: RequestUpdate, current_admin: UserRead) -> RequestRead:
        
        # Get the request first to validate it exists
        request = self.repository.get_request_by_id(request_id)
        if not request:
            raise NotFoundException(detail=f"Request with id {request_id} not found")
            
        # Validate current state
        if request.request_state != RequestState.WAITING_FOR_RETURNING:
            logger.warning(f"Admin {current_admin.id} attempted to complete request {request_id} with state {request.request_state}")
            raise BusinessException(
                detail="Only requests with 'Waiting for returning' state can be completed"
            )
            
        # Validate the requested state change
        if request_update.request_state != RequestState.COMPLETED:
            raise BusinessException(
                detail="Only completion of return requests is currently supported"
            )
            
        # Validate location permissions
        asset = request.assignment.asset
        if asset.asset_location != current_admin.location:
            logger.info(f"Admin at {current_admin.location} attempted to complete return request for asset at {asset.asset_location}")
            raise BusinessException(
                detail="You can only complete requests for assets in your location"
            )
        
        # Complete the request
        completed_request = self.repository.complete_return_request(request_id, current_admin.id)
        
        # Update the assignment state to RETURNED
        assignment = request.assignment
        if assignment:
            assignment_state_update = AssignmentStateUpdate(assignment_state=AssignmentState.RETURNED)
            self.assignment_repository.update_assignment_state(assignment.id, assignment_state_update)
            logger.info(f"Assignment {assignment.id} state updated to RETURNED for completed return request {request_id}")
        
        # Update asset state to AVAILABLE
        asset_update = AssetUpdate(asset_state=AssetState.AVAILABLE)
        self.asset_repository.update_asset(asset.id, asset_update)
        
        return RequestRead.model_validate(completed_request, from_attributes=True)

    def cancel_request(self, request_id: int, current_admin: UserRead) -> bool:
        """
        Cancel a request for returning.

        Args:
            request_id: The ID of the request to cancel
            current_admin: The admin user performing the cancellation

        Returns:
            bool: True if request was successfully cancelled

        Raises:
            NotFoundException: If request with given ID is not found
            BusinessException: If request is not in 'Waiting for returning' state
        """
        # Get the request first to validate it exists
        request = self.repository.get_request_by_id(request_id)
        if not request:
            raise NotFoundException(detail=f"Request with id {request_id} not found")

        # Validate current state - only allow cancelling requests in WAITING_FOR_RETURNING state
        if request.request_state != RequestState.WAITING_FOR_RETURNING:
            logger.warning(f"Admin {current_admin.id} attempted to cancel request {request_id} with state {request.request_state}")
            raise BusinessException(
                detail="Only requests with 'Waiting for returning' state can be cancelled"
            )

        # Delete the request
        success = self.repository.delete_request_by_id(request_id)

        if success:
            logger.info(f"Admin {current_admin.id} successfully cancelled request {request_id}")
        else:
            logger.error(f"Failed to cancel request {request_id}")
            raise BusinessException(detail="Failed to cancel request")

        return success