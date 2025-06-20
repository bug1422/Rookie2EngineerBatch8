from sqlalchemy.orm import Session
from typing import List, Optional
from schemas.query.check.isValid import IsValid
from schemas.query.filter.user import UserFilter
from schemas.shared.paginated_response import PaginatedResponse
from schemas.user import UserCreate, UserRead, UserUpdate
from models.user import User
from repositories.user import UserRepository
from utils.generator import Generator
from core.logging_config import get_logger
from enums.user.type import Type
from enums.shared.location import Location
from core.exceptions import (
    AuthenticationException,
    PermissionDeniedException,
    NotFoundException,
    BusinessException,
)
from utils.hash import verify_password
from core.config import settings

logger = get_logger(__name__)


class UserService:
    def __init__(self, db: Session):
        self.repository = UserRepository(db)

    def create_user(
        self, user: UserCreate, current_admin_location: Location
    ) -> UserRead:
        logger.info(f"Creating user: {user}")
        if user.type == Type.STAFF and user.location != current_admin_location:
            raise PermissionDeniedException(
                detail="You are not allowed to create a staff in other location"
            )

        base_username = Generator.generate_username(user.first_name, user.last_name)
        generated_username = base_username
        count = 1

        while self.repository.is_username_exists(generated_username):
            logger.warning(
                f"Username {generated_username} already exists, generating new username"
            )
            generated_username = f"{base_username}{count}"
            count += 1
        logger.info(f"Generated username: {generated_username}")

        count_all_users = self.repository.get_count_all_users()
        generated_staff_code = Generator.generate_staff_code(count_all_users)
        logger.info(f"Generated staff code: {generated_staff_code}")

        generated_password = Generator.generate_password(generated_username, user.date_of_birth)

        user_model = User(
            staff_code=generated_staff_code,
            username=generated_username,
            password=generated_password,
            first_name=user.first_name,
            last_name=user.last_name,
            date_of_birth=user.date_of_birth,
            join_date=user.join_date,
            gender=user.gender,
            type=user.type,
            location=user.location,
            is_first_login=True  # Explicitly set as boolean
        )

        created_user = self.repository.create_user(user_model)
        logger.info(f"User created successfully")

        return created_user

    def get_user_by_username(self, username: str) -> UserRead:
        return self.repository.get_user_by_username(username)

    def authenticate_user(self, username: str, password: str) -> UserRead:
        user = self.get_user_by_username(username)
        if not user:
            raise AuthenticationException(detail="Invalid username or password")
        if not verify_password(password, user.password):
            raise AuthenticationException(detail="Invalid username or password")
        return user

    def edit_user(
        self, user_id: int, user: UserUpdate, current_admin_location: Location
    ) -> UserRead:
        logger.info(f"Editing user: {user}")
        if user.type == Type.STAFF and user.location != current_admin_location:
            raise PermissionDeniedException(
                detail="You are not allowed to edit a staff in other location"
            )

        updated_user = self.repository.edit_user(user_id, user)
        if not updated_user:
            raise AuthenticationException(detail="User not found")

        logger.info(f"User edited successfully")
        return updated_user

    def read_user(self, user_id: int) -> UserRead:
        logger.info(f"Reading user with id: {user_id}")

        user_data = self.repository.get_user_by_id(user_id)
        if user_data is None:
            logger.warning(f"User with id {user_id} not found")
            raise NotFoundException(detail=f"User with id {user_id} not found")

        print(user_data)
        return user_data

    def read_users_paginated(
        self, user_filter: UserFilter, current_user: UserRead
    ) -> PaginatedResponse[UserRead]:
        users = self.repository.get_users_paginated(user_filter, current_user)
        logger.info(f"Users read from database successfully: {users}")
        return users

    def search_users(self, query: Optional[str], location: Location) -> List[UserRead]:
        """
        Search for users by staff code or username within the same location
        
        Args:
            query: Search term (staff code or username)
            location: Location to filter users by
            
        Returns:
            List of users matching the search criteria
        """
        return self.repository.search_users(query, location)

    def create_root_user(self) -> UserRead:
        if not settings.ROOT_ACCOUNT_USERNAME or not settings.ROOT_ACCOUNT_PASSWORD:
            logger.error(
                "ROOT_ACCOUNT_USERNAME or ROOT_ACCOUNT_PASSWORD not configured"
            )
            raise ValueError(
                "ROOT_ACCOUNT_USERNAME and ROOT_ACCOUNT_PASSWORD must be configured"
            )

        if self.repository.is_username_exists(settings.ROOT_ACCOUNT_USERNAME):
            logger.warning("Root user already exists")
            return

        try:
            hashed_password = Generator.generate_root_password(
                settings.ROOT_ACCOUNT_PASSWORD
            )
            staff_code = Generator.generate_staff_code(
                self.repository.get_count_all_users()
            )
            return self.repository.create_root_user(
                settings.ROOT_ACCOUNT_USERNAME, hashed_password, staff_code
            )

        except Exception as e:
            logger.error(f"Error creating root user: {e}")
            raise e

    def disable_user(self, user_id: int) -> UserRead:
        logger.info(f"Disabling user with ID: {user_id}")

        user = self.repository.get_user_by_id(user_id)
        if not user:
            logger.error(f"User with ID {user_id} not found")
            raise NotFoundException(detail="User not found")
        if self.repository.has_active_assignments(user):
            logger.error(
                f"User with ID {user_id} has active assignments and cannot be disabled."
            )
            raise BusinessException(
                detail="Cannot disable user. User has one or more valid assignments."
            )
        disabled_user = self.repository.disable_user(user)
        logger.info(f"User with ID {user_id} disabled successfully")

        return disabled_user

    def check_user_valid(
        self, user_id: int
    ) -> UserRead:
        logger.info(f"Check user is valid or not: {user_id}")

        user = self.repository.get_user_by_id(user_id)
        if not user:
            logger.error(f"User with ID {user_id} not found")
            raise NotFoundException(detail="User not found")
        if self.repository.has_active_assignments(user):
            logger.error(
                f"User with ID {user_id} has active assignments and cannot be disabled."
            )
            return IsValid(is_valid=False, user=user)
        
        return IsValid(is_valid=True, user=user)
