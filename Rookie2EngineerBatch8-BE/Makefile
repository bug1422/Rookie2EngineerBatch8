.PHONY: help install run test clean env docker-build docker-run docker-stop docker-logs docker-clean

# Default target
help:
	@echo "Available commands:"
	@echo "  make install        Install project dependencies"
	@echo "  make run            Run the FastAPI application"
	@echo "  make test           Run tests"
	@echo "  make clean          Remove temporary files and caches"
	@echo "  make env            Create .env file from .env.example if it doesn't exist"
	@echo "  make docker-build   Build Docker images"
	@echo "  make docker-run     Run application using Docker Compose"
	@echo "  make docker-stop    Stop Docker Compose services"
	@echo "  make docker-logs    View logs from Docker Compose services"
	@echo "  make docker-clean   Remove Docker Compose services, networks, and volumes"

# Environment setup
VENV_DIR := .venv
PYTHON := $(VENV_DIR)/bin/python
PIP := $(VENV_DIR)/bin/pip

# Create .env file from example if it doesn't exist
env:
	@if [ ! -f .env ]; then \
		echo "Creating .env file from .env.example..."; \
		cp .env.example .env; \
	else \
		echo ".env file already exists."; \
	fi

# Install dependencies
install: $(VENV_DIR)/touchfile
$(VENV_DIR)/touchfile: requirements.txt
	@if [ ! -d "$(VENV_DIR)" ]; then \
		echo "Creating virtual environment..."; \
		python3 -m venv $(VENV_DIR); \
	fi
	$(PIP) install -r requirements.txt
	@touch $(VENV_DIR)/touchfile
	@echo "Dependencies installed."

# Run the application
run: env
	$(PYTHON) -m uvicorn main:app --host 0.0.0.0 --reload

# Run tests
test: env
	$(PYTHON) -m pytest

# Clean up temporary files
clean:
	@echo "Cleaning up..."
	find . -type f -name '*.py[co]' -delete
	find . -type d -name '__pycache__' -delete
	rm -rf build/ dist/ *.egg-info/ .cache .pytest_cache/ htmlcov/ .DS_Store

# Docker commands
docker-build:
	@echo "Building Docker images..."
	docker compose build

docker-run: env
	@echo "Starting Docker containers..."
	docker compose up -d

docker-stop:
	@echo "Stopping Docker containers..."
	docker compose stop

docker-logs:
	@echo "Showing Docker logs..."
	docker compose logs -f

docker-clean:
	@echo "Cleaning up Docker resources..."
	docker compose down -v --remove-orphans