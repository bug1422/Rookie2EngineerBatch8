from typing import Optional
from pydantic import BaseModel, Field

class IsValid(BaseModel):
    """
    Schema for checking if a user is valid.
    """
    is_valid: bool = Field(
        description="Indicates if the user is valid or not.",
    )

