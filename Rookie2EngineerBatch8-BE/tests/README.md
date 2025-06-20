# Tests

This directory contains all test files for the application. The tests are organized by type and follow pytest conventions.

## Structure

```
tests/
├── unit/                  # Unit tests
│   ├── test_models.py
│   ├── test_services.py
│   └── test_repositories.py
├── integration/          # Integration tests
│   ├── test_api.py
│   └── test_database.py
├── e2e/                 # End-to-end tests
│   └── test_flows.py
├── fixtures/            # Test fixtures
│   ├── user.py
│   └── database.py
└── conftest.py         # Shared pytest configuration
```

## Running Tests

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=app tests/

# Run specific test file
pytest tests/unit/test_users.py

# Run tests matching a pattern
pytest -k "user"

# Run tests with detailed output
pytest -v

# Run tests and stop on first failure
pytest -x

# Run tests with print statements
pytest -s
```

## Running User Endpoint Tests

To run the tests for the user endpoint, including the 'get user by ID' tests, use:

```bash
# Run all user endpoint tests
pytest tests/unit/endpoints/test_user.py -v

# Run specific test for get user by ID
pytest tests/unit/endpoints/test_user.py::test_get_user_by_id_success -v

# Run with coverage report
pytest tests/unit/endpoints/test_user.py --cov=api.v1.endpoints.user
```

These tests validate the functionality of:
1. Successfully retrieving a user by ID
2. Handling non-existent user IDs (should return 404)
3. Handling invalid ID formats (should return 422)

## Running User Service Tests

```bash
# Run user service tests
pytest tests/unit/services/test_user_service.py -v
```

These tests verify that:
1. The service correctly retrieves a user by ID
2. The service raises a NotFoundException when a user isn't found

## Writing Tests

### Unit Test Example

```python
import pytest
from datetime import datetime
from models.user import User
from schemas.user import UserCreate
from services.user import UserService

def test_create_user():
    # Arrange
    user_data = UserCreate(
        email="test@example.com",
        password="password123",
        full_name="Test User"
    )
    
    # Act
    user = UserService().create_user(user_data)
    
    # Assert
    assert user.email == user_data.email
    assert user.full_name == user_data.full_name
    assert user.hashed_password != user_data.password
```

### Integration Test Example

```python
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_user_api():
    # Arrange
    user_data = {
        "email": "test@example.com",
        "password": "password123",
        "full_name": "Test User"
    }
    
    # Act
    response = client.post("/api/v1/users/", json=user_data)
    
    # Assert
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == user_data["email"]
    assert data["full_name"] == user_data["full_name"]
    assert "id" in data
```

## Fixtures

### Database Fixture Example

```python
# conftest.py
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.postgres import get_session
from models.base import Base

@pytest.fixture(scope="session")
def engine():
    return create_engine("postgresql://postgres:postgres@localhost:5432/test_db")

@pytest.fixture(scope="session")
def tables(engine):
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)

@pytest.fixture
def db_session(engine, tables):
    connection = engine.connect()
    transaction = connection.begin()
    session = sessionmaker(bind=connection)()
    
    yield session
    
    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture
def client(db_session):
    app.dependency_overrides[get_session] = lambda: db_session
    with TestClient(app) as client:
        yield client
```

### Data Fixtures Example

```python
# fixtures/user.py
import pytest
from models.user import User
from services.auth import get_password_hash

@pytest.fixture
def test_user(db_session):
    user = User(
        email="test@example.com",
        hashed_password=get_password_hash("password123"),
        full_name="Test User"
    )
    db_session.add(user)
    db_session.commit()
    return user

@pytest.fixture
def test_superuser(db_session):
    user = User(
        email="admin@example.com",
        hashed_password=get_password_hash("admin123"),
        full_name="Admin User",
        is_superuser=True
    )
    db_session.add(user)
    db_session.commit()
    return user
```

## Mocking Example

```python
from unittest.mock import Mock, patch
import pytest
from services.email import EmailService

@pytest.fixture
def mock_email_service():
    with patch("services.email.send_email") as mock:
        yield mock

def test_send_welcome_email(mock_email_service):
    # Arrange
    email_service = EmailService()
    user_email = "test@example.com"
    
    # Act
    email_service.send_welcome_email(user_email)
    
    # Assert
    mock_email_service.assert_called_once_with(
        to=user_email,
        subject="Welcome!",
        template="welcome_email.html"
    )
```

## Testing Async Code

```python
import pytest
import asyncio
from httpx import AsyncClient
from main import app

@pytest.mark.asyncio
async def test_async_endpoint():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/api/v1/users/")
        assert response.status_code == 200

@pytest.mark.asyncio
async def test_async_service():
    # Arrange
    service = AsyncService()
    
    # Act
    result = await service.process_data()
    
    # Assert
    assert result is not None
```

## Test Coverage

To generate a coverage report:

```bash
# Generate coverage report
pytest --cov=app --cov-report=html tests/

# Open the report
open htmlcov/index.html
```

## Best Practices

1. Follow the AAA pattern:
   - Arrange: Set up test data and conditions
   - Act: Execute the code being tested
   - Assert: Verify the results

2. Use meaningful test names:
```python
def test_user_creation_with_valid_data():
    pass

def test_user_creation_fails_with_invalid_email():
    pass
```

3. Test edge cases and error conditions:
```python
def test_division_by_zero_raises_error():
    with pytest.raises(ZeroDivisionError):
        calculate_ratio(10, 0)
```

4. Use parametrized tests for multiple scenarios:
```python
@pytest.mark.parametrize("email,password,expected", [
    ("test@example.com", "short", False),
    ("invalid-email", "password123", False),
    ("test@example.com", "password123", True),
])
def test_user_validation(email, password, expected):
    assert validate_user_input(email, password) == expected
```

5. Clean up test data:
```python
def test_file_operations(tmp_path):
    # Create temporary file
    test_file = tmp_path / "test.txt"
    test_file.write_text("test content")
    
    # Test operations
    assert process_file(test_file) == "PROCESSED"
    
    # Clean up
    test_file.unlink()
```
