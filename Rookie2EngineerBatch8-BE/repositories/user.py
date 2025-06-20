from sqlalchemy.orm import Session
from sqlalchemy import or_, func
from enums.assignment.state import AssignmentState
from enums.user.status import Status
from models.assignment import Assignment
from models.user import User
from schemas.query.filter.user import UserFilter
from schemas.user import UserRead
from schemas.shared.paginated_response import PaginatedResponse, PaginationMeta
from schemas.query.sort.sort_type import SortUserBy, SortDirection
from schemas.user import UserUpdate

from enums.user.type import Type
from enums.shared.location import Location
from datetime import date, datetime, timezone

from typing import List, Optional



class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_user(self, user: User) -> User:
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def get_user_by_username(self, username: str) -> User:
        return (
            self.db.query(User)
            .filter(User.username == username, User.status == Status.ACTIVE)
            .first()
        )

    def is_username_exists(self, username: str) -> bool:
        return self.db.query(User).filter(User.username == username).first() is not None

    def get_count_all_users(self) -> int:
        return self.db.query(User).count()

    def get_user_by_staff_code(self, staff_code: str) -> User:
        return (
            self.db.query(User)
            .filter(User.staff_code == staff_code, User.status == Status.ACTIVE)
            .first()
        )

    def create_root_user(self, username: str, password: str, staff_code: str) -> User:
        root_user = User(
            username=username,
            password=password,
            staff_code=staff_code,
            first_name="Root",
            last_name="Root",
            date_of_birth=date(1990, 1, 1),
            join_date=date(2021, 1, 1),
            type=Type.ADMIN,
            location=Location.HCM,
            status=Status.ACTIVE,
            is_first_login=True  # Explicitly set as boolean
        )
        self.db.add(root_user)
        self.db.commit()

    def edit_user(self, user_id: int, user: UserUpdate) -> User:
        existing_user = self.db.query(User).filter(User.id == user_id).first()
        if existing_user:
            for key, value in user.model_dump(exclude_unset=True).items():
                setattr(existing_user, key, value)
            existing_user.updated_at = datetime.now(timezone.utc)
            self.db.commit()
            self.db.refresh(existing_user)
            return existing_user
        return None

    def get_user_by_id(self, user_id: int) -> Optional[User]:
        return self.db.query(User).filter(User.id == user_id).first()

    def get_users_paginated(
        self, user_filter: UserFilter, user_current: User
    ) -> PaginatedResponse[UserRead]:
        query = self.db.query(User)

        # Exclude the current user from the results
        query = query.filter(User.id != user_current.id)

        # Exclude users with different location than that of the current user
        query = query.filter(User.location == user_current.location)

        # Exclude disabled users
        query = query.filter(User.status == Status.ACTIVE)

        if user_filter.type:
            query = query.filter(User.type == user_filter.type)

        if user_filter.search:
            query = query.filter(
                (User.staff_code.ilike(f"%{user_filter.search}%"))
                | (User.first_name.ilike(f"%{user_filter.search}%"))
                | (User.last_name.ilike(f"%{user_filter.search}%"))
            )

        if user_filter.sort_by:
            if user_filter.sort_by == SortUserBy.FIRST_NAME:
                query = query.order_by(
                    func.lower(User.first_name).asc()
                    if user_filter.sort_direction == SortDirection.ASC
                    else func.lower(User.first_name).desc()
                )
            elif user_filter.sort_by == SortUserBy.STAFF_CODE:
                query = query.order_by(
                    User.staff_code.asc()
                    if user_filter.sort_direction == SortDirection.ASC
                    else User.staff_code.desc()
                )
            elif user_filter.sort_by == SortUserBy.JOIN_DATE:
                query = query.order_by(
                    User.join_date.asc()
                    if user_filter.sort_direction == SortDirection.ASC
                    else User.join_date.desc()
                )
            elif user_filter.sort_by == SortUserBy.TYPE:
                query = query.order_by(
                    User.type.asc()
                    if user_filter.sort_direction == SortDirection.ASC
                    else User.type.desc()
                )
            elif user_filter.sort_by == SortUserBy.UPDATED_AT:
                query = query.order_by(
                    User.updated_at.asc()
                    if user_filter.sort_direction == SortDirection.ASC
                    else User.updated_at.desc()
                )

        total = query.count()
        total_pages = (total + user_filter.size - 1) // user_filter.size

        users = (
            query.offset((user_filter.page - 1) * user_filter.size)
            .limit(user_filter.size)
            .all()
        )

        return PaginatedResponse(
            data=users,
            meta=PaginationMeta(
                total=total,
                total_pages=total_pages,
                page=user_filter.page,
                page_size=user_filter.size,
            ),
        )

    def has_active_assignments(self, user: User) -> bool:
        return (
            self.db.query(Assignment)
            .filter(
                Assignment.assigned_to_id == user.id,
                Assignment.assignment_state.in_(
                    [
                        AssignmentState.WAITING_FOR_ACCEPTANCE,
                        AssignmentState.ACCEPTED,
                    ]
                ),
            )
            .first()
            is not None
        )

    def search_users(self, query: Optional[str], location: Location) -> List[User]:
        """
        Search for users by staff code or username within the same location
        
        Args:
            query: Search term (staff code or username)
            location: Location to filter users by
            
        Returns:
            List of users matching the search criteria
        """
        query_builder = self.db.query(User).filter(
            User.status == Status.ACTIVE,
            User.location == location
        )
        
        if query:
            search = f"%{query}%"
            query_builder = query_builder.filter(
                or_(
                    User.staff_code.ilike(search),
                    User.username.ilike(search)
                )
            )
            
        return query_builder.all()

    def disable_user(self, user: User) -> User:
        user.status = Status.DISABLED
        self.db.commit()
        self.db.refresh(user)
        return user
