from datetime import date
import pytest

from core.exceptions import BusinessException, NotFoundException
from enums.asset.state import AssetState
from enums.assignment.state import AssignmentState
from enums.request.state import RequestState
from enums.shared.location import Location
from models.request import Request
from schemas.asset import AssetRead
from schemas.assignment import AssignmentReadDetail, AssignmentReadSimple
from schemas.request import RequestRead


class TestRequestReturningCreate:
    def test_create_request_returning_success(self, request_returning_service, mock_staff_user, mock_assignment, mock_request_create, mocker):
        # Arrange
        expected_request = RequestRead(
            id=1,
            assignment_id=mock_assignment.id,
            requested_by_id=mock_staff_user.id,
            request_state=RequestState.WAITING_FOR_RETURNING,
            accepted_by_id=None,
            return_date=None
        )
        
        # Mock assignment service response
        mock_read_assignment = mocker.patch.object(
            request_returning_service.assignment_service,
            'read_assignment',
            return_value=AssignmentReadDetail(
                assignment=AssignmentReadSimple(
                    id=mock_assignment.id,
                    assign_date=mock_assignment.assign_date,
                    assignment_state=AssignmentState.ACCEPTED,
                    assignment_note=mock_assignment.assignment_note
                ),
                asset=mock_assignment.asset,
                assigned_to_user=mock_staff_user,
                assigned_by_user=mock_staff_user
            )
        )

        # Mock repository responses
        mock_create = mocker.patch.object(
            request_returning_service.repository,
            'create_request_returning',
            return_value=expected_request
        )
        mock_check_exist = mocker.patch.object(
            request_returning_service,
            'check_request_exist_by_assignment_id',
            return_value=False
        )

        # Act
        result = request_returning_service.create_request_returning(mock_request_create, mock_staff_user)

        # Assert
        assert result == expected_request
        mock_create.assert_called_once()
        mock_read_assignment.assert_called_once()
        mock_check_exist.assert_called_once()

    @pytest.mark.parametrize("assignment_state,expected_error", [
        (AssignmentState.WAITING_FOR_ACCEPTANCE, "Assignment is not in accepted state to return"),
        (AssignmentState.DECLINED, "Assignment is not in accepted state to return"),
        (AssignmentState.RETURNED, "Assignment is not in accepted state to return")
    ])
    def test_create_request_invalid_assignment_state(self, request_returning_service, mock_staff_user, mock_assignment, mock_request_create, assignment_state, expected_error, mocker):
        # Arrange
        mock_read_assignment = mocker.patch.object(
            request_returning_service.assignment_service,
            'read_assignment',
            return_value=AssignmentReadDetail(
                assignment=AssignmentReadSimple(
                    id=mock_assignment.id,
                    assign_date=mock_assignment.assign_date,
                    assignment_state=assignment_state,
                    assignment_note=mock_assignment.assignment_note
                ),
                asset=mock_assignment.asset,
                assigned_to_user=mock_staff_user,
                assigned_by_user=mock_staff_user
            )
        )

        # Act & Assert
        with pytest.raises(BusinessException, match=expected_error):
            request_returning_service.create_request_returning(mock_request_create, mock_staff_user)
            
        mock_read_assignment.assert_called_once()

    def test_create_request_existing_request(self, request_returning_service, mock_staff_user, mock_request_create, mock_assignment, mocker):
        # Arrange
        mock_read_assignment = mocker.patch.object(
            request_returning_service.assignment_service,
            'read_assignment',
            return_value=AssignmentReadDetail(
                assignment=AssignmentReadSimple(
                    id=mock_assignment.id,
                    assign_date=mock_assignment.assign_date,
                    assignment_state=AssignmentState.ACCEPTED,
                    assignment_note=mock_assignment.assignment_note
                ),
                asset=mock_assignment.asset,
                assigned_to_user=mock_staff_user,
                assigned_by_user=mock_staff_user
            )
        )
        mock_check_exist = mocker.patch.object(
            request_returning_service,
            'check_request_exist_by_assignment_id',
            return_value=True
        )

        # Act & Assert
        with pytest.raises(BusinessException, match="Request already exists for this assignment with waiting for returning state."):
            request_returning_service.create_request_returning(mock_request_create, mock_staff_user)
        
        mock_read_assignment.assert_called_once()
        mock_check_exist.assert_called_once()

    def test_create_request_different_user(self, request_returning_service, mock_staff_user, mock_admin_user, mock_request_create, mocker):
        # Arrange 
        mock_request_create.assignment_id = 1
        mocker.patch.object(
            request_returning_service.assignment_service.repository,
            'get_assignment_by_id_no_join',
            return_value=None
        )

        # Act & Assert
        with pytest.raises(BusinessException, match=f"Assignment with id {mock_request_create.assignment_id} not found"):
            request_returning_service.create_request_returning_by_staff(mock_request_create, mock_admin_user)

    def test_create_request_non_assignee(self, request_returning_service, mock_staff_user, mock_admin_user, mock_assignment, mock_request_create, mocker):
        # Arrange
        mock_assignment.assigned_to_id = mock_staff_user.id
        mocker.patch.object(
            request_returning_service.assignment_service.repository,
            'get_assignment_by_id_no_join',
            return_value=mock_assignment
        )

        # Act & Assert
        with pytest.raises(BusinessException, match="You can only create return requests for your own assignments"):
            request_returning_service.create_request_returning_by_staff(mock_request_create, mock_admin_user)

    def test_create_request_unexpected_error(self, request_returning_service, mock_staff_user, mock_assignment, mock_request_create, mocker):
        # Arrange
        mock_read_assignment = mocker.patch.object(
            request_returning_service.assignment_service,
            'read_assignment',
            return_value=AssignmentReadDetail(
                assignment=AssignmentReadSimple(
                    id=mock_assignment.id,
                    assign_date=mock_assignment.assign_date,
                    assignment_state=AssignmentState.ACCEPTED,
                    assignment_note=mock_assignment.assignment_note
                ),
                asset=mock_assignment.asset,
                assigned_to_user=mock_staff_user,
                assigned_by_user=mock_staff_user
            )
        )
        
        mock_check_exist = mocker.patch.object(
            request_returning_service,
            'check_request_exist_by_assignment_id',
            return_value=False
        )

        # Mock repository to raise an exception
        error_message = "Database connection error"
        mock_create = mocker.patch.object(
            request_returning_service.repository,
            'create_request_returning',
            side_effect=Exception(error_message)
        )

        # Act & Assert
        with pytest.raises(BusinessException, match=error_message):
            request_returning_service.create_request_returning(mock_request_create, mock_staff_user)
        
        # Verify all mocks were called
        mock_read_assignment.assert_called_once()
        mock_check_exist.assert_called_once()
        mock_create.assert_called_once()

    @pytest.mark.parametrize("db_request,request_state,expected_result", [
        (None, None, False),  # No request exists
        (
            Request(id=1, assignment_id=1, request_state=RequestState.WAITING_FOR_RETURNING), 
            RequestState.WAITING_FOR_RETURNING, 
            True
        ),  # Request exists with WAITING_FOR_RETURNING state
        (
            Request(id=1, assignment_id=1, request_state=RequestState.COMPLETED), 
            RequestState.COMPLETED, 
            False
        ),  # Request exists but not in WAITING_FOR_RETURNING state
    ])
    def test_check_request_exist_by_assignment_id(
        self, 
        request_returning_service, 
        mocker,
        db_request,
        request_state,
        expected_result
    ):
        # Arrange
        mock_get_request = mocker.patch.object(
            request_returning_service.repository,
            'get_request_by_assignment_id',
            return_value=db_request
        )

        assignment_id = 1

        # Act
        result = request_returning_service.check_request_exist_by_assignment_id(assignment_id)

        # Assert
        assert result == expected_result
        mock_get_request.assert_called_once_with(assignment_id)

    def test_create_request_by_staff_success(self, request_returning_service, mock_staff_user, mock_assignment, mock_request_create, mocker):
        # Arrange
        mock_get_assignment = mocker.patch.object(
            request_returning_service.assignment_service.repository,
            'get_assignment_by_id_no_join',
            return_value=mock_assignment
        )
        
        # Mock the create_request_returning method
        expected_request = RequestRead(
            id=1,
            assignment_id=mock_assignment.id,
            requested_by_id=mock_staff_user.id,
            request_state=RequestState.WAITING_FOR_RETURNING,
            accepted_by_id=None,
            return_date=None
        )
        
        mock_create = mocker.patch.object(
            request_returning_service,
            'create_request_returning',
            return_value=expected_request
        )

        # Set up the mock assignment to match the staff user
        mock_assignment.assigned_to_id = mock_staff_user.id

        # Act
        result = request_returning_service.create_request_returning_by_staff(mock_request_create, mock_staff_user)

        # Assert
        assert result == expected_request
        mock_get_assignment.assert_called_once_with(mock_request_create.assignment_id)
        mock_create.assert_called_once_with(mock_request_create, mock_staff_user)

    @pytest.mark.parametrize("assignment_exists,assigned_to_id,expected_error", [
        (False, None, "Assignment with id 1 not found"),
        (True, 999, "You can only create return requests for your own assignments"),
    ])
    def test_create_request_by_staff_validation_errors(
        self, 
        request_returning_service, 
        mock_staff_user, 
        mock_assignment, 
        mock_request_create, 
        assignment_exists,
        assigned_to_id,
        expected_error,
        mocker
    ):
        # Arrange
        mock_request_create.assignment_id = 1
        
        if assignment_exists:
            mock_assignment.assigned_to_id = assigned_to_id
            mock_get_assignment = mocker.patch.object(
                request_returning_service.assignment_service.repository,
                'get_assignment_by_id_no_join',
                return_value=mock_assignment
            )
        else:
            mock_get_assignment = mocker.patch.object(
                request_returning_service.assignment_service.repository,
                'get_assignment_by_id_no_join',
                return_value=None
            )

        # Act & Assert
        with pytest.raises(BusinessException, match=expected_error):
            request_returning_service.create_request_returning_by_staff(mock_request_create, mock_staff_user)
        
        mock_get_assignment.assert_called_once_with(mock_request_create.assignment_id)
