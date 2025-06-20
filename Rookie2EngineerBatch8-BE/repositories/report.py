from sqlalchemy.orm import Session
from sqlalchemy import func, case, desc, asc
from schemas.query.sort.report import ReportSort, SortDirection, SortReportBy
from models.category import Category
from models.asset import Asset
from enums.shared.location import Location
from enums.asset.state import AssetState
from schemas.report import ReportRead
from schemas.shared.paginated_response import PaginatedResponse, PaginationMeta


class ReportRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_report_paginated(self, sort: ReportSort, location: Location) -> PaginatedResponse[ReportRead]:
        base_query = self.db.query(
            Category.category_name.label('category'),
            func.count(case((Asset.asset_location == location,
                       Asset.id), else_=None)).label('total'),
            func.sum(case((Asset.asset_state == AssetState.ASSIGNED, 1), else_=0)).label(
                'assigned'),
            func.sum(case((Asset.asset_state == AssetState.AVAILABLE, 1), else_=0)).label(
                'available'),
            func.sum(case((Asset.asset_state == AssetState.NOT_AVAILABLE, 1), else_=0)).label(
                'not_available'),
            func.sum(case((Asset.asset_state == AssetState.WAITING_FOR_RECYCLING, 1), else_=0)).label(
                'waiting_for_recycling'),
            func.sum(case((Asset.asset_state == AssetState.RECYCLED, 1), else_=0)).label(
                'recycled'),
        ).outerjoin(
            Asset, Category.id == Asset.category_id
        ).group_by(
            Category.category_name
        )

        if sort.sort_by:
            subquery = base_query.subquery()
            query = self.db.query(subquery)
            
            if sort.sort_by == SortReportBy.CATEGORY:
                column = func.lower(subquery.c.category)
            else:
                column = subquery.c.get(sort.sort_by)

            if column is None:
                raise ValueError(f"Invalid sort field: {sort.sort_by}")

            direction = asc(
                column) if sort.sort_direction == SortDirection.ASC else desc(column)
            query = query.order_by(direction)
        else:
            query = base_query

        total = query.count()
        total_pages = (total + sort.size - 1) // sort.size

        results = query.offset(
            (sort.page - 1) * sort.size).limit(sort.size).all()
        reports = [ReportRead(**row._asdict()) for row in results]

        return PaginatedResponse(
            data=reports,
            meta=PaginationMeta(
                total=total,
                total_pages=total_pages,
                page=sort.page,
                page_size=sort.size
            )
        )

    async def get_excel_reports(self, page: int, size: int, location: Location) -> list[ReportRead]:
        query = self.db.query(
            Category.category_name.label('category'),
            func.count(case((Asset.asset_location == location,
                       Asset.id), else_=None)).label('total'),
            func.sum(case((Asset.asset_state == AssetState.ASSIGNED, 1), else_=0)).label(
                'assigned'),
            func.sum(case((Asset.asset_state == AssetState.AVAILABLE, 1), else_=0)).label(
                'available'),
            func.sum(case((Asset.asset_state == AssetState.NOT_AVAILABLE, 1), else_=0)).label(
                'not_available'),
            func.sum(case((Asset.asset_state == AssetState.WAITING_FOR_RECYCLING, 1), else_=0)).label(
                'waiting_for_recycling'),
            func.sum(case((Asset.asset_state == AssetState.RECYCLED, 1), else_=0)).label(
                'recycled'),
        ).outerjoin(
            Asset, Category.id == Asset.category_id
        ).group_by(
            Category.category_name
        )
        subquery = query.subquery()
        query = self.db.query(subquery)
        column = func.lower(subquery.c.category)

        direction = asc(column)
        query = query.order_by(direction)
        results = query.offset((page - 1) * size).limit(size).all()
        return [ReportRead(**row._asdict()) for row in results]
