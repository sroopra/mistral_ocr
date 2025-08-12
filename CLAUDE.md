# Claude Instructions for mistral_ocr

## Project Overview
Modern Python project using uv for dependency management and virtual environment handling. This is an OCR project leveraging Mistral AI capabilities.

## Development Environment

### Core Tools
- **uv**: Modern Python package and project manager (replaces pip, pipenv, poetry)
- **ruff**: Fast Python linter and formatter
- **mypy**: Static type checker

## Project Commands

### Environment Setup
```bash
# Install dependencies
uv sync

# Add new dependency
uv add <package>

# Add development dependency  
uv add --dev <package>

# Remove dependency
uv remove <package>
```

### Development Workflow
```bash
# Run the application
uv run python -m mistral_ocr

# Run with arguments
uv run python -m mistral_ocr --help

# Install and run script
uv run <script-name>
```

### Code Quality
```bash
# Lint with ruff
uv run ruff check .

# Format with ruff
uv run ruff format .

# Type check with mypy
uv run mypy .

# Run all quality checks
uv run ruff check . && uv run ruff format . && uv run mypy .
```

### Testing
```bash
# Run tests
uv run pytest

# Run tests with coverage
uv run pytest --cov=mistral_ocr

# Run specific test file
uv run pytest tests/test_specific.py
```

## Project Structure
```
mistral_ocr/
├── src/
│   └── mistral_ocr/
│       ├── __init__.py
│       ├── __main__.py
│       ├── core/
│       ├── models/
│       └── utils/
├── tests/
├── pyproject.toml
├── uv.lock
├── README.md
└── CLAUDE.md
```

## Configuration Files

### pyproject.toml
The project uses pyproject.toml for all configuration:
- Project metadata and dependencies
- Build system configuration
- Tool configuration (ruff, mypy, pytest)

### Key Configuration Sections
- `[project]`: Package metadata and dependencies
- `[tool.ruff]`: Linting and formatting rules
- `[tool.mypy]`: Type checking configuration
- `[tool.pytest]`: Test configuration

## Development Guidelines

### Code Quality Standards
- **Type Hints**: All functions must have type annotations
- **Linting**: Code must pass ruff checks
- **Formatting**: Use ruff format (no manual formatting)
- **Testing**: Maintain >80% test coverage

### Import Organization
- Standard library imports first
- Third-party imports second  
- Local imports last
- Use absolute imports for src/mistral_ocr modules

### Error Handling
- Use specific exception types
- Provide meaningful error messages
- Log errors appropriately
- Handle edge cases gracefully

## Dependencies Management

### Adding Dependencies
```bash
# Production dependency
uv add requests pillow

# Development dependency
uv add --dev pytest black mypy

# Optional dependency group
uv add --optional ocr tesseract-python
```

### Version Constraints
- Use compatible release operator (~=) for patch updates
- Pin exact versions for critical dependencies
- Keep dependencies minimal and well-maintained

## Environment Variables
Use `.env` files for local development:
```bash
# .env
MISTRAL_API_KEY=your_api_key_here
LOG_LEVEL=INFO
```

## Deployment
```bash
# Build package
uv build

# Install in production
uv sync --frozen

# Run in production
uv run python -m mistral_ocr
```

## Troubleshooting

### Common Issues
- **Import errors**: Ensure you're using `uv run` or activate the virtual environment
- **Dependency conflicts**: Use `uv lock --upgrade` to resolve
- **Type errors**: Run `uv run mypy .` to see detailed type issues

### Debug Mode
```bash
# Run with debug logging
uv run python -m mistral_ocr --debug

# Run with verbose output
uv run python -m mistral_ocr --verbose
```

## CI/CD Integration
```yaml
# GitHub Actions example
- name: Install uv
  uses: astral-sh/setup-uv@v1

- name: Install dependencies  
  run: uv sync

- name: Run tests
  run: uv run pytest

- name: Run linting
  run: uv run ruff check .

- name: Run type checking
  run: uv run mypy .
```