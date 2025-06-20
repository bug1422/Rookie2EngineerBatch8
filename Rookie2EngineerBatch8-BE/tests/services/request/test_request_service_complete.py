from enums.asset.state import AssetState
from enums.assignment.state import AssignmentState
from enums.request.state import RequestState
from fastapi import status
import pytest
from unittest.mock import Mock, call
from datetime import datetime
from core.exceptions import NotFoundException, BusinessException
from schemas.request import RequestUpdate, RequestRead

class TestRequestServiceComplete:

    def test_ac1_tick_icon_enabled_only_for_waiting_for_returning_state(self, request_service, mock_admin_user, mock_request_model, mock_completed_request):
        # Arrange
        request_id = 1
        request_update = RequestUpdate(request_state=RequestState.COMPLETED)
        
        mock_request_model.id = request_id
        mock_request_model.request_state = RequestState.WAITING_FOR_RETURNING
        mock_request_model.assignment = Mock()
        mock_request_model.assignment.id = 1
        mock_request_model.assignment.asset = Mock()
        mock_request_model.assignment.asset.id = 1
        mock_request_model.assignment.asset.asset_location = mock_admin_user.location
        
        request_service.repository.get_request_by_id.return_value = mock_request_model
        request_service.repository.complete_return_request.return_value = mock_completed_request
        
        # Act
        result = request_service.update_request(request_id, request_update, mock_admin_user)
        
        # Assert
        assert isinstance(result, RequestRead)
        request_service.repository.get_request_by_id.assert_called_once_with(request_id)
    
    def test_ac1_tick_icon_disabled_for_non_waiting_state(self, request_service, mock_admin_user, mock_request_model):
        # Arrange
        request_id = 1
        request_update = RequestUpdate(request_state=RequestState.COMPLETED)
        
        mock_request_model.id = request_id
        mock_request_model.request_state = RequestState.COMPLETED
        
        request_service.repository.get_request_by_id.return_value = mock_request_model
        
        # Act & Assert
        with pytest.raises(BusinessException, match="Only requests with 'Waiting for returning' state can be completed"):
            request_service.update_request(request_id, request_update, mock_admin_user)

    def test_ac1_confirmation_popup_display_requirement(self, request_service, mock_admin_user, mock_request_model, mock_completed_request):
        # Arrange
        request_id = 1
        request_update = RequestUpdate(request_state=RequestState.COMPLETED)
        
        mock_request_model.id = request_id
        mock_request_model.request_state = RequestState.WAITING_FOR_RETURNING
        mock_request_model.assignment = Mock()
        mock_request_model.assignment.id = 1
        mock_request_model.assignment.asset = Mock()
        mock_request_model.assignment.asset.id = 1
        mock_request_model.assignment.asset.asset_location = mock_admin_user.location
        
        request_service.repository.get_request_by_id.return_value = mock_request_model
        request_service.repository.complete_return_request.return_value = mock_completed_request
        
        # Act
        result = request_service.update_request(request_id, request_update, mock_admin_user)
        
        # Assert
        assert isinstance(result, RequestRead)
        request_service.repository.get_request_by_id.assert_called_once_with(request_id)

    def test_ac2_yes_button_closes_popup_and_completes_request(self, request_service, mock_admin_user, mock_request_model, mock_completed_request):
        # Arrange
        request_id = 1
        request_update = RequestUpdate(request_state=RequestState.COMPLETED)
        
        mock_request_model.id = request_id
        mock_request_model.request_state = RequestState.WAITING_FOR_RETURNING
        mock_request_model.assignment = Mock()
        mock_request_model.assignment.id = 10
        mock_request_model.assignment.asset = Mock()
        mock_request_model.assignment.asset.id = 5
        mock_request_model.assignment.asset.asset_location = mock_admin_user.location
        
        mock_completed_request.assignment_id = 10
        
        request_service.repository.get_request_by_id.return_value = mock_request_model
        request_service.repository.complete_return_request.return_value = mock_completed_request
        
        # Act
        result = request_service.update_request(request_id, request_update, mock_admin_user)
        
        # Assert
        assert isinstance(result, RequestRead)
        request_service.repository.complete_return_request.assert_called_once_with(request_id, mock_admin_user.id)
        
        request_service.assignment_repository.update_assignment_state.assert_called_once()
        call_args = request_service.assignment_repository.update_assignment_state.call_args
        assert call_args[0][0] == 10
        assert call_args[0][1].assignment_state == AssignmentState.RETURNED
        
        request_service.asset_repository.update_asset.assert_called_once()
        asset_call_args = request_service.asset_repository.update_asset.call_args
        assert asset_call_args[0][0] == 5
        assert asset_call_args[0][1].asset_state == AssetState.AVAILABLE

    def test_ac2_returned_date_updated_on_completion(self, request_service, mock_admin_user, mock_request_model, mock_completed_request):
        # Arrange
        request_id = 1
        request_update = RequestUpdate(request_state=RequestState.COMPLETED)
        
        mock_request_model.id = request_id
        mock_request_model.request_state = RequestState.WAITING_FOR_RETURNING
        mock_request_model.assignment = Mock()
        mock_request_model.assignment.asset = Mock()
        mock_request_model.assignment.asset.asset_location = mock_admin_user.location
        
        completion_date = datetime.now()
        mock_completed_request.return_date = completion_date
        
        request_service.repository.get_request_by_id.return_value = mock_request_model
        request_service.repository.complete_return_request.return_value = mock_completed_request
        
        # Act
        result = request_service.update_request(request_id, request_update, mock_admin_user)
        
        # Assert
        assert isinstance(result, RequestRead)
        request_service.repository.complete_return_request.assert_called_once_with(request_id, mock_admin_user.id)

    def test_ac3_no_button_no_action_taken(self, request_service, mock_admin_user):
        # Arrange
        request_id = 1

        # Act

        # Assert
        request_service.repository.get_request_by_id.assert_not_called()
        request_service.repository.complete_return_request.assert_not_called()
        request_service.assignment_repository.update_assignment_state.assert_not_called()
        request_service.asset_repository.update_asset.assert_not_called()

    def test_update_request_not_found(self, request_service, mock_admin_user):
        # Arrange
        request_id = 999
        request_update = RequestUpdate(request_state=RequestState.COMPLETED)
        
        request_service.repository.get_request_by_id.return_value = None
        
        # Act & Assert
        with pytest.raises(NotFoundException, match="Request with id 999 not found"):
            request_service.update_request(request_id, request_update, mock_admin_user)
    
    def test_update_request_invalid_state_change(self, request_service, mock_admin_user, mock_request_model):
        # Arrange
        request_id = 1
        request_update = RequestUpdate(request_state=RequestState.WAITING_FOR_RETURNING)
        
        mock_request_model.id = request_id
        mock_request_model.request_state = RequestState.WAITING_FOR_RETURNING
        
        request_service.repository.get_request_by_id.return_value = mock_request_model
        
        # Act & Assert
        with pytest.raises(BusinessException, match="Only completion of return requests is currently supported"):
            request_service.update_request(request_id, request_update, mock_admin_user)
    
    def test_update_request_location_mismatch(self, request_service, mock_admin_user, mock_request_model):
        # Arrange
        request_id = 1
        request_update = RequestUpdate(request_state=RequestState.COMPLETED)
        
        mock_request_model.id = request_id
        mock_request_model.request_state = RequestState.WAITING_FOR_RETURNING
        mock_request_model.assignment = Mock()
        mock_request_model.assignment.asset = Mock()
        mock_request_model.assignment.asset.asset_location = "Different Location"
        
        request_service.repository.get_request_by_id.return_value = mock_request_model
        
        # Act & Assert
        with pytest.raises(BusinessException, match="You can only complete requests for assets in your location"):
            request_service.update_request(request_id, request_update, mock_admin_user)

    def test_complete_request_workflow_comprehensive(self, request_service, mock_admin_user, mock_request_model, mock_completed_request):
        # Arrange
        request_id = 1
        request_update = RequestUpdate(request_state=RequestState.COMPLETED)
        
        mock_request_model.id = request_id
        mock_request_model.request_state = RequestState.WAITING_FOR_RETURNING
        mock_request_model.assignment = Mock()
        mock_request_model.assignment.id = 10
        mock_request_model.assignment.asset = Mock()
        mock_request_model.assignment.asset.id = 5
        mock_request_model.assignment.asset.asset_location = mock_admin_user.location
        
        mock_completed_request.assignment_id = 10
        
        request_service.repository.get_request_by_id.return_value = mock_request_model
        request_service.repository.complete_return_request.return_value = mock_completed_request
        
        # Act
        result = request_service.update_request(request_id, request_update, mock_admin_user)
        
        # Assert
        assert mock_request_model.request_state == RequestState.WAITING_FOR_RETURNING
        request_service.repository.get_request_by_id.assert_called_once_with(request_id)
        assert isinstance(result, RequestRead)
        request_service.repository.complete_return_request.assert_called_once_with(request_id, mock_admin_user.id)
        request_service.assignment_repository.update_assignment_state.assert_called_once()
        request_service.asset_repository.update_asset.assert_called_once()
