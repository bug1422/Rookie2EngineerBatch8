# User Endpoint Tests

This directory contains tests for the User endpoints, services, and repositories.

## Test Structure

The tests are organized into three levels:

1. **API Tests**: Test the HTTP endpoints directly using the FastAPI TestClient
2. **Service Tests**: Test the service layer methods
3. **Repository Tests**: Test the repository layer methods

## Running the Tests

### Running All Tests

```bash
# From the project root directory
python -m pytest
```

### Running Specific Test Files

```bash
# Run all user endpoint tests
python -m pytest tests/api/test_user_endpoints.py

# Run all user service tests
python -m pytest tests/services/test_user_service.py

# Run all user repository tests
python -m pytest tests/repositories/test_user_repository.py
```

### Running Specific Test Functions

```bash
# Run a specific test function
python -m pytest tests/api/test_user_endpoints.py::test_get_user_by_id_success
```

## Test Database

The tests use an in-memory SQLite database that is created and destroyed for each test session. The database is populated with test data using fixtures defined in `conftest.py`.

### Available Fixtures

- `test_engine`: SQLite in-memory engine for testing (session-scoped)
- `test_session`: Clean database session for each test (function-scoped)
- `client`: FastAPI TestClient with overridden database session
- `user_repository`: UserRepository instance for testing
- `user_service`: UserService instance for testing
- `sample_user`: A single user for basic tests
- `multiple_users`: Multiple users with different attributes for more comprehensive tests

## Test Data

The `multiple_users` fixture creates 5 different users with various attributes:

1. John Doe (STAFF, HANOI) - Username: "johnd1", Staff Code: unique UUID-based code
2. Jane Doe (ADMIN, HCM) - Username: "janed2", Staff Code: unique UUID-based code
3. Bob Smith (STAFF, DANANG, DISABLED) - Username: "bobs3", Staff Code: unique UUID-based code
4. Alice Jones (STAFF, HANOI) - Username: "alicej4", Staff Code: unique UUID-based code
5. Charlie Brown (ADMIN, HCM) - Username: "charlieb5", Staff Code: unique UUID-based code

All users have the default password "123456".

The usernames are generated according to the rule: lowercase first name + first letter of each word in the lowercase last name + a suffix to ensure uniqueness.
The staff codes are generated as "SD" + a random UUID fragment to ensure uniqueness.

These users can be used to test different scenarios in the get user by id endpoint.
