import pytest
from models.user import User
from schemas.query.filter.user import UserFilter
from enums.shared.location import Location
from enums.user.type import Type
from schemas.query.sort.sort_type import SortDirection, SortUserBy
from sqlmodel import func

class TestUserRead:
    def test_get_user_by_id_calls_filter_correct(self, user_repository, mock_user_read, mocker):
        user_id = mock_user_read.id
        
        mock_query = mocker.MagicMock()
        mock_query.filter.return_value = mock_query
        mock_query.first.return_value = mock_user_read
        user_repository.db.query.return_value = mock_query
        
        result = user_repository.get_user_by_id(user_id)
        expected_filter = User.id == user_id
        assert any(expected_filter.compare(expr)
                   for call_args in mock_query.filter.call_args_list for expr in call_args[0])
        assert result == mock_user_read
        
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
            "total_pages": 2,
            "page": 3,
            "page_size": 1
        },
    ])
    def test_get_paginated_user_returns_paging_correct(self, expected_meta, user_repository, mock_user_read, mocker):
        page = expected_meta["page"]
        size = expected_meta["page_size"]
        multiple_users = [mock_user_read] * expected_meta["total"]
        user_filter = UserFilter(
            page=page,
            size=size,
        )

        mock_query = mocker.MagicMock()
        user_repository.db.query.return_value = mock_query
        mock_query.filter.return_value = mock_query
        mock_query.order_by.return_value = mock_query
        mock_query.offset.return_value = mock_query
        mock_query.limit.return_value = mock_query

        mock_query.count.return_value = expected_meta["total"]
        
        paged_index_start = (page - 1) * size
        paged_index_end = paged_index_start + size
        page_users = multiple_users[paged_index_start:paged_index_end]
        mock_query.all.return_value = page_users
        
        paginated_response = user_repository.get_users_paginated(
            user_filter=user_filter,
            user_current=mock_user_read
        )
        
        assert paginated_response.meta.total == expected_meta["total"]
        assert paginated_response.meta.total_pages == expected_meta["total_pages"]
        assert paginated_response.meta.page == expected_meta["page"]
        assert paginated_response.meta.page_size == expected_meta["page_size"]
        
        assert paginated_response.data == page_users

    def test_get_paginated_user_calls_type_filter_admin(self, user_repository, mock_user_read, mocker):
        user_filter = UserFilter(
            page=1,
            size=10,
            type=Type.ADMIN,
        )
        # Mock query chain
        mock_query = mocker.MagicMock()
        user_repository.db.query.return_value = mock_query
        mock_query.filter.return_value = mock_query
        mock_query.order_by.return_value = mock_query
        expected_filter = User.type == user_filter.type
        user_repository.get_users_paginated(
            user_filter=user_filter,
            user_current=mock_user_read
        )
        
        assert any(expected_filter.compare(expr)
                   for call_args in mock_query.filter.call_args_list for expr in call_args[0])
    
    def test_get_paginated_user_calls_type_filter_staff(self, user_repository, mock_user_read, mocker):
        user_filter = UserFilter(
            page=1,
            size=10,
            type=Type.STAFF,
        )
        # Mock query chain
        mock_query = mocker.MagicMock()
        user_repository.db.query.return_value = mock_query
        mock_query.filter.return_value = mock_query
        mock_query.order_by.return_value = mock_query
        expected_filter = User.type == user_filter.type
        user_repository.get_users_paginated(
            user_filter=user_filter,
            user_current=mock_user_read
        )
        
        assert any(expected_filter.compare(expr)
                   for call_args in mock_query.filter.call_args_list for expr in call_args[0])
        
    def test_get_paginated_user_calls_search_filter(self, user_repository, mock_user_read, mocker):
        user_filter = UserFilter(
            page=1,
            size=10,
            search="test",
        )
        # Mock query chain
        mock_query = mocker.MagicMock()
        user_repository.db.query.return_value = mock_query
        mock_query.filter.return_value = mock_query
        mock_query.order_by.return_value = mock_query
        expected_filter = (User.staff_code.ilike(f"%{user_filter.search}%")) | (
            User.first_name.ilike(f"%{user_filter.search}%")) | (
            User.last_name.ilike(f"%{user_filter.search}%"))
        user_repository.get_users_paginated(
            user_filter=user_filter,
            user_current=mock_user_read
        )
        assert any(expected_filter.compare(expr)
                   for call_args in mock_query.filter.call_args_list for expr in call_args[0])
        
    @pytest.mark.parametrize(("sort_by", "sort_direction"), [
        (SortUserBy.FIRST_NAME, SortDirection.ASC),
        (SortUserBy.FIRST_NAME, SortDirection.DESC),
        (SortUserBy.STAFF_CODE, SortDirection.ASC),
        (SortUserBy.STAFF_CODE, SortDirection.DESC),
        (SortUserBy.JOIN_DATE, SortDirection.ASC),
        (SortUserBy.JOIN_DATE, SortDirection.DESC),
        (SortUserBy.TYPE, SortDirection.ASC),
        (SortUserBy.TYPE, SortDirection.DESC),
        (SortUserBy.UPDATED_AT, SortDirection.ASC),
        (SortUserBy.UPDATED_AT, SortDirection.DESC),
    ])
    def test_get_paginated_user_calls_sort_by_correct(self, sort_by, sort_direction, user_repository, mock_user_read, mocker):
        user_filter = UserFilter(
            page=1,
            size=10,
            sort_by=sort_by,
            sort_direction=sort_direction
        )
        # Mock query chain
        mock_query = mocker.MagicMock()
        user_repository.db.query.return_value = mock_query
        mock_query.filter.return_value = mock_query
        mock_query.order_by.return_value = mock_query
        if sort_by == SortUserBy.FIRST_NAME:
            expected_sort = func.lower(User.first_name).asc() if sort_direction == SortDirection.ASC else func.lower(User.first_name).desc()
        elif sort_by == SortUserBy.STAFF_CODE:
            expected_sort = User.staff_code.asc(
            ) if sort_direction == SortDirection.ASC else User.staff_code.desc()
        elif sort_by == SortUserBy.JOIN_DATE:
            expected_sort = User.join_date.asc(
            ) if sort_direction == SortDirection.ASC else User.join_date.desc()
        elif sort_by == SortUserBy.TYPE:
            expected_sort = User.type.asc(
            ) if sort_direction == SortDirection.ASC else User.type.desc()
        elif sort_by == SortUserBy.UPDATED_AT:
            expected_sort = User.updated_at.asc(
            ) if sort_direction == SortDirection.ASC else User.updated_at.desc()
        
        user_repository.get_users_paginated(
            user_filter=user_filter,
            user_current=mock_user_read
        )
        assert any(expected_sort.compare(expr)
                   for call_args in mock_query.order_by.call_args_list for expr in call_args[0])
