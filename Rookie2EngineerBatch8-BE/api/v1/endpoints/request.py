from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from api.dependencies import get_current_admin, get_current_user, get_db_session
from enums.user.type import Type
from schemas.query.filter.request import RequestFilter
from schemas.request import RequestCreate, RequestRead, RequestUpdate, RequestReadDetail
from schemas.shared.paginated_response import PaginatedResponse
from schemas.user import UserRead
from services.request import RequestReturningService

router = APIRouter(prefix="/requests", tags=["Requests"])


@router.get(
    "",
    response_model=PaginatedResponse[RequestReadDetail],
    status_code=status.HTTP_200_OK,
    summary="Get paginated list of all requests",
    description="Get a paginated list of all requests."
)
async def get_requests(
    filter: RequestFilter = Depends(),
    db: Session = Depends(get_db_session),
    current_user = Depends(get_current_user)
):
    """Get a paginated list of all requests"""
    request_service = RequestReturningService(db)
    return request_service.read_requests_paginated(filter, current_user)



@router.post(
    "",
    response_model=RequestRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new request",
    description="Create a new request with the provided details."
)
async def create_request(
    request: RequestCreate,
    db: Session = Depends(get_db_session),
    current_user: UserRead = Depends(get_current_user)
):
    """Create a new request"""
    print(f"Endpoint pass")
    if current_user.type == Type.ADMIN:
        return RequestReturningService(db).create_request_returning(request, current_user)
    return RequestReturningService(db).create_request_returning_by_staff(request, current_user)


@router.patch(
    "/{request_id}",
    response_model=RequestRead,
    status_code=status.HTTP_200_OK,
    summary="Partially update request by ID",
    description="Partially update a request by its ID with the provided details."
)
async def update_request(
    request_id: int,
    request: RequestUpdate,
    db: Session = Depends(get_db_session),
    current_admin : UserRead = Depends(get_current_admin)
):
    """Partially update a request by ID"""
    request_service = RequestReturningService(db)
    updated_request = request_service.update_request(request_id, request, current_admin)
    return updated_request


@router.delete(
    "/{request_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Cancel request for returning by ID",
    description="Cancel a request for returning by its ID. Only admin can cancel requests with 'Waiting for returning' state."
)
async def delete_request(
    request_id: int,
    db: Session = Depends(get_db_session),
    current_admin: UserRead = Depends(get_current_admin)
):
    """Cancel a request for returning by ID"""
    request_service = RequestReturningService(db)
    request_service.cancel_request(request_id, current_admin)
    return