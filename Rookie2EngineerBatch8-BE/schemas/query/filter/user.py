from typing import Optional
from fastapi import Query
from pydantic import Field

from enums.user.type import Type
from schemas.query.sort.sort_type import SortDirection, SortUserBy
from schemas.shared.paginated_param import PaginationParams 

class UserFilter(PaginationParams):
    """Base filter model for user queries"""
    # Filter options
    type: Optional[Type] = Field(None, description="Filter by user type")
    
    # Search options
    search: Optional[str] = Query(None, description="Search by staff code or name")
    
    # Sorting options
    sort_by: Optional[SortUserBy] = Query(SortUserBy.FIRST_NAME, 
                                   description="Column to sort by")
    sort_direction: Optional[SortDirection] = Field(SortDirection.ASC, description="Sort direction: asc or desc")
    
    class Config:
        """Pydantic config"""
        use_enum_values = True