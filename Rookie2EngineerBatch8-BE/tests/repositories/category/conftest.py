import pytest
from repositories.category import CategoryRepository
from unittest.mock import Mock
from schemas.category import CategoryCreate, CategoryRead

@pytest.fixture
def mock_category_create():
    return CategoryCreate(
        category_name="Test Category",
        prefix="TC"
    )


@pytest.fixture
def mock_category_read():
    return CategoryRead(
        id=1,
        category_name="Test Category",
        prefix="TC"
    )


@pytest.fixture(
    scope="function"
)
def category_repository():
    db = Mock()
    repository = CategoryRepository(db)
    yield repository
