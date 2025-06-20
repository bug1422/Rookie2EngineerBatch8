import pytest
from datetime import date
from unittest.mock import Mock

from core.exceptions import PermissionDeniedException, AuthenticationException
from enums.user.type import Type
from enums.user.gender import Gender
from enums.shared.location import Location
from schemas.user import UserUpdate


class TestUserEdit:
    def test_edit_user_success_with_all_fields(self, user_service, mock_user_read, mock_admin_user):
        user_update = UserUpdate(
            date_of_birth=date(1988, 12, 23),
            join_date=date(2022, 1, 17),
            type=Type.STAFF,
            gender=Gender.FEMALE,
            location=mock_admin_user.location
        )
        
        updated_user = mock_user_read.model_copy(deep=True)
        for field, value in user_update.model_dump(exclude_unset=True).items():
            setattr(updated_user, field, value)
        
        user_service.repository.edit_user.return_value = updated_user
        
        result = user_service.edit_user(mock_user_read.id, user_update, mock_admin_user.location)
        
        assert result.date_of_birth == user_update.date_of_birth
        assert result.join_date == user_update.join_date
        assert result.type == user_update.type
        assert result.gender == user_update.gender
        assert result.location == user_update.location
        
        user_service.repository.edit_user.assert_called_once_with(mock_user_read.id, user_update)

    def test_edit_user_not_found(self, user_service, mock_admin_user):
        user_update = UserUpdate(
            date_of_birth=date(1990, 1, 1),
            join_date=date(2023, 1, 2),
            gender=Gender.FEMALE
        )
        user_service.repository.edit_user.return_value = None
        
        with pytest.raises(AuthenticationException, match="User not found"):
            user_service.edit_user(999, user_update, mock_admin_user.location)
        
        user_service.repository.edit_user.assert_called_once_with(999, user_update)

    @pytest.mark.parametrize("field_name,field_value,extra_fields", [
        ("gender", Gender.FEMALE, {"date_of_birth": date(1990, 1, 1), "join_date": date(2023, 1, 2)}),
        ("type", Type.ADMIN, {"date_of_birth": date(1990, 1, 1), "join_date": date(2023, 1, 2)}),
        ("location", Location.HCM, {"date_of_birth": date(1990, 1, 1), "join_date": date(2023, 1, 2)}),
    ])
    def test_edit_user_individual_fields_simple(self, field_name, field_value, extra_fields, user_service, mock_user_read, mock_admin_user):
        user_update_data = {field_name: field_value, **extra_fields}
        user_update = UserUpdate(**user_update_data)
        
        updated_user = mock_user_read.model_copy(deep=True)
        setattr(updated_user, field_name, field_value)
        
        user_service.repository.edit_user.return_value = updated_user
        
        result = user_service.edit_user(mock_user_read.id, user_update, mock_admin_user.location)
        
        assert getattr(result, field_name) == field_value
        user_service.repository.edit_user.assert_called_once_with(mock_user_read.id, user_update)

    def test_edit_user_date_of_birth_only(self, user_service, mock_user_read, mock_admin_user):
        mock_user_read.join_date = date(2023, 6, 12)
        
        user_update = UserUpdate(
            date_of_birth=date(1992, 6, 15),
            join_date=date(2023, 6, 12)
        )
        
        updated_user = mock_user_read.model_copy(deep=True)
        updated_user.date_of_birth = user_update.date_of_birth
        
        user_service.repository.edit_user.return_value = updated_user
        
        result = user_service.edit_user(mock_user_read.id, user_update, mock_admin_user.location)
        
        assert result.date_of_birth == user_update.date_of_birth
        user_service.repository.edit_user.assert_called_once_with(mock_user_read.id, user_update)

    def test_edit_user_join_date_only(self, user_service, mock_user_read, mock_admin_user):
        mock_user_read.date_of_birth = date(1990, 1, 1)
        
        user_update = UserUpdate(
            date_of_birth=date(1990, 1, 1),
            join_date=date(2023, 3, 20)
        )
        
        updated_user = mock_user_read.model_copy(deep=True)
        updated_user.join_date = user_update.join_date
        
        user_service.repository.edit_user.return_value = updated_user
        
        result = user_service.edit_user(mock_user_read.id, user_update, mock_admin_user.location)
        
        assert result.join_date == user_update.join_date
        user_service.repository.edit_user.assert_called_once_with(mock_user_read.id, user_update)

    def test_edit_user_workflow_complete(self, user_service, mock_user_read, mock_admin_user):
        # Arrange
        mock_user_read.location = mock_admin_user.location
        
        user_update = UserUpdate(
            date_of_birth=date(1987, 9, 5),
            gender=Gender.FEMALE,
            join_date=date(2022, 11, 28),
            type=Type.STAFF,
            location=mock_admin_user.location
        )
        
        updated_user = mock_user_read.model_copy(deep=True)
        updated_user.date_of_birth = user_update.date_of_birth
        updated_user.gender = user_update.gender
        updated_user.join_date = user_update.join_date
        updated_user.type = user_update.type
        updated_user.location = user_update.location
        
        user_service.repository.edit_user.return_value = updated_user
        
        # Act
        result = user_service.edit_user(mock_user_read.id, user_update, mock_admin_user.location)
        
        # Assert
        assert result.date_of_birth == user_update.date_of_birth
        assert result.gender == user_update.gender
        assert result.join_date == user_update.join_date
        assert result.type == user_update.type
        
        user_service.repository.edit_user.assert_called_once_with(mock_user_read.id, user_update)
        
        assert result is not None

    def test_edit_user_staff_location_permission_denied(self, user_service, mock_user_read, mock_admin_user):
        user_update = UserUpdate(
            date_of_birth=date(1990, 1, 1),
            join_date=date(2023, 1, 2),
            type=Type.STAFF,
            location=Location.DANANG
        )
        
        with pytest.raises(PermissionDeniedException, match="You are not allowed to edit a staff in other location"):
            user_service.edit_user(mock_user_read.id, user_update, mock_admin_user.location)

    def test_edit_user_admin_different_location_allowed(self, user_service, mock_user_read, mock_admin_user):
        user_update = UserUpdate(
            date_of_birth=date(1990, 1, 1),
            join_date=date(2023, 1, 2),
            type=Type.ADMIN,
            location=Location.DANANG
        )
        
        updated_user = mock_user_read.model_copy(deep=True)
        updated_user.type = user_update.type
        updated_user.location = user_update.location
        
        user_service.repository.edit_user.return_value = updated_user
        
        result = user_service.edit_user(mock_user_read.id, user_update, mock_admin_user.location)
        
        assert result.type == Type.ADMIN
        assert result.location == Location.DANANG
