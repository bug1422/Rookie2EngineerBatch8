import pytest
from tests.test_data.mock_user import get_mock_user_create, get_mock_user_read

@pytest.fixture
def mock_user_create():
    return get_mock_user_create()

@pytest.fixture
def mock_user_read():
    return get_mock_user_read() 