from pydantic import BaseModel, root_validator, field_validator
from datetime import date
from enums.shared.location import Location
from enums.asset.state import AssetState
from typing import Optional
from schemas.category import CategoryRead

class AssetHistory(BaseModel):
    """Asset history model"""
    id: int
    assign_date: date
    assigned_to: str
    assigned_by: str
    return_date: Optional[date] = None

class AssetBase(BaseModel):
    asset_name: str
    

class AssetCreate(AssetBase):
    category_id: int
    specification: str
    installed_date: date
    asset_state: AssetState

class AssetRead(AssetBase):
    id: int
    asset_code: str
    specification: str
    installed_date: date
    asset_state: AssetState
    asset_location: Location
    category: CategoryRead

class AssetUpdate(BaseModel):
    asset_name: Optional[str] = None
    specification: Optional[str] = None
    installed_date: Optional[date] = None
    asset_state: Optional[AssetState] = None

    @root_validator(pre=True)
    def check_at_least_one_field(cls, values):
        if not any(values.get(field) is not None for field in ['asset_name', 'specification', 'installed_date', 'asset_state']):
            raise ValueError('At least one field must be provided fr update')
        return values
    
    @field_validator('installed_date')
    def check_installed_date(cls, v):
        if v > date.today():
            raise ValueError('Installed date cannot be in the future')
        return v