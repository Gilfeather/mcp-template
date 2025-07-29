# Contributing to Company API MCP Server Template

Thank you for your interest in contributing to this project!

## Development Setup

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/your-username/company-api-mcp.git
   cd company-api-mcp
   ```
3. Create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```
4. Install dependencies:
   ```bash
   make install-dev
   ```
5. Copy `.env.example` to `.env` and configure your API settings
6. Set up pre-commit hooks:
   ```bash
   pre-commit install
   ```

## Pull Request Workflow

1. Create a new branch from `main`:
   ```bash
   git checkout main
   git pull origin main
   git checkout -b feature/your-feature-name
   ```

2. Make your changes following our coding standards

3. Test your changes:
   ```bash
   # Run all checks
   make check
   
   # Run tests
   make test
   
   # Test imports
   python -c "import server; print('Success')"
   
   # Run main module
   python main.py
   ```

4. Commit your changes:
   ```bash
   git add .
   git commit -m "feat: add your feature description"
   ```

5. Push to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```

6. Create a Pull Request on GitHub

## Commit Message Convention

We follow conventional commits:
- `feat:` - New features
- `fix:` - Bug fixes
- `docs:` - Documentation changes
- `style:` - Code style changes
- `refactor:` - Code refactoring
- `test:` - Adding tests
- `chore:` - Maintenance tasks

## Code Style

- Follow PEP 8 for Python code (enforced by ruff)
- Use type hints where appropriate
- Add docstrings for all functions and classes
- Keep functions focused and small
- Use ruff for linting and formatting
- Run `make check` before submitting PRs
- Maximum line length: 88 characters (enforced by ruff)
- Use meaningful variable and function names

## Testing Guidelines

Before submitting a pull request:

1. Run `make check` to ensure code quality
2. Run `make test` to verify all tests pass
3. Ensure all imports work correctly
4. Test the MCP server with a mock API if possible
5. Verify all tools work as expected
6. Check error handling scenarios
7. Run `pre-commit run --all-files` to check hooks

## Documentation

- Update README.md if adding new features
- Add docstrings to new functions
- Update examples if changing tool signatures
- Include usage examples for new tools

## Issue Templates

Use the provided issue templates:
- Bug reports: Include reproduction steps and environment details
- Feature requests: Describe the use case and proposed solution

## Review Process

1. All PRs require at least one review
2. CI checks must pass
3. Documentation must be updated for new features
4. Breaking changes require discussion in issues first

## Getting Help

- Open an issue for questions
- Check existing issues and PRs
- Review the README for setup instructions