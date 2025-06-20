import pytest
from models.user import User

class TestUserCreate:
    def test_create_user_calls_add_commit_refresh(self,user_repository,mock_user_create):
        user_data = User(
            **mock_user_create.model_dump(),
            staff_code="SD001",
            username="test_user"
        )
        result = user_repository.create_user(user_data)
        user_repository.db.add.assert_called_once_with(user_data)
        user_repository.db.commit.assert_called_once()
        user_repository.db.refresh.assert_called_once_with(user_data)
        assert result == user_data