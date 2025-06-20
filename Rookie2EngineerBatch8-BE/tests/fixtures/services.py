import pytest

@pytest.fixture
def user_service(db_session):
    """Fixture that provides a UserService instance for testing"""
    from services.user import UserService
    return UserService(db_session)

@pytest.fixture
def asset_service(db_session):
    """Fixture that provides an AssetService instance for testing"""
    from services.asset import AssetService
    return AssetService(db_session) 