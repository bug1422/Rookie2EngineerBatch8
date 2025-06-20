# Assets Management API

A comprehensive FastAPI-based backend service for managing assets, built with modern Python tools and best practices.

## Features

- RESTful API endpoints for asset management
- JWT-based authentication and authorization
- PostgreSQL database with SQLModel ORM
- Comprehensive test coverage
- Docker containerization
- Automated CI/CD with Azure Pipelines

## Tech Stack

- **Framework**: FastAPI
- **Database**: PostgreSQL
- **ORM**: SQLModel/SQLAlchemy
- **Authentication**: JWT (JSON Web Tokens)
- **Testing**: pytest
- **Documentation**: OpenAPI/Swagger
- **Containerization**: Docker
- **CI/CD**: Azure Pipelines

## Project Structure

```
Rookie2EngineerBatch8-BE/
├── api/                  # API endpoints and routers
│   └── v1/              # API version 1
│       └── endpoints/    # API endpoint handlers
├── controllers/         # Request handlers and business logic
├── core/               # Core application configuration
├── database/           # Database configuration and sessions
├── enums/              # Enumeration types
├── middleware/         # FastAPI middleware components
├── models/             # SQLModel database models
├── repositories/       # Data access layer
├── schemas/            # Pydantic models for request/response
├── services/          # Business logic layer
├── tests/             # Test suite
└── utils/             # Utility functions and helpers
```

## Getting Started

### Prerequisites

- Python 3.8+
- PostgreSQL
- Docker (optional)

### Local Development Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd Rookie2EngineerBatch8-BE
```

2. Create and activate virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# or
.venv\Scripts\activate  # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. Run the application:
```bash
uvicorn main:app --reload
```

### Docker Setup

1. Build and run with Docker Compose:
```bash
docker-compose up --build
```

## API Documentation

Once the application is running, you can access:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Testing

Run tests with pytest:
```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=app tests/

# Run specific test file
pytest tests/unit/test_users.py
```

## Project Components

- **API (api/)**: FastAPI route handlers and endpoint definitions
- **Controllers (controllers/)**: Request handling and response formatting
- **Models (models/)**: Database models using SQLModel
- **Schemas (schemas/)**: Pydantic models for request/response validation
- **Services (services/)**: Business logic implementation
- **Repositories (repositories/)**: Data access layer for database operations
- **Middleware (middleware/)**: Request/response processing middleware
- **Utils (utils/)**: Helper functions and utilities

## Contributing

We follow a Git branching strategy with the following branches:

- `main`: Production-ready code
- `develop`: Main development branch, all features and fixes are merged here first
- `feature/*`: Feature branches for new development (e.g., `feature/user-auth`)
- `release/*`: Release preparation branches (e.g., `release/1.2.0`)
- `hotfix/*`: Emergency fixes for production issues (e.g., `hotfix/login-fix`)

### Development Workflow:

1. Create a new feature branch from `develop`:
```bash
git checkout develop
git checkout -b feature/your-feature-name
```

2. Make your changes and commit them:
```bash
git add .
git commit -m "Description of changes"
```

3. Keep your branch updated with develop:
```bash
git checkout develop
git pull
git checkout feature/your-feature-name
git rebase develop
```

4. Submit a pull request to the `develop` branch

### Release Process:

1. Create a release branch from `develop`:
```bash
git checkout develop
git checkout -b release/version-number
```

2. Prepare release (version bumps, final fixes)
3. Merge to `main` and `develop` when ready
4. Tag the release on `main`

### Hotfix Process:

1. Create hotfix branch from `main`:
```bash
git checkout main
git checkout -b hotfix/issue-description
```

2. Fix the issue
3. Merge to both `main` and `develop`

## Environment Variables

Key environment variables needed in `.env`:

```
# Application
APP_NAME=AssetsManagementAPI
ENVIRONMENT=development
DEBUG=True

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/db_name

# Security
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS
BACKEND_CORS_ORIGINS=["http://localhost:3000"]
```

## Deployment

The project includes Azure Pipelines configuration for CI/CD:

1. Build and test
2. Docker image creation
3. Deployment to target environment

See `azure-pipelines.yml` for detailed configuration.