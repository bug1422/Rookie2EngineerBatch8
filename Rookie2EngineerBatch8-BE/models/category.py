from sqlmodel import Field, Relationship
from typing import TYPE_CHECKING, List
from models.base import Base

if TYPE_CHECKING:
    from models.asset import Asset

class Category(Base, table=True):
    __tablename__ = "category"
    category_name: str = Field(..., max_length=100)
    prefix: str = Field(..., max_length=10)
    id_counter: int = Field(default=0)
    
    assets: List["Asset"] = Relationship(back_populates="category")