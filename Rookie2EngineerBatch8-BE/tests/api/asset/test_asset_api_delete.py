from fastapi import status
import pytest
from core.exceptions import NotFoundException, ValidationException

class TestAssetDelete:
    def test_delete_asset_success(self, client, mocker, mock_asset):
        """Test deleting an asset successfully."""
        mocker.patch("services.asset.AssetService.delete_asset")
        
        response = client.delete(f"/v1/assets/{mock_asset.id}")
        
        assert response.status_code == status.HTTP_204_NO_CONTENT
    
    def test_delete_asset_not_found(self, client, mocker):
        """Test deleting a non-existent asset."""
        non_existent_id = 9999
        mocker.patch(
            "services.asset.AssetService.delete_asset",
            side_effect=NotFoundException(f"Asset with id {non_existent_id} not found"),
        )
        
        response = client.delete(f"/v1/assets/{non_existent_id}")
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
        error_data = response.json()
        assert "detail" in error_data
        assert f"Asset with id {non_existent_id} not found" in error_data["detail"]
    
    def test_delete_asset_with_assignments(self, client, mocker, mock_asset):
        """Test deleting an asset that has historical assignments."""
        error_message = "Cannot delete asset with historical assignments"
        mocker.patch(
            "services.asset.AssetService.delete_asset",
            side_effect=ValidationException(error_message),
        )
        
        response = client.delete(f"/v1/assets/{mock_asset.id}")
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        error_data = response.json()
        assert "detail" in error_data
        assert error_message in error_data["detail"]
    
    @pytest.mark.parametrize(("invalid_id", "expected_status_code"), [
        ("invalid", status.HTTP_422_UNPROCESSABLE_ENTITY),
        ("abc123", status.HTTP_422_UNPROCESSABLE_ENTITY)
    ])
    def test_delete_asset_invalid_id(self, client, invalid_id, expected_status_code):
        """Test deleting an asset with invalid ID formats."""
        response = client.delete(f"/v1/assets/{invalid_id}")
        assert response.status_code == expected_status_code 