from sqlmodel import Field, Relationship
from typing import TYPE_CHECKING, Optional
from models.base import Base
from enums.assignment.state import AssignmentState
from datetime import datetime

if TYPE_CHECKING:
    from models.asset import Asset
    from models.user import User
    from models.request import Request

class Assignment(Base, table=True):
    __tablename__ = "assignment"
    asset_id: int = Field(foreign_key="asset.id")
    assigned_to_id: int = Field(foreign_key="user.id")
    assigned_by_id: int = Field(foreign_key="user.id")
    assign_date: datetime = Field(...)
    assignment_note: Optional[str] = Field(default=None)
    assignment_state: AssignmentState = Field(default=AssignmentState.WAITING_FOR_ACCEPTANCE)

    asset: "Asset" = Relationship(back_populates="assignments")
    assigned_to_user: "User" = Relationship(
        back_populates="assignments_to",
        sa_relationship_kwargs={"foreign_keys": "[Assignment.assigned_to_id]"}
    )
    assigned_by_user: "User" = Relationship(
        back_populates="assignments_by",
        sa_relationship_kwargs={"foreign_keys": "[Assignment.assigned_by_id]"}
    )
    requests: "Request" = Relationship(
        back_populates="assignment",
        sa_relationship_kwargs={"foreign_keys": "[Request.assignment_id]"}
    )
