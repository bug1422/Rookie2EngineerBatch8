from datetime import datetime, date, timezone
from fastapi import HTTPException
import pytest
from unittest.mock import Mock

from enums.asset.state import AssetState
from enums.shared.location import Location
from models.asset import Asset
from services.asset import AssetService
from tests.test_data.mock_asset import get_mock_asset_create
from tests.test_data.mock_user import get_mock_user_read
from tests.services.assignment.conftest import mock_category as base_mock_category

@pytest.fixture
def mock_category():
    mock = Mock()
    mock.id = 1
    mock.category_name = "Test Category"
    mock.prefix = "TC"
    mock.id_counter = 0
    return mock

@pytest.fixture
def mock_current_user():
    return get_mock_user_read()

@pytest.fixture
def asset_service(mocker):
    mock_repo = Mock()
    mock_db = Mock()
    service = AssetService(mock_db)
    service.repository = mock_repo
    return service

class TestAssetServiceCreate:
    def test_create_asset_success(self, asset_service, mock_category, mock_current_user, mocker):
        mock_category_service = Mock()
        mock_category_service.get_category_by_id.return_value = mock_category
        mock_category_service.update_category.return_value = mock_category
        mocker.patch('services.asset.CategoryService', return_value=mock_category_service)

        mock_asset = Asset(
            id=1,
            asset_code="TC0001",
            asset_name="Test Asset",
            category_id=1,
            specification="Test Spec",
            installed_date=date(2024, 1, 1),
            asset_state=AssetState.AVAILABLE,
            asset_location=Location.HANOI,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc)
        )
        asset_service.repository.create_asset.return_value = mock_asset

        asset_data = get_mock_asset_create()
        result = asset_service.create_asset(asset_data, mock_current_user)
        assert result.id == 1
        assert result.asset_code == "TC0001"
        assert result.asset_name == "Test Asset"
        mock_category_service.update_category.assert_called_once()
        asset_service.repository.create_asset.assert_called_once()

    def test_create_asset_category_not_found(self, asset_service, mock_current_user, mocker):
        mock_category_service = Mock()
        mock_category_service.get_category_by_id.return_value = None
        mocker.patch('services.asset.CategoryService', return_value=mock_category_service)

        asset_data = get_mock_asset_create()
        asset_data.category_id = 999
        with pytest.raises(HTTPException) as exc_info:
            asset_service.create_asset(asset_data, mock_current_user)
        assert exc_info.value.status_code == 500
        assert "Category not found" in str(exc_info.value.detail)

    def test_create_asset_database_error(self, asset_service, mock_category, mock_current_user, mocker):
        mock_category_service = Mock()
        mock_category_service.get_category_by_id.return_value = mock_category
        mocker.patch('services.asset.CategoryService', return_value=mock_category_service)
        asset_service.repository.create_asset.side_effect = Exception("Database error")

        asset_data = get_mock_asset_create()
        with pytest.raises(HTTPException) as exc_info:
            asset_service.create_asset(asset_data, mock_current_user)
        assert exc_info.value.status_code == 500
        assert "Database error" in str(exc_info.value.detail)

    def test_create_asset_code_generation(self, asset_service, mock_category, mock_current_user, mocker):
        mock_category_service = Mock()
        mock_category_service.get_category_by_id.return_value = mock_category
        mock_category_service.update_category.return_value = mock_category
        mocker.patch('services.asset.CategoryService', return_value=mock_category_service)

        mock_asset = Asset(
            id=1,
            asset_code="TC0001",
            asset_name="Test Asset",
            category_id=1,
            specification="Test Spec",
            installed_date=date(2024, 1, 1),
            asset_state=AssetState.AVAILABLE,
            asset_location=Location.HANOI,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc)
        )
        asset_service.repository.create_asset.return_value = mock_asset

        asset_data = get_mock_asset_create()
        result = asset_service.create_asset(asset_data, mock_current_user)
        assert result.asset_code == "TC0001"
        mock_category_service.update_category.assert_called_once()

    def test_create_asset_allows_empty_and_special_fields(self, asset_service, mock_category, mock_current_user, mocker):
        mock_category_service = Mock()
        mock_category_service.get_category_by_id.return_value = mock_category
        mock_category_service.update_category.return_value = mock_category
        mocker.patch('services.asset.CategoryService', return_value=mock_category_service)
        mock_asset = Asset(
            id=2,
            asset_code="TC0002",
            asset_name="!@#",
            category_id=1,
            specification="",
            installed_date=date(2024, 1, 1),
            asset_state=AssetState.AVAILABLE,
            asset_location=Location.HANOI,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc)
        )
        asset_service.repository.create_asset.return_value = mock_asset
        asset_data = get_mock_asset_create()
        asset_data.asset_name = "!@#"
        asset_data.specification = ""
        result = asset_service.create_asset(asset_data, mock_current_user)
        assert result.asset_code == "TC0002"
        assert result.asset_name == "!@#"
        assert result.specification == ""

    def test_create_asset_with_none_id_counter(self, asset_service, mock_current_user, mocker):
        # Category with id_counter=None should raise an exception
        mock_category = Mock()
        mock_category.id = 1
        mock_category.category_name = "Test Category"
        mock_category.prefix = "TC"
        mock_category.id_counter = None
        mock_category_service = Mock()
        mock_category_service.get_category_by_id.return_value = mock_category
        mock_category_service.update_category.return_value = mock_category
        mocker.patch('services.asset.CategoryService', return_value=mock_category_service)
        asset_data = get_mock_asset_create()
        with pytest.raises(HTTPException) as exc_info:
            asset_service.create_asset(asset_data, mock_current_user)
        assert exc_info.value.status_code == 500
        assert "NoneType" in str(exc_info.value.detail) or "unsupported operand" in str(exc_info.value.detail)

    def test_create_asset_repository_returns_none(self, asset_service, mock_category, mock_current_user, mocker):
        # Repository returns None for created asset
        mock_category_service = Mock()
        mock_category_service.get_category_by_id.return_value = mock_category
        mock_category_service.update_category.return_value = mock_category
        mocker.patch('services.asset.CategoryService', return_value=mock_category_service)
        asset_service.repository.create_asset.return_value = None
        asset_data = get_mock_asset_create()
        # Should raise AttributeError when trying to access new_asset.id
        with pytest.raises(HTTPException) as exc_info:
            asset_service.create_asset(asset_data, mock_current_user)
        assert exc_info.value.status_code == 500
        assert "'NoneType' object has no attribute 'id'" in str(exc_info.value.detail)

    def test_create_asset_with_user_location_none(self, asset_service, mock_category, mocker):
        # User with location=None
        mock_category_service = Mock()
        mock_category_service.get_category_by_id.return_value = mock_category
        mock_category_service.update_category.return_value = mock_category
        mocker.patch('services.asset.CategoryService', return_value=mock_category_service)
        mock_user = get_mock_user_read()
        mock_user.location = None
        mock_asset = Asset(
            id=4,
            asset_code="TC0004",
            asset_name="No Location Asset",
            category_id=1,
            specification="No Location Spec",
            installed_date=date(2024, 3, 1),
            asset_state=AssetState.AVAILABLE,
            asset_location=None,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc)
        )
        asset_service.repository.create_asset.return_value = mock_asset
        asset_data = get_mock_asset_create()
        asset_data.asset_name = "No Location Asset"
        asset_data.specification = "No Location Spec"
        asset_data.installed_date = date(2024, 3, 1)
        result = asset_service.create_asset(asset_data, mock_user)
        assert result.asset_location is None
        assert result.asset_name == "No Location Asset"

   