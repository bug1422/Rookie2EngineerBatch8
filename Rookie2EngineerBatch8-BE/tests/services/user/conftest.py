import pytest
from unittest.mock import Mock, patch
from enums.shared.location import Location
from tests.test_data.mock_user import get_mock_user_create, get_mock_user_read
from services.user import UserService
from enums.user.type import Type

@pytest.fixture
def mock_user_create():
    return get_mock_user_create()


@pytest.fixture
def mock_user_read():
    user = get_mock_user_read()
    # Ensure consistent location for permission tests
    user.location = Location.HANOI
    return user


@pytest.fixture
def mock_current_user():
    user = get_mock_user_read()
    user.location = Location.HANOI
    return user


@pytest.fixture
def mock_admin_user():
    user = get_mock_user_read()
    user.id = 999
    user.type = Type.ADMIN
    user.location = Location.HANOI
    return user


@pytest.fixture
def mock_staff_user():
    user = get_mock_user_read()
    user.id = 100
    user.type = Type.STAFF
    user.location = Location.HANOI
    return user


@pytest.fixture
def user_service():
    db = Mock()
    repository = Mock()
    with patch("services.assignment.AssignmentRepository", return_value=repository):
        service = UserService(db)
        service.repository = repository
        yield service 
