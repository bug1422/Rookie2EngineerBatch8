from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from api.dependencies import get_current_admin, get_db_session, get_current_user
from schemas.assignment import (
    AssignmentRead,
    AssignmentCreate,
    AssignmentStateUpdate,
    AssignmentUpdate,
    AssignmentUpdateResponse,
    AssignmentReadDetail,
    AssignmentUserReadByUID,
)
from schemas.query.filter.assignment import AssignmentFilter, HomeAssignmentFilter
from schemas.shared.paginated_response import PaginatedResponse
from schemas.user import UserRead
from services.assignment import AssignmentService

router = APIRouter(prefix="/assignments", tags=["Assignments"])


@router.get(
    "",
    response_model=PaginatedResponse[AssignmentRead],
    status_code=status.HTTP_200_OK,
    summary="Get paginated list of assignments",
    description="Get a paginated list of assignments with optional filters."
)
async def get_assignments(
    filter: AssignmentFilter = Depends(),
    db: Session = Depends(get_db_session),
    current_user: UserRead = Depends(get_current_admin)
):
    """Get a list of all assignments"""
    assignment_service = AssignmentService(db)
    return assignment_service.read_assignments_paginated(filter, current_user)


@router.get(
    "/me",
    response_model=PaginatedResponse[AssignmentUserReadByUID],
    status_code=status.HTTP_200_OK,
    summary="Get assignments of the current user",
    description="Get all assignments for the current user until current date.",
)
async def get_assignments_by_user(
    filter: HomeAssignmentFilter = Depends(),
    db: Session = Depends(get_db_session),
    current_user: UserRead = Depends(get_current_user),
):
    """Get all assignments for a specific user until current date"""
    assignment_service = AssignmentService(db)
    return assignment_service.get_user_assignments_until_current_date(
        filter, current_user
    )

@router.get(
    "/{assignment_id}",
    response_model=AssignmentReadDetail,
    status_code=status.HTTP_200_OK,
    summary="Get assignment by ID",
    description="Get an assignment by its ID."
)
async def get_assignment(assignment_id: int, db: Session = Depends(get_db_session), current_user: UserRead = Depends(get_current_admin)):
    """Get an assignment by ID"""
    assignment_service = AssignmentService(db)
    return assignment_service.read_assignment(assignment_id, current_user)

@router.post(
    "",
    response_model=AssignmentRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new assignment",
    description="Create a new assignment with the provided details."
)
async def create_assignment(
    assignment: AssignmentCreate,
    db: Session = Depends(get_db_session),
    current_user: UserRead = Depends(get_current_admin)
):
    """
    Create a new assignment

    - **asset_id**: ID of the asset to assign (required)
    - **assigned_to_id**: ID of the user to assign to (required)
    - **assignment_note**: Note about the assignment (optional)
    - **assign_date**: Date when the assignment takes effect (required, must be today or in the future)
    """


    # Create the assignment with current user info
    assignment_service = AssignmentService(db)

    # Create a new assignment object with the current user's ID
    db_assignment = assignment_service.create_assignment(
        assignment=assignment,
        assigned_by_id=current_user.id,
        current_user=current_user
    )

    return db_assignment


@router.put(
    "/{assignment_id}",
    response_model=AssignmentUpdateResponse,
    status_code=status.HTTP_200_OK,
    summary="Update assignment by ID",
    description="Update an assignment by its ID with the provided details."
)
async def update_assignment(
    assignment_id: int,
    assignment_update: AssignmentUpdate,
    db: Session = Depends(get_db_session),
    current_user: UserRead = Depends(get_current_admin)
):
    """Update an assignment by ID"""
    assignment_service = AssignmentService(db)
    return assignment_service.edit_assignment(assignment_id, assignment_update, current_user)


@router.patch(
    "/{assignment_id}",
    response_model=AssignmentUpdateResponse,
    status_code=status.HTTP_200_OK,
    summary="Partially update assignment's state by ID",
    description="Partially update an assignment's state by its ID."
)
async def update_assignment_state(
    assignment_id: int,
    assignment: AssignmentStateUpdate,
    db: Session = Depends(get_db_session),
    current_user: UserRead = Depends(get_current_user),
):
    """Partially update an assignment's state by ID"""
    assignment_service = AssignmentService(db)
    user_id = current_user.id
    location = current_user.location
    return assignment_service.update_assignment_state(assignment_id, assignment, user_id, location)


@router.delete(
    "/{assignment_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete assignment by ID",
    description="Delete an assignment by its ID."
)
async def delete_assignment(assignment_id: int, db: Session = Depends(get_db_session), current_user: UserRead = Depends(get_current_admin)):
    """Delete an assignment by ID"""
    assignment_service = AssignmentService(db)
    location = current_user.location
    return assignment_service.delete_assignment(assignment_id, location)
