import pytest
from datetime import datetime, timedelta, timezone
from schemas.auth import AccessTokenPayload, RefreshTokenPayload
from enums.user.type import Type
from enums.shared.location import Location
import uuid
from unittest.mock import Mock, patch
from services.user import UserService

@pytest.fixture
def mock_access_token_payload():
    """Fixture that returns a mock access token payload"""
    return AccessTokenPayload(
        sub="testuser",
        user_id=1,
        first_name="Test",
        last_name="User",
        type=Type.ADMIN,
        is_first_login=False,
        location=Location.HANOI,
        exp=0  # exp will be set by create_access_token
    )

@pytest.fixture
def mock_access_token_data():
    """Fixture that returns mock access token data as a dictionary"""
    return {
        "sub": "testuser",
        "user_id": 1,
        "first_name": "Test",
        "last_name": "User",
        "type": Type.ADMIN.value,  # Note: Using .value for enum
        "is_first_login": False,
        "location": Location.HANOI.value  # Note: Using .value for enum
        # exp will be set by create_access_token
    }

@pytest.fixture
def mock_refresh_token_payload():
    """Fixture that returns a mock refresh token payload"""
    return RefreshTokenPayload(
        sub="testuser",
        user_id=1,
        jti=str(uuid.uuid4()),
        exp=0  # exp will be set by create_refresh_token
    )
    
@pytest.fixture
def mock_refresh_token_data():
    """Fixture that returns mock refresh token data as a dictionary"""
    return {
        "sub": "testuser",
        "user_id": 1,
        "jti": str(uuid.uuid4())
        # exp will be set by create_refresh_token
    }

@pytest.fixture
def mock_expired_token_data():
    """Fixture that returns mock expired token data"""
    return {
        "sub": "testuser",
        "user_id": 1,
        "first_name": "Test",
        "last_name": "User",
        "type": Type.ADMIN.value,
        "is_first_login": False,
        "location": Location.HANOI.value,
        "exp": int((datetime.now(timezone.utc) - timedelta(minutes=15)).timestamp())  # Note: Past time
    }

@pytest.fixture
def mock_custom_expiry_delta():
    """Fixture that returns a custom expiry timedelta"""
    return timedelta(minutes=30)  # Custom 30 minute expiry

@pytest.fixture
def user_service():
    db = Mock()
    repository = Mock()
    with patch("services.assignment.AssignmentRepository", return_value=repository):
        service = UserService(db)
        service.repository = repository
        yield service
