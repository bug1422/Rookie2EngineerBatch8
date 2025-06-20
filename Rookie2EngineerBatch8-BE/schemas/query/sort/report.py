from typing import Optional
from fastapi import Query
from schemas.shared.paginated_param import PaginationParams
from schemas.query.sort.sort_type import SortReportBy, SortDirection
from pydantic import Field

class ReportSort(PaginationParams):
    """Report sort model"""
    sort_by: Optional[SortReportBy] = Query(SortReportBy.CATEGORY, description="Sort by category")
    sort_direction: Optional[SortDirection] = Field(SortDirection.ASC, description="Sort direction: asc or desc")

