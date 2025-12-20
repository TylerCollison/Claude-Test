# Agent Framework Documentation

## Common Bash Commands
```bash
# Start Redis server locally
docker run -d --name redis-agent -p 6379:6379 redis:alpine

# Build agent container
docker build -t agent-service .

# Run agent with environment variables
docker run -e REDIS_URL=redis://host.docker.internal:6379 -e LOG_LEVEL=debug agent-service

# Run tests
pytest --cov=agents --cov-report=html
```

## Core Files & Utilities
| File | Purpose |
|------|---------|
| `/agents/core/agent_base.py` | Abstract base class for agents |
| `/agents/infrastructure/redis_connector.py` | Redis pub/sub implementation |
| `/agents/core/di_container.py` | Dependency injection container |
| `/agents/infrastructure/config_loader.py` | Configuration management |
| `/agents/services/error_handler.py` | Decorators for error recovery |

Key utility functions:
- `@retry_policy(max_attempts=3)` - Automatic retry decorator
- `@circuit_breaker(failure_threshold=5)` - Circuit breaker pattern
- `structured_logger(context)` - Contextual logger

## Code Style Guidelines
1. **Python**: PEP-8 with Black formatting (line length 100)
2. **Type Hints**: Mandatory for all function signatures
3. **Docstrings**: Google-style with Args/Returns/Raises
4. **Logging**: Use structured logging exclusively
5. **Imports**: Grouped as:
   ```python
   # Standard library
   import os
   import sys

   # Third-party
   import redis

   # Local
   from .config import ConfigLoader
   ```

## Testing Instructions
```bash
# Run all tests with coverage
pytest --cov=agents --cov-report=term-missing

# Test specific module
pytest agents/infrastructure/test_redis_connector.py -v

# Generate HTML coverage report
pytest --cov=agents --cov-report=html
open htmlcov/index.html
```

## Repository Etiquette
- **Branch Naming**: `feature/<short-description>`, `fix/<issue-ref>`
- **Workflow**: Feature branches → PR → Squash Merge
- **Commits**: Conventional commits format:
  ```
  feat: add dead-letter queue support
  fix(redis): handle connection timeout
  docs: update framework overview
  ```
- **Review**: 2 approvals required for main merges

## Developer Environment Setup
1. **Python**: Pyenv with Python 3.11
   ```bash
   pyenv install 3.11.5
   pyenv local 3.11.5
   ```
2. **Dependencies**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements-dev.txt
   ```
3. **Redis**: Use Docker container (see bash commands)
4. **IDE**: VS Code with Python, Docker, and Redis extensions

## Unexpected Behaviors & Warnings
⚠️ **Message Ordering**: Redis Pub/Sub doesn't guarantee message ordering
⚠️ **Message Persistence**: Messages are ephemeral by default - enable Redis persistence for critical workflows
⚠️ **Thread Safety**: DI container is not thread-safe - instantiate per thread
⚠️ **Log Saturation**: File logging can fill disk - use log rotation in production

## Claude Memory Context
- Agent communication uses Redis Pub/Sub with JSON messages
- Core business logic goes in `AgentBase.run()` implementation
- Configuration hierarchy: Environment vars > config.yaml > defaults
- Error recovery uses exponential backoff with jitter