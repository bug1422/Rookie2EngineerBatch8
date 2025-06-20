import pytest
from datetime import datetime, timedelta, timezone
from jose import jwt
from core.config import settings
from schemas.user import UserRead
from enums.shared.location import Location
from enums.user.status import Status
from enums.user.type import Type

@pytest.fixture
def mock_current_user():
    """Mock the current authenticated user"""
    return UserRead(
        id=1,
        username="testuser",
        staff_code="SD0001",
        first_name="Test",
        last_name="User",
        date_of_birth=datetime.now().date() - timedelta(days=365*30),
        join_date=datetime.now().date(),
        location=Location.HANOI,
        status=Status.ACTIVE,
        is_first_login=False,
        type=Type.ADMIN
    )

@pytest.fixture
def mock_token(mock_current_user):
    """Create a mock JWT token"""
    payload = {
        "sub": mock_current_user.username,
        "type": mock_current_user.type,
        "user_id": mock_current_user.id,
        "first_name": mock_current_user.first_name,
        "last_name": mock_current_user.last_name,
        "is_first_login": mock_current_user.is_first_login,
        "location": mock_current_user.location,
        "exp": datetime.now(timezone.utc).timestamp() + 3600  # 1 hour from now
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM) 