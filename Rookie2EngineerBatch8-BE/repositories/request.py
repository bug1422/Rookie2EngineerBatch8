from datetime import datetime, timezone
from models.request import Request
from models.asset import Asset
from models.user import User
from schemas.query.filter.request import RequestFilter
from schemas.shared.paginated_response import PaginatedResponse, PaginationMeta
from schemas.request import RequestReadDetail, RequestRead
from schemas.user import UserReadSimple, UserRead
from sqlalchemy.orm import Session, aliased, joinedload
from schemas.query.sort.sort_type import SortRequestBy, SortDirection
from models.assignment import Assignment
from schemas.assignment import AssignmentReadSimple
from schemas.asset import AssetRead
from enums.user.type import Type
from sqlalchemy import or_,func
from datetime import time

from enums.request.state import RequestState

class RequestReturningRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_requests_paginated(
        self,
        request_filter: RequestFilter,
        current_user: UserRead
    ) -> PaginatedResponse[RequestReadDetail]:
        
        RequestedBy = aliased(User)
        AcceptedBy = aliased(User)
        
        query = (
            self.db.query(Request)
            .join(Assignment, onclause=Request.assignment_id == Assignment.id)
            .join(Asset, onclause=Assignment.asset_id == Asset.id)
            .join(RequestedBy, onclause=Request.requested_by_id == RequestedBy.id)
            .outerjoin(AcceptedBy, onclause=Request.accepted_by_id == AcceptedBy.id)
            .where(Asset.asset_location == current_user.location)
        )
        
        if request_filter.state:
            query = query.filter(Request.request_state == request_filter.state)
        
        if request_filter.return_date:
            # Convert the filter date to datetime range for that day
            filter_date = request_filter.return_date.date()  # Get just the date part
            start_of_day = datetime.combine(filter_date, time.min)  # Start of the day (00:00:00)
            end_of_day = datetime.combine(filter_date, time.max)    # End of the day (23:59:59.999999)
            
            query = query.filter(
                Request.return_date.between(start_of_day, end_of_day)
            )
            
        if request_filter.search:
            query = query.filter(
                (Asset.asset_code.ilike(f"%{request_filter.search}%"))
                | (Asset.asset_name.ilike(f"%{request_filter.search}%"))
                | (RequestedBy.username.ilike(f"%{request_filter.search}%"))
            )
            
        if request_filter.sort_by:
            if request_filter.sort_by == SortRequestBy.ID:
                query = query.order_by(
                    Request.id.asc() if request_filter.sort_direction == SortDirection.ASC
                    else Request.id.desc()
                )
            elif request_filter.sort_by == SortRequestBy.ASSET_CODE:
                query = query.order_by(
                    Asset.asset_code.asc() if request_filter.sort_direction == SortDirection.ASC
                    else Asset.asset_code.desc()
                )
            elif request_filter.sort_by == SortRequestBy.ASSET_NAME:
                query = query.order_by(
                    func.lower(Asset.asset_name).asc() if request_filter.sort_direction == SortDirection.ASC
                    else func.lower(Asset.asset_name).desc()
                )
            elif request_filter.sort_by == SortRequestBy.REQUESTED_BY:
                query = query.order_by(
                    func.lower(RequestedBy.username).asc() if request_filter.sort_direction == SortDirection.ASC
                    else func.lower(RequestedBy.username).desc()
                )
            elif request_filter.sort_by == SortRequestBy.ACCEPTED_BY:
                query = query.order_by(
                    func.lower(AcceptedBy.username).asc() if request_filter.sort_direction == SortDirection.ASC
                    else func.lower(AcceptedBy.username).desc()
                )
            elif request_filter.sort_by == SortRequestBy.ASSIGN_DATE:
                query = query.order_by(
                    Assignment.assign_date.asc() if request_filter.sort_direction == SortDirection.ASC
                    else Assignment.assign_date.desc()
                )
            elif request_filter.sort_by == SortRequestBy.RETURN_DATE:
                query = query.order_by(
                    Request.return_date.asc() if request_filter.sort_direction == SortDirection.ASC
                    else Request.return_date.desc()
                )
            elif request_filter.sort_by == SortRequestBy.STATE:
                query = query.order_by(
                    Request.request_state.asc() if request_filter.sort_direction == SortDirection.ASC
                    else Request.request_state.desc()
                )
        
        
        # Function already designed for admin, staff filter will return requests made by staff or correspond to the assignment which was assigned to staff
        if current_user.type == Type.STAFF:
            query = query.filter(or_(Request.requested_by_id == current_user.id, Request.assignment.has(Assignment.assigned_to_id == current_user.id)))
                
        total = query.count()
        total_pages = (total + request_filter.size - 1) // request_filter.size
        
        requests = (
            query.offset((request_filter.page - 1) * request_filter.size)
            .limit(request_filter.size)
            .all()
        )
        
        request_reads = [
            RequestReadDetail(
                id = request.id,
                asset= AssetRead.model_validate(request.assignment.asset, from_attributes=True),
                requested_by = UserReadSimple.model_validate(request.requested_by_user, from_attributes=True),
                accepted_by = UserReadSimple.model_validate(request.accepted_by_user, from_attributes=True) if request.accepted_by_user else None,
                request_state = request.request_state,
                return_date = request.return_date.date() if request.return_date else None,
                assignment = AssignmentReadSimple(
                    id=request.assignment.id,
                    assign_date=request.assignment.assign_date.date(), 
                    assignment_state=request.assignment.assignment_state,
                    assignment_note=request.assignment.assignment_note
                )
            )
            for request in requests
        ]
        
        return PaginatedResponse(
            data = request_reads,
            meta = PaginationMeta(
                total = total,
                total_pages = total_pages,
                page = request_filter.page,
                page_size = request_filter.size,
            ),
        )

    def create_request_returning(self, request_data: Request) -> RequestRead:
        """Create a new request returning entry in the database."""
        self.db.add(request_data)
        self.db.commit()
        self.db.refresh(request_data)
        return request_data
    
    def get_request_by_assignment_id(self, assignment_id: int) -> Request:
        """
        Retrieve a request by its assignment ID with WAITING_FOR_RETURNING state.
        
        Args:
            assignment_id: The assignment ID to search for
            
        Returns:
            Request: The request if found, None otherwise
        """
        return (
            self.db.query(Request)
            .filter(
                Request.assignment_id == assignment_id,
                Request.request_state == RequestState.WAITING_FOR_RETURNING
            )
            .first()
        )
        
    def get_request_by_id(self, request_id: int) -> Request:
        """Get a request by ID with all related data loaded."""
        return (
            self.db.query(Request)
            .options(
                joinedload(Request.assignment).joinedload(Assignment.asset),
                joinedload(Request.requested_by_user),
                joinedload(Request.accepted_by_user)
            )
            .filter(Request.id == request_id)
            .first()
        )

    def complete_return_request(self, request_id: int, current_admin_id: int) -> Request:
        """Complete a return request by updating state and returned date."""
        request = self.get_request_by_id(request_id)

        if request:
            request.request_state = RequestState.COMPLETED
            request.return_date = datetime.now(timezone.utc)
            request.updated_at = datetime.now(timezone.utc)
            request.accepted_by_id = current_admin_id

            self.db.commit()
            self.db.refresh(request)

        return request

    def delete_request_by_id(self, request_id: int) -> bool:
        """
        Delete a request by its ID.

        Args:
            request_id: The ID of the request to delete

        Returns:
            bool: True if request was deleted, False if not found
        """
        request = self.get_request_by_id(request_id)
        if request:
            self.db.delete(request)
            self.db.commit()
            return True
        return False
