# Contributing to Company API MCP Server Template

Thank you for your interest in contributing to this project!

## Development Setup

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -e .
   ```
4. Copy `.env.example` to `.env` and configure your API settings

## Making Changes

1. Create a new branch for your feature/fix
2. Make your changes
3. Test your changes thoroughly
4. Update documentation if necessary
5. Submit a pull request

## Code Style

- Follow PEP 8 for Python code
- Use type hints where appropriate
- Add docstrings for all functions and classes
- Keep functions focused and small

## Testing

Before submitting a pull request:

1. Test the MCP server with a real API
2. Verify all tools work as expected
3. Check error handling scenarios

## Submitting Issues

When submitting issues, please include:

- Clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Environment details (Python version, OS, etc.)