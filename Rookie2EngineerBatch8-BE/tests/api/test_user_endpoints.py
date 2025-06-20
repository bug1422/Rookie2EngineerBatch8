import pytest
from fastapi import status
from core.exceptions import NotFoundException
from tests.test_data.test_data import Id
from schemas.user import UserRead
from datetime import date
from enums.user.gender import Gender
from enums.user.type import Type
from enums.shared.location import Location
from enums.user.status import Status


# Unit tests with mocks
def test_get_user_by_id_success_with_mock(client, mocker):
    """Test getting a user by ID when the user exists using mocks."""
    # Arrange
    user_id = 1
    mock_user = UserRead(
        id=user_id,
        username="testuser",
        staff_code="SD0001",
        first_name="Test",
        last_name="User",
        date_of_birth=date(1990, 1, 1),
        join_date=date(2023, 1, 1),
        gender=Gender.MALE,
        type=Type.STAFF,
        location=Location.HANOI,
        status=Status.ACTIVE,
        is_first_login=True,
    )

    # Mock the UserService.read_user method
    mocker.patch("services.user.UserService.read_user", return_value=mock_user)

    # Act
    response = client.get(f"/api/v1/users/{user_id}")

    # Assert
    assert response.status_code == status.HTTP_200_OK

    user_data = response.json()
    assert user_data["id"] == user_id
    assert user_data["username"] == mock_user.username
    assert user_data["staff_code"] == mock_user.staff_code
    assert user_data["first_name"] == mock_user.first_name
    assert user_data["last_name"] == mock_user.last_name


def test_get_user_by_id_not_found_with_mock(client, mocker):
    """Test getting a user by ID when the user does not exist using mocks."""
    # Arrange
    non_existent_id = Id.USER_ID_NOT_EXIST.value

    # Mock the UserService.read_user method to raise NotFoundException
    mocker.patch(
        "services.user.UserService.read_user",
        side_effect=NotFoundException(
            f"User with id {non_existent_id} not found"),
    )

    # Act
    response = client.get(f"/api/v1/users/{non_existent_id}")

    # Assert
    assert response.status_code == status.HTTP_404_NOT_FOUND

    error_data = response.json()
    assert "detail" in error_data
    assert f"User with id {non_existent_id} not found" in error_data["detail"]


@pytest.mark.parametrize(("invalid_id", "expected_status_code"), [
    ("invalid", status.HTTP_422_UNPROCESSABLE_ENTITY),
    ("abc123", status.HTTP_422_UNPROCESSABLE_ENTITY),
    ("", status.HTTP_404_NOT_FOUND)
])
def test_get_user_by_id_invalid_id_with_mock(client, invalid_id, expected_status_code):
    """Test getting a user by ID with various invalid ID formats."""
    # Act
    response = client.get(f"/api/v1/users/{invalid_id}")

    # Assert
    assert response.status_code == expected_status_code


def test_get_multiple_users_by_id_with_mock(client, mocker):
    """Test getting multiple users by their IDs using mocks."""
    # Arrange
    mock_users = [
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

    # Create a side_effect function that returns the appropriate user based on ID
    def mock_read_user(user_id):
        for user in mock_users:
            if user.id == user_id:
                return user
        raise NotFoundException(f"User with id {user_id} not found")

    # Mock the UserService.read_user method
    mock_read_user_patch = mocker.patch(
        "services.user.UserService.read_user", side_effect=mock_read_user
    )

    # Act & Assert
    for user in mock_users:
        response = client.get(f"/api/v1/users/{user.id}")

        # Check that the response status code is 200 OK
        assert response.status_code == status.HTTP_200_OK

        # Check that the response data matches the user
        user_data = response.json()
        assert user_data["id"] == user.id
        assert user_data["username"] == user.username
        assert user_data["staff_code"] == user.staff_code
        assert user_data["first_name"] == user.first_name
        assert user_data["last_name"] == user.last_name

    # Verify the mock was called correctly
    assert mock_read_user_patch.call_count == len(mock_users)


# Keep the original integration tests for comparison, but rename them
def test_get_user_by_id_success_integration(client, multiple_users):
    """Integration test getting a user by ID when the user exists."""
    # Get the first user from the multiple_users fixture
    user = multiple_users[0]

    # Make a GET request to the endpoint
    response = client.get(f"/api/v1/users/{user.id}")

    # Check that the response status code is 200 OK
    assert response.status_code == status.HTTP_200_OK

    # Check that the response data matches the user
    user_data = response.json()
    assert user_data["id"] == user.id
    assert user_data["username"] == user.username
    assert user_data["staff_code"] == user.staff_code
    assert user_data["first_name"] == user.first_name
    assert user_data["last_name"] == user.last_name


def test_get_user_by_id_not_found_integration(client, sample_user):
    """Integration test getting a user by ID when the user does not exist."""
    # Use a non-existent user ID
    non_existent_id = Id.USER_ID_NOT_EXIST.value

    # Make a GET request to the endpoint
    response = client.get(f"/api/v1/users/{non_existent_id}")

    # Check that the response status code is 404 Not Found
    assert response.status_code == status.HTTP_404_NOT_FOUND

    # Check that the response contains an error message
    error_data = response.json()
    assert "detail" in error_data
    assert f"User with id {non_existent_id} not found" in error_data["detail"]


def test_get_user_by_id_invalid_id_integration(client):
    """Integration test getting a user by ID with an invalid ID format."""
    # Use an invalid ID format (string instead of integer)
    invalid_id = "invalid"

    # Make a GET request to the endpoint
    response = client.get(f"/api/v1/users/{invalid_id}")

    # Check that the response status code is 422 Unprocessable Entity
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_get_multiple_users_by_id_integration(client, multiple_users):
    """Integration test getting multiple users by their IDs."""
    # Test getting each user from the multiple_users fixture
    for user in multiple_users:
        response = client.get(f"/api/v1/users/{user.id}")

        # Check that the response status code is 200 OK
        assert response.status_code == status.HTTP_200_OK

        # Check that the response data matches the user
        user_data = response.json()
        assert user_data["id"] == user.id
        assert user_data["username"] == user.username
        assert user_data["staff_code"] == user.staff_code
        assert user_data["first_name"] == user.first_name
        assert user_data["last_name"] == user.last_name
