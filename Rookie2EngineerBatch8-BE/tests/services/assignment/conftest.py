import pytest
from datetime import date
from unittest.mock import Mock, patch

from enums.asset.state import AssetState
from enums.assignment.state import AssignmentState
from enums.shared.location import Location
from enums.user.status import Status
from schemas.asset import AssetRead
from schemas.assignment import AssignmentRead, AssignmentReadDetail, AssignmentReadSimple
from schemas.category import CategoryRead
from schemas.user import UserRead
from services.assignment import AssignmentService
from services.asset import AssetService
from models.asset import Asset
from models.assignment import Assignment
from services.user import UserService

@pytest.fixture
def mock_staff_user():
    return UserRead(
        id=2,
        username="test_user",
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
        username="test_admin",
        staff_code="SD001",
        first_name="Test",
        last_name="Admin",
        date_of_birth=date(1990, 1, 1),
        join_date=date(2023, 1, 1),
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
def mock_asset_hanoi(mock_category):
    return AssetRead(
        id=3,
        asset_code="AS000001",
        asset_name="Test Asset",
        specification="Test Specification",
        asset_location=Location.HANOI,
        asset_state=AssetState.AVAILABLE,
        installed_date=date(2023, 1, 1),
        category= mock_category,
    )

@pytest.fixture
def mock_assignment(mock_staff_user, mock_admin_user, mock_asset):
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
def assignment_service():
    db = Mock()
    repository = Mock()
    with patch("services.assignment.AssignmentRepository", return_value=repository):
        service = AssignmentService(db)
        service.repository = repository
        yield service

@pytest.fixture
def mock_user():
    return UserRead(
        id=3,
        username="test_user",
        staff_code="SD003",
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
def mock_assignment_accepted():
    """Mock assignment with accepted state"""
    assignment = Mock()
    assignment.id = 1
    assignment.assignment_state = AssignmentState.ACCEPTED
    assignment.asset_id = 1
    assignment.assigned_to_id = 2
    assignment.assigned_by_id = 1
    assignment.assignment_note = "Test assignment"
    return assignment

@pytest.fixture
def mock_assignment_declined():
    """Mock assignment with declined state"""
    assignment = Mock()
    assignment.id = 1
    assignment.assignment_state = AssignmentState.DECLINED
    assignment.asset_id = 1
    assignment.assigned_to_id = 2
    assignment.assigned_by_id = 1
    assignment.assignment_note = "Test assignment"
    return assignment

@pytest.fixture
def mock_assignment_waiting():
    """Mock assignment with waiting for acceptance state"""
    assignment = Mock()
    assignment.id = 1
    assignment.assignment_state = AssignmentState.WAITING_FOR_ACCEPTANCE
    assignment.asset_id = 1
    assignment.assigned_to_id = 2
    assignment.assigned_by_id = 1
    assignment.assignment_note = "Test assignment"
    return assignment
        
@pytest.fixture
def asset_service():
    db = Mock()
    repository = Mock()
    with patch("services.asset.AssetRepository", return_value=repository):
        service = AssetService(db)
        service.repository = repository
        yield service
        
@pytest.fixture
def user_service():
    db = Mock()
    repository = Mock()
    with patch("services.user.UserRepository", return_value=repository):
        service = UserService(db)
        service.repository = repository
        yield service

@pytest.fixture
def mock_assignment_model(mock_staff_user, mock_admin_user, mock_asset_hanoi):
    """Fixture that provides a mock assignment detail for testing"""
    assignment = Assignment(
        id=1,
        asset_id=mock_asset_hanoi.id,
        assigned_to_id=mock_staff_user.id,
        assigned_by_id=mock_admin_user.id,
        assign_date=date(2023, 1, 1),
        assignment_note="Test note",
        assignment_state=AssignmentState.ACCEPTED,
    )
    return assignment

@pytest.fixture
def mock_asset_model(mock_category):
    return Asset(
        id=3,
        asset_code="AS000001",
        asset_name="Test Asset",
        specification="Test Specification",
        asset_location=Location.HANOI,
        asset_state=AssetState.AVAILABLE,
        installed_date=date(2023, 1, 1),
        category_id= mock_category.id,
    )

@pytest.fixture
def mock_assignment_detail(mock_staff_user_hanoi, mock_admin_user_hanoi, mock_asset_hanoi):
    assignment_detail = AssignmentReadDetail(
        assignment=AssignmentReadSimple(
            id=1,
            assign_date=date(2023, 1, 1),
            assignment_state=AssignmentState.ACCEPTED,
            assignment_note="Test note",
        ),
        assigned_to_user=mock_staff_user_hanoi,
        assigned_by_user=mock_admin_user_hanoi,
        asset=mock_asset_hanoi,
    )
    return assignment_detail

@pytest.fixture
def mock_staff_user_hanoi():
    return UserRead(
        id=2,
        username="test_user",
        staff_code="SD002",
        first_name="Test",
        last_name="User",
        date_of_birth=date(1990, 1, 1),
        join_date=date(2023, 1, 1),
        location=Location.HANOI,
        status=Status.ACTIVE,
        is_first_login=False,
        type="staff",
    )


@pytest.fixture
def mock_admin_user_hanoi():
    return UserRead(
        id=1,
        username="test_admin",
        staff_code="SD001",
        first_name="Test",
        last_name="Admin",
        date_of_birth=date(1990, 1, 1),
        join_date=date(2023, 1, 1),
        location=Location.HANOI,
        status=Status.ACTIVE,
        is_first_login=False,
        type="admin",
    )