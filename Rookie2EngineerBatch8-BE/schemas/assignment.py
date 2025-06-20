from pydantic import BaseModel, root_validator, model_validator
from datetime import datetime, date
from typing import Optional
from enums.assignment.state import AssignmentState
from schemas.user import UserRead
from schemas.asset import AssetRead

class AssignmentBase(BaseModel):
    asset_id: int
    assigned_to_id: int
    assigned_by_id: int
    assigned_to_username: str
    assigned_by_username: str
    assignment_note: Optional[str]

class AssignmentUpdate(BaseModel):
    assigned_to_id: Optional[int] = None
    asset_id: Optional[int] = None
    assign_date: Optional[datetime] = None
    assignment_note: Optional[str] = None

    @root_validator(pre=True)
    def check_at_least_one_field(cls, values):
        if not any(values.values()):
            raise ValueError('At least one field must be provided for update')
        return values
    
class AssignmentStateUpdate(BaseModel):
    assignment_state: AssignmentState

class AssignmentCreate(BaseModel):
    asset_id: int
    assigned_to_id: int
    assign_date: datetime
    assignment_note: Optional[str] = None

    @model_validator(mode='after')
    def validate_assign_date(self):
        if self.assign_date.date() < datetime.now().date():
            raise ValueError("Assign date must be today or in the future")
        return self

class AssignmentRead(AssignmentBase):
    id: int
    assign_date: date
    assignment_state: AssignmentState
    asset: AssetRead

class AssignmentUpdateResponse(BaseModel):
    asset_id: int
    assigned_to_id: int
    assigned_by_id: int
    assignment_note: str
    assignment_state: Optional[AssignmentState] = None

class AssignmentUserReadByUID(BaseModel):
    id: int
    assign_date: date
    assignment_note: Optional[str]
    assignment_state: AssignmentState
    assigned_to_user: UserRead
    assigned_by_user: UserRead
    asset: AssetRead

class AssignmentReadSimple(BaseModel):
    id: int
    assign_date: date
    assignment_state: AssignmentState
    assignment_note: Optional[str] = None

class AssignmentReadDetail(BaseModel):
    assignment: AssignmentReadSimple
    assigned_to_user: UserRead
    assigned_by_user: UserRead
    asset: AssetRead