from fastapi import status, Depends
import pytest
from datetime import datetime, date
from enums.asset.state import AssetState
from enums.shared.location import Location
from schemas.asset import AssetCreate
from tests.test_data.mock_asset import get_mock_asset_create
from tests.test_data.mock_user import get_mock_user_read
from core.exceptions import BusinessException, NotFoundException
from pydantic import ValidationError
from main import app

def get_mock_asset_create_dict():
    # Returns a dict with all fields as JSON-serializable types
    return {
        "asset_name": "Test Asset",
        "category_id": 1,
        "specification": "Test Specification",
        "installed_date": date(2024, 1, 1).isoformat(),
        "asset_state": "AVAILABLE"
    }

def override_get_current_user():
    return get_mock_user_read()

class TestAssetCreate:
    def test_create_asset_success(self, client, mocker, mock_asset):
        """Test creating a new asset successfully."""
        # Override authentication dependency
        app.dependency_overrides[Depends(override_get_current_user)] = override_get_current_user

        # Mock the category service to return a category with id_counter
        mock_category = mocker.Mock()
        mock_category.id = 1
        mock_category.prefix = "TC"
        mock_category.id_counter = 0
        mock_category_service = mocker.Mock()
        mock_category_service.get_category_by_id.return_value = mock_category
        mock_category_service.update_category.return_value = mock_category
        mocker.patch("services.asset.CategoryService", return_value=mock_category_service)
        
        # Mock the asset service to return our mock asset
        mocker.patch("services.asset.AssetService.create_asset", return_value=mock_asset)
        
        asset_data = get_mock_asset_create_dict()
        
        response = client.post("/v1/assets/", json=asset_data, headers={"Authorization": "Bearer fake-admin-token"})
        
        assert response.status_code == status.HTTP_201_CREATED
        response_data = response.json()
        assert response_data["asset_name"] == asset_data["asset_name"]
        assert response_data["category_id"] == asset_data["category_id"]
        assert response_data["specification"] == asset_data["specification"]
        assert response_data["installed_date"] == asset_data["installed_date"]
        assert response_data["asset_state"] == asset_data["asset_state"]
        
        # Clean up
        app.dependency_overrides = {}
    
    def test_create_asset_invalid_data(self, client, mocker):
        """Test creating a new asset with invalid data."""
        # Override authentication dependency
        app.dependency_overrides[Depends(override_get_current_user)] = override_get_current_user

        invalid_data = {
            "asset_name": "Test@Asset",  # Special character
            "category_id": 0,  # Invalid category ID
            "specification": "",  # Empty specification
            "installed_date": "invalid-date",  # Invalid date format
            "asset_state": "invalid-state"  # Invalid state
        }
        
        response = client.post("/v1/assets/", json=invalid_data, headers={"Authorization": "Bearer fake-admin-token"})
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        errors = response.json()
        assert "detail" in errors
        assert any("asset_name" in str(error) for error in errors["detail"])
        assert any("category_id" in str(error) for error in errors["detail"])
        assert any("specification" in str(error) for error in errors["detail"])
        assert any("installed_date" in str(error) for error in errors["detail"])
        assert any("asset_state" in str(error) for error in errors["detail"])
        
        # Clean up
        app.dependency_overrides = {}
    
    def test_create_asset_special_characters(self, client, mocker):
        """Test creating an asset with special characters in the name."""
        # Override authentication dependency
        app.dependency_overrides[Depends(override_get_current_user)] = override_get_current_user

        asset_data = get_mock_asset_create_dict()
        asset_data["asset_name"] = "Test@Asset"  # Special character
        
        response = client.post("/v1/assets/", json=asset_data, headers={"Authorization": "Bearer fake-admin-token"})
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        errors = response.json()
        assert "detail" in errors
        assert any("asset_name" in str(error) for error in errors["detail"])
        
        # Clean up
        app.dependency_overrides = {}
    
    def test_create_asset_missing_required_fields(self, client, mocker):
        """Test creating an asset with missing required fields."""
        # Override authentication dependency
        app.dependency_overrides[Depends(override_get_current_user)] = override_get_current_user

        incomplete_data = {
            "asset_name": "Test Asset"
            # Missing other required fields
        }
        
        response = client.post("/v1/assets/", json=incomplete_data, headers={"Authorization": "Bearer fake-admin-token"})
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        errors = response.json()
        assert "detail" in errors
        assert any("category_id" in str(error) for error in errors["detail"])
        assert any("specification" in str(error) for error in errors["detail"])
        assert any("installed_date" in str(error) for error in errors["detail"])
        assert any("asset_state" in str(error) for error in errors["detail"])
        
        # Clean up
        app.dependency_overrides = {}
    
    def test_create_asset_future_date(self, client, mocker):
        """Test creating an asset with a future installed date."""
        # Override authentication dependency
        app.dependency_overrides[Depends(override_get_current_user)] = override_get_current_user

        future_date = date.today().replace(year=date.today().year + 1)
        asset_data = get_mock_asset_create_dict()
        asset_data["installed_date"] = future_date.isoformat()
        
        response = client.post("/v1/assets/", json=asset_data, headers={"Authorization": "Bearer fake-admin-token"})
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        errors = response.json()
        assert "detail" in errors
        assert any("installed_date" in str(error) for error in errors["detail"])
        
        # Clean up
        app.dependency_overrides = {}
    
    def test_create_asset_category_not_found(self, client, mocker):
        """Test creating an asset with a non-existent category."""
        # Override authentication dependency
        app.dependency_overrides[Depends(override_get_current_user)] = override_get_current_user

        # Mock the category service to return None
        mock_category_service = mocker.Mock()
        mock_category_service.get_category_by_id.return_value = None
        mocker.patch("services.asset.CategoryService", return_value=mock_category_service)
        
        asset_data = get_mock_asset_create_dict()
        asset_data["category_id"] = 999  # Non-existent category
        
        response = client.post("/v1/assets/", json=asset_data, headers={"Authorization": "Bearer fake-admin-token"})
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
        error_data = response.json()
        assert "detail" in error_data
        assert "Category not found" in error_data["detail"]
        
        # Clean up
        app.dependency_overrides = {}
    
    def test_create_asset_duplicate_name(self, client, mocker):
        """Test creating an asset with a duplicate name."""
        # Override authentication dependency
        app.dependency_overrides[Depends(override_get_current_user)] = override_get_current_user

        # Mock the category service to return a category with id_counter
        mock_category = mocker.Mock()
        mock_category.id = 1
        mock_category.prefix = "TC"
        mock_category.id_counter = 0
        mock_category_service = mocker.Mock()
        mock_category_service.get_category_by_id.return_value = mock_category
        mocker.patch("services.asset.CategoryService", return_value=mock_category_service)
        
        # Mock the asset service to raise BusinessException
        mocker.patch(
            "services.asset.AssetService.create_asset",
            side_effect=BusinessException("Asset name already exists")
        )
        
        asset_data = get_mock_asset_create_dict()
        
        response = client.post("/v1/assets/", json=asset_data, headers={"Authorization": "Bearer fake-admin-token"})
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        error_data = response.json()
        assert "detail" in error_data
        assert "Asset name already exists" in error_data["detail"]
        
        # Clean up
        app.dependency_overrides = {}
    
    def test_create_asset_database_error(self, client, mocker):
        """Test handling database errors during asset creation."""
        # Override authentication dependency
        app.dependency_overrides[Depends(override_get_current_user)] = override_get_current_user

        # Mock the category service to return a category with id_counter
        mock_category = mocker.Mock()
        mock_category.id = 1
        mock_category.prefix = "TC"
        mock_category.id_counter = 0
        mock_category_service = mocker.Mock()
        mock_category_service.get_category_by_id.return_value = mock_category
        mocker.patch("services.asset.CategoryService", return_value=mock_category_service)
        
        # Mock the asset service to raise Exception
        mocker.patch(
            "services.asset.AssetService.create_asset",
            side_effect=Exception("Database error")
        )
        
        asset_data = get_mock_asset_create_dict()
        
        response = client.post("/v1/assets/", json=asset_data, headers={"Authorization": "Bearer fake-admin-token"})
        
        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        error_data = response.json()
        assert "detail" in error_data
        assert "Database error" in error_data["detail"]
        
        # Clean up
        app.dependency_overrides = {}
    
    def test_create_asset_unauthorized(self):
        """Test creating an asset without authentication."""
        from fastapi.testclient import TestClient
        from main import app
        
        asset_data = get_mock_asset_create_dict()
        
        # Create a new client without authentication
        unauthorized_client = TestClient(app)
        # Remove any default headers that might be set
        unauthorized_client.headers = {}
        
        response = unauthorized_client.post("/v1/assets/", json=asset_data)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        error_data = response.json()
        assert error_data["error"] == "no_tokens"
        assert error_data["message"] == "Missing authentication token"