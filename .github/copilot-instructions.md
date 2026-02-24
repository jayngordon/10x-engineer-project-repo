# GitHub Copilot Instructions for PromptLab

This document contains coding standards, conventions, and patterns to be followed when contributing to the PromptLab project.

## Project Coding Standards
- **Python Version**: Ensure compatibility with Python 3.10+.
- **Typing**: Utilize Python type hints for all functions to improve code readability and maintenance.
- **Documentation**: Every module, class, and function should have docstrings following the [PEP 257](https://www.python.org/dev/peps/pep-0257/) convention.
- **Testing**: Write unit tests for all new features and modifications. Ensure test coverage is maintained.

## Preferred Patterns and Conventions
- **Models**: Use Pydantic models for data validation and serialization. Define them in `models.py`.
- **Utilities**: Any shared functionality across modules should be placed in `utils.py`.
- **Async Programming**: Prefer using asynchronous functions where I/O operations are involved, especially when dealing with API endpoints.
- **API Design**: Follow REST principles. Ensure that all endpoints are well defined and documented in `API_REFERENCE.md`.

## File Naming Conventions
- Use lowercase with underscores for Python scripts and directories, e.g., `api.py`, `models.py`.
- Test files should mirror their corresponding module files with a `test_` prefix, e.g., `test_api.py` for `api.py`.
- Document files are written in uppercase, e.g., `README.md`, `PROJECT_BRIEF.md`.

## Error Handling Approach
- **Exceptions**: Use custom exception classes for API-specific errors. Ensure they inherit from Python's built-in exceptions appropriately.
- **Logging**: Implement logging for all exceptions that are caught and handled, especially at the API level to facilitate debugging.
- **Validation**: Leverage Pydantic's validators to ensure data integrity and provide meaningful feedback on data errors.
