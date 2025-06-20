from sqlalchemy.orm import Session
from repositories.report import ReportRepository
from schemas.query.sort.sort_type import SortDirection, SortReportBy
from schemas.query.sort.report import ReportSort
from schemas.user import UserRead
from schemas.shared.paginated_response import PaginatedResponse
from openpyxl import Workbook
from io import BytesIO 
from asyncio import to_thread

class ReportService:
    def __init__(self, db: Session):
        self.repository = ReportRepository(db)

    def get_report_paginated(self, sort: ReportSort, current_user: UserRead) -> PaginatedResponse:
        return self.repository.get_report_paginated(sort, current_user.location)

    async def convert_to_excel(self, current_user: UserRead) -> BytesIO:
        workbook = Workbook(write_only=True)
        worksheet = workbook.create_sheet(title="Report")
        worksheet.append(["Category", "Total", "Assigned", "Available",
                  "Not available", "Waiting for recycling", "Recycled"])
        sort = ReportSort(page=1, size=100,sort_by=SortReportBy.CATEGORY,sort_direction=SortDirection.DESC)
        while True:
            response = await to_thread(self.repository.get_report_paginated, sort, current_user.location)
            reports = response.data
            if len(reports) == 0:
                break
            for report in reports:
                worksheet.append([report.category, report.total, report.assigned, report.available,
                          report.not_available, report.waiting_for_recycling, report.recycled])

            sort.page += 1
        stream = BytesIO()
        workbook.save(stream)
        stream.seek(0)
        return stream