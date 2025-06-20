from typing import Generic, TypeVar, List
from pydantic import BaseModel
from pydantic.generics import GenericModel

T = TypeVar("T")

class PaginationMeta(BaseModel):
    total: int
    total_pages: int
    page: int
    page_size: int

class PaginatedResponse(GenericModel, Generic[T]):
    data: List[T]
    meta: PaginationMeta
