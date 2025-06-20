import pytest
from schemas.query.filter.request import RequestFilter
from schemas.query.sort.sort_type import SortRequestBy, SortDirection
from schemas.shared.paginated_response import PaginatedResponse
from schemas.request import RequestReadDetail

class TestRequestServiceRead:
    def test_read_request_paginated_success(self, request_service, mock_request_read_detail, mock_current_user):
        # Arrange
        request_filter = RequestFilter(
            page=1,
            size=20,
            sort_by=SortRequestBy.ID,
            sort_direction=SortDirection.DESC
        )
        
        mock_requests = [mock_request_read_detail]
        total = len(mock_requests)
        
        expected_response = PaginatedResponse[RequestReadDetail](
            data=mock_requests,
            meta={
                "page": request_filter.page,
                "page_size": request_filter.size,
                "total": total,
                "total_pages": (total + request_filter.size - 1) // request_filter.size,
            },
        )
        
        request_service.repository.get_requests_paginated.return_value = expected_response
        
        # Act
        result = request_service.read_requests_paginated(request_filter, mock_current_user)
        
        # Assert
        assert len(result.data) == 1
        assert result.meta.total == 1
        assert result.meta.page == 1
        request_service.repository.get_requests_paginated.assert_called_once_with(request_filter, mock_current_user)
        