from fastapi import status
from core.exceptions import PermissionDeniedException
import pytest

from enums.user.type import Type
from enums.shared.location import Location

class TestUserCreate:
    def test_create_user_success(self, client, mocker, mock_user_create, mock_user_read):
        mocker.patch("services.user.UserService.create_user", return_value=mock_user_read)
        user_data = mock_user_create.model_dump_json()
        
        response = client.post("/v1/users/",json=user_data)
        assert response.status_code == status.HTTP_201_CREATED
        response_data = response.json()
        assert response_data["first_name"] == user_data["first_name"]
        assert response_data["last_name"] == user_data["last_name"]
        assert response_data["date_of_birth"] == user_data["date_of_birth"]
        assert response_data["join_date"] == user_data["join_date"]
        assert response_data["type"] == user_data["type"]
        assert response_data["gender"] == user_data["gender"]
        assert response_data["location"] == user_data["location"]

    def test_create_user_invalid_data(self, client):
        invalid_data = {
            "first_name": "",
            "last_name": "",
            "date_of_birth": "invalid-date",
            "join_date": "invalid-state",
            "type": "",
            "gender": "",
            "location": "",
        }
        response = client.post("/v1/users/", json=invalid_data)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        errors = response.json()
        assert "detail" in errors