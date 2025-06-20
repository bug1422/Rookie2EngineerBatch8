from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from enums.request.state import RequestState
from schemas.assignment import AssignmentRead, AssignmentReadSimple
from schemas.asset import AssetRead
from schemas.user import UserReadSimple

class RequestBase(BaseModel):
    assignment_id: int
    requested_by_id: int
    return_date: Optional[datetime] = None

class RequestCreate(BaseModel):
    assignment_id: int

class RequestRead(RequestBase):
    id: int
    accepted_by_id: Optional[int] = None
    request_state: RequestState

    
class RequestUpdate(BaseModel):
    request_state: Optional[RequestState] = None

class RequestCompleteResponse(BaseModel):
    id: int
    request_state: RequestState
    return_date: datetime

    
class RequestReadDetail(BaseModel):
    id: int
    asset: AssetRead
    requested_by: UserReadSimple
    accepted_by: Optional[UserReadSimple] = None
    assignment: AssignmentReadSimple
    return_date: Optional[datetime] = None
    request_state: RequestState
