from sqlmodel import Field, Relationship
from enums.user.gender import Gender
from enums.user.status import Status
from enums.user.type import Type
from enums.shared.location import Location
from datetime import date
from typing import Optional, TYPE_CHECKING, List
from models.base import Base

if TYPE_CHECKING:
    from models.assignment import Assignment
    from models.request import Request

class User(Base, table=True):
    __tablename__ = "user"
    staff_code: str = Field(unique=True, index=True)
    username: str = Field(unique=True, index=True)
    password: str
    first_name: str = Field(..., min_length=1, max_length=128)
    last_name: str = Field(..., min_length=1, max_length=128)
    date_of_birth: date
    join_date: date
    gender: Optional[Gender] = None
    type: Type = Field(default=Type.STAFF)
    location: Location
    status: Status = Field(default=Status.ACTIVE)
    is_first_login: bool = Field(default=True)

    # Assignments where user is the assignee
    assignments_to: List["Assignment"] = Relationship(
        back_populates="assigned_to_user",
        sa_relationship_kwargs={"foreign_keys": "Assignment.assigned_to_id"}
    )
    # Assignments where user is the assigner
    assignments_by: List["Assignment"] = Relationship(
        back_populates="assigned_by_user",
        sa_relationship_kwargs={"foreign_keys": "Assignment.assigned_by_id"}
    )
    # Requests made by this user
    requests_made: List["Request"] = Relationship(
        back_populates="requested_by_user",
        sa_relationship_kwargs={"foreign_keys": "Request.requested_by_id"}
    )
    # Requests accepted by this user
    requests_accepted: List["Request"] = Relationship(
        back_populates="accepted_by_user",
        sa_relationship_kwargs={"foreign_keys": "Request.accepted_by_id"}
    )
