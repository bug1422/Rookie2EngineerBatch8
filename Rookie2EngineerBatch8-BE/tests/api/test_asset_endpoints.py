from fastapi import status
import pytest
import random
from core.exceptions import NotFoundException
from test_data.mock_asset import get_mock_asset, get_mock_assets

def test_get_asset_by_id_success_with_mock(client, mocker):
    """Test getting an asset by ID when the asset exists using mocks."""
    mock_asset = get_mock_asset()
    mocker.patch("services.asset.AssetService.read_asset", return_value=mock_asset)
    
    response = client.get(f"/api/v1/assets/{mock_asset.id}")
    
    assert response.status_code == status.HTTP_200_OK
    
    asset_data = response.json()
    
    assert asset_data["id"] == mock_asset.id
    assert asset_data["asset_code"] == mock_asset.asset_code
    assert asset_data["asset_name"] == mock_asset.asset_name
    assert asset_data["asset_location"] == mock_asset.asset_location
    assert asset_data["asset_state"] == mock_asset.asset_state
    assert asset_data["installed_date"] == mock_asset.installed_date 
    
def test_get_asset_by_id_not_found_with_mock(client, mocker):
    """Test getting an asset by ID when the asset does not exist using mocks."""
    non_existent_id = 9999
    mocker.patch(
        "services.asset.AssetService.read_asset",
        side_effect=NotFoundException(
            f"Asset with id {non_existent_id} not found"),
    )

    # Act
    response = client.get(f"/api/v1/assets/{non_existent_id}")

    # Assert
    assert response.status_code == status.HTTP_404_NOT_FOUND

    error_data = response.json()
    assert "detail" in error_data
    assert f"Asset with id {non_existent_id} not found" in error_data["detail"]
    
@pytest.mark.parametrize(("invalid_id", "expected_status_code"), [
    ("invalid", status.HTTP_422_UNPROCESSABLE_ENTITY),
    ("abc123", status.HTTP_422_UNPROCESSABLE_ENTITY),
    ("", status.HTTP_404_NOT_FOUND)
])
def test_get_asset_by_id_invalid_id_with_mock(client, invalid_id, expected_status_code):
    """Test getting a asset by ID with various invalid ID formats."""
    # Act
    response = client.get(f"/api/v1/assets/{invalid_id}")

    # Assert
    assert response.status_code == expected_status_code
