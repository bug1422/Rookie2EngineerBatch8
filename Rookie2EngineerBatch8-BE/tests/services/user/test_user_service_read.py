import pytest
from fastapi import HTTPException
from schemas.query.filter.user import UserFilter
from schemas.query.sort.sort_type import SortUserBy, SortDirection
from schemas.shared.paginated_response import PaginatedResponse
from schemas.user import UserRead
from enums.user.type import Type

class TestUserRead:
    def test_read_user_paginated_success(self, user_service, mock_current_user, mock_user_read):
        # Arrange
        user_filter = UserFilter(
            page=1,
            size=20,
            sort_by=SortUserBy.FIRST_NAME,
            sort_direction=SortDirection.ASC
        )
        current_user = mock_current_user
        staff_user = mock_user_read.model_copy(deep=True, update={"type": Type.STAFF})
        mock_users = [staff_user]
        total = len(mock_users)
        
        expected_response = PaginatedResponse[UserRead](
            data=mock_users,
            meta={   
                "page": user_filter.page,
                "page_size": user_filter.size,
                "total": total,
                "total_pages": (total + user_filter.size - 1) // user_filter.size
            }
        )
        user_service.repository.get_users_paginated.return_value = expected_response

        # Act
        result = user_service.read_users_paginated(user_filter, current_user)
        
        # Assert
        assert len(result.data) == 1
        assert result.meta.total == 1
        assert result.meta.page == 1
        user_service.repository.get_users_paginated.assert_called_once_with(user_filter, current_user)

    def test_read_user_success(self, user_service, mock_user_read):
        # Arrange
        user_service.repository.get_user_by_id.return_value = mock_user_read
        
        # Act
        result = user_service.read_user(mock_user_read.id)
        
        # Assert
        assert result == mock_user_read
        user_service.repository.get_user_by_id.assert_called_once_with(mock_user_read.id)
        
    def test_read_user_not_found(self, user_service):
        # Arrange
        user_service.repository.get_user_by_id.return_value = None
        
        # Act & Assert
        with pytest.raises(HTTPException, match="User with id 9999 not found"):
            user_service.read_user(9999)
        
        
        