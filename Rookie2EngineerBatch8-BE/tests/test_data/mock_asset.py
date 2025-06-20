from enums.shared.location import Location
from enums.asset.state import AssetState
from schemas.asset import AssetRead, AssetCreate
from schemas.category import CategoryRead
from datetime import datetime, timezone

def get_mock_asset_create():
    return AssetCreate(
        asset_name="Test Asset",
        category_id=1,
        specification="Test Specification",
        installed_date=datetime.now(timezone.utc).date(),
        asset_state=AssetState.AVAILABLE,
        asset_location=Location.HANOI
    )

def get_mock_asset():
    return AssetRead(
        id=1,
        asset_code="LA000001",
        asset_name="Test Asset",
        asset_state=AssetState.AVAILABLE,
        category_id=1,
        category=CategoryRead(
            id=1,
            category_name="Laptop",
            prefix="LA"
        ),
        asset_location=Location.HANOI,
        installed_date=datetime.now(timezone.utc).date(),
        specification="Test Specification"
    )

def get_mock_assets(count=5):
    category = CategoryRead(
        id=1,
        category_name="Laptop",
        prefix="LA"
    )
    return [
        AssetRead(
            id=index,
            asset_code=f"LA{str(index).zfill(6)}",
            asset_name=f"Test Asset {index}",
            asset_state=AssetState.AVAILABLE,
            category_id=1,
            category=category,
            asset_location=Location.HANOI,
            installed_date=datetime.now(timezone.utc).date(),
            specification="Test Specification"
        )
        for index in range(1, count+1)
    ]


def get_mock_asset_for_deletion():
    """Get a mock asset that can be safely deleted (no historical assignments)"""
    return AssetRead(
        id=1,
        asset_code="LA000001",
        asset_name="Test Asset for Deletion",
        asset_state=AssetState.AVAILABLE,
        category_id=1,
        category=CategoryRead(id=1, category_name="Laptop", prefix="LA"),
        asset_location=Location.HANOI,
        installed_date=datetime.now(timezone.utc).date(),
        specification="Test Specification",
    )


def get_mock_asset_with_assignments():
    """Get a mock asset that has historical assignments"""
    return AssetRead(
        id=2,
        asset_code="LA000002",
        asset_name="Test Asset with Assignments",
        asset_state=AssetState.ASSIGNED,
        category_id=1,
        category=CategoryRead(id=1, category_name="Laptop", prefix="LA"),
        asset_location=Location.HANOI,
        installed_date=datetime.now(timezone.utc).date(),
        specification="Test Specification",
    )
