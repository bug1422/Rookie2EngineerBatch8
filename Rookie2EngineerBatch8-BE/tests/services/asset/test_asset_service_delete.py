import pytest
from core.exceptions import BusinessException, NotFoundException
from enums.shared.location import Location
from schemas.query.check.isValid import IsValid


class TestAssetDelete:
    def test_delete_asset_success(self, asset_service, mock_user, mock_asset_read):
        # Arrange
        asset_service.repository.get_asset_by_id.return_value = mock_asset_read
        asset_service.repository.has_historical_assignments.return_value = IsValid(
            is_valid=True
        )

        # Act
        asset_service.delete_asset(mock_asset_read.id, mock_user.location)

        # Assert
        asset_service.repository.delete_asset.assert_called_once_with(mock_asset_read)


    def test_delete_asset_with_historical_assignments(self, asset_service, mock_user, mock_asset_read):
        # Arrange
        asset_service.repository.get_asset_by_id.return_value = mock_asset_read
        asset_service.repository.has_historical_assignments.return_value = IsValid(is_valid=False, detail="Asset has historical assignments")

        # Act & Assert
        with pytest.raises(BusinessException, match="Cannot delete the asset because it belongs to one or more historical assignments"):
            asset_service.delete_asset(mock_asset_read.id, mock_user.location)

    def test_check_asset_valid_success(self, asset_service, mock_asset_read):
        # Arrange
        asset_service.repository.get_asset_by_id.return_value = mock_asset_read
        asset_service.repository.has_historical_assignments.return_value = IsValid(
            is_valid=False
        )

        # Act
        result = asset_service.check_asset_valid(mock_asset_read.id)

        # Assert
        assert result.is_valid is False