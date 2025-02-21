# Makefile for FastAPI Service

# Variables
PYTHON = python
VENV_ACTIVATE = call venvScriptsactivate
HOST = 0.0.0.0
PORT = 8000

# Installation of dependencies
install
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install -r requirements.txt

# Code Quality Checks (Linting)
check
	$(VENV_ACTIVATE) && python -m flake8 . --max-line-length=100

# Build and Test API Locally
build
	$(VENV_ACTIVATE) && uvicorn appapp --host $(HOST) --port $(PORT) --reload

# API Testing
test_api
	$(VENV_ACTIVATE) && pytest tests

# Deploy API
deploy
	$(VENV_ACTIVATE) && uvicorn appapp --host $(HOST) --port $(PORT) --reload

# Full CICD Pipeline
all install check build test_api deploy
