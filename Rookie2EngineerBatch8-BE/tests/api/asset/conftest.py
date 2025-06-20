import pytest
from tests.test_data.mock_asset import get_mock_asset, get_mock_assets

@pytest.fixture
def mock_asset():
    """Fixture that returns a mock asset"""
    return get_mock_asset()

@pytest.fixture
def mock_assets():
    """Fixture that returns a list of mock assets"""
    return get_mock_assets() 