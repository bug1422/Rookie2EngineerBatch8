from pydantic import BaseModel, Field


class PaginationParams(BaseModel):
    """Base pagination parameters for query parameters"""
    page: int = Field(1, ge=1, description="Page number, starting from 1")
    size: int = Field(10, ge=1, le=100, description="Number of items per page")