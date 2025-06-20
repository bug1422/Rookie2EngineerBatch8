import pytest
from fastapi import status
from unittest.mock import Mock, patch

from core.exceptions import NotFoundException, PermissionDeniedException
from enums.assignment.state import AssignmentState


class TestAssignmentStateUpdate:
    def test_update_assignment_state_accept_success(self, client, mock_assignment_accepted, mocker):
        """Test successfully accepting an assignment via API."""
        # Arrange
        assignment_id = 1
        mocker.patch(
            "services.assignment.AssignmentService.update_assignment_state",
            return_value=mock_assignment_accepted
        )
        
        # Act
        response = client.patch(
            f"/v1/assignments/{assignment_id}",
            json={"assignment_state": "Accepted"}
        )
        
        # Assert
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["assignment_state"] == "Accepted"

    def test_update_assignment_state_decline_success(self, client, mock_assignment_declined, mocker):
        """Test successfully declining an assignment via API."""
        # Arrange
        assignment_id = 1
        mocker.patch(
            "services.assignment.AssignmentService.update_assignment_state",
            return_value=mock_assignment_declined
        )
        
        # Act
        response = client.patch(
            f"/v1/assignments/{assignment_id}",
            json={"assignment_state": "Declined"}
        )
        
        # Assert
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["assignment_state"] == "Declined"

    def test_update_assignment_state_not_found(self, client, mocker):
        """Test updating state of non-existent assignment."""
        # Arrange
        mocker.patch(
            "services.assignment.AssignmentService.update_assignment_state",
            side_effect=NotFoundException("Assignment not found")
        )
        
        # Act
        response = client.patch(
            "/v1/assignments/999",
            json={"assignment_state": "Accepted"}
        )
        
        # Assert
        assert response.status_code == status.HTTP_404_NOT_FOUND
        error_data = response.json()
        assert "Assignment not found" in error_data["detail"]

    def test_update_assignment_state_permission_denied(self, client, mocker):
        """Test updating assignment state without permission."""
        # Arrange
        assignment_id = 1
        mocker.patch(
            "services.assignment.AssignmentService.update_assignment_state",
            side_effect=PermissionDeniedException("You can only update your own assignments")
        )
        
        # Act
        response = client.patch(
            f"/v1/assignments/{assignment_id}",
            json={"assignment_state": "Accepted"}
        )
        
        # Assert
        assert response.status_code == status.HTTP_403_FORBIDDEN
        error_data = response.json()
        assert "You can only update your own assignments" in error_data["detail"]

    def test_update_assignment_state_invalid_state(self, client, mocker):
        """Test updating assignment with invalid state."""
        # Act
        response = client.patch(
            "/v1/assignments/1",
            json={"assignment_state": "InvalidState"}
        )
        
        # Assert
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_update_assignment_state_missing_data(self, client):
        """Test updating assignment state without required data."""
        # Act
        response = client.patch("/v1/assignments/1", json={})
        
        # Assert
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    @pytest.mark.parametrize("assignment_state,fixture_name", [
        ("Accepted", "mock_assignment_accepted"),
        ("Declined", "mock_assignment_declined"),
        ("Waiting for acceptance", "mock_assignment_waiting")
    ])
    def test_update_assignment_state_valid_states(self, assignment_state, fixture_name, client, request, mocker):
        """Test updating assignment with all valid states."""
        # Arrange
        assignment_id = 1
        mock_assignment = request.getfixturevalue(fixture_name)
        mock_assignment.assignment_state = assignment_state
        
        mocker.patch(
            "services.assignment.AssignmentService.update_assignment_state",
            return_value=mock_assignment
        )
        
        # Act
        response = client.patch(
            f"/v1/assignments/{assignment_id}",
            json={"assignment_state": assignment_state}
        )
        
        # Assert
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["assignment_state"] == assignment_state

    @pytest.mark.parametrize("invalid_id", ["invalid", "abc123", "-1", "0"])
    def test_update_assignment_state_invalid_id(self, invalid_id, client):
        """Test updating assignment state with invalid ID formats."""
        # Act
        response = client.patch(
            f"/v1/assignments/{invalid_id}",
            json={"assignment_state": "Accepted"}
        )
        
        # Assert
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
