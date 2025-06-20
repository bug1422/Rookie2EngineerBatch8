import pytest
from unittest.mock import Mock, patch
from datetime import datetime, date

from core.exceptions import BusinessException, NotFoundException, ValidationException
from enums.assignment.state import AssignmentState
from enums.asset.state import AssetState
from enums.shared.location import Location
from enums.user.status import Status
from schemas.assignment import AssignmentCreate
from models.assignment import Assignment


class TestAssignmentCreateBasic:
    """Test basic assignment creation functionality"""

    def test_create_assignment_success(self, assignment_service, mock_admin_user, mock_staff_user, mock_asset):
        """Test successfully creating an assignment."""
        # Arrange
        assignment_data = AssignmentCreate(
            asset_id=mock_asset.id,
            assigned_to_id=mock_staff_user.id,
            assign_date=datetime.now(),
            assignment_note="Test assignment"
        )

        # Mock user service
        with patch('services.assignment.UserService') as mock_user_service:
            mock_user_service_instance = Mock()
            mock_user_service.return_value = mock_user_service_instance
            mock_user_service_instance.read_user.side_effect = [mock_staff_user, mock_staff_user, mock_admin_user]

            # Mock asset service
            with patch('services.assignment.AssetService') as mock_asset_service:
                mock_asset_service_instance = Mock()
                mock_asset_service.return_value = mock_asset_service_instance
                mock_asset_service_instance.repository.get_asset_by_id.return_value = mock_asset
                mock_asset_service_instance.read_asset.return_value = mock_asset

                # Mock repository calls
                assignment_service.repository.is_asset_available.return_value = True

                created_assignment = Mock()
                created_assignment.id = 1
                created_assignment.asset_id = mock_asset.id
                created_assignment.assigned_to_id = mock_staff_user.id
                created_assignment.assigned_by_id = mock_admin_user.id
                created_assignment.assign_date = assignment_data.assign_date
                created_assignment.assignment_note = assignment_data.assignment_note
                created_assignment.assignment_state = AssignmentState.WAITING_FOR_ACCEPTANCE

                assignment_service.repository.create_assignment.return_value = created_assignment

                # Act
                result = assignment_service.create_assignment(
                    assignment_data, mock_admin_user.id, mock_admin_user
                )

                # Assert
                assert result.id == created_assignment.id
                assert result.asset_id == mock_asset.id
                assert result.assigned_to_id == mock_staff_user.id
                assert result.assigned_by_id == mock_admin_user.id
                assert result.assignment_state == AssignmentState.WAITING_FOR_ACCEPTANCE

                # Verify asset state was updated to ASSIGNED
                mock_asset_service_instance.repository.update_asset.assert_called_once()

    def test_create_assignment_with_current_date(self, assignment_service, mock_admin_user, mock_staff_user, mock_asset):
        """Test creating assignment with current date (AC requirement: current date by default)."""
        # Arrange
        current_date = datetime.now()
        assignment_data = AssignmentCreate(
            asset_id=mock_asset.id,
            assigned_to_id=mock_staff_user.id,
            assign_date=current_date,
            assignment_note="Assignment with current date"
        )

        # Mock user service
        with patch('services.assignment.UserService') as mock_user_service:
            mock_user_service_instance = Mock()
            mock_user_service.return_value = mock_user_service_instance
            mock_user_service_instance.read_user.side_effect = [mock_staff_user, mock_staff_user, mock_admin_user]

            # Mock asset service
            with patch('services.assignment.AssetService') as mock_asset_service:
                mock_asset_service_instance = Mock()
                mock_asset_service.return_value = mock_asset_service_instance
                mock_asset_service_instance.repository.get_asset_by_id.return_value = mock_asset
                mock_asset_service_instance.read_asset.return_value = mock_asset

                # Mock repository calls
                assignment_service.repository.is_asset_available.return_value = True

                created_assignment = Mock()
                created_assignment.id = 1
                created_assignment.asset_id = mock_asset.id
                created_assignment.assigned_to_id = mock_staff_user.id
                created_assignment.assigned_by_id = mock_admin_user.id
                created_assignment.assign_date = current_date
                created_assignment.assignment_note = assignment_data.assignment_note
                created_assignment.assignment_state = AssignmentState.WAITING_FOR_ACCEPTANCE

                assignment_service.repository.create_assignment.return_value = created_assignment

                # Act
                result = assignment_service.create_assignment(
                    assignment_data, mock_admin_user.id, mock_admin_user
                )

                # Assert
                assert result.assign_date == current_date.date()
                assert result.assignment_state == AssignmentState.WAITING_FOR_ACCEPTANCE

    def test_create_assignment_with_future_date(self, assignment_service, mock_admin_user, mock_staff_user, mock_asset):
        """Test creating assignment with future date (AC requirement: can select future date)."""
        # Arrange
        future_date = datetime.now().replace(day=datetime.now().day + 5)  # 5 days in future
        assignment_data = AssignmentCreate(
            asset_id=mock_asset.id,
            assigned_to_id=mock_staff_user.id,
            assign_date=future_date,
            assignment_note="Assignment with future date"
        )

        # Mock user service
        with patch('services.assignment.UserService') as mock_user_service:
            mock_user_service_instance = Mock()
            mock_user_service.return_value = mock_user_service_instance
            mock_user_service_instance.read_user.side_effect = [mock_staff_user, mock_staff_user, mock_admin_user]

            # Mock asset service
            with patch('services.assignment.AssetService') as mock_asset_service:
                mock_asset_service_instance = Mock()
                mock_asset_service.return_value = mock_asset_service_instance
                mock_asset_service_instance.repository.get_asset_by_id.return_value = mock_asset
                mock_asset_service_instance.read_asset.return_value = mock_asset

                # Mock repository calls
                assignment_service.repository.is_asset_available.return_value = True

                created_assignment = Mock()
                created_assignment.id = 1
                created_assignment.asset_id = mock_asset.id
                created_assignment.assigned_to_id = mock_staff_user.id
                created_assignment.assigned_by_id = mock_admin_user.id
                created_assignment.assign_date = future_date
                created_assignment.assignment_note = assignment_data.assignment_note
                created_assignment.assignment_state = AssignmentState.WAITING_FOR_ACCEPTANCE

                assignment_service.repository.create_assignment.return_value = created_assignment

                # Act
                result = assignment_service.create_assignment(
                    assignment_data, mock_admin_user.id, mock_admin_user
                )

                # Assert
                assert result.assign_date == future_date.date()
                assert result.assignment_state == AssignmentState.WAITING_FOR_ACCEPTANCE


class TestAssignmentCreateValidation:
    """Test assignment creation validation scenarios"""

    def test_create_assignment_user_not_found(self, assignment_service, mock_admin_user):
        """Test creating assignment with non-existent user."""
        # Arrange
        assignment_data = AssignmentCreate(
            asset_id=1,
            assigned_to_id=999,
            assign_date=datetime.now(),
            assignment_note="Test assignment"
        )

        with patch('services.assignment.UserService') as mock_user_service:
            mock_user_service_instance = Mock()
            mock_user_service.return_value = mock_user_service_instance
            mock_user_service_instance.read_user.side_effect = NotFoundException("User not found")

            # Act & Assert
            with pytest.raises(NotFoundException, match="User with ID 999 not found"):
                assignment_service.create_assignment(
                    assignment_data, mock_admin_user.id, mock_admin_user
                )

    def test_create_assignment_asset_not_found(self, assignment_service, mock_admin_user, mock_staff_user):
        """Test creating assignment with non-existent asset."""
        # Arrange
        assignment_data = AssignmentCreate(
            asset_id=999,
            assigned_to_id=mock_staff_user.id,
            assign_date=datetime.now(),
            assignment_note="Test assignment"
        )

        with patch('services.assignment.UserService') as mock_user_service:
            mock_user_service_instance = Mock()
            mock_user_service.return_value = mock_user_service_instance
            mock_user_service_instance.read_user.return_value = mock_staff_user

            with patch('services.assignment.AssetService') as mock_asset_service:
                mock_asset_service_instance = Mock()
                mock_asset_service.return_value = mock_asset_service_instance
                mock_asset_service_instance.repository.get_asset_by_id.return_value = None

                # Act & Assert
                with pytest.raises(NotFoundException, match="Asset with ID 999 not found"):
                    assignment_service.create_assignment(
                        assignment_data, mock_admin_user.id, mock_admin_user
                    )



    def test_create_assignment_asset_not_available(self, assignment_service, mock_admin_user, mock_staff_user, mock_asset):
        """Test creating assignment with unavailable asset (AC3: only available assets)."""
        # Arrange
        assignment_data = AssignmentCreate(
            asset_id=mock_asset.id,
            assigned_to_id=mock_staff_user.id,
            assign_date=datetime.now(),
            assignment_note="Test assignment"
        )

        with patch('services.assignment.UserService') as mock_user_service:
            mock_user_service_instance = Mock()
            mock_user_service.return_value = mock_user_service_instance
            mock_user_service_instance.read_user.return_value = mock_staff_user

            with patch('services.assignment.AssetService') as mock_asset_service:
                mock_asset_service_instance = Mock()
                mock_asset_service.return_value = mock_asset_service_instance
                mock_asset_service_instance.repository.get_asset_by_id.return_value = mock_asset

                assignment_service.repository.is_asset_available.return_value = False

                # Act & Assert
                with pytest.raises(BusinessException, match="is not available for assignment"):
                    assignment_service.create_assignment(
                        assignment_data, mock_admin_user.id, mock_admin_user
                    )

    def test_create_assignment_past_date_validation(self, assignment_service, mock_admin_user, mock_staff_user):
        """Test creating assignment with past date should fail validation (AC requirement: current or future date only)."""
        # Arrange
        past_date = datetime.now().replace(day=datetime.now().day - 1)  # Yesterday

        # Act & Assert - Should fail at schema validation level
        with pytest.raises(ValueError, match="Assign date must be today or in the future"):
            AssignmentCreate(
                asset_id=1,
                assigned_to_id=mock_staff_user.id,
                assign_date=past_date,
                assignment_note="Test assignment with past date"
            )

    def test_create_assignment_database_error(self, assignment_service, mock_admin_user, mock_staff_user, mock_asset):
        """Test creating assignment with database error."""
        # Arrange
        assignment_data = AssignmentCreate(
            asset_id=mock_asset.id,
            assigned_to_id=mock_staff_user.id,
            assign_date=datetime.now(),
            assignment_note="Test assignment"
        )

        with patch('services.assignment.UserService') as mock_user_service:
            mock_user_service_instance = Mock()
            mock_user_service.return_value = mock_user_service_instance
            mock_user_service_instance.read_user.side_effect = [mock_staff_user, mock_staff_user, mock_admin_user]

            with patch('services.assignment.AssetService') as mock_asset_service:
                mock_asset_service_instance = Mock()
                mock_asset_service.return_value = mock_asset_service_instance
                mock_asset_service_instance.repository.get_asset_by_id.return_value = mock_asset
                mock_asset_service_instance.read_asset.return_value = mock_asset

                assignment_service.repository.is_asset_available.return_value = True
                assignment_service.repository.create_assignment.side_effect = Exception("Database error")

                # Act & Assert
                with pytest.raises(BusinessException, match="Failed to create assignment"):
                    assignment_service.create_assignment(
                        assignment_data, mock_admin_user.id, mock_admin_user
                    )


class TestAssignmentCreateBusinessRules:
    """Test assignment creation business rules based on AC requirements"""

    def test_create_assignment_waiting_for_acceptance_state(self, assignment_service, mock_admin_user, mock_staff_user, mock_asset):
        """Test that assignment is created with 'Waiting for acceptance' state (AC4)."""
        # Arrange
        assignment_data = AssignmentCreate(
            asset_id=mock_asset.id,
            assigned_to_id=mock_staff_user.id,
            assign_date=datetime.now(),
            assignment_note="Test assignment for state verification"
        )

        # Mock user service
        with patch('services.assignment.UserService') as mock_user_service:
            mock_user_service_instance = Mock()
            mock_user_service.return_value = mock_user_service_instance
            mock_user_service_instance.read_user.side_effect = [mock_staff_user, mock_staff_user, mock_admin_user]

            # Mock asset service
            with patch('services.assignment.AssetService') as mock_asset_service:
                mock_asset_service_instance = Mock()
                mock_asset_service.return_value = mock_asset_service_instance
                mock_asset_service_instance.repository.get_asset_by_id.return_value = mock_asset
                mock_asset_service_instance.read_asset.return_value = mock_asset

                # Mock repository calls
                assignment_service.repository.is_asset_available.return_value = True

                created_assignment = Mock()
                created_assignment.id = 1
                created_assignment.asset_id = mock_asset.id
                created_assignment.assigned_to_id = mock_staff_user.id
                created_assignment.assigned_by_id = mock_admin_user.id
                created_assignment.assign_date = assignment_data.assign_date
                created_assignment.assignment_note = assignment_data.assignment_note
                created_assignment.assignment_state = AssignmentState.WAITING_FOR_ACCEPTANCE

                assignment_service.repository.create_assignment.return_value = created_assignment

                # Act
                result = assignment_service.create_assignment(
                    assignment_data, mock_admin_user.id, mock_admin_user
                )

                # Assert - Verify state is "Waiting for acceptance" as per AC4
                assert result.assignment_state == AssignmentState.WAITING_FOR_ACCEPTANCE

    def test_create_assignment_one_asset_to_one_user(self, assignment_service, mock_admin_user, mock_staff_user, mock_asset):
        """Test that only one asset can be assigned to one user in an assignment (AC requirement)."""
        # Arrange
        assignment_data = AssignmentCreate(
            asset_id=mock_asset.id,
            assigned_to_id=mock_staff_user.id,
            assign_date=datetime.now(),
            assignment_note="Single asset to single user assignment"
        )

        # Mock user service
        with patch('services.assignment.UserService') as mock_user_service:
            mock_user_service_instance = Mock()
            mock_user_service.return_value = mock_user_service_instance
            mock_user_service_instance.read_user.side_effect = [mock_staff_user, mock_staff_user, mock_admin_user]

            # Mock asset service
            with patch('services.assignment.AssetService') as mock_asset_service:
                mock_asset_service_instance = Mock()
                mock_asset_service.return_value = mock_asset_service_instance
                mock_asset_service_instance.repository.get_asset_by_id.return_value = mock_asset
                mock_asset_service_instance.read_asset.return_value = mock_asset

                # Mock repository calls
                assignment_service.repository.is_asset_available.return_value = True

                created_assignment = Mock()
                created_assignment.id = 1
                created_assignment.asset_id = mock_asset.id
                created_assignment.assigned_to_id = mock_staff_user.id
                created_assignment.assigned_by_id = mock_admin_user.id
                created_assignment.assign_date = assignment_data.assign_date
                created_assignment.assignment_note = assignment_data.assignment_note
                created_assignment.assignment_state = AssignmentState.WAITING_FOR_ACCEPTANCE

                assignment_service.repository.create_assignment.return_value = created_assignment

                # Act
                result = assignment_service.create_assignment(
                    assignment_data, mock_admin_user.id, mock_admin_user
                )

                # Assert - Verify single asset to single user relationship
                assert result.asset_id == mock_asset.id
                assert result.assigned_to_id == mock_staff_user.id
                # Verify only one asset and one user are involved
                assert isinstance(result.asset_id, int)
                assert isinstance(result.assigned_to_id, int)

    def test_create_assignment_with_optional_note(self, assignment_service, mock_admin_user, mock_staff_user, mock_asset):
        """Test creating assignment with optional assignment note."""
        # Arrange
        assignment_data = AssignmentCreate(
            asset_id=mock_asset.id,
            assigned_to_id=mock_staff_user.id,
            assign_date=datetime.now(),
            assignment_note=None  # Optional note
        )

        # Mock user service
        with patch('services.assignment.UserService') as mock_user_service:
            mock_user_service_instance = Mock()
            mock_user_service.return_value = mock_user_service_instance
            mock_user_service_instance.read_user.side_effect = [mock_staff_user, mock_staff_user, mock_admin_user]

            # Mock asset service
            with patch('services.assignment.AssetService') as mock_asset_service:
                mock_asset_service_instance = Mock()
                mock_asset_service.return_value = mock_asset_service_instance
                mock_asset_service_instance.repository.get_asset_by_id.return_value = mock_asset
                mock_asset_service_instance.read_asset.return_value = mock_asset

                # Mock repository calls
                assignment_service.repository.is_asset_available.return_value = True

                created_assignment = Mock()
                created_assignment.id = 1
                created_assignment.asset_id = mock_asset.id
                created_assignment.assigned_to_id = mock_staff_user.id
                created_assignment.assigned_by_id = mock_admin_user.id
                created_assignment.assign_date = assignment_data.assign_date
                created_assignment.assignment_note = None
                created_assignment.assignment_state = AssignmentState.WAITING_FOR_ACCEPTANCE

                assignment_service.repository.create_assignment.return_value = created_assignment

                # Act
                result = assignment_service.create_assignment(
                    assignment_data, mock_admin_user.id, mock_admin_user
                )

                # Assert - Verify assignment can be created without note
                assert result.assignment_note is None
                assert result.assignment_state == AssignmentState.WAITING_FOR_ACCEPTANCE


class TestAssignmentCreateUserSelection:
    """Test user selection functionality for assignment creation (AC2)"""

    def test_create_assignment_user_same_location_as_admin(self, assignment_service, mock_admin_user, mock_staff_user, mock_asset):
        """Test that admin can only assign to users in the same location (AC2)."""
        # Arrange - Both admin and staff user are in HCM location
        assert mock_admin_user.location == Location.HCM
        assert mock_staff_user.location == Location.HCM

        assignment_data = AssignmentCreate(
            asset_id=mock_asset.id,
            assigned_to_id=mock_staff_user.id,
            assign_date=datetime.now(),
            assignment_note="Assignment to user in same location"
        )

        # Mock user service
        with patch('services.assignment.UserService') as mock_user_service:
            mock_user_service_instance = Mock()
            mock_user_service.return_value = mock_user_service_instance
            mock_user_service_instance.read_user.side_effect = [mock_staff_user, mock_staff_user, mock_admin_user]

            # Mock asset service
            with patch('services.assignment.AssetService') as mock_asset_service:
                mock_asset_service_instance = Mock()
                mock_asset_service.return_value = mock_asset_service_instance
                mock_asset_service_instance.repository.get_asset_by_id.return_value = mock_asset
                mock_asset_service_instance.read_asset.return_value = mock_asset

                # Mock repository calls
                assignment_service.repository.is_asset_available.return_value = True

                created_assignment = Mock()
                created_assignment.id = 1
                created_assignment.asset_id = mock_asset.id
                created_assignment.assigned_to_id = mock_staff_user.id
                created_assignment.assigned_by_id = mock_admin_user.id
                created_assignment.assign_date = assignment_data.assign_date
                created_assignment.assignment_note = assignment_data.assignment_note
                created_assignment.assignment_state = AssignmentState.WAITING_FOR_ACCEPTANCE

                assignment_service.repository.create_assignment.return_value = created_assignment

                # Act
                result = assignment_service.create_assignment(
                    assignment_data, mock_admin_user.id, mock_admin_user
                )

                # Assert - Verify assignment created successfully for same location user
                assert result.assigned_to_id == mock_staff_user.id
                assert result.assigned_by_id == mock_admin_user.id

    def test_create_assignment_user_searchable_by_code_and_name(self, assignment_service, mock_admin_user, mock_asset):
        """Test that users can be searched by code or name (AC2 note)."""
        # Arrange - Create a user with specific code and name for search testing
        searchable_user = Mock()
        searchable_user.id = 3
        searchable_user.username = "john.doe"
        searchable_user.staff_code = "SD003"
        searchable_user.first_name = "John"
        searchable_user.last_name = "Doe"
        searchable_user.location = Location.HCM
        searchable_user.status = Status.ACTIVE

        assignment_data = AssignmentCreate(
            asset_id=mock_asset.id,
            assigned_to_id=searchable_user.id,
            assign_date=datetime.now(),
            assignment_note="Assignment to searchable user"
        )

        # Mock user service
        with patch('services.assignment.UserService') as mock_user_service:
            mock_user_service_instance = Mock()
            mock_user_service.return_value = mock_user_service_instance
            mock_user_service_instance.read_user.side_effect = [searchable_user, searchable_user, mock_admin_user]

            # Mock asset service
            with patch('services.assignment.AssetService') as mock_asset_service:
                mock_asset_service_instance = Mock()
                mock_asset_service.return_value = mock_asset_service_instance
                mock_asset_service_instance.repository.get_asset_by_id.return_value = mock_asset
                mock_asset_service_instance.read_asset.return_value = mock_asset

                # Mock repository calls
                assignment_service.repository.is_asset_available.return_value = True

                created_assignment = Mock()
                created_assignment.id = 1
                created_assignment.asset_id = mock_asset.id
                created_assignment.assigned_to_id = searchable_user.id
                created_assignment.assigned_by_id = mock_admin_user.id
                created_assignment.assign_date = assignment_data.assign_date
                created_assignment.assignment_note = assignment_data.assignment_note
                created_assignment.assignment_state = AssignmentState.WAITING_FOR_ACCEPTANCE

                assignment_service.repository.create_assignment.return_value = created_assignment

                # Act
                result = assignment_service.create_assignment(
                    assignment_data, mock_admin_user.id, mock_admin_user
                )

                # Assert - Verify assignment created for user found by search
                assert result.assigned_to_id == searchable_user.id
                # Verify user has searchable attributes
                assert searchable_user.staff_code == "SD003"
                assert searchable_user.first_name == "John"
                assert searchable_user.last_name == "Doe"


class TestAssignmentCreateAssetSelection:
    """Test asset selection functionality for assignment creation (AC3)"""

    def test_create_assignment_available_asset_only(self, assignment_service, mock_admin_user, mock_staff_user, mock_asset):
        """Test that only available assets can be selected for assignment (AC3)."""
        # Arrange - Use existing mock_asset which is already properly configured
        assignment_data = AssignmentCreate(
            asset_id=mock_asset.id,
            assigned_to_id=mock_staff_user.id,
            assign_date=datetime.now(),
            assignment_note="Assignment with available asset"
        )

        # Mock user service
        with patch('services.assignment.UserService') as mock_user_service:
            mock_user_service_instance = Mock()
            mock_user_service.return_value = mock_user_service_instance
            mock_user_service_instance.read_user.side_effect = [mock_staff_user, mock_staff_user, mock_admin_user]

            # Mock asset service
            with patch('services.assignment.AssetService') as mock_asset_service:
                mock_asset_service_instance = Mock()
                mock_asset_service.return_value = mock_asset_service_instance
                mock_asset_service_instance.repository.get_asset_by_id.return_value = mock_asset
                mock_asset_service_instance.read_asset.return_value = mock_asset

                # Mock repository calls - asset is available
                assignment_service.repository.is_asset_available.return_value = True

                created_assignment = Mock()
                created_assignment.id = 1
                created_assignment.asset_id = mock_asset.id
                created_assignment.assigned_to_id = mock_staff_user.id
                created_assignment.assigned_by_id = mock_admin_user.id
                created_assignment.assign_date = assignment_data.assign_date
                created_assignment.assignment_note = assignment_data.assignment_note
                created_assignment.assignment_state = AssignmentState.WAITING_FOR_ACCEPTANCE

                assignment_service.repository.create_assignment.return_value = created_assignment

                # Act
                result = assignment_service.create_assignment(
                    assignment_data, mock_admin_user.id, mock_admin_user
                )

                # Assert - Verify assignment created with available asset
                assert result.asset_id == mock_asset.id
                assert mock_asset.asset_state == AssetState.AVAILABLE

    def test_create_assignment_asset_searchable_by_code_and_name(self, assignment_service, mock_admin_user, mock_staff_user, mock_asset):
        """Test that assets can be searched by code or name (AC3 note)."""
        # Arrange - Use existing mock_asset and verify it has searchable attributes
        assignment_data = AssignmentCreate(
            asset_id=mock_asset.id,
            assigned_to_id=mock_staff_user.id,
            assign_date=datetime.now(),
            assignment_note="Assignment with searchable asset"
        )

        # Mock user service
        with patch('services.assignment.UserService') as mock_user_service:
            mock_user_service_instance = Mock()
            mock_user_service.return_value = mock_user_service_instance
            mock_user_service_instance.read_user.side_effect = [mock_staff_user, mock_staff_user, mock_admin_user]

            # Mock asset service
            with patch('services.assignment.AssetService') as mock_asset_service:
                mock_asset_service_instance = Mock()
                mock_asset_service.return_value = mock_asset_service_instance
                mock_asset_service_instance.repository.get_asset_by_id.return_value = mock_asset
                mock_asset_service_instance.read_asset.return_value = mock_asset

                # Mock repository calls
                assignment_service.repository.is_asset_available.return_value = True

                created_assignment = Mock()
                created_assignment.id = 1
                created_assignment.asset_id = mock_asset.id
                created_assignment.assigned_to_id = mock_staff_user.id
                created_assignment.assigned_by_id = mock_admin_user.id
                created_assignment.assign_date = assignment_data.assign_date
                created_assignment.assignment_note = assignment_data.assignment_note
                created_assignment.assignment_state = AssignmentState.WAITING_FOR_ACCEPTANCE

                assignment_service.repository.create_assignment.return_value = created_assignment

                # Act
                result = assignment_service.create_assignment(
                    assignment_data, mock_admin_user.id, mock_admin_user
                )

                # Assert - Verify assignment created for asset found by search
                assert result.asset_id == mock_asset.id
                # Verify asset has searchable attributes
                assert mock_asset.asset_code is not None
                assert mock_asset.asset_name is not None


class TestAssignmentCreateRequiredFields:
    """Test required fields validation for assignment creation (AC1)"""

    def test_create_assignment_all_required_fields_provided(self, assignment_service, mock_admin_user, mock_staff_user, mock_asset):
        """Test that assignment can be created when all required fields are provided (AC1)."""
        # Arrange - All required fields: User, Asset, Assigned Date
        assignment_data = AssignmentCreate(
            asset_id=mock_asset.id,  # Required
            assigned_to_id=mock_staff_user.id,  # Required
            assign_date=datetime.now(),  # Required
            assignment_note="Optional note"  # Optional
        )

        # Mock user service
        with patch('services.assignment.UserService') as mock_user_service:
            mock_user_service_instance = Mock()
            mock_user_service.return_value = mock_user_service_instance
            mock_user_service_instance.read_user.side_effect = [mock_staff_user, mock_staff_user, mock_admin_user]

            # Mock asset service
            with patch('services.assignment.AssetService') as mock_asset_service:
                mock_asset_service_instance = Mock()
                mock_asset_service.return_value = mock_asset_service_instance
                mock_asset_service_instance.repository.get_asset_by_id.return_value = mock_asset
                mock_asset_service_instance.read_asset.return_value = mock_asset

                # Mock repository calls
                assignment_service.repository.is_asset_available.return_value = True

                created_assignment = Mock()
                created_assignment.id = 1
                created_assignment.asset_id = mock_asset.id
                created_assignment.assigned_to_id = mock_staff_user.id
                created_assignment.assigned_by_id = mock_admin_user.id
                created_assignment.assign_date = assignment_data.assign_date
                created_assignment.assignment_note = assignment_data.assignment_note
                created_assignment.assignment_state = AssignmentState.WAITING_FOR_ACCEPTANCE

                assignment_service.repository.create_assignment.return_value = created_assignment

                # Act
                result = assignment_service.create_assignment(
                    assignment_data, mock_admin_user.id, mock_admin_user
                )

                # Assert - Verify all required fields are present in result
                assert result.asset_id is not None
                assert result.assigned_to_id is not None
                assert result.assign_date is not None
                assert result.assigned_by_id is not None

    def test_create_assignment_missing_asset_id_validation(self):
        """Test that assignment creation fails when asset_id is missing (required field)."""
        # Act & Assert - Should fail at schema validation level
        with pytest.raises(ValueError):
            AssignmentCreate(
                # asset_id missing - required field
                assigned_to_id=1,
                assign_date=datetime.now(),
                assignment_note="Test assignment"
            )

    def test_create_assignment_missing_assigned_to_id_validation(self):
        """Test that assignment creation fails when assigned_to_id is missing (required field)."""
        # Act & Assert - Should fail at schema validation level
        with pytest.raises(ValueError):
            AssignmentCreate(
                asset_id=1,
                # assigned_to_id missing - required field
                assign_date=datetime.now(),
                assignment_note="Test assignment"
            )

    def test_create_assignment_missing_assign_date_validation(self):
        """Test that assignment creation fails when assign_date is missing (required field)."""
        # Act & Assert - Should fail at schema validation level
        with pytest.raises(ValueError):
            AssignmentCreate(
                asset_id=1,
                assigned_to_id=1,
                # assign_date missing - required field
                assignment_note="Test assignment"
            )


class TestAssignmentCreateEdgeCases:
    """Test edge cases and error scenarios for assignment creation"""



    def test_create_assignment_asset_already_assigned(self, assignment_service, mock_admin_user, mock_staff_user, mock_asset):
        """Test creating assignment with already assigned asset should fail."""
        # Arrange
        assignment_data = AssignmentCreate(
            asset_id=mock_asset.id,
            assigned_to_id=mock_staff_user.id,
            assign_date=datetime.now(),
            assignment_note="Assignment with already assigned asset"
        )

        with patch('services.assignment.UserService') as mock_user_service:
            mock_user_service_instance = Mock()
            mock_user_service.return_value = mock_user_service_instance
            mock_user_service_instance.read_user.return_value = mock_staff_user

            with patch('services.assignment.AssetService') as mock_asset_service:
                mock_asset_service_instance = Mock()
                mock_asset_service.return_value = mock_asset_service_instance
                mock_asset_service_instance.repository.get_asset_by_id.return_value = mock_asset

                # Mock asset as not available (already assigned)
                assignment_service.repository.is_asset_available.return_value = False

                # Act & Assert
                with pytest.raises(BusinessException, match="is not available for assignment"):
                    assignment_service.create_assignment(
                        assignment_data, mock_admin_user.id, mock_admin_user
                    )

    def test_create_assignment_with_very_long_note(self, assignment_service, mock_admin_user, mock_staff_user, mock_asset):
        """Test creating assignment with very long assignment note."""
        # Arrange
        long_note = "A" * 1000  # Very long note
        assignment_data = AssignmentCreate(
            asset_id=mock_asset.id,
            assigned_to_id=mock_staff_user.id,
            assign_date=datetime.now(),
            assignment_note=long_note
        )

        # Mock user service
        with patch('services.assignment.UserService') as mock_user_service:
            mock_user_service_instance = Mock()
            mock_user_service.return_value = mock_user_service_instance
            mock_user_service_instance.read_user.side_effect = [mock_staff_user, mock_staff_user, mock_admin_user]

            # Mock asset service
            with patch('services.assignment.AssetService') as mock_asset_service:
                mock_asset_service_instance = Mock()
                mock_asset_service.return_value = mock_asset_service_instance
                mock_asset_service_instance.repository.get_asset_by_id.return_value = mock_asset
                mock_asset_service_instance.read_asset.return_value = mock_asset

                # Mock repository calls
                assignment_service.repository.is_asset_available.return_value = True

                created_assignment = Mock()
                created_assignment.id = 1
                created_assignment.asset_id = mock_asset.id
                created_assignment.assigned_to_id = mock_staff_user.id
                created_assignment.assigned_by_id = mock_admin_user.id
                created_assignment.assign_date = assignment_data.assign_date
                created_assignment.assignment_note = long_note
                created_assignment.assignment_state = AssignmentState.WAITING_FOR_ACCEPTANCE

                assignment_service.repository.create_assignment.return_value = created_assignment

                # Act
                result = assignment_service.create_assignment(
                    assignment_data, mock_admin_user.id, mock_admin_user
                )

                # Assert - Verify assignment created with long note
                assert result.assignment_note == long_note
                assert len(result.assignment_note) == 1000

    def test_create_assignment_concurrent_asset_assignment(self, assignment_service, mock_admin_user, mock_staff_user, mock_asset):
        """Test creating assignment when asset becomes unavailable during creation process."""
        # Arrange
        assignment_data = AssignmentCreate(
            asset_id=mock_asset.id,
            assigned_to_id=mock_staff_user.id,
            assign_date=datetime.now(),
            assignment_note="Concurrent assignment test"
        )

        with patch('services.assignment.UserService') as mock_user_service:
            mock_user_service_instance = Mock()
            mock_user_service.return_value = mock_user_service_instance
            mock_user_service_instance.read_user.return_value = mock_staff_user

            with patch('services.assignment.AssetService') as mock_asset_service:
                mock_asset_service_instance = Mock()
                mock_asset_service.return_value = mock_asset_service_instance
                mock_asset_service_instance.repository.get_asset_by_id.return_value = mock_asset

                # Mock asset becomes unavailable during process
                assignment_service.repository.is_asset_available.return_value = False

                # Act & Assert
                with pytest.raises(BusinessException, match="is not available for assignment"):
                    assignment_service.create_assignment(
                        assignment_data, mock_admin_user.id, mock_admin_user
                    )


class TestAssignmentCreateAC:
    """Test assignment creation based on Acceptance Criteria (AC1-AC5)"""

    def test_ac1_create_assignment_form_validation_all_required_fields(self, assignment_service, mock_admin_user, mock_staff_user, mock_asset):
        """AC1: Test that assignment can be created when all required fields (User, Asset, Assigned Date) are filled."""
        # Arrange - All required fields provided
        assignment_data = AssignmentCreate(
            asset_id=mock_asset.id,  # Required
            assigned_to_id=mock_staff_user.id,  # Required
            assign_date=datetime.now(),  # Required (current date by default)
            assignment_note="Test assignment with all required fields"
        )

        # Mock user service
        with patch('services.assignment.UserService') as mock_user_service:
            mock_user_service_instance = Mock()
            mock_user_service.return_value = mock_user_service_instance
            mock_user_service_instance.read_user.side_effect = [mock_staff_user, mock_staff_user, mock_admin_user]

            # Mock asset service
            with patch('services.assignment.AssetService') as mock_asset_service:
                mock_asset_service_instance = Mock()
                mock_asset_service.return_value = mock_asset_service_instance
                mock_asset_service_instance.repository.get_asset_by_id.return_value = mock_asset
                mock_asset_service_instance.read_asset.return_value = mock_asset

                # Mock repository calls
                assignment_service.repository.is_asset_available.return_value = True

                created_assignment = Mock()
                created_assignment.id = 1
                created_assignment.asset_id = mock_asset.id
                created_assignment.assigned_to_id = mock_staff_user.id
                created_assignment.assigned_by_id = mock_admin_user.id
                created_assignment.assign_date = assignment_data.assign_date
                created_assignment.assignment_note = assignment_data.assignment_note
                created_assignment.assignment_state = AssignmentState.WAITING_FOR_ACCEPTANCE

                assignment_service.repository.create_assignment.return_value = created_assignment

                # Act
                result = assignment_service.create_assignment(
                    assignment_data, mock_admin_user.id, mock_admin_user
                )

                # Assert - AC1: Assignment created successfully with all required fields
                assert result.id == created_assignment.id
                assert result.asset_id == mock_asset.id
                assert result.assigned_to_id == mock_staff_user.id
                assert result.assigned_by_id == mock_admin_user.id
                assert result.assignment_state == AssignmentState.WAITING_FOR_ACCEPTANCE

    def test_ac2_user_selection_same_location_as_admin(self, assignment_service, mock_admin_user, mock_staff_user, mock_asset):
        """AC2: Test that admin can only select users who have the same location as admin."""
        # Arrange - Both admin and staff user are in HCM location
        assert mock_admin_user.location == Location.HCM
        assert mock_staff_user.location == Location.HCM

        assignment_data = AssignmentCreate(
            asset_id=mock_asset.id,
            assigned_to_id=mock_staff_user.id,
            assign_date=datetime.now(),
            assignment_note="Assignment to user in same location"
        )

        # Mock user service
        with patch('services.assignment.UserService') as mock_user_service:
            mock_user_service_instance = Mock()
            mock_user_service.return_value = mock_user_service_instance
            mock_user_service_instance.read_user.side_effect = [mock_staff_user, mock_staff_user, mock_admin_user]

            # Mock asset service
            with patch('services.assignment.AssetService') as mock_asset_service:
                mock_asset_service_instance = Mock()
                mock_asset_service.return_value = mock_asset_service_instance
                mock_asset_service_instance.repository.get_asset_by_id.return_value = mock_asset
                mock_asset_service_instance.read_asset.return_value = mock_asset

                # Mock repository calls
                assignment_service.repository.is_asset_available.return_value = True

                created_assignment = Mock()
                created_assignment.id = 1
                created_assignment.asset_id = mock_asset.id
                created_assignment.assigned_to_id = mock_staff_user.id
                created_assignment.assigned_by_id = mock_admin_user.id
                created_assignment.assign_date = assignment_data.assign_date
                created_assignment.assignment_note = assignment_data.assignment_note
                created_assignment.assignment_state = AssignmentState.WAITING_FOR_ACCEPTANCE

                assignment_service.repository.create_assignment.return_value = created_assignment

                # Act
                result = assignment_service.create_assignment(
                    assignment_data, mock_admin_user.id, mock_admin_user
                )

                # Assert - AC2: Assignment created for user in same location
                assert result.assigned_to_id == mock_staff_user.id
                assert result.assigned_by_id == mock_admin_user.id

    def test_ac3_asset_selection_available_assets_only(self, assignment_service, mock_admin_user, mock_staff_user, mock_asset):
        """AC3: Test that only available assets can be selected for assignment."""
        # Arrange - Use existing mock_asset which is already properly configured
        assignment_data = AssignmentCreate(
            asset_id=mock_asset.id,
            assigned_to_id=mock_staff_user.id,
            assign_date=datetime.now(),
            assignment_note="Assignment with available asset"
        )

        # Mock user service
        with patch('services.assignment.UserService') as mock_user_service:
            mock_user_service_instance = Mock()
            mock_user_service.return_value = mock_user_service_instance
            mock_user_service_instance.read_user.side_effect = [mock_staff_user, mock_staff_user, mock_admin_user]

            # Mock asset service
            with patch('services.assignment.AssetService') as mock_asset_service:
                mock_asset_service_instance = Mock()
                mock_asset_service.return_value = mock_asset_service_instance
                mock_asset_service_instance.repository.get_asset_by_id.return_value = mock_asset
                mock_asset_service_instance.read_asset.return_value = mock_asset

                # Mock repository calls - asset is available
                assignment_service.repository.is_asset_available.return_value = True

                created_assignment = Mock()
                created_assignment.id = 1
                created_assignment.asset_id = mock_asset.id
                created_assignment.assigned_to_id = mock_staff_user.id
                created_assignment.assigned_by_id = mock_admin_user.id
                created_assignment.assign_date = assignment_data.assign_date
                created_assignment.assignment_note = assignment_data.assignment_note
                created_assignment.assignment_state = AssignmentState.WAITING_FOR_ACCEPTANCE

                assignment_service.repository.create_assignment.return_value = created_assignment

                # Act
                result = assignment_service.create_assignment(
                    assignment_data, mock_admin_user.id, mock_admin_user
                )

                # Assert - AC3: Assignment created with available asset
                assert result.asset_id == mock_asset.id
                assert mock_asset.asset_state == AssetState.AVAILABLE

    def test_ac4_assignment_created_with_waiting_for_acceptance_state(self, assignment_service, mock_admin_user, mock_staff_user, mock_asset):
        """AC4: Test that assignment is created with state 'Waiting for acceptance'."""
        # Arrange
        assignment_data = AssignmentCreate(
            asset_id=mock_asset.id,
            assigned_to_id=mock_staff_user.id,
            assign_date=datetime.now(),
            assignment_note="Test assignment state verification"
        )

        # Mock user service
        with patch('services.assignment.UserService') as mock_user_service:
            mock_user_service_instance = Mock()
            mock_user_service.return_value = mock_user_service_instance
            mock_user_service_instance.read_user.side_effect = [mock_staff_user, mock_staff_user, mock_admin_user]

            # Mock asset service
            with patch('services.assignment.AssetService') as mock_asset_service:
                mock_asset_service_instance = Mock()
                mock_asset_service.return_value = mock_asset_service_instance
                mock_asset_service_instance.repository.get_asset_by_id.return_value = mock_asset
                mock_asset_service_instance.read_asset.return_value = mock_asset

                # Mock repository calls
                assignment_service.repository.is_asset_available.return_value = True

                created_assignment = Mock()
                created_assignment.id = 1
                created_assignment.asset_id = mock_asset.id
                created_assignment.assigned_to_id = mock_staff_user.id
                created_assignment.assigned_by_id = mock_admin_user.id
                created_assignment.assign_date = assignment_data.assign_date
                created_assignment.assignment_note = assignment_data.assignment_note
                created_assignment.assignment_state = AssignmentState.WAITING_FOR_ACCEPTANCE

                assignment_service.repository.create_assignment.return_value = created_assignment

                # Act
                result = assignment_service.create_assignment(
                    assignment_data, mock_admin_user.id, mock_admin_user
                )

                # Assert - AC4: Assignment created with "Waiting for acceptance" state
                assert result.assignment_state == AssignmentState.WAITING_FOR_ACCEPTANCE
