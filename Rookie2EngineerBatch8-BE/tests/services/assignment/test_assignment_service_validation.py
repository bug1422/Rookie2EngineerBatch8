import pytest
from unittest.mock import Mock, patch

from core.exceptions import ValidationException
from enums.asset.state import AssetState
from enums.shared.location import Location
from enums.user.status import Status


class TestAssignmentValidation:
    def test_validate_assigned_user_success(self, assignment_service):
        """Test successful user validation."""
        # Arrange
        mock_user = Mock()
        mock_user.location = Location.HCM
        mock_user.status = Status.ACTIVE
        
        with patch('services.assignment.UserService') as mock_user_service:
            mock_user_service_instance = Mock()
            mock_user_service.return_value = mock_user_service_instance
            mock_user_service_instance.read_user.return_value = mock_user
            
            # Act & Assert - Should not raise exception
            assignment_service.validate_assigned_user(1, Location.HCM)

    def test_validate_assigned_user_inactive(self, assignment_service):
        """Test validation with inactive user."""
        # Arrange
        mock_user = Mock()
        mock_user.location = Location.HCM
        mock_user.status = Status.DISABLED
        
        with patch('services.assignment.UserService') as mock_user_service:
            mock_user_service_instance = Mock()
            mock_user_service.return_value = mock_user_service_instance
            mock_user_service_instance.read_user.return_value = mock_user
            
            # Act & Assert
            with pytest.raises(ValidationException, match="is not active"):
                assignment_service.validate_assigned_user(1, Location.HCM)

    def test_validate_asset_success(self, assignment_service):
        """Test successful asset validation."""
        # Arrange
        mock_asset = Mock()
        mock_asset.asset_location = Location.HCM
        mock_asset.asset_state = AssetState.AVAILABLE
        
        with patch('services.assignment.AssetService') as mock_asset_service:
            mock_asset_service_instance = Mock()
            mock_asset_service.return_value = mock_asset_service_instance
            mock_asset_service_instance.read_asset.return_value = mock_asset
            
            # Act & Assert - Should not raise exception
            assignment_service.validate_asset(1, Location.HCM)

    def test_validate_asset_not_available(self, assignment_service):
        """Test validation with unavailable asset."""
        # Arrange
        mock_asset = Mock()
        mock_asset.asset_location = Location.HCM
        mock_asset.asset_state = AssetState.ASSIGNED
        
        with patch('services.assignment.AssetService') as mock_asset_service:
            mock_asset_service_instance = Mock()
            mock_asset_service.return_value = mock_asset_service_instance
            mock_asset_service_instance.read_asset.return_value = mock_asset
            
            # Act & Assert
            with pytest.raises(ValidationException, match="is not available"):
                assignment_service.validate_asset(1, Location.HCM)

    def test_validate_assigned_user_none_id(self, assignment_service):
        """Test validation with None user ID."""
        # Act & Assert - Should not raise exception
        assignment_service.validate_assigned_user(None, Location.HCM)

    def test_validate_asset_none_id(self, assignment_service):
        """Test validation with None asset ID."""
        # Act & Assert - Should not raise exception
        assignment_service.validate_asset(None, Location.HCM)
