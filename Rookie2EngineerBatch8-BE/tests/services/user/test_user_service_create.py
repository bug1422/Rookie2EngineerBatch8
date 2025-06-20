from core.exceptions import PermissionDeniedException
import pytest

from enums.user.type import Type
from enums.shared.location import Location

class TestUserCreate:
    def test_create_user_success(self, user_service, mocker, mock_user_create, mock_user_read):
        user_service.repository.create_user.return_value = mock_user_read
        user_service.repository.is_username_exists.return_value = False
        user_service.repository.get_count_all_users.return_value = 0

        mocker.patch("services.user.Generator.generate_username",
                    return_value="testu")
        mocker.patch("services.user.Generator.generate_staff_code",
                    return_value="SD0001")
        mocker.patch("services.user.Generator.generate_password",
                    return_value="123")
        result = user_service.create_user(
            mock_user_create, mock_user_create.location)
        assert result == mock_user_read
 
    @pytest.mark.parametrize(("duplicate_count", "expected_username"), [
        (1, "testu1"),
        (5, "testu5"),
        (17, "testu17"),
        (100, "testu100"),
    ])
    def test_create_user_with_duplicate_username_success(self, duplicate_count, expected_username, user_service, mocker, mock_user_create, mock_user_read):
        user_service.repository.create_user.return_value = mock_user_read
        user_service.repository.is_username_exists.side_effect = [
            True] * duplicate_count+[False]
        user_service.repository.get_count_all_users.return_value = 0
        mocker.patch("services.user.Generator.generate_username",
                     return_value="testu")
        mocker.patch("services.user.Generator.generate_staff_code",
                     return_value="SD0001")
        mocker.patch("services.user.Generator.generate_password",
                     return_value="123")
        user_service.create_user(mock_user_create, Location.HANOI)

        expected_call_count = duplicate_count+1
        assert user_service.repository.is_username_exists.call_count == expected_call_count
        user_service.repository.get_count_all_users.assert_called_once()
        user_service.repository.create_user.assert_called_once()
        user_model_param = user_service.repository.create_user.call_args[0][0]
        assert user_model_param.username == expected_username

    @pytest.mark.parametrize(("user_count", "expected_code"), [
        (7, "SD0008"),
        (123, "SD0124"),
        (295, "SD0296"),
        (10000, "SD10001"),
    ])
    def test_create_user_with_incremental_staff_code_success(self, user_count, expected_code, mocker, user_service, mock_user_create):
        # Don't need to test for return value
        user_service.repository.create_user.return_value = None
        user_service.repository.is_username_exists.return_value = False
        user_service.repository.get_count_all_users.return_value = user_count

        mocker.patch("services.user.Generator.generate_username",
                     return_value="testu")
        mock_generate_staff_code = mocker.patch("services.user.Generator.generate_staff_code",
                                                return_value=f"SD{user_count + 1:04d}")
        mocker.patch("services.user.Generator.generate_password",
                     return_value="123")
        user_service.create_user(mock_user_create, Location.HANOI)
        user_service.repository.is_username_exists.assert_called_once()
        user_service.repository.get_count_all_users.assert_called_once()
        user_service.repository.create_user.assert_called_once()
        user_model_param = user_service.repository.create_user.call_args[0][0]
        assert mock_generate_staff_code.call_args[0][0] == user_count
        assert user_model_param.staff_code == expected_code

    @pytest.mark.parametrize(("user_type", "user_location", "admin_location"), [
        (Type.ADMIN, Location.DANANG, Location.HANOI),
        (Type.ADMIN, Location.HCM, Location.HANOI),
        (Type.ADMIN, Location.HANOI, Location.HANOI),
        (Type.STAFF, Location.HANOI, Location.HANOI),
    ])
    def test_create_user_with_correct_location_success(
            self, user_type, user_location, admin_location, mocker, user_service, mock_user_create, mock_user_read):
        mock_user_create.location = user_location
        user_service.repository.create_user.return_value = mock_user_read
        user_service.repository.is_username_exists.return_value = False
        user_service.repository.get_count_all_users.return_value = 0
        mocker.patch("services.user.UserRepository",
                     return_value=user_service.repository)

        mocker.patch("services.user.Generator.generate_username",
                     return_value="testu")
        mocker.patch("services.user.Generator.generate_staff_code",
                     return_value="SD0001")
        mocker.patch("services.user.Generator.generate_password",
                     return_value="123")
        result = user_service.create_user(mock_user_create, admin_location)

        assert result.username == "testu"
        assert result.staff_code == "SD0001"
        assert result.first_name == "Test"
        assert result.last_name == "User"
        user_service.repository.is_username_exists.assert_called_once()
        user_service.repository.get_count_all_users.assert_called_once()
        user_service.repository.create_user.assert_called_once()
        user_model_param = user_service.repository.create_user.call_args[0][0]
        assert user_model_param.username == "testu"

    @pytest.mark.parametrize(("user_type", "user_location", "admin_location"), [
        (Type.STAFF, Location.DANANG, Location.HANOI),
        (Type.STAFF, Location.HCM, Location.HANOI),
    ])
    def test_create_user_with_incorrect_location_error(
        self, user_type, user_location, admin_location, user_service, mock_user_create
    ):
        mock_user_create.location = user_location
        mock_user_create.type = user_type
        user_service.repository.create_user.return_value = mock_user_create
        user_service.repository.is_username_exists.return_value = False
        user_service.repository.get_count_all_users.return_value = 0

        with pytest.raises(PermissionDeniedException) as exc_info:
            user_service.create_user(mock_user_create, admin_location)
        assert "You are not allowed to create a staff in other location" in str(
            exc_info.value)
