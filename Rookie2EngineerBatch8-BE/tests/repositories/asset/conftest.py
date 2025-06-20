import pytest
from datetime import date
from unittest.mock import Mock
from enums.asset.state import AssetState
from enums.shared.location import Location
from enums.user.status import Status
from schemas.asset import AssetRead
from schemas.category import CategoryRead
from schemas.user import UserRead
from repositories.asset import AssetRepository
from tests.test_data.test_data import Id

@pytest.fixture
def mock_user():
    return UserRead(
        id=Id.USER_ID_VALID.value,
        username="test_user",
        staff_code="SD001",
        first_name="Test",
        last_name="User",
        date_of_birth=date(1990, 1, 1),
        join_date=date(2023, 1, 1),
        location=Location.HANOI,
        status=Status.ACTIVE,
        is_first_login=False,
        type="staff"
    )

@pytest.fixture
def mock_category():
    return CategoryRead(
        id=1,
        category_name="Laptop",
        prefix="LA"
    )

@pytest.fixture
def mock_asset_read(mock_category):
    return AssetRead(
        id=1,
        asset_code="LA000001",
        asset_name="Test Laptop",
        specification="Test specs",
        asset_location=Location.HANOI,
        asset_state=AssetState.AVAILABLE,
        installed_date=date(2023, 1, 1),
        category_id=mock_category.id,
        category=mock_category
    )

@pytest.fixture(
    scope="function"
)
def asset_repository():
    db = Mock()
    repository = AssetRepository(db)
    yield repository