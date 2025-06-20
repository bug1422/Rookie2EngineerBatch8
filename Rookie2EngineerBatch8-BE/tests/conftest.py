import pytest
from unittest.mock import Mock, patch
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from datetime import date, datetime, timezone, timedelta
from jose import jwt
from core.config import settings

# Import fixtures from the new files
from enums.assignment.state import AssignmentState
from enums.user.gender import Gender
from tests.fixtures.auth import mock_current_user, mock_token
from tests.fixtures.database import mock_db_query, db_session, load_metadata
from tests.fixtures.services import user_service, asset_service
from tests.fixtures.test_data import multiple_users, multiple_assets



class MockUser:
    pass

# Patch database and models before importing app
with patch('database.postgres.PostgresDatabase') as mock_db, \
     patch('models.user.User', MockUser):
    
    # Mock the database instance
    mock_instance = Mock()
    mock_db.return_value = mock_instance
    
    # Mock the engine and connection
    mock_instance.engine = Mock()
    mock_instance.engine.connect.return_value = Mock()
    
    from main import app
    from api.dependencies import get_db_session, get_current_user, get_current_admin
    from schemas.user import UserRead
    from enums.shared.location import Location
    from enums.user.status import Status
    from enums.user.type import Type
    from utils.date_and_time import get_current_date
    
@pytest.fixture
def mock_current_user():
    """Mock the current authenticated user"""
    return UserRead(
        id=1,
        username="testuser",
        staff_code="SD0001",
        first_name="Test",
        last_name="User",
        date_of_birth=get_current_date() - timedelta(days=365*30),
        join_date=get_current_date(),
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

@pytest.fixture
def mock_db_query(multiple_users, multiple_assets):
    """Mock database query object"""
    mock = Mock()
    mock.filter.return_value = mock
    mock.join.return_value = mock
    mock.order_by.return_value = mock
    mock.offset.return_value = mock
    mock.limit.return_value = mock
    mock.count.return_value = len(multiple_users)  # Return actual count
    mock.all.return_value = multiple_users  # Return test data
    mock.first.return_value = multiple_users[0] if multiple_users else None
    return mock

@pytest.fixture
def db_session(mock_db_query):
    """Mock database session for testing"""
    session = Mock(spec=Session)
    session.query.return_value = mock_db_query
    session.add.return_value = None
    session.commit.return_value = None
    session.refresh.return_value = None
    session.delete.return_value = None
    session.rollback.return_value = None
    session.close.return_value = None
    return session

@pytest.fixture
def client(db_session, mock_current_user, mock_token):
    """Fixture that creates a FastAPI TestClient with mocked dependencies"""
    def override_get_db():
        yield db_session
    
    async def override_get_current_user():
        return mock_current_user
    
    async def override_get_current_admin():
        return mock_current_user
    
    app.dependency_overrides[get_db_session] = override_get_db
    app.dependency_overrides[get_current_user] = override_get_current_user
    app.dependency_overrides[get_current_admin] = override_get_current_admin
    
    with TestClient(app) as test_client:
        # Set cookie and authorization header for the mock user
        test_client.cookies.set("access_token", mock_token)
        test_client.headers.update({"Authorization": f"Bearer {mock_token}"})
        yield test_client
    
    app.dependency_overrides.clear()

@pytest.fixture
def load_metadata(db_session):
    """Fixture to load metadata for tests"""
    from sqlalchemy import MetaData
    from unittest.mock import Mock, MagicMock
    
    metadata = MetaData()
    if isinstance(db_session, Mock):
        # For mock sessions, create a mock bind with inspection context
        mock_bind = MagicMock()
        mock_inspector = MagicMock()
        mock_inspector.get_table_names.return_value = []
        mock_inspector.get_columns.return_value = []
        mock_inspector.get_pk_constraint.return_value = {'constrained_columns': []}
        mock_inspector.get_foreign_keys.return_value = []
        mock_inspector.get_unique_constraints.return_value = []
        mock_inspector.get_check_constraints.return_value = []
        mock_inspector.get_indexes.return_value = []
        
        mock_bind._inspection_context.return_value.__enter__.return_value = mock_inspector
        db_session.bind = mock_bind
        metadata.bind = mock_bind
    else:
        # For real sessions, use the actual database
        metadata.reflect(bind=db_session.bind)
    return metadata

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

@pytest.fixture
def multiple_users():
    """Fixture that provides multiple test users"""
    from datetime import date
    from schemas.user import UserRead
    from enums.user.type import Type
    from enums.user.status import Status
    from enums.shared.location import Location
    from enums.user.gender import Gender

    return [
        UserRead(
            id=1,
            username="user1",
            staff_code="SD0001",
            first_name="User",
            last_name="One",
            date_of_birth=date(1990, 1, 1),
            join_date=date(2023, 1, 1),
            gender=Gender.MALE,
            type=Type.STAFF,
            location=Location.HANOI,
            status=Status.ACTIVE,
            is_first_login=True,
        ),
        UserRead(
            id=2,
            username="user2",
            staff_code="SD0002",
            first_name="User",
            last_name="Two",
            date_of_birth=date(1990, 1, 1),
            join_date=date(2023, 1, 1),
            gender=Gender.FEMALE,
            type=Type.ADMIN,
            location=Location.HCM,
            status=Status.ACTIVE,
            is_first_login=False,
        ),
    ]

@pytest.fixture
def multiple_assets():
    """Fixture that provides multiple test assets"""
    from datetime import date
    from schemas.asset import AssetRead
    from schemas.category import CategoryRead
    from enums.asset.state import AssetState
    from enums.shared.location import Location

    category = CategoryRead(
        id=1,
        category_name="Test Category",
        prefix="A"
    )

    return [
        AssetRead(
            id=1,
            asset_code="A001",
            asset_name="Test Asset 1",
            category_id=1,
            specification="Test Specification 1",
            installed_date=date(2023, 1, 1),
            asset_state=AssetState.AVAILABLE,
            asset_location=Location.HANOI,
            category=category
        ),
        AssetRead(
            id=2,
            asset_code="A002",
            asset_name="Test Asset 2",
            category_id=1,
            specification="Test Specification 2",
            installed_date=date(2023, 1, 2),
            asset_state=AssetState.AVAILABLE,
            asset_location=Location.HANOI,
            category=category
        )
    ]

@pytest.fixture
def mock_user_read():
    """Mock UserRead object for testing"""
    from datetime import date
    from schemas.user import UserRead
    from enums.user.type import Type
    from enums.user.status import Status
    from enums.shared.location import Location
    from enums.user.gender import Gender
    
    return UserRead(
        id=1,
        username="testuser",
        staff_code="SD0001",
        first_name="Test",
        last_name="User",
        date_of_birth=date(1990, 1, 1),
        join_date=date(2023, 1, 2),
        gender=Gender.MALE,
        type=Type.ADMIN,
        location=Location.HANOI,
        status=Status.ACTIVE,
        is_first_login=True
    )

@pytest.fixture
def mock_admin_user():
    """Mock admin user for testing"""
    return UserRead(
        id=2,
        username="adminuser",
        staff_code="SD0002",
        first_name="Admin",
        last_name="User",
        date_of_birth=date(1990, 1, 1),
        join_date=date(2023, 1, 2),
        gender=Gender.MALE,
        type=Type.ADMIN,
        location=Location.HANOI,
        status=Status.ACTIVE,
        is_first_login=True
    )
