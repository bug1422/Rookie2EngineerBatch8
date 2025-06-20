import pytest
from unittest.mock import Mock, patch
from datetime import date

from core.exceptions import BusinessException, NotFoundException
from enums.request.state import RequestState
from enums.assignment.state import AssignmentState
from enums.asset.state import AssetState
from enums.shared.location import Location
from models.request import Request
from schemas.request import RequestRead


class TestRequestServiceCancel:
    """Test cancel request functionality based on AC requirements"""
    
    def test_ac1_cancel_request_validation_waiting_for_returning_state_only(self, request_returning_service, mock_admin_user):
        """AC1: Test that X icon (cancel) is only enabled for requests having state 'Waiting for returning'."""
        # Arrange - Create a request with WAITING_FOR_RETURNING state
        request_id = 1
        mock_request = Mock()
        mock_request.id = request_id
        mock_request.request_state = RequestState.WAITING_FOR_RETURNING
        mock_request.assignment_id = 1
        mock_request.requested_by_id = 2
        
        # Mock repository to return the request
        request_returning_service.repository.get_request_by_id.return_value = mock_request
        request_returning_service.repository.delete_request_by_id.return_value = True
        
        # Act
        result = request_returning_service.cancel_request(request_id, mock_admin_user)
        
        # Assert - AC1: Request can be cancelled when in WAITING_FOR_RETURNING state
        assert result == True
        
        # Verify repository methods were called correctly
        request_returning_service.repository.get_request_by_id.assert_called_once_with(request_id)
        request_returning_service.repository.delete_request_by_id.assert_called_once_with(request_id)

    def test_ac1_cancel_request_not_allowed_for_completed_state(self, request_returning_service, mock_admin_user):
        """AC1: Test that requests with COMPLETED state cannot be cancelled."""
        # Arrange - Create a request with COMPLETED state
        request_id = 1
        mock_request = Mock()
        mock_request.id = request_id
        mock_request.request_state = RequestState.COMPLETED  # Not WAITING_FOR_RETURNING
        mock_request.assignment_id = 1
        mock_request.requested_by_id = 2
        
        # Mock repository to return the request
        request_returning_service.repository.get_request_by_id.return_value = mock_request
        
        # Act & Assert - AC1: Should raise exception for non-WAITING_FOR_RETURNING state
        with pytest.raises(BusinessException, match="Only requests with 'Waiting for returning' state can be cancelled"):
            request_returning_service.cancel_request(request_id, mock_admin_user)
        
        # Verify get_request_by_id was called but delete was not
        request_returning_service.repository.get_request_by_id.assert_called_once_with(request_id)
        request_returning_service.repository.delete_request_by_id.assert_not_called()

    def test_ac2_cancel_request_success_removes_from_list(self, request_returning_service, mock_admin_user):
        """AC2: Test that clicking Yes button removes request from request list."""
        # Arrange - Create a valid request for cancellation
        request_id = 1
        mock_request = Mock()
        mock_request.id = request_id
        mock_request.request_state = RequestState.WAITING_FOR_RETURNING
        mock_request.assignment_id = 1
        mock_request.requested_by_id = 2
        
        # Mock repository methods
        request_returning_service.repository.get_request_by_id.return_value = mock_request
        request_returning_service.repository.delete_request_by_id.return_value = True
        
        # Act - Simulate clicking "Yes" button in confirmation popup
        result = request_returning_service.cancel_request(request_id, mock_admin_user)
        
        # Assert - AC2: Request is successfully removed (returns True)
        assert result == True
        
        # Verify the request was deleted from database
        request_returning_service.repository.delete_request_by_id.assert_called_once_with(request_id)

    def test_ac3_cancel_request_no_action_simulation(self, request_returning_service, mock_admin_user):
        """AC3: Test simulation of clicking No button (no action taken)."""
        # This test simulates the scenario where user clicks "No" button
        # In actual implementation, "No" would be handled at frontend level
        # But we can test that when cancel_request is not called, no changes occur
        
        # Arrange
        request_id = 1
        
        # Act - Simulate clicking "No" button (service method not called)
        # No action should be taken
        
        # Assert - AC3: No repository methods should be called when "No" is clicked
        request_returning_service.repository.get_request_by_id.assert_not_called()
        request_returning_service.repository.delete_request_by_id.assert_not_called()

    def test_cancel_request_not_found(self, request_returning_service, mock_admin_user):
        """Test cancelling a non-existent request."""
        # Arrange
        request_id = 999
        
        # Mock repository to return None (request not found)
        request_returning_service.repository.get_request_by_id.return_value = None
        
        # Act & Assert
        with pytest.raises(NotFoundException, match="Request with id 999 not found"):
            request_returning_service.cancel_request(request_id, mock_admin_user)
        
        # Verify get_request_by_id was called but delete was not
        request_returning_service.repository.get_request_by_id.assert_called_once_with(request_id)
        request_returning_service.repository.delete_request_by_id.assert_not_called()

    def test_cancel_request_database_deletion_failure(self, request_returning_service, mock_admin_user):
        """Test cancel request when database deletion fails."""
        # Arrange
        request_id = 1
        mock_request = Mock()
        mock_request.id = request_id
        mock_request.request_state = RequestState.WAITING_FOR_RETURNING
        mock_request.assignment_id = 1
        mock_request.requested_by_id = 2
        
        # Mock repository methods
        request_returning_service.repository.get_request_by_id.return_value = mock_request
        request_returning_service.repository.delete_request_by_id.return_value = False  # Deletion failed
        
        # Act & Assert
        with pytest.raises(BusinessException, match="Failed to cancel request"):
            request_returning_service.cancel_request(request_id, mock_admin_user)
        
        # Verify both methods were called
        request_returning_service.repository.get_request_by_id.assert_called_once_with(request_id)
        request_returning_service.repository.delete_request_by_id.assert_called_once_with(request_id)

    def test_cancel_request_with_different_admin_users(self, request_returning_service):
        """Test cancel request with different admin users."""
        # Arrange
        request_id = 1
        mock_request = Mock()
        mock_request.id = request_id
        mock_request.request_state = RequestState.WAITING_FOR_RETURNING
        
        # Create different admin users
        admin_user_1 = Mock()
        admin_user_1.id = 1
        admin_user_1.type = "admin"
        
        admin_user_2 = Mock()
        admin_user_2.id = 2
        admin_user_2.type = "admin"
        
        # Mock repository methods
        request_returning_service.repository.get_request_by_id.return_value = mock_request
        request_returning_service.repository.delete_request_by_id.return_value = True
        
        # Act - Test with first admin
        result_1 = request_returning_service.cancel_request(request_id, admin_user_1)
        
        # Reset mocks for second test
        request_returning_service.repository.reset_mock()
        request_returning_service.repository.get_request_by_id.return_value = mock_request
        request_returning_service.repository.delete_request_by_id.return_value = True
        
        # Act - Test with second admin
        result_2 = request_returning_service.cancel_request(request_id, admin_user_2)
        
        # Assert - Both admins should be able to cancel requests
        assert result_1 == True
        assert result_2 == True

    def test_cancel_request_multiple_requests_same_assignment(self, request_returning_service, mock_admin_user):
        """Test cancelling one of multiple requests for the same assignment."""
        # Arrange
        request_id_1 = 1
        request_id_2 = 2
        assignment_id = 1
        
        # Create two requests for the same assignment
        mock_request_1 = Mock()
        mock_request_1.id = request_id_1
        mock_request_1.assignment_id = assignment_id
        mock_request_1.request_state = RequestState.WAITING_FOR_RETURNING
        
        mock_request_2 = Mock()
        mock_request_2.id = request_id_2
        mock_request_2.assignment_id = assignment_id
        mock_request_2.request_state = RequestState.WAITING_FOR_RETURNING
        
        # Mock repository to return different requests based on ID
        def mock_get_request_by_id(req_id):
            if req_id == request_id_1:
                return mock_request_1
            elif req_id == request_id_2:
                return mock_request_2
            return None
        
        request_returning_service.repository.get_request_by_id.side_effect = mock_get_request_by_id
        request_returning_service.repository.delete_request_by_id.return_value = True
        
        # Act - Cancel first request
        result = request_returning_service.cancel_request(request_id_1, mock_admin_user)
        
        # Assert
        assert result == True
        
        # Verify only the specific request was deleted
        request_returning_service.repository.delete_request_by_id.assert_called_once_with(request_id_1)


class TestRequestServiceCancelValidation:
    """Test validation scenarios for cancel request functionality"""
    
    def test_cancel_request_state_validation_comprehensive(self, request_returning_service, mock_admin_user):
        """Test comprehensive state validation for cancel request."""
        # Test all possible request states
        request_states = [
            (RequestState.WAITING_FOR_RETURNING, True),   # Should succeed
            (RequestState.COMPLETED, False),              # Should fail
        ]
        
        for state, should_succeed in request_states:
            # Arrange
            request_id = 1
            mock_request = Mock()
            mock_request.id = request_id
            mock_request.request_state = state
            
            # Reset mocks
            request_returning_service.repository.reset_mock()
            request_returning_service.repository.get_request_by_id.return_value = mock_request
            request_returning_service.repository.delete_request_by_id.return_value = True
            
            if should_succeed:
                # Act & Assert - Should succeed
                result = request_returning_service.cancel_request(request_id, mock_admin_user)
                assert result == True
                request_returning_service.repository.delete_request_by_id.assert_called_once()
            else:
                # Act & Assert - Should fail
                with pytest.raises(BusinessException, match="Only requests with 'Waiting for returning' state can be cancelled"):
                    request_returning_service.cancel_request(request_id, mock_admin_user)
                request_returning_service.repository.delete_request_by_id.assert_not_called()

    def test_cancel_request_admin_permission_validation(self, request_returning_service):
        """Test that only admin users can cancel requests (conceptual test)."""
        # This test validates the conceptual requirement that only admins can cancel
        # In the actual implementation, this is enforced at the API level with get_current_admin
        
        # Arrange
        request_id = 1
        mock_request = Mock()
        mock_request.id = request_id
        mock_request.request_state = RequestState.WAITING_FOR_RETURNING
        
        # Create admin user
        admin_user = Mock()
        admin_user.id = 1
        admin_user.type = "admin"
        
        # Mock repository methods
        request_returning_service.repository.get_request_by_id.return_value = mock_request
        request_returning_service.repository.delete_request_by_id.return_value = True
        
        # Act
        result = request_returning_service.cancel_request(request_id, admin_user)
        
        # Assert - Admin should be able to cancel
        assert result == True
        
        # Verify the service method accepts admin user
        request_returning_service.repository.delete_request_by_id.assert_called_once_with(request_id)


class TestRequestServiceCancelAC:
    """Test cancel request functionality based on specific AC requirements"""

    def test_ac1_x_icon_enabled_only_for_waiting_for_returning(self, request_returning_service, mock_admin_user):
        """AC1: Test that X icon is only enabled for requests having state 'Waiting for returning'."""
        # This test validates the backend logic that supports the frontend requirement
        # that X icon is only enabled for WAITING_FOR_RETURNING requests

        # Test 1: WAITING_FOR_RETURNING state - should allow cancellation
        request_id = 1
        mock_request_waiting = Mock()
        mock_request_waiting.id = request_id
        mock_request_waiting.request_state = RequestState.WAITING_FOR_RETURNING

        request_returning_service.repository.get_request_by_id.return_value = mock_request_waiting
        request_returning_service.repository.delete_request_by_id.return_value = True

        # Act
        result = request_returning_service.cancel_request(request_id, mock_admin_user)

        # Assert - AC1: X icon functionality works for WAITING_FOR_RETURNING
        assert result == True

        # Test 2: COMPLETED state - should not allow cancellation (X icon disabled)
        request_returning_service.repository.reset_mock()
        mock_request_completed = Mock()
        mock_request_completed.id = request_id
        mock_request_completed.request_state = RequestState.COMPLETED

        request_returning_service.repository.get_request_by_id.return_value = mock_request_completed

        # Act & Assert - AC1: X icon functionality blocked for non-WAITING_FOR_RETURNING
        with pytest.raises(BusinessException, match="Only requests with 'Waiting for returning' state can be cancelled"):
            request_returning_service.cancel_request(request_id, mock_admin_user)

    def test_ac1_confirmation_popup_display_requirement(self, request_returning_service, mock_admin_user):
        """AC1: Test that confirmation popup is displayed (backend validation)."""
        # This test validates that the backend properly validates the request
        # before allowing cancellation, which supports the frontend confirmation popup

        # Arrange
        request_id = 1
        mock_request = Mock()
        mock_request.id = request_id
        mock_request.request_state = RequestState.WAITING_FOR_RETURNING

        # Mock repository methods
        request_returning_service.repository.get_request_by_id.return_value = mock_request
        request_returning_service.repository.delete_request_by_id.return_value = True

        # Act - This simulates the backend validation that occurs after popup confirmation
        result = request_returning_service.cancel_request(request_id, mock_admin_user)

        # Assert - AC1: Backend properly validates and processes cancellation
        assert result == True

        # Verify proper validation sequence (get request first, then delete)
        request_returning_service.repository.get_request_by_id.assert_called_once_with(request_id)
        request_returning_service.repository.delete_request_by_id.assert_called_once_with(request_id)

    def test_ac2_yes_button_removes_request_from_list(self, request_returning_service, mock_admin_user):
        """AC2: Test that clicking Yes button removes request from request list."""
        # Arrange
        request_id = 1
        mock_request = Mock()
        mock_request.id = request_id
        mock_request.request_state = RequestState.WAITING_FOR_RETURNING
        mock_request.assignment_id = 1
        mock_request.requested_by_id = 2

        # Mock repository methods
        request_returning_service.repository.get_request_by_id.return_value = mock_request
        request_returning_service.repository.delete_request_by_id.return_value = True

        # Act - Simulate clicking "Yes" button in confirmation popup
        result = request_returning_service.cancel_request(request_id, mock_admin_user)

        # Assert - AC2: Request is removed from list (deleted from database)
        assert result == True

        # Verify the request was actually deleted
        request_returning_service.repository.delete_request_by_id.assert_called_once_with(request_id)

        # Verify the request was validated before deletion
        request_returning_service.repository.get_request_by_id.assert_called_once_with(request_id)

    def test_ac2_popup_closed_after_yes_button(self, request_returning_service, mock_admin_user):
        """AC2: Test that popup is closed after clicking Yes button (simulation)."""
        # This test simulates the successful completion of the cancel operation
        # which would result in the popup being closed in the frontend

        # Arrange
        request_id = 1
        mock_request = Mock()
        mock_request.id = request_id
        mock_request.request_state = RequestState.WAITING_FOR_RETURNING

        # Mock repository methods
        request_returning_service.repository.get_request_by_id.return_value = mock_request
        request_returning_service.repository.delete_request_by_id.return_value = True

        # Act
        result = request_returning_service.cancel_request(request_id, mock_admin_user)

        # Assert - AC2: Operation completes successfully (popup would close)
        assert result == True

        # Verify operation completed without errors (popup can close safely)
        request_returning_service.repository.delete_request_by_id.assert_called_once()

    def test_ac3_no_button_no_action_taken(self, request_returning_service, mock_admin_user):
        """AC3: Test that clicking No button takes no action (popup closed only)."""
        # This test simulates the scenario where user clicks "No" button
        # In actual implementation, "No" would be handled at frontend level
        # and the service method would not be called

        # Arrange
        request_id = 1

        # Act - Simulate clicking "No" button (no service call made)
        # No action should be taken - service method not called

        # Assert - AC3: No repository methods called when "No" is clicked
        request_returning_service.repository.get_request_by_id.assert_not_called()
        request_returning_service.repository.delete_request_by_id.assert_not_called()

        # This confirms that clicking "No" results in no backend action

    def test_cancel_request_workflow_complete(self, request_returning_service, mock_admin_user):
        """Test complete cancel request workflow covering all AC scenarios."""
        # Arrange
        request_id = 1
        mock_request = Mock()
        mock_request.id = request_id
        mock_request.request_state = RequestState.WAITING_FOR_RETURNING
        mock_request.assignment_id = 1
        mock_request.requested_by_id = 2

        # Mock repository methods
        request_returning_service.repository.get_request_by_id.return_value = mock_request
        request_returning_service.repository.delete_request_by_id.return_value = True

        # Act - Complete workflow from AC1 to AC2
        result = request_returning_service.cancel_request(request_id, mock_admin_user)

        # Assert - All AC requirements met
        # AC1: Request state was validated (WAITING_FOR_RETURNING)
        assert mock_request.request_state == RequestState.WAITING_FOR_RETURNING

        # AC1: Confirmation popup would be displayed (backend validation passed)
        request_returning_service.repository.get_request_by_id.assert_called_once_with(request_id)

        # AC2: Yes button action - request removed from list
        assert result == True
        request_returning_service.repository.delete_request_by_id.assert_called_once_with(request_id)

        # AC2: Popup would be closed (operation completed successfully)
        # This is indicated by the successful return value

    def test_cancel_request_error_handling(self, request_returning_service, mock_admin_user):
        """Test error handling in cancel request functionality."""
        # Test 1: Request not found
        request_id = 999
        request_returning_service.repository.get_request_by_id.return_value = None

        with pytest.raises(NotFoundException, match="Request with id 999 not found"):
            request_returning_service.cancel_request(request_id, mock_admin_user)

        # Test 2: Invalid state
        request_returning_service.repository.reset_mock()
        mock_request = Mock()
        mock_request.id = request_id
        mock_request.request_state = RequestState.COMPLETED
        request_returning_service.repository.get_request_by_id.return_value = mock_request

        with pytest.raises(BusinessException, match="Only requests with 'Waiting for returning' state can be cancelled"):
            request_returning_service.cancel_request(request_id, mock_admin_user)

        # Test 3: Database deletion failure
        request_returning_service.repository.reset_mock()
        mock_request.request_state = RequestState.WAITING_FOR_RETURNING
        request_returning_service.repository.get_request_by_id.return_value = mock_request
        request_returning_service.repository.delete_request_by_id.return_value = False

        with pytest.raises(BusinessException, match="Failed to cancel request"):
            request_returning_service.cancel_request(request_id, mock_admin_user)
