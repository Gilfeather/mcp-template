.PHONY: help install install-dev test lint format check clean pre-commit

help: ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install the package
	pip install -e .

install-dev: ## Install development dependencies
	pip install -e ".[dev]"
	pre-commit install

test: ## Run tests
	pytest

test-cov: ## Run tests with coverage
	pytest --cov=. --cov-report=html --cov-report=term

lint: ## Run linting
	ruff check .

format: ## Format code
	ruff format .

check: ## Run all checks (lint, format, type check)
	ruff check .
	ruff format --check .
	mypy server.py --ignore-missing-imports

fix: ## Fix linting issues
	ruff check --fix .
	ruff format .

clean: ## Clean up build artifacts
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf htmlcov/
	rm -rf .coverage
	find . -type d -name __pycache__ -delete
	find . -type f -name "*.pyc" -delete

pre-commit: ## Run pre-commit hooks
	pre-commit run --all-files

docker-build: ## Build Docker image
	docker build -t company-api-mcp .

docker-run: ## Run Docker container
	docker run -e API_BASE_URL="https://api.example.com" -e API_KEY="your-api-key" company-api-mcp