# Contributing to PorosData

We welcome contributions from the community! This guide will help you get started with contributing to the PorosData project.
{: .lead}

## Development Setup

### Prerequisites

- Python 3.8+
- Git
- Virtual environment (recommended)
{: .tight-list}

### Clone and Setup

```bash
git clone https://github.com/KiventYip/porosdata-processor.git
cd porosdata-processor
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -e .[dev]
```

## Development Workflow

### 1. Choose an Issue

Visit our [GitHub Issues](https://github.com/KiventYip/porosdata-processor/issues) page and pick an issue to work on. Look for issues labeled `good first issue` if you're new to the project.

### 2. Create a Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/issue-number-description
```

### 3. Make Changes

Follow our coding standards:
- Use type hints
- Write comprehensive tests
- Update documentation
- Follow PEP 8 style guidelines
{: .tight-list}

### 4. Run Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_specific_feature.py

# Run with coverage
pytest --cov=porosdata_processor
```

### 5. Update Documentation

If your changes affect the API or add new features, update the relevant documentation files.

### 6. Commit Changes

```bash
git add .
git commit -m "feat: add new feature description"
```

Use conventional commit format:
- `feat:` for new features
- `fix:` for bug fixes
- `docs:` for documentation changes
- `test:` for test-related changes
{: .tight-list}

### 7. Create Pull Request

Push your branch and create a pull request on GitHub. Include:
- Clear description of changes
- Reference to related issues
- Screenshots if UI changes
- Test results
{: .tight-list}

## Code Standards

### Python Style

We follow PEP 8 with some modifications:
- Line length: 88 characters (Black default)
- Use double quotes for strings
- Use f-strings for string formatting
{: .tight-list}

### Testing

- Write unit tests for all new functions
- Aim for >90% code coverage
- Use descriptive test names
- Test edge cases and error conditions
{: .tight-list}

### Documentation

- Use Google-style docstrings
- Keep README updated
- Document breaking changes
{: .tight-list}

## Plugin Development

### Plugin Structure

```python
from porosdata_processor.plugins.base import BasePlugin

class MyCustomPlugin(BasePlugin):
    """Plugin description."""

    def __init__(self, config=None):
        super().__init__(config)

    def process(self, text: str) -> str:
        """Process the input text."""
        # Implementation here
        return processed_text

    def validate_config(self):
        """Validate plugin configuration."""
        # Validation logic here
        pass
```

### Plugin Registration

Register your plugin in `porosdata_processor/plugins/__init__.py`:
{: .section-intro}

```python
from .my_plugin import MyCustomPlugin

__all__ = ['MyCustomPlugin']
```

## Getting Help

- **Discussions**: Use [GitHub Discussions](https://github.com/KiventYip/porosdata-processor/discussions) for questions
- **Issues**: Report bugs or request features via [GitHub Issues](https://github.com/KiventYip/porosdata-processor/issues)
- **Discord**: Join our community Discord server
{: .tight-list}

## Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md
- Mentioned in release notes
- Invited to join the core team for significant contributions
{: .tight-list}