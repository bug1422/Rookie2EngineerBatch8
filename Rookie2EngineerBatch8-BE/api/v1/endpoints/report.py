from fastapi import APIRouter, Depends, status
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from api.dependencies import get_db_session
from core.exceptions import NotImplementedException
from schemas.report import ReportRead
from typing import List
from schemas.query.sort.report import ReportSort
from schemas.shared.paginated_response import PaginatedResponse
from services.report import ReportService
from schemas.user import UserRead
from api.dependencies import get_current_admin
from datetime import datetime

router = APIRouter(prefix="/reports", tags=["Reports"])


@router.get("",
            response_model=PaginatedResponse[ReportRead],
            status_code=status.HTTP_200_OK,
            summary="Get paginated list of report",
            description="Get paginated list of report with the provided details.")
async def get_report_paginated(
    sort: ReportSort = Depends(),
    db: Session = Depends(get_db_session),
    current_user: UserRead = Depends(get_current_admin)
) -> PaginatedResponse[ReportRead]:
    report_service = ReportService(db)
    return report_service.get_report_paginated(sort, current_user)


@router.get("/all",
            response_model=List[ReportRead],
            status_code=status.HTTP_200_OK,
            summary="Get all report",
            description="Get all report with the provided details.")
async def get_all_report(sort: ReportSort = Depends(), db: Session = Depends(get_db_session)):
    raise NotImplementedException()


@router.get("/export",
            status_code=status.HTTP_200_OK,
            summary="Export report file",
            description="Export all report into an excel file.")
async def export_to_excel(
    db: Session = Depends(get_db_session),
    current_user: UserRead = Depends(get_current_admin)
):
    now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"reports_{now}.xlsx"
    service = ReportService(db)
    stream = await service.convert_to_excel(current_user)
    return StreamingResponse(
        content=stream,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )
