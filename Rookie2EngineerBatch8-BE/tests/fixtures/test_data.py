import pytest
from datetime import date
from schemas.user import UserRead
from schemas.asset import AssetRead
from schemas.category import CategoryRead
from enums.user.type import Type
from enums.user.status import Status
from enums.shared.location import Location
from enums.user.gender import Gender
from enums.asset.state import AssetState

@pytest.fixture
def multiple_users():
    """Fixture that provides multiple test users"""
    return [
        UserRead(
            id=1,
            username="user1",
            staff_code="SD0001",
            first_name="User",
            last_name="One",
            date_of_birth=date(1990, 1, 1),
            join_date=date(2023, 1, 1),
            gender=Gender.MALE,
            type=Type.STAFF,
            location=Location.HANOI,
            status=Status.ACTIVE,
            is_first_login=True,
        ),
        UserRead(
            id=2,
            username="user2",
            staff_code="SD0002",
            first_name="User",
            last_name="Two",
            date_of_birth=date(1990, 1, 1),
            join_date=date(2023, 1, 1),
            gender=Gender.FEMALE,
            type=Type.ADMIN,
            location=Location.HCM,
            status=Status.ACTIVE,
            is_first_login=False,
        ),
    ]

@pytest.fixture
def multiple_assets():
    """Fixture that provides multiple test assets"""
    return [
        AssetRead(
            id=1,
            asset_code="A001",
            asset_name="Test Asset 1",
            category_id=1,
            specification="Test Specification 1",
            installed_date=date(2023, 1, 1),
            asset_state=AssetState.AVAILABLE,
            asset_location=Location.HANOI,
            category=CategoryRead(
                id=1,
                category_name="Test Category",
                prefix="A"
            )
        ),
        AssetRead(
            id=2,
            asset_code="A002",
            asset_name="Test Asset 2",
            category_id=1,
            specification="Test Specification 2",
            installed_date=date(2023, 1, 2),
            asset_state=AssetState.AVAILABLE,
            asset_location=Location.HANOI,
            category=CategoryRead(
                id=1,
                category_name="Test Category",
                prefix="A"
            )
        )
    ] 