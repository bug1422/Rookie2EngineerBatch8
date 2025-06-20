import pytest
from core.exceptions import NotFoundException, ValidationException
from enums.asset.state import AssetState
from enums.shared.location import Location
from enums.user.status import Status
from schemas.assignment import AssignmentUpdate


class TestAssignmentUpdate:        
    def test_edit_assignment_success(self, mock_admin_user, mock_assignment, assignment_service, mock_staff_user, mock_asset):
        # Arrange
        updated_assignment = mock_assignment.model_copy()
        expected_assignment = mock_assignment.model_copy()
        
        expected_assignment.assigned_to_id = 10
        expected_assignment.assignment_note = "Updated assignment note"
        
        assignment_update = AssignmentUpdate(
            assigned_to_id=10,
            asset_id=mock_assignment.asset_id,
            assignment_note="Updated assignment note"
        )
        
        updated_assignment.asset_id = mock_assignment.asset_id
        updated_assignment.assigned_to_id = 10
        updated_assignment.assignment_note = "Updated assignment note"
        
        # Mock the repository calls for both user and asset validation
        mock_returns = [mock_staff_user]
        assignment_service.repository.db.query().filter().first.side_effect = mock_returns
        
        assignment_service.repository.update_assignment.return_value = updated_assignment
        
        # Act
        result = assignment_service.edit_assignment(mock_assignment.id, assignment_update, mock_admin_user)
        
        # Assert
        assert result == expected_assignment
        
        # Verify both validation calls were made
        assert assignment_service.repository.db.query().filter().first.call_count == 1
        
    @pytest.mark.parametrize("assignment_id,expected_error", [
        (9999, "Assignment with ID 9999 not found."),
    ])
    def test_edit_assignment_not_found(self, mock_admin_user, mock_assignment, assignment_service, expected_error, assignment_id):
        # Arrange
        assignment_update = AssignmentUpdate(
            assigned_to_id=mock_assignment.assigned_to_id,
            asset_id=mock_assignment.asset_id,
            assignment_note="Updated assignment note"
        )
        
        # Mock the repository calls for user validation
        assignment_service.repository.get_assignment_by_id_no_join.return_value = None
        
        # Act & Assert
        with pytest.raises(NotFoundException, match=expected_error):
            assignment_service.edit_assignment(assignment_id, assignment_update, mock_admin_user)
        
        # Verify the user validation was called
        assert assignment_service.repository.get_assignment_by_id_no_join.call_count == 1
    
    @pytest.mark.parametrize("user_id,admin_location,expected_error", [
        (2, Location.HANOI, "User with ID 2 belongs to Ho Chi Minh location, but assignment is for Hanoi location"),
        (3, Location.HCM, None),
        (4, Location.DANANG, "User with ID 4 belongs to Ho Chi Minh location, but assignment is for Danang location")
    ])    
    def test_validate_assigned_user_location(self, assignment_service, mock_staff_user, admin_location, user_id, expected_error):  
        # Mock the repository call
        assignment_service.repository.db.query().filter().first.return_value = mock_staff_user
        
        # Assert
        if expected_error:
            with pytest.raises(
                ValidationException, 
                match=expected_error
                ):
                assignment_service.validate_assigned_user(user_id, admin_location)
        else:
            assignment_service.validate_assigned_user(user_id, admin_location)
                
        assert assignment_service.repository.db.query().filter().first.call_count == 1
    
    @pytest.mark.parametrize("user_id,admin_location,expected_error", [
        (2, Location.HCM, "User with id 2 not found"),
        (3, Location.HCM, "User with id 3 not found")
    ])
    def test_validate_assigned_user_not_found(self, assignment_service, admin_location, user_id, expected_error):      
        # Mock the repository call
        assignment_service.repository.db.query().filter().first.return_value = None
        
        # Assert
        with pytest.raises(
            NotFoundException, 
            match=expected_error
            ):
            assignment_service.validate_assigned_user(user_id, admin_location)
            
        # assert assignment_service.validate_assigned_user == 1
    
    @pytest.mark.parametrize("user_id,status,expected_error", [
        (2, Status.DISABLED, "User with ID 2 is not active \\(current status: disabled\\)"),
        (3, Status.ACTIVE, None)
    ])        
    def test_validate_assigned_user_state(self, assignment_service, mock_staff_user, mock_admin_user, status, expected_error, user_id):
        # Act
        mock_staff_user.status = status
        mock_staff_user.id = user_id
        
        # Mock the repository call
        assignment_service.repository.db.query().filter().first.return_value = mock_staff_user
        
        # Assert
        if expected_error:
            with pytest.raises(
                ValidationException, 
                match=expected_error
            ):
                assignment_service.validate_assigned_user(mock_staff_user.id, mock_admin_user.location)
        else:
            assignment_service.validate_assigned_user(mock_staff_user.id, mock_admin_user.location)
                
        assert assignment_service.repository.db.query().filter().first.call_count == 1
    
    def test_edit_assignment_database_error(self, mock_admin_user, mock_assignment, assignment_service, mock_staff_user):
        """Test that database errors during assignment update are properly handled"""
        # Arrange
        assignment_update = AssignmentUpdate(
            assigned_to_id=mock_staff_user.id,
            asset_id=mock_assignment.asset_id,
            assignment_note="Updated note"
        )
        
        # Mock the repository calls
        assignment_service.repository.get_assignment_by_id_no_join.return_value = mock_assignment
        assignment_service.repository.db.query().filter().first.return_value = mock_staff_user
        
        # Mock the update to raise an exception
        db_error = Exception("Database connection error")
        assignment_service.repository.update_assignment.side_effect = db_error
        
        # Act & Assert
        with pytest.raises(ValidationException, match=f"Failed to update assignment: {str(db_error)}"):
            assignment_service.edit_assignment(mock_assignment.id, assignment_update, mock_admin_user)
        
        # Verify the calls
        assignment_service.repository.get_assignment_by_id_no_join.assert_called_once_with(mock_assignment.id)
        assignment_service.repository.update_assignment.assert_called_once_with(
            mock_assignment.id, 
            assignment_update,
            mock_admin_user.id
        )