import pytest
from schemas.query.filter.asset import AssetFilter
from schemas.query.sort.sort_type import SortAssetBy, SortDirection
from enums.shared.location import Location
from enums.asset.state import AssetState
from models.category import Category
from models.asset import Asset
from sqlmodel import func

class TestAssetRead:
    def test_get_asset_by_id_calls_filter_correct(self, asset_repository, mock_asset_read, mocker):
        asset_id = mock_asset_read.id
        
        mock_query = mocker.MagicMock()
        mock_query.filter.return_value = mock_query
        mock_query.first.return_value = mock_asset_read
        asset_repository.db.query.return_value = mock_query
        
        result = asset_repository.get_asset_by_id(asset_id)
        expected_filter = Asset.id == asset_id
        assert any(expected_filter.compare(expr)
                   for call_args in mock_query.filter.call_args_list for expr in call_args[0])
        assert result == mock_asset_read
        
    @pytest.mark.parametrize(("expected_meta"), [
        {
            "total": 2,
            "total_pages": 2,
            "page": 1,
            "page_size": 1
        },
        {
            "total": 2,
            "total_pages": 1,
            "page": 1,
            "page_size": 2
        },
        {
            "total": 2,
            "total_pages": 2,
            "page": 2,
            "page_size": 1
        },
        {
            "total": 2,
            "total_pages": 1,
            "page": 2,
            "page_size": 2
        },
    ])
    def test_get_paginated_asset_returns_paging_correct(self, expected_meta, asset_repository, mock_asset_read, mocker):
        page = expected_meta["page"]
        size = expected_meta["page_size"]
        multiple_assets = [mock_asset_read] * expected_meta["total"]
        asset_filter = AssetFilter(
            page=page,
            size=size,
        )

        # Mock query chain
        mock_query = mocker.MagicMock()
        mock_query.filter.return_value = mock_query
        mock_query.join.return_value = mock_query
        mock_query.order_by.return_value = mock_query
        asset_repository.db.query.return_value = mock_query
        mock_query.count.return_value = expected_meta["total"]

        # expected page slice
        paged_index_start = (page - 1) * size
        paged_index_end = paged_index_start + size
        page_assets = multiple_assets[paged_index_start:paged_index_end]
        mock_query.offset.return_value.limit.return_value.all.return_value = page_assets

        # Call the repository method directly!
        paginated_response = asset_repository.get_assets_paginated(
            states=[AssetState.AVAILABLE],
            asset_filter=asset_filter,
            current_user_location=Location.HCM
        )
        data_count = expected_meta.get("page_size")
        assert paginated_response.meta.total == expected_meta["total"]
        assert paginated_response.meta.total_pages == expected_meta["total_pages"]
        assert paginated_response.meta.page == expected_meta["page"]
        assert paginated_response.meta.page_size == expected_meta["page_size"]

        if paginated_response.meta.total_pages >= expected_meta["page"]:
            for index in range(data_count):
                paged_index = (page - 1) * size + index
                assert paginated_response.data[index].id == multiple_assets[paged_index].id
        else:
            assert paginated_response.data == []  # No data for non-existing page

    def test_get_paginated_asset_calls_category_filter(self, asset_repository, mock_asset_read, mocker):
        asset_filter = AssetFilter(
            page=1,
            size=10,
            category="test",
        )
        # Mock query chain
        mock_query = mocker.MagicMock()
        mock_query.filter.return_value = mock_query
        mock_query.join.return_value = mock_query
        mock_query.order_by.return_value = mock_query
        asset_repository.db.query.return_value = mock_query
        expected_filter = Category.category_name.ilike(
            f"%{asset_filter.category}%")
        asset_repository.get_assets_paginated(
            states=[mock_asset_read.asset_state],
            asset_filter=asset_filter,
            current_user_location=Location.HCM
        )
        assert any(expected_filter.compare(expr)
                   for call_args in mock_query.filter.call_args_list for expr in call_args[0])

    def test_get_paginated_asset_calls_search_filter(self, asset_repository, mock_asset_read, mocker):
        asset_filter = AssetFilter(
            page=1,
            size=10,
            search="test",
        )
        # Mock query chain
        mock_query = mocker.MagicMock()
        mock_query.filter.return_value = mock_query
        mock_query.join.return_value = mock_query
        mock_query.order_by.return_value = mock_query
        asset_repository.db.query.return_value = mock_query
        expected_filter = (Asset.asset_code.ilike(f"%{asset_filter.search}%")) | (
            Asset.asset_name.ilike(f"%{asset_filter.search}%"))
        asset_repository.get_assets_paginated(
            states=[mock_asset_read.asset_state],
            asset_filter=asset_filter,
            current_user_location=Location.HCM
        )
        assert any(expected_filter.compare(expr)
                   for call_args in mock_query.filter.call_args_list for expr in call_args[0])

    def test_get_paginated_asset_calls_states_filter(self, asset_repository, mock_asset_read, mocker):
        asset_filter = AssetFilter(
            page=1,
            size=10,
        )
        states = [AssetState.AVAILABLE, AssetState.NOT_AVAILABLE]
        # Mock query chain
        mock_query = mocker.MagicMock()
        mock_query.filter.return_value = mock_query
        mock_query.join.return_value = mock_query
        mock_query.order_by.return_value = mock_query
        asset_repository.db.query.return_value = mock_query
        expected_filter = (Asset.asset_state.in_(states))
        asset_repository.get_assets_paginated(
            states=states,
            asset_filter=asset_filter,
            current_user_location=Location.HCM
        )
        assert any(expected_filter.compare(expr)
                   for call_args in mock_query.filter.call_args_list for expr in call_args[0])

    @pytest.mark.parametrize(("sort_by", "sort_direction"), [
        (SortAssetBy.ASSET_CODE, SortDirection.ASC),
        (SortAssetBy.ASSET_CODE, SortDirection.DESC),
        (SortAssetBy.ASSET_NAME, SortDirection.ASC),
        (SortAssetBy.ASSET_NAME, SortDirection.DESC),
        (SortAssetBy.CATEGORY, SortDirection.ASC),
        (SortAssetBy.CATEGORY, SortDirection.DESC),
        (SortAssetBy.STATE, SortDirection.ASC),
        (SortAssetBy.STATE, SortDirection.DESC),
        (SortAssetBy.UPDATED_AT, SortDirection.ASC),
        (SortAssetBy.UPDATED_AT, SortDirection.DESC),
    ])
    def test_get_paginated_asset_calls_sort_by_correct(self, sort_by, sort_direction, asset_repository, mocker):
        asset_filter = AssetFilter(
            page=1,
            size=10,
            sort_by=sort_by,
            sort_direction=sort_direction
        )
        # Mock query chain
        mock_query = mocker.MagicMock()
        mock_query.filter.return_value = mock_query
        mock_query.join.return_value = mock_query
        mock_query.order_by.return_value = mock_query
        asset_repository.db.query.return_value = mock_query
        if sort_by == SortAssetBy.ASSET_CODE:
            expected_sort = Asset.asset_code.asc(
            ) if sort_direction == SortDirection.ASC else Asset.asset_code.desc()
        elif sort_by == SortAssetBy.ASSET_NAME:
            expected_sort = func.lower(Asset.asset_name).asc(
            ) if sort_direction == SortDirection.ASC else func.lower(Asset.asset_name).desc()
        elif sort_by == SortAssetBy.CATEGORY:
            expected_sort = func.lower(Category.category_name).asc(
            ) if sort_direction == SortDirection.ASC else func.lower(Category.category_name).desc()
        elif sort_by == SortAssetBy.STATE:
            expected_sort = Asset.asset_state.asc(
            ) if sort_direction == SortDirection.ASC else Asset.asset_state.desc()
        elif sort_by == SortAssetBy.UPDATED_AT:
            expected_sort = Asset.updated_at.asc(
            ) if sort_direction == SortDirection.ASC else Asset.updated_at.desc()

        asset_repository.get_assets_paginated(
            states=[AssetState.AVAILABLE],
            asset_filter=asset_filter,
            current_user_location=Location.HCM
        )
        assert any(expected_sort.compare(expr)
                   for call_args in mock_query.order_by.call_args_list for expr in call_args[0])
