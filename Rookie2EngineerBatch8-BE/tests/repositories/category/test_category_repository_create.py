import pytest
from models.category import Category

class TestCategoryCreate:
    def test_create_category_calls_add_commit_refresh(self, category_repository, mock_category_create):
        category_data = Category(
            **mock_category_create.model_dump(),
            id_counter=0
        )
        result = category_repository.create_category(category_data)
        category_repository.db.add.assert_called_once_with(category_data)
        category_repository.db.commit.assert_called_once()
        category_repository.db.refresh.assert_called_once_with(category_data)
        assert result == category_data

    def test_create_category_with_all_fields(self, category_repository, mock_category_create):
        category_data = Category(
            **mock_category_create.model_dump(),
            id_counter=1  # Simulating a specific value for testing
        )
        result = category_repository.create_category(category_data)
        category_repository.db.add.assert_called_once_with(category_data)
        category_repository.db.commit.assert_called_once()
        category_repository.db.refresh.assert_called_once_with(category_data)
        assert result == category_data  # Verify the result matches input

    def test_create_category_commit_exception(self, category_repository, mock_category_create):
        category_data = Category(
            **mock_category_create.model_dump(),
            id_counter=0
        )
        category_repository.db.commit.side_effect = Exception("DB commit failed")
        with pytest.raises(Exception) as exc_info:
            category_repository.create_category(category_data)
        assert "DB commit failed" in str(exc_info.value)

    

    def test_get_next_id_counter_increments(self, category_repository):
        mock_last_category = Category(id=2, category_name="Test", prefix="TC10", id_counter=10)
        category_repository.db.query().filter().order_by().first.return_value = mock_last_category
        next_counter = category_repository.get_next_id_counter("TC")
        assert next_counter == 11

    def test_get_next_id_counter_starts_at_one(self, category_repository):
        category_repository.db.query().filter().order_by().first.return_value = None
        next_counter = category_repository.get_next_id_counter("TC")
        assert next_counter == 1
