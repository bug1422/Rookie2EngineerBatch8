from datetime import datetime
from typing import Optional
from fastapi import Query
from pydantic import Field

from enums.request.state import RequestState
from schemas.query.sort.sort_type import SortDirection, SortRequestBy
from schemas.shared.paginated_param import PaginationParams

class RequestFilter(PaginationParams):
    """Base filter model for request queries"""
    # Filter options
    state: Optional[RequestState] = Field(None, description="Filter by state")
    return_date: Optional[datetime] = Field(None, description="Filter by return date")
    
    # Search options
    search: Optional[str] = Query(None, description="Search by asset code or asset name or requester's username")
    
    # Sorting options
    sort_by: Optional[SortRequestBy] = Query(SortRequestBy.ID, 
                                   description="Column to sort by")
    sort_direction: Optional[SortDirection] = Field(SortDirection.ASC, description="Sort direction: asc or desc")
    
    class Config:
        """Pydantic config"""
        use_enum_values = True