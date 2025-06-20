import pytest
from repositories.user import UserRepository
from unittest.mock import Mock
from tests.test_data.mock_user import get_mock_user_create, get_mock_user_read

@pytest.fixture
def mock_user_create():
    return get_mock_user_create()


@pytest.fixture
def mock_user_read():
    return get_mock_user_read()


@pytest.fixture(
    scope="function"
)
def user_repository():
    db = Mock()
    repository = UserRepository(db)
    yield repository