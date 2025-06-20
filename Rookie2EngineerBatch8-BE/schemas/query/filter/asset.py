from typing import Optional
from fastapi import Query
from pydantic import Field, BaseModel

from enums.asset.state import AssetState
from schemas.query.sort.sort_type import SortDirection, SortAssetBy
from schemas.shared.paginated_param import PaginationParams

class AssetFilter(PaginationParams):
    """Filter for asset queries"""
    # Filter options
    # state: Optional[AssetState] = Field(None, description="Filter by asset state")
    category: Optional[str] = Field(None, description="Filter by asset category")

    # Search options
    search: Optional[str] = Query(None, description="Search by asset code, asset name, or username")
    
    # Sorting options
    sort_by: Optional[SortAssetBy] = Query(SortAssetBy.ASSET_CODE, description="Column to sort by")
    sort_direction: Optional[SortDirection] = Field(SortDirection.ASC, description="Sort direction: asc or desc")
    
    
    
    
    class Config:
        """Pydantic config"""
        use_enum_values = True
        orm_mode = True
