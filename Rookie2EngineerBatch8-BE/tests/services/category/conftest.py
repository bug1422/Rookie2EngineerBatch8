import pytest
from unittest.mock import Mock, patch
from schemas.category import CategoryCreate, CategoryRead
from models.category import Category
from services.category import CategoryService

@pytest.fixture
def mock_category_create():
    return CategoryCreate(
        category_name='Test Category',
        prefix='TC'
    )

@pytest.fixture
def mock_category_read():
    return CategoryRead(
        id=1,
        category_name='Test Category',
        prefix='TC'
    )

@pytest.fixture
def mock_category_model():
    return Category(
        id=1,
        category_name='Test Category',
        prefix='TC',
        id_counter=0
    )

@pytest.fixture
def category_service():
    db = Mock()
    repository = Mock()
    with patch('services.category.CategoryRepository', return_value=repository):
        service = CategoryService(db)
        service.repository = repository
        yield service
