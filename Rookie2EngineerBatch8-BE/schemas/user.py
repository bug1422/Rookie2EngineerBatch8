from pydantic import BaseModel, root_validator, field_validator, model_validator
from datetime import date
from typing import Optional
from enums.shared.location import Location
from enums.user.gender import Gender
from enums.user.type import Type
from enums.user.status import Status
from utils.validator import Validator
from core.exceptions import BusinessException
from pydantic import Field


class UserBase(BaseModel):
    date_of_birth: date
    join_date: date
    type: Type = Field(default=Type.STAFF)


class UserLogin(BaseModel):
    username: str
    password: str


class UserCreate(UserBase):
    first_name: str = Field(..., min_length=1, max_length=128)
    last_name: str = Field(..., min_length=1, max_length=128)
    gender: Optional[Gender] = None
    location: Location

    @field_validator("gender", mode="before")
    @classmethod
    def blank_gender_to_none(cls, v):
        if v == "":
            return None
        return v

    @field_validator("date_of_birth")
    @classmethod
    def validate_date_of_birth(cls, v: date) -> date:
        if v > date.today():
            raise BusinessException(detail="Date of birth cannot be in the future")
        if not Validator.validate_age_at_least(v, 18):
            raise BusinessException(detail="User must be at least 18 years old")
        return v

    @model_validator(mode="after")
    def validate_dates(self) -> "UserCreate":
        if self.join_date < self.date_of_birth:
            raise ValueError("Join date cannot be before date of birth")
        if self.join_date.weekday() >= 5:  # 5 is Saturday, 6 is Sunday
            raise BusinessException(
                detail="Joined date is Saturday or Sunday. Please select a different date"
            )
        return self


class UserRead(UserBase):
    id: int
    staff_code: str
    first_name: str
    last_name: str
    username: str
    gender: Optional[Gender] = None
    location: Location
    status: Status
    is_first_login: bool

class UserReadSimple(BaseModel):
    staff_code: str
    first_name: str
    last_name: str
    username: str


class UserUpdate(BaseModel):
    date_of_birth: Optional[date] = None
    join_date: Optional[date] = None
    type: Optional[Type] = None
    gender: Optional[Gender] = None
    location: Optional[Location] = None

    @root_validator(pre=True)
    def check_at_least_one_field(cls, values):
        if not any(values.values()):
            raise ValueError("At least one field must be provided for update")
        return values

    @field_validator("date_of_birth")
    @classmethod
    def validate_date_of_birth(cls, v: date) -> date:
        if v > date.today():
            raise BusinessException(detail="Date of birth cannot be in the future")
        if not Validator.validate_age_at_least(v, 18):
            raise BusinessException(detail="User must be at least 18 years old")
        return v

    @model_validator(mode="after")
    def validate_dates(self) -> "UserCreate":
        if self.join_date < self.date_of_birth:
            raise ValueError("Join date cannot be before date of birth")
        if self.join_date.weekday() >= 5:  # 5 is Saturday, 6 is Sunday
            raise BusinessException(
                detail="Joined date is Saturday or Sunday. Please select a different date"
            )
        return self
