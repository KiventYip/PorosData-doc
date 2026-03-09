# API Reference

## Core Classes

### TextCleaner

The main class for text cleaning operations.

#### Constructor

```python
TextCleaner(pipeline=None, clean_options=None)
```

**Parameters:**
- `pipeline` (list, optional): List of cleaning plugins to apply
- `clean_options` (dict, optional): Additional cleaning options

#### Methods

##### clean(text)

Clean the input text using the configured pipeline.

**Parameters:**
- `text` (str): Input text to clean

**Returns:**
- `str`: Cleaned text

**Example:**
```python
cleaner = TextCleaner()
result = cleaner.clean("Raw text with $formulas$")
```

##### clean_file(input_path, output_path, encoding='utf-8')

Clean a file and save the result.

**Parameters:**
- `input_path` (str): Path to input file
- `output_path` (str): Path to output file
- `encoding` (str): File encoding (default: 'utf-8')

## Plugins

### Available Plugins

- `citation_rules`: Normalize citation formats
- `greek_to_latex`: Convert Greek letters to LaTeX
- `normalize_whitespace`: Clean up spacing issues
- `latex_math_spaces`: Remove extra spaces in math formulas

### Custom Plugins

To create a custom plugin:

```python
from porosdata_processor.plugins.base import BasePlugin

class MyPlugin(BasePlugin):
    def process(self, text):
        # Your processing logic here
        return processed_text
```

## Exceptions

### ProcessingError

Raised when text processing fails.

```python
try:
    result = cleaner.clean(text)
except ProcessingError as e:
    print(f"Processing failed: {e}")
```

### ConfigurationError

Raised when configuration is invalid.

```python
try:
    cleaner = TextCleaner(invalid_config)
except ConfigurationError as e:
    print(f"Configuration error: {e}")
```