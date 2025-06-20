from datetime import datetime
from typing import Optional
from fastapi import Query
from pydantic import Field

from enums.assignment.state import AssignmentState
from schemas.query.sort.sort_type import SortAssignmentBy, SortDirection, SortHomeAssignmentBy
from schemas.shared.paginated_param import PaginationParams


class AssignmentFilter(PaginationParams):
    """Base filter model for assignment queries"""
    # Filter options
    state: Optional[AssignmentState] = Field(None, description="Filter by state")
    assign_date: Optional[datetime] = Field(None, description="Filter by assigned date")
    asset_id: Optional[int] = Field(None, description="Filter by asset id for asset history")
    
    # Search options
    search: Optional[str] = Query(None, description="Search by asset code, asset name, or assignee's username")
    
    # Sorting options
    sort_by: Optional[SortAssignmentBy] = Query(SortAssignmentBy.ID, description="Column to sort by")
    
    sort_direction: Optional[SortDirection] = Field(SortDirection.ASC, description="Sort direction: asc or desc")
    
    class Config:
        """Pydantic config"""
        use_enum_values = True
        

class HomeAssignmentFilter(PaginationParams):
    """Filter for home assignment queries"""
    
    # Sorting options
    sort_by: Optional[SortHomeAssignmentBy] = Query(SortHomeAssignmentBy.ASSET_CODE, description="Column to sort by")
    sort_direction: Optional[SortDirection] = Field(SortDirection.ASC, description="Sort direction: asc or desc")
    class Config:
        """Pydantic config"""
        use_enum_values = True