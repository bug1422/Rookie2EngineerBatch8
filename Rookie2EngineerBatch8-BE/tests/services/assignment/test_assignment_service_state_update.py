import pytest
from unittest.mock import Mock, patch
from datetime import date

from core.exceptions import BusinessException, NotFoundException, PermissionDeniedException
from enums.assignment.state import AssignmentState
from enums.asset.state import AssetState
from enums.shared.location import Location
from schemas.assignment import AssignmentStateUpdate
from schemas.asset import AssetUpdate


class TestAssignmentStateUpdate:
    def test_update_assignment_state_accept_success(self, assignment_service, mock_assignment, mock_staff_user, mock_asset):
        """Test successfully accepting an assignment."""
        # Arrange
        mock_assignment.assignment_state = AssignmentState.WAITING_FOR_ACCEPTANCE
        mock_assignment.assigned_to_id = mock_staff_user.id
        assignment_service.repository.get_assignment_by_id.return_value = mock_assignment
        
        state_update = AssignmentStateUpdate(assignment_state=AssignmentState.ACCEPTED)
        
        updated_assignment = mock_assignment.model_copy()
        updated_assignment.assignment_state = AssignmentState.ACCEPTED
        assignment_service.repository.update_assignment_state.return_value = updated_assignment
        
        # Act
        result = assignment_service.update_assignment_state(
            mock_assignment.id, state_update, mock_staff_user.id, mock_staff_user.location 
        )
        
        # Assert
        assert result.assignment_state == AssignmentState.ACCEPTED
        assignment_service.repository.update_assignment_state.assert_called_once_with(
            mock_assignment.id, state_update
        )

    def test_update_assignment_state_decline_success(self, assignment_service, mock_assignment, mock_staff_user, mock_asset):
        """Test successfully declining an assignment and updating asset state."""
        # Arrange
        mock_assignment.assignment_state = AssignmentState.WAITING_FOR_ACCEPTANCE
        mock_assignment.assigned_to_id = mock_staff_user.id
        assignment_service.repository.get_assignment_by_id.return_value = mock_assignment
        
        state_update = AssignmentStateUpdate(assignment_state=AssignmentState.DECLINED)
        
        updated_assignment = mock_assignment.model_copy()
        updated_assignment.assignment_state = AssignmentState.DECLINED
        assignment_service.repository.update_assignment_state.return_value = updated_assignment
        
        # Mock AssetService
        with patch('services.assignment.AssetService') as mock_asset_service:
            mock_asset_service_instance = Mock()
            mock_asset_service.return_value = mock_asset_service_instance
            mock_asset_service_instance.read_asset.return_value = mock_asset
            
            # Act
            result = assignment_service.update_assignment_state(
                mock_assignment.id, state_update, mock_staff_user.id, mock_staff_user.location
            )
            
            # Assert
            assert result.assignment_state == AssignmentState.DECLINED
            mock_asset_service_instance.read_asset.assert_called_once_with(mock_assignment.asset_id, mock_staff_user.location)
            mock_asset_service_instance.repository.update_asset.assert_called_once()
            
            # Verify asset state update call
            call_args = mock_asset_service_instance.repository.update_asset.call_args
            assert call_args[0][0] == mock_asset.id  # asset_id
            assert isinstance(call_args[0][1], AssetUpdate)
            assert call_args[0][1].asset_state == AssetState.AVAILABLE

    def test_update_assignment_state_assignment_not_found(self, assignment_service, mock_staff_user):
        """Test updating state of non-existent assignment."""
        # Arrange
        assignment_service.repository.get_assignment_by_id.return_value = None
        state_update = AssignmentStateUpdate(assignment_state=AssignmentState.ACCEPTED)
        
        # Act & Assert
        with pytest.raises(NotFoundException, match="Assignment not found"):
            assignment_service.update_assignment_state(999, state_update, mock_staff_user.id, mock_staff_user.location)

    def test_update_assignment_state_permission_denied_wrong_user(self, assignment_service, mock_assignment, mock_staff_user, mock_admin_user):
        """Test updating assignment state by wrong user."""
        # Arrange
        mock_assignment.assigned_to_id = mock_admin_user.id  # Different user
        assignment_service.repository.get_assignment_by_id.return_value = mock_assignment
        
        state_update = AssignmentStateUpdate(assignment_state=AssignmentState.ACCEPTED)
        
        # Act & Assert
        with pytest.raises(PermissionDeniedException, match="You can only update your own assignments"):
            assignment_service.update_assignment_state(
                mock_assignment.id, state_update, mock_staff_user.id, mock_staff_user.location
            )

    def test_update_assignment_state_already_accepted(self, assignment_service, mock_assignment, mock_staff_user):
        """Test updating assignment that is already accepted."""
        # Arrange
        mock_assignment.assignment_state = AssignmentState.ACCEPTED
        mock_assignment.assigned_to_id = mock_staff_user.id
        assignment_service.repository.get_assignment_by_id.return_value = mock_assignment
        
        state_update = AssignmentStateUpdate(assignment_state=AssignmentState.DECLINED)
        
        # Act & Assert
        with pytest.raises(PermissionDeniedException, match="You can only update assignments that are waiting for acceptance"):
            assignment_service.update_assignment_state(
                mock_assignment.id, state_update, mock_staff_user.id, mock_staff_user.location
            )

    def test_update_assignment_state_already_declined(self, assignment_service, mock_assignment, mock_staff_user):
        """Test updating assignment that is already declined."""
        # Arrange
        mock_assignment.assignment_state = AssignmentState.DECLINED
        mock_assignment.assigned_to_id = mock_staff_user.id
        assignment_service.repository.get_assignment_by_id.return_value = mock_assignment
        
        state_update = AssignmentStateUpdate(assignment_state=AssignmentState.ACCEPTED)
        
        # Act & Assert
        with pytest.raises(PermissionDeniedException, match="You can only update assignments that are waiting for acceptance"):
            assignment_service.update_assignment_state(
                mock_assignment.id, state_update, mock_staff_user.id, mock_staff_user.location
            )

    @pytest.mark.parametrize("initial_state,new_state,should_succeed", [
        (AssignmentState.WAITING_FOR_ACCEPTANCE, AssignmentState.ACCEPTED, True),
        (AssignmentState.WAITING_FOR_ACCEPTANCE, AssignmentState.DECLINED, True),
        (AssignmentState.ACCEPTED, AssignmentState.DECLINED, False),
        (AssignmentState.DECLINED, AssignmentState.ACCEPTED, False),
    ])
    def test_update_assignment_state_transitions(self, initial_state, new_state, should_succeed, assignment_service, mock_assignment, mock_staff_user):
        """Test various assignment state transitions."""
        # Arrange
        mock_assignment.assignment_state = initial_state
        mock_assignment.assigned_to_id = mock_staff_user.id
        assignment_service.repository.get_assignment_by_id.return_value = mock_assignment
        
        state_update = AssignmentStateUpdate(assignment_state=new_state)
        
        if should_succeed:
            updated_assignment = mock_assignment.model_copy()
            updated_assignment.assignment_state = new_state
            assignment_service.repository.update_assignment_state.return_value = updated_assignment
            
            # Mock AssetService for decline case
            if new_state == AssignmentState.DECLINED:
                with patch('services.assignment.AssetService') as mock_asset_service:
                    mock_asset_service_instance = Mock()
                    mock_asset_service.return_value = mock_asset_service_instance
                    mock_asset_service_instance.read_asset.return_value = Mock(id=1)
                    
                    # Act
                    result = assignment_service.update_assignment_state(
                        mock_assignment.id, state_update, mock_staff_user.id, mock_staff_user.location
                    )
                    
                    # Assert
                    assert result.assignment_state == new_state
            else:
                # Act
                result = assignment_service.update_assignment_state(
                    mock_assignment.id, state_update, mock_staff_user.id, mock_staff_user.location
                )
                
                # Assert
                assert result.assignment_state == new_state
        else:
            # Act & Assert
            with pytest.raises(PermissionDeniedException):
                assignment_service.update_assignment_state(
                    mock_assignment.id, state_update, mock_staff_user.id, mock_staff_user.location
                )
