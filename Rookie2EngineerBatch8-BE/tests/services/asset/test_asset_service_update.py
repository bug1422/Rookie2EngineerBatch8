import pytest
from core.exceptions import BusinessException, NotFoundException
from enums.asset.state import AssetState
from enums.shared.location import Location
from schemas.asset import AssetUpdate

class TestAssetUpdate:
    @pytest.mark.parametrize("asset_state,expected_error", [
        (AssetState.AVAILABLE, None),
        (AssetState.ASSIGNED, "Asset is currently assigned to a user, cannot be updated"),
        (AssetState.RECYCLED, None),
        (AssetState.NOT_AVAILABLE, None),
    ])
    def test_update_asset_state_validation(self, asset_state, expected_error, asset_service, mock_user, mock_asset_read):
        # Arrange
        mock_asset = mock_asset_read.model_copy()
        mock_asset.asset_state = asset_state
        asset_service.repository.get_asset_by_id.return_value = mock_asset
        
        update_data = AssetUpdate(asset_name="Updated Name")

        # Act & Assert
        if expected_error:
            with pytest.raises(BusinessException, match=expected_error):
                asset_service.update_asset(mock_user, mock_asset.id, update_data)
        else:
            asset_service.repository.update_asset.return_value = mock_asset
            result = asset_service.update_asset(mock_user, mock_asset.id, update_data)
            assert result.id == mock_asset.id

    @pytest.mark.parametrize("user_location,asset_location,should_succeed", [
        (Location.HANOI, Location.HANOI, True),
        (Location.HCM, Location.HANOI, False),
        (Location.HANOI, Location.HCM, False),
    ])
    def test_update_asset_location_validation(self, user_location, asset_location, should_succeed, asset_service, mock_user, mock_asset_read):
        # Arrange
        mock_user.location = user_location
        mock_asset = mock_asset_read.model_copy()
        mock_asset.asset_location = asset_location
        asset_service.repository.get_asset_by_id.return_value = mock_asset
        
        update_data = AssetUpdate(asset_name="Updated Name")

        # Act & Assert
        if should_succeed:
            asset_service.repository.update_asset.return_value = mock_asset
            result = asset_service.update_asset(mock_user, mock_asset.id, update_data)
            assert result.id == mock_asset.id
        else:
            with pytest.raises(BusinessException, match="You are not allowed to update asset from other location"):
                asset_service.update_asset(mock_user, mock_asset.id, update_data)

    def test_update_asset_not_found(self, asset_service, mock_user):
        # Arrange
        asset_service.repository.get_asset_by_id.return_value = None
        update_data = AssetUpdate(asset_name="Updated Name")

        # Act & Assert
        with pytest.raises(NotFoundException, match="Asset not found"):
            asset_service.update_asset(mock_user, 1, update_data) 