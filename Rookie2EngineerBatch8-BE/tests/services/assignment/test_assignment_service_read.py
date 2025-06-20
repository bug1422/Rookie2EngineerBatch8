import pytest
from schemas.query.filter.assignment import AssignmentFilter
from schemas.query.sort.sort_type import SortAssignmentBy, SortDirection
from schemas.shared.paginated_response import PaginatedResponse
from schemas.assignment import AssignmentRead
from core.exceptions import NotFoundException

class TestAssignmentRead:
    def test_read_assignment_paginated_success(self, assignment_service, mock_assignment, mock_current_user):
        # Arrange
        assignment_filter = AssignmentFilter(
            page=1,
            size=20,
            sort_by=SortAssignmentBy.ID,
            sort_direction=SortDirection.DESC
        )
        mock_assignments = [mock_assignment]
        total = len(mock_assignments)
        
        expected_response = PaginatedResponse[AssignmentRead](
            data=mock_assignments,
            meta={
                "page": assignment_filter.page,
                "page_size": assignment_filter.size,
                "total": total,
                "total_pages": (total + assignment_filter.size - 1) // assignment_filter.size,
            },
        )
        assignment_service.repository.get_assignments_paginated.return_value = expected_response

        # Act
        result = assignment_service.read_assignments_paginated(assignment_filter, mock_current_user)
        
        # Assert
        assert len(result.data) == 1
        assert result.meta.total == 1
        assert result.meta.page == 1
        assignment_service.repository.get_assignments_paginated.assert_called_once_with(assignment_filter, mock_current_user)
        
    def test_read_assignment_success(
        self,
        assignment_service,
        mock_assignment_model,
        mock_asset_model,
        mock_staff_user_hanoi,
        mock_admin_user_hanoi,
        mock_current_user,
        mock_assignment_detail,
        asset_service,
        user_service,
        mock_asset_hanoi,
    ):
        # Arrange
        # Mock assignment retrieval
        assignment_service.repository.get_assignment_by_id_no_join.return_value = mock_assignment_model

        # Mock asset service - mock at repository level
        asset_service.repository.get_asset_by_id.return_value = mock_asset_hanoi
        assignment_service.repository.db = asset_service.repository.db

        def mock_get_user_by_id(user_id):
            if user_id == mock_assignment_model.assigned_to_id:  # id=2
                return mock_staff_user_hanoi
            elif user_id == mock_assignment_model.assigned_by_id:  # id=1
                return mock_admin_user_hanoi
            return None

        user_service.repository.get_user_by_id.side_effect = mock_get_user_by_id
        
        assignment_service.repository.read_assignment.return_value = mock_assignment_detail

        # Act
        result = assignment_service.read_assignment(mock_assignment_model.id, mock_current_user)
        
        # Assert
        assert result == mock_assignment_detail
        assignment_service.repository.get_assignment_by_id_no_join.assert_called_once_with(mock_assignment_model.id)
        
    def test_read_assignment_not_found(self, assignment_service, mock_current_user):
        # Arrange
        assignment_service.repository.get_assignment_by_id_no_join.return_value = None
        
        # Act & Assert
        with pytest.raises(NotFoundException, match="Assignment with id 9999 not found"):
            assignment_service.read_assignment(9999, mock_current_user)
        
        assignment_service.repository.get_assignment_by_id_no_join.assert_called_once_with(9999)
        
        