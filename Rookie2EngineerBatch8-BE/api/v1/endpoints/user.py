from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from core.exceptions import NotFoundException
from schemas.query.check.isValid import IsValid
from schemas.query.filter.user import UserFilter
from schemas.shared.paginated_response import PaginatedResponse
from schemas.user import UserRead, UserCreate, UserUpdate

from services.user import UserService
from api.dependencies import get_db_session
from api.dependencies import get_current_admin, get_current_user
router = APIRouter(prefix="/users", tags=["Users"])


@router.get(
    "",
    response_model=PaginatedResponse[UserRead],
    status_code=200,
    summary="Get paginated list of users",
    description="Get a paginated list of users with optional filters.",
)
async def get_users(
    filter: UserFilter = Depends(),
    db: Session = Depends(get_db_session),
    current_user: UserRead = Depends(get_current_admin),
):
    user_service = UserService(db)
    return user_service.read_users_paginated(filter, current_user)

@router.get(
    "/{user_id}",
    response_model=UserRead,
    status_code=status.HTTP_200_OK,
    summary="Get user by ID",
    description="Get a user by their ID.",
)
async def get_user(user_id: int, db: Session = Depends(get_db_session), current_user: UserRead = Depends(get_current_user)):
    """Get a user by ID"""
    user_service = UserService(db)
    return user_service.read_user(user_id)


@router.post(
    "",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new user",
    description="Create a new user with the provided details.",
)
async def create_user(
    user: UserCreate,
    db: Session = Depends(get_db_session),
    current_user: UserRead = Depends(get_current_admin),
):
    user_service = UserService(db)
    created_user = user_service.create_user(user, current_user.location)
    # No need to convert is_first_login as it's now properly defined as an enum
    return created_user


@router.put(
    "/{user_id}",
    response_model=UserRead,
    status_code=status.HTTP_200_OK,
    summary="Update user by ID",
    description="Update a user by their ID with the provided details.",
)
async def update_user(
    user_id: int,
    user: UserUpdate,
    db: Session = Depends(get_db_session),
    current_user: UserRead = Depends(get_current_admin),
):
    user_service = UserService(db)
    if not current_user:
        raise NotFoundException(detail="User not found")
    updated_user = user_service.edit_user(user_id, user, current_user.location)
    return updated_user


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Disable user by ID",
    description="Disable a user by their ID.",
)
async def delete_user(
    user_id: int,
    db: Session = Depends(get_db_session),
    current_user: UserRead = Depends(get_current_admin),
):
    user_service = UserService(db)
    return user_service.disable_user(user_id)


@router.get(
    "/valid-user/{user_id}",
    response_model=IsValid,
    status_code=status.HTTP_200_OK,
    summary="Get and check if user valid by ID",
    description="Get a user and check if user valid by their ID.",
)
async def get_valid_user(user_id: int, db: Session = Depends(get_db_session), current_user: UserRead = Depends(get_current_user)):
    """Get a valid user by ID"""
    user_service = UserService(db)
    return user_service.check_user_valid(user_id)
