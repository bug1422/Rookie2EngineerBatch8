from sqlmodel import Field, Relationship
from typing import Optional, TYPE_CHECKING
from models.base import Base
from enums.request.state import RequestState
from datetime import datetime

if TYPE_CHECKING:
    from models.user import User
    from models.assignment import Assignment

class Request(Base, table=True):
    __tablename__ = "request"
    assignment_id: int = Field(foreign_key="assignment.id")
    requested_by_id: int = Field(foreign_key="user.id")
    accepted_by_id: Optional[int] = Field(foreign_key="user.id", default=None)
    return_date: Optional[datetime] = Field(...)
    request_state: RequestState = Field(default=RequestState.WAITING_FOR_RETURNING)
    
    requested_by_user: "User" = Relationship(
        back_populates="requests_made",
        sa_relationship_kwargs={"foreign_keys": "[Request.requested_by_id]"}
    )
    accepted_by_user: Optional["User"] = Relationship(
        back_populates="requests_accepted",
        sa_relationship_kwargs={"foreign_keys": "[Request.accepted_by_id]"}
    )
    assignment: "Assignment" = Relationship(
        sa_relationship_kwargs={"foreign_keys": "[Request.assignment_id]"}
    )
