import pytest
from enums.asset.state import AssetState
from schemas.asset import AssetCreate
from datetime import date
from tests.test_data.mock_asset import get_mock_asset_create
from sqlalchemy.exc import IntegrityError

@pytest.fixture
def mock_asset_create():
    return get_mock_asset_create()

class TestAssetCreate:
    def test_create_asset_success(self, asset_repository, mock_asset_create, mocker):
        # Mock database behavior
        asset_repository.db.add.return_value = None
        asset_repository.db.commit.return_value = None
        asset_repository.db.refresh.return_value = None

        result = asset_repository.create_asset(asset_data=mock_asset_create)

        assert result is not None
        assert result.asset_state == AssetState.AVAILABLE
        asset_repository.db.add.assert_called_once_with(mock_asset_create)
        asset_repository.db.commit.assert_called_once()



    def test_create_asset_duplicate(self, asset_repository, mock_asset_create, mocker):
        # Simulate a unique constraint violation
        asset_repository.db.add.side_effect = IntegrityError("duplicate key", {}, None)
        asset_repository.db.commit.return_value = None
        asset_repository.db.refresh.return_value = None

        with pytest.raises(IntegrityError):
            asset_repository.create_asset(asset_data=mock_asset_create)
