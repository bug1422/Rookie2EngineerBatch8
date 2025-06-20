import pytest
from core.exceptions import NotFoundException, BusinessException
from schemas.query.filter.asset import AssetFilter
from schemas.query.sort.sort_type import SortAssetBy, SortDirection
from schemas.shared.paginated_response import PaginatedResponse
from schemas.asset import AssetRead
from enums.shared.location import Location

class TestAssetRead:
    def test_read_assets_paginated(self, asset_service, mock_user, mock_asset_read):
        # Arrange
        states=[mock_asset_read.asset_state]
        asset_filter = AssetFilter(
            page=1,
            size=10,
            sort_by=SortAssetBy.ASSET_CODE,
            sort_direction=SortDirection.ASC
        )
        mock_assets = [mock_asset_read, mock_asset_read]
        total = len(mock_assets)
        paginated_response = PaginatedResponse[AssetRead](
            data=mock_assets,
            meta={
                "page": asset_filter.page,
                "page_size": asset_filter.size,
                "total": total,
                "total_pages": (total + asset_filter.size - 1) // asset_filter.size
            }
        )
        asset_service.repository.get_assets_paginated.return_value = paginated_response

        # Act
        result = asset_service.read_assets_paginated(
            states,asset_filter, mock_user.location)

        # Assert
        assert len(result.data) == 2
        assert result.meta.total == 2
        assert result.meta.page == 1
        asset_service.repository.get_assets_paginated.assert_called_once_with(
            states,
            asset_filter,
            mock_user.location
        )

    def test_read_asset_success(self, asset_service, mock_asset_read, mock_user):
        # Arrange
        asset_service.repository.get_asset_by_id.return_value = mock_asset_read

        # Act
        result = asset_service.read_asset(1, mock_user.location)

        # Assert
        assert result == mock_asset_read
        asset_service.repository.get_asset_by_id.assert_called_once_with(1)

    def test_read_asset_not_found(self, asset_service, mock_user):
        # Arrange
        asset_service.repository.get_asset_by_id.return_value = None

        # Act & Assert
        with pytest.raises(NotFoundException, match="Asset with id 1 not found"):
            asset_service.read_asset(1, mock_user.location)
            
        
    def test_read_asset_location_mismatch(self, asset_service, mock_asset_read):
        # Arrange
        mock_asset_read.asset_location = Location.DANANG
        asset_service.repository.get_asset_by_id.return_value = mock_asset_read

         # Act & Assert
        with pytest.raises(BusinessException, match="You can only read asset that are in the same location as you"):
            asset_service.read_asset(1, Location.HANOI)
            