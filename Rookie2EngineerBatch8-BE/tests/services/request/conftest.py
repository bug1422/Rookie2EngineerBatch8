import pytest
from datetime import date, datetime
from unittest.mock import Mock, patch

from enums.asset.state import AssetState
from enums.assignment.state import AssignmentState
from enums.user.status import Status
from repositories.asset import AssetRepository
from schemas.assignment import AssignmentRead, AssignmentReadSimple, AssignmentState
from schemas.request import RequestCreate, RequestUpdate
from schemas.user import UserRead
from services.assignment import AssignmentService
from enums.request.state import RequestState
from models.request import Request
from services.request import RequestReturningService
from schemas.request import RequestRead, RequestReadDetail
from schemas.asset import AssetRead, AssetState
from schemas.category import CategoryRead
from enums.shared.location import Location
from schemas.user import UserReadSimple


@pytest.fixture
def mock_staff_user():
    return UserRead(
        id=2,
        username="test_staff_user",
        staff_code="SD002",
        first_name="Test",
        last_name="User",
        date_of_birth=date(1990, 1, 1),
        join_date=date(2023, 1, 1),
        location=Location.HCM,
        status=Status.ACTIVE,
        is_first_login=False,
        type="staff"
    )
    
@pytest.fixture
def mock_admin_user():
    return UserRead(
        id=1,
        username="test_admin_user",
        staff_code="AD001",
        first_name="Admin",
        last_name="User",
        date_of_birth=date(1985, 5, 15),
        join_date=date(2022, 6, 1),
        location=Location.HCM,
        status=Status.ACTIVE,
        is_first_login=False,
        type="admin"
    )
    
@pytest.fixture
def mock_category():
    return CategoryRead(
        prefix="CA",
        id=1,
        category_name="Test Category"
    )
    
@pytest.fixture
def mock_asset(mock_category):
    return AssetRead(
        id=3,
        asset_code="AS000001",
        asset_name="Test Asset",
        specification="Test Specification",
        asset_location=Location.HCM,
        asset_state=AssetState.AVAILABLE,
        installed_date=date(2023, 1, 1),
        category= mock_category,
    )

@pytest.fixture
def mock_assignment(mock_staff_user, mock_asset, mock_admin_user):
    return AssignmentRead(
        id=1,
        asset_id=mock_asset.id,
        assigned_to_id=mock_staff_user.id,
        assigned_by_id=mock_admin_user.id,
        assigned_to_username=mock_staff_user.username,
        assigned_by_username=mock_admin_user.username,
        assign_date=date(2023, 1, 15),
        assignment_state=AssignmentState.ACCEPTED,
        assignment_note= "Test assignment note",
        asset= mock_asset,
    )

@pytest.fixture
def mock_request_create(mock_assignment):
    return RequestCreate(
        assignment_id=mock_assignment.id,
    )
    
@pytest.fixture
def request_returning_service():
    db = Mock()
    repository = Mock()
    assignment_service = Mock()
    
    with patch("repositories.request.RequestReturningRepository", return_value=repository), \
         patch("services.assignment.AssignmentService", return_value=assignment_service):
        service = RequestReturningService(db)
        service.repository = repository
        service.assignment_service = assignment_service
        # Add missing repository assignments
        service.assignment_repository = Mock()
        service.asset_repository = Mock()
        yield service
        
@pytest.fixture
def assignment_service():
    db = Mock()
    repository = Mock()
    with patch("services.assignment.AssignmentRepository", return_value=repository):
        service = AssignmentService(db)
        service.repository = repository
        yield service

@pytest.fixture
def request_service():
    db = Mock()
    repository = Mock()
    assignment_repository = Mock()
    asset_repository = Mock()
    
    with patch("services.request.RequestReturningRepository", return_value=repository), \
         patch("services.request.AssignmentRepository", return_value=assignment_repository), \
         patch("services.request.AssetRepository", return_value=asset_repository), \
         patch("services.request.AssignmentService") as mock_assignment_service:
        
        service = RequestReturningService(db)
        service.repository = repository
        service.assignment_repository = assignment_repository
        service.asset_repository = asset_repository
        service.assignment_service = mock_assignment_service.return_value
        yield service

@pytest.fixture
def mock_request_model():
    return Request(
        assignment_id=1,
        requested_by_id=1,
        accepted_by_id=2,
        return_date=date(2023, 1, 1),
        request_state=RequestState.COMPLETED
    )
    
@pytest.fixture
def mock_asset_hanoi():
    return AssetRead(
        id=1,
        asset_code="AS000001",
        asset_name="Test Asset" ,
        specification="Test Specification",
        installed_date=date(2023, 1, 1),
        asset_state=AssetState.ASSIGNED,
        asset_location=Location.HANOI,
        category=CategoryRead(
            id=1,
            category_name="Test Category",
            prefix="TC"
        )
    )

@pytest.fixture
def mock_staff_user_hanoi():
    return UserReadSimple(
        username="test_user",
        staff_code="SD002",
        first_name="Test",
        last_name="User",
    )


@pytest.fixture
def mock_admin_user_hanoi():
    return UserReadSimple(
        username="test_admin",
        staff_code="SD001",
        first_name="Test",
        last_name="Admin",
    )

@pytest.fixture
def mock_assignment_hanoi():
    return AssignmentReadSimple(
        id=1,
        assign_date=date(2023, 1, 1),
        assignment_state=AssignmentState.ACCEPTED,
        assignment_note="Test Assignment",
    )

@pytest.fixture
def mock_request_read_detail(mock_assignment_hanoi, mock_asset_hanoi, mock_staff_user_hanoi, mock_admin_user_hanoi):
    return RequestReadDetail(
        id=1,
        asset=mock_asset_hanoi,
        requested_by=mock_staff_user_hanoi,
        accepted_by=mock_admin_user_hanoi,
        assignment=mock_assignment_hanoi,
        return_date=date(2023, 1, 1),
        request_state=RequestState.COMPLETED
    )

@pytest.fixture
def mock_current_user():
    """Mock current user for general testing"""
    return UserRead(
        id=1,
        username="current_user",
        staff_code="CU001",
        first_name="Current",
        last_name="User",
        date_of_birth=date(1990, 1, 1),
        join_date=date(2023, 1, 1),
        location=Location.HCM,
        status=Status.ACTIVE,
        is_first_login=False,
        type="admin"
    )

@pytest.fixture
def mock_request_update():
    """Mock request update data"""
    return RequestUpdate(request_state=RequestState.COMPLETED)

@pytest.fixture
def mock_request_waiting_state(mock_request_model):
    """Mock request in waiting for returning state"""
    mock_request_model.request_state = RequestState.WAITING_FOR_RETURNING
    return mock_request_model

@pytest.fixture
def mock_request_completed_state(mock_request_model):
    """Mock request in completed state"""
    mock_request_model.request_state = RequestState.COMPLETED
    return mock_request_model

@pytest.fixture
def mock_completed_request(mock_admin_user):
    """Mock completed request"""
    mock_completed_request = Mock()
    mock_completed_request.id = 1
    mock_completed_request.request_state = RequestState.COMPLETED
    mock_completed_request.requested_by_id = 1
    mock_completed_request.assignment_id = 1
    mock_completed_request.return_date = datetime.now()
    mock_completed_request.accepted_by_id = mock_admin_user.id
    return mock_completed_request