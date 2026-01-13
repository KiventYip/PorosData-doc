# Installation

## System Requirements

- **Python**: 3.8 or higher
- **Operating System**: Windows, macOS, Linux
- **Memory**: Minimum 256MB RAM (more recommended for large documents)

## Installation Methods

### From PyPI (Recommended)

```bash
pip install porosdata-processor
```

For development installation with additional tools:

```bash
pip install porosdata-processor[dev]
```

### From Source Code

```bash
# Clone the repository
git clone https://github.com/KiventYip/porosdata-processor.git
cd porosdata-processor

# Install in development mode
pip install -e .

# Or install with development dependencies
pip install -e ".[dev]"
```

### Docker Installation

```bash
# Build the Docker image
docker build -t porosdata-processor .

# Run the container
docker run -it porosdata-processor
```

## Verification

After installation, verify that everything is working correctly:

```python
import porosdata_processor
from porosdata_processor import TextCleaner

print(f"PorosData-Processor version: {porosdata_processor.__version__}")

# Quick functionality test
cleaner = TextCleaner()
result = cleaner.clean("Test text with α and $E=mc^2$")
print(f"Test result: {result}")
```

## Dependencies

PorosData-Processor has minimal dependencies and works with Python's standard library. Optional development dependencies include:

- **pytest**: For running tests
- **black**: Code formatting
- **mypy**: Type checking
- **flake8**: Code linting
- **sphinx**: Documentation building

## Troubleshooting

### Common Issues

**Import Error**: Make sure you're using the correct import name:

```python
# Correct
import porosdata_processor
from porosdata_processor import TextCleaner

# Incorrect
# import PorosData-Processor  # Wrong case and hyphens (invalid Python syntax)
```

**Encoding Issues**: Ensure your files are properly encoded:

```python
# Specify encoding explicitly
with open('document.md', 'r', encoding='utf-8') as f:
    content = f.read()
```

**Memory Issues**: For very large files, consider processing in chunks:

```python
# Process large files in chunks
chunk_size = 1024 * 1024  # 1MB chunks
with open('large_file.md', 'r', encoding='utf-8') as f:
    while chunk := f.read(chunk_size):
        cleaned_chunk = cleaner.clean(chunk)
        # Process cleaned_chunk
```

## Development Setup

For contributors and developers:

```bash
# Clone and setup
git clone https://github.com/KiventYip/porosdata-processor.git
cd porosdata-processor

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Build documentation
cd docs_sphinx
make html
```