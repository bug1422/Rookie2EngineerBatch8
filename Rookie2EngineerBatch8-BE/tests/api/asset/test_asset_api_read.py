from fastapi import status
import pytest
from core.exceptions import NotFoundException
from schemas.shared.paginated_response import PaginatedResponse

class TestAssetRead:
    def test_get_asset_by_id_success(self, client, mocker, mock_asset):
        """Test getting an asset by ID when the asset exists."""
        mocker.patch("services.asset.AssetService.read_asset", return_value=mock_asset)
        
        response = client.get(f"/v1/assets/{mock_asset.id}")
        
        assert response.status_code == status.HTTP_200_OK
        asset_data = response.json()
        assert asset_data["id"] == mock_asset.id
        assert asset_data["asset_code"] == mock_asset.asset_code
        assert asset_data["asset_name"] == mock_asset.asset_name
        assert asset_data["asset_location"] == mock_asset.asset_location
        assert asset_data["asset_state"] == mock_asset.asset_state
        assert asset_data["installed_date"] == mock_asset.installed_date.isoformat()
    
    def test_get_asset_by_id_not_found(self, client, mocker):
        """Test getting an asset by ID when the asset does not exist."""
        non_existent_id = 9999
        mocker.patch(
            "services.asset.AssetService.read_asset",
            side_effect=NotFoundException(f"Asset with id {non_existent_id} not found"),
        )

        response = client.get(f"/v1/assets/{non_existent_id}")

        assert response.status_code == status.HTTP_404_NOT_FOUND
        error_data = response.json()
        assert "detail" in error_data
        assert f"Asset with id {non_existent_id} not found" in error_data["detail"]
    
    @pytest.mark.parametrize(("invalid_id", "expected_status_code"), [
        ("invalid", status.HTTP_422_UNPROCESSABLE_ENTITY),
        ("abc123", status.HTTP_422_UNPROCESSABLE_ENTITY)
    ])
    def test_get_asset_by_id_invalid_id(self, client, invalid_id, expected_status_code):
        """Test getting an asset by ID with various invalid ID formats."""
        response = client.get(f"/v1/assets/{invalid_id}")
        assert response.status_code == expected_status_code
    
    def test_get_assets_list(self, client, mocker, mock_assets):
        """Test getting a list of assets."""
        # Mock the service to return proper AssetRead objects
        mocker.patch(
            "services.asset.AssetService.read_assets_paginated",
            return_value=PaginatedResponse(
                data=mock_assets,
                meta={
                    "page": 1,
                    "page_size": 10,
                    "total": len(mock_assets),
                    "total_pages": (len(mock_assets) + 9) // 10
                }
            )
        )
        
        response = client.get("/v1/assets")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "data" in data
        assert "meta" in data
        assert data["meta"]["page"] == 1
        assert data["meta"]["page_size"] == 10
        assert data["meta"]["total"] == len(mock_assets)
        assert data["meta"]["total_pages"] == (len(mock_assets) + 9) // 10 