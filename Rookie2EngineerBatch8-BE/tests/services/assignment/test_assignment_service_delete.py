import pytest
from unittest.mock import Mock, patch
from datetime import date

from core.exceptions import BusinessException, NotFoundException
from enums.assignment.state import AssignmentState
from enums.shared.location import Location
from services.assignment import AssignmentService
from schemas.user import UserRead


class TestAssignmentDelete:
    def test_delete_assignment_success(self, mocker, assignment_service, mock_assignment, mock_user):
        """Test deleting an assignment successfully."""
        # Arrange
        mock_assignment.assignment_state = AssignmentState.WAITING_FOR_ACCEPTANCE
        # Ensure asset location matches user location
        mock_assignment.asset.asset_location = mock_user.location
        mocker.patch("services.assignment.AssetService.read_asset",return_value=mock_assignment.asset)
        assignment_service.repository.get_assignment_by_id.return_value = mock_assignment
        
        # Act
        assignment_service.delete_assignment(mock_assignment.id, mock_user.location)
        
        # Assert
        assignment_service.repository.delete_assignment.assert_called_once_with(mock_assignment)
    
    def test_delete_assignment_not_found(self, assignment_service, mock_user):
        """Test deleting a non-existent assignment."""
        # Arrange
        assignment_service.repository.get_assignment_by_id.return_value = None
        
        # Act & Assert
        with pytest.raises(NotFoundException, match="Assignment not found"):
            assignment_service.delete_assignment(999, mock_user.location)
    
    def test_delete_assignment_different_location(self, assignment_service, mock_assignment, mock_user):
        """Test deleting an assignment from a different location."""
        # Arrange
        mock_assignment.asset.asset_location = Location.HCM
        assignment_service.repository.get_assignment_by_id.return_value = mock_assignment
        
        # Act & Assert
        with pytest.raises(BusinessException, match="You can only delete assignments that are in the same location as you"):
            assignment_service.delete_assignment(mock_assignment.id, Location.HANOI)
    
    def test_delete_assignment_accepted_state(self, assignment_service, mock_assignment, mock_user):
        """Test deleting an assignment that is in ACCEPTED state."""
        # Arrange
        mock_assignment.assignment_state = AssignmentState.ACCEPTED
        mock_assignment.asset.asset_location = mock_user.location
        assignment_service.repository.get_assignment_by_id.return_value = mock_assignment
        
        # Act & Assert
        with pytest.raises(BusinessException, match="You can only delete assignments that are 'Waiting for acceptance' or 'Declined'"):
            assignment_service.delete_assignment(mock_assignment.id, mock_user.location)
    
    def test_delete_assignment_declined_state(self, mocker, assignment_service, mock_assignment, mock_user):
        """Test deleting an assignment that is in DECLINED state."""
        # Arrange
        mock_assignment.assignment_state = AssignmentState.DECLINED
        mock_assignment.asset.asset_location = mock_user.location
        mocker.patch("services.assignment.AssetService.read_asset",return_value=mock_assignment.asset)
        assignment_service.repository.get_assignment_by_id.return_value = mock_assignment
        
        # Act
        assignment_service.delete_assignment(mock_assignment.id, mock_user.location)
        
        # Assert
        assignment_service.repository.delete_assignment.assert_called_once_with(mock_assignment)