# Project: AI Agent Test

A Python FastAPI project for testing AI agent development pipelines.

## Language and Framework

- **Language:** Python
- **Framework:** FastAPI
- **Package Manager:** pip

## Getting Started

### Prerequisites

- Python 3.10+
- pip

### Installation

```bash
pip install -r requirements.txt
```

### Running Tests

```bash
pytest tests/ -v --cov=. --cov-report=term-missing
```

## Project Structure

```
ai-agent-test/
├── src/                    # Application source code
│   ├── main.py             # FastAPI app entry point
│   ├── routes/             # API route handlers
│   ├── services/           # Business logic
│   └── models/             # Pydantic models
├── tests/                  # Test files
│   ├── test_*.py           # Unit and integration tests
├── requirements.txt        # Python dependencies
└── README.md
```

## Architecture Rules

- Route handlers must be thin — delegate to services
- Services contain business logic — no HTTP concerns
- Models use Pydantic for validation
- No business logic in route handlers

## Naming Conventions

| Element | Convention | Example |
|---------|-----------|---------|
| Functions | snake_case | `get_user` |
| Classes | PascalCase | `UserService` |
| Files | snake_case | `user_service.py` |
| Constants | UPPER_SNAKE | `MAX_RETRIES` |
| Branches | feature/ or fix/ | `feature/add-search` |
| Commits | Conventional Commits | `feat: add search endpoint` |

## Code Quality Tools

| Tool | Command | Purpose |
|------|---------|---------|
| Linter | `ruff check .` | Code linting |
| Formatter | `ruff format .` | Code formatting |
| Type Check | `mypy .` | Type checking |
| Tests | `pytest tests/ -v` | Run tests |
| Coverage | `pytest --cov=. --cov-report=term-missing` | Test coverage |

## Testing Conventions

- **Test Framework:** pytest
- **Test Location:** `tests/` directory
- **Test Naming:** `test_<function_name>`
- **Minimum Coverage:** 80%

## Team Rules

- Always use structured logging (never `print()`)
- Always validate API input with Pydantic models
- Never commit `.env` files
- All API endpoints must have type hints on request/response
- Use `httpx.AsyncClient` for async test clients
