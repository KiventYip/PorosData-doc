# Contributing to PorosData-Processor

We welcome contributions from the community! This document provides guidelines for contributing to the project.

## Ways to Contribute

- **Report Bugs**: Found a bug? Open an issue on GitHub
- **Suggest Features**: Have an idea? Create a feature request
- **Write Code**: Fix bugs or implement new features
- **Improve Documentation**: Help make our docs better
- **Write Tests**: Increase our test coverage

## Development Setup

### Prerequisites

- Python 3.8 or higher
- Git
- (Optional) Docker for containerized development

### Setup Steps

1. **Fork the repository** on GitHub
2. **Clone your fork**:

```bash
git clone https://github.com/KiventYip/porosdata-processor.git
cd porosdata-processor
```

3. **Create a virtual environment**:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

4. **Install development dependencies**:

```bash
pip install -e ".[dev]"
```

5. **Run tests to ensure everything works**:

```bash
pytest
```

## Development Workflow

### 1. Choose an Issue

- Check our [GitHub Issues](https://github.com/KiventYip/porosdata-processor/issues)
- Look for issues labeled "good first issue" or "help wanted"
- Comment on the issue to indicate you're working on it

### 2. Create a Branch

```bash
# Create and switch to a new branch
git checkout -b feature/your-feature-name
# or
git checkout -b fix/issue-number-description
```

### 3. Make Changes

- Write clear, concise commit messages
- Follow our coding standards (see below)
- Add tests for new functionality
- Update documentation as needed

### 4. Run Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=porosdata_processor --cov-report=html

# Run specific test file
pytest tests/unit/test_cleaner.py

# Run tests matching pattern
pytest -k "test_text_clean"
```

### 5. Update Documentation

```bash
# Build documentation
cd docs_sphinx
make html

# View documentation
open _build/html/index.html  # or start a local server
```

### 6. Commit Changes

```bash
# Stage your changes
git add .

# Commit with a clear message
git commit -m "feat: add new cleaning plugin for academic citations

- Add citation normalization plugin
- Handle various citation formats ([1], [2], etc.)
- Add comprehensive tests
- Update documentation

Closes #123"
```

### 7. Push and Create Pull Request

```bash
# Push your branch
git push origin feature/your-feature-name

# Create a Pull Request on GitHub
```

## Coding Standards

### Python Style

We follow [PEP 8](https://pep8.org/) with some modifications. Use [Black](https://black.readthedocs.io/) for code formatting:

```bash
# Format code
black src/ tests/

# Check formatting
black --check src/ tests/
```

### Type Hints

Use type hints for all function parameters and return values:

```python
from typing import List, Optional

def process_text(text: str, options: Optional[dict] = None) -> str:
    """Process text with given options."""
    pass
```

### Docstrings

Use Google-style docstrings:

```python
def clean_text(text: str) -> str:
    """Clean and normalize text content.

    Args:
        text: The input text to be cleaned.

    Returns:
        The cleaned and normalized text.

    Raises:
        ValueError: If the input text is empty.

    Example:
        >>> clean_text("  hello   world  ")
        'hello world'
    """
    pass
```

### Naming Conventions

- **Functions**: snake_case (e.g., `clean_text`, `process_file`)
- **Classes**: PascalCase (e.g., `TextCleaner`, `PluginRegistry`)
- **Constants**: UPPER_CASE (e.g., `DEFAULT_ENCODING`)
- **Modules**: snake_case (e.g., `text_cleaner.py`)

## Testing

### Test Structure

Tests are organized in the `tests/` directory:

```
tests/
├── unit/          # Unit tests
├── integration/   # Integration tests
└── fixtures/      # Test data
```

### Writing Tests

```python
import pytest
from porosdata_processor import TextCleaner

class TestTextCleaner:
    def setup_method(self):
        self.cleaner = TextCleaner()

    def test_basic_cleaning(self):
        """Test basic text cleaning functionality."""
        input_text = "This is  a   test."
        expected = "This is a test."
        result = self.cleaner.clean(input_text)
        assert result == expected

    def test_formula_protection(self):
        """Test that LaTeX formulas are protected."""
        input_text = "Formula: $E = mc^2$"
        result = self.cleaner.clean(input_text)
        assert "$E = mc^2$" in result
```

### Test Coverage

Aim for high test coverage. Run coverage reports:

```bash
pytest --cov=porosdata_processor --cov-report=term-missing
```

Target: >90% coverage for new code.

## Plugin Development

### Creating a Plugin

1. **Define the plugin function**:

```python
from porosdata_processor.plugin_system import PluginRegistry

@PluginRegistry.register("my_custom_plugin")
def my_custom_plugin(text: str) -> str:
    """Custom text processing plugin."""
    # Your processing logic here
    return processed_text
```

2. **Add tests** for your plugin:

```python
def test_my_custom_plugin():
    from porosdata_processor.plugin_system import PluginRegistry

    plugin = PluginRegistry.get_plugin("my_custom_plugin")
    assert plugin is not None

    result = plugin("test input")
    assert result == "expected output"
```

3. **Update documentation** in `docs_sphinx/api-reference.md`

### Plugin Guidelines

- **Idempotent**: Running the plugin multiple times should not change the result
- **Pure Functions**: No side effects, same input always produces same output
- **Error Handling**: Handle errors gracefully or raise appropriate exceptions
- **Performance**: Optimize for speed and memory usage

## Documentation

### Building Docs

```bash
cd docs_sphinx
make html
```

### Writing Docs

- Use Markdown (.md) files in `docs_sphinx/`
- Follow the existing structure and style
- Include code examples and use cases
- Keep language clear and accessible

### API Documentation

Use docstrings for automatic API documentation generation:

```python
def important_function(param1: str, param2: int = 0) -> dict:
    """One-line summary of what the function does.

    Detailed description of the function's behavior, including
    edge cases and important notes.

    Args:
        param1: Description of param1
        param2: Description of param2 (default: 0)

    Returns:
        Dictionary containing the results

    Raises:
        ValueError: When param1 is invalid

    Example:
        >>> result = important_function("test", 5)
        >>> result['status']
        'success'
    """
```

## Commit Guidelines

### Commit Message Format

```
type(scope): description

[optional body]

[optional footer]
```

### Types

- **feat**: New feature
- **fix**: Bug fix
- **docs**: Documentation changes
- **style**: Code style changes (formatting, etc.)
- **refactor**: Code refactoring
- **test**: Adding or updating tests
- **chore**: Maintenance tasks

### Examples

```
feat: add citation normalization plugin

- Support for [1], [2] style citations
- Automatic conversion from 【1】 format
- Comprehensive test coverage

Closes #42
```

```
fix: resolve ReDoS vulnerability in regex patterns

- Replace vulnerable regex with secure alternatives
- Add timeout protection for regex operations
- Update tests to cover edge cases

Fixes #123
```

## Release Process

### Version Numbering

We follow [Semantic Versioning](https://semver.org/):

- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes (backward compatible)

### Release Checklist

- [ ] All tests pass
- [ ] Documentation is updated
- [ ] Changelog is updated
- [ ] Version number is updated in `pyproject.toml`
- [ ] Tag is created: `git tag v1.2.3`
- [ ] Push tag: `git push origin v1.2.3`

## Code of Conduct

- Be respectful and inclusive
- Focus on constructive feedback
- Help newcomers learn and contribute
- Follow our community guidelines

## Getting Help

- **Documentation**: Check our [docs](https://porosdata-processor.readthedocs.io/)
- **Issues**: Search existing issues or create new ones
- **Discussions**: Use GitHub Discussions for questions
- **Email**: Contact maintainers for sensitive matters

Thank you for contributing to PorosData-Processor! 🎉