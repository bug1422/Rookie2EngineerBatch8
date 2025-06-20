import pytest
from datetime import date
from unittest.mock import Mock, patch

from enums.shared.location import Location
from enums.user.status import Status
from schemas.user import UserRead
from schemas.report import ReportRead
from services.report import ReportService

@pytest.fixture
def mock_user():
    return UserRead(
        id=1,
        username="test_user",
        staff_code="SD001",
        first_name="Test",
        last_name="User",
        date_of_birth=date(1990, 1, 1),
        join_date=date(2023, 1, 1),
        location=Location.HCM,
        status=Status.ACTIVE,
        is_first_login=False,
        type="staff"
    )

@pytest.fixture
def mock_report():
    return ReportRead(
        category="Laptop",
        total=10,
        assigned=5,
        available=2,
        not_available=1,
        waiting_for_recycling=1,
        recycled=1
    )

@pytest.fixture
def report_service():
    db = Mock()
    repository = Mock()
    with patch("services.report.ReportRepository", return_value=repository):
        service = ReportService(db)
        service.repository = repository
        yield service 