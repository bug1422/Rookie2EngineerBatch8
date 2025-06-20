from sqlmodel import Field, Relationship
from typing import List, TYPE_CHECKING
from models.base import Base
from models.category import Category
from datetime import date
from enums.asset.state import AssetState
from enums.shared.location import Location

if TYPE_CHECKING:
    from models.assignment import Assignment

class Asset(Base, table=True):
    __tablename__ = "asset"
    asset_code: str = Field(...)
    asset_name: str = Field(...)
    specification: str = Field(...)
    installed_date: date = Field(...)
    asset_state: AssetState = Field(default=AssetState.NOT_AVAILABLE)
    asset_location: Location = Field(...)
    category_id: int = Field(foreign_key="category.id")
    
    category: "Category" = Relationship(back_populates="assets")
    assignments: List["Assignment"] = Relationship(back_populates="asset")
