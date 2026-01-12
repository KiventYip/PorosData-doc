# API Reference

This section provides comprehensive documentation of the PorosData-Processor API.

## TextCleaner

The main class for text cleaning operations.

### Constructor

```python
TextCleaner(pipeline=None, clean_options=None)
```

**Parameters:**
- `pipeline` (Optional[List[str]]): List of plugin names to execute in order. If None, uses default pipeline.
- `clean_options` (Optional[Dict[str, bool]]): Additional cleaning options.

### Methods

#### clean(text: str) -> str

Clean the input text using the configured pipeline.

**Parameters:**
- `text` (str): Input text to clean

**Returns:**
- `str`: Cleaned text

**Example:**
```python
cleaner = TextCleaner()
result = cleaner.clean("Input text")
```

#### clean_file(input_path: str, output_path: Optional[str] = None, encoding: str = "utf-8") -> str

Clean a file and optionally save the result.

**Parameters:**
- `input_path` (str): Path to input file
- `output_path` (Optional[str]): Path for output file. If None, overwrites input file.
- `encoding` (str): File encoding, default "utf-8"

**Returns:**
- `str`: Cleaned content

## Plugin System

### PluginRegistry

Registry for managing text processing plugins.

#### register(name: str)

Decorator to register a plugin function.

**Example:**
```python
@PluginRegistry.register("my_plugin")
def my_plugin(text: str) -> str:
    return processed_text
```

#### get_plugin(name: str)

Get a registered plugin by name.

#### list_plugins()

List all registered plugin names.

## Available Plugins

### Built-in Plugins

| Plugin | Description |
|--------|-------------|
| `patterns_cleaning` | General text pattern cleanup |
| `citation_rules` | Citation format normalization |
| `greek_to_latex` | Greek letter to LaTeX conversion |
| `document_numbering_rules` | Document structure normalization |
| `normalize_whitespace` | Whitespace standardization |
| `remove_extra_spaces` | Space compression |

### Plugin Signatures

All plugins follow the same signature:

```python
def plugin_function(text: str) -> str:
    """
    Process the input text and return the result.

    Args:
        text: Input text to process

    Returns:
        Processed text
    """
    # Plugin implementation
    return processed_text
```

## Configuration

### Default Pipeline

The default processing pipeline includes:

1. `unicode_normalization` - Unicode character normalization
2. `patterns_cleaning` - General pattern cleanup
3. `citation_rules` - Citation normalization
4. `document_numbering_rules` - Document structure fixes
5. `normalize_whitespace` - Whitespace cleanup
6. `remove_extra_spaces` - Space compression

### Clean Options

Available options in `clean_options`:

- `"clean_latex_math_spaces"` (bool): Whether to clean spaces inside LaTeX formulas. Default: False

## Error Handling

### Exceptions

- `TextProcessorError`: Base exception for all processing errors
- `PluginError`: Errors specific to plugin execution
- `ConfigurationError`: Configuration-related errors

### Error Recovery

The cleaner supports graceful error recovery:

```python
cleaner = TextCleaner(ignore_errors=True)  # Continue processing on errors
cleaner = TextCleaner(ignore_errors=False)  # Raise exceptions on errors
```

## Advanced Usage

### Custom Pipeline Creation

```python
# Minimal pipeline
minimal_cleaner = TextCleaner(pipeline=[
    "normalize_whitespace",
    "remove_extra_spaces"
])

# Scientific-focused pipeline
science_cleaner = TextCleaner(pipeline=[
    "greek_to_latex",
    "citation_rules",
    "patterns_cleaning"
])
```

### Plugin Development

```python
from porosdata_processor.plugin_system import PluginRegistry

@PluginRegistry.register("custom_plugin")
def custom_plugin(text: str) -> str:
    """
    Custom text processing plugin.

    This plugin demonstrates the basic structure of a custom plugin.
    """
    # Your processing logic here
    return text.upper()  # Example: convert to uppercase

# Use the custom plugin
cleaner = TextCleaner(pipeline=["custom_plugin"])
result = cleaner.clean("hello world")  # Output: "HELLO WORLD"
```

## Performance Considerations

- **Memory Usage**: Large documents are processed in memory
- **Plugin Ordering**: Plugin order can affect performance
- **Caching**: Consider implementing caching for repeated operations

## Thread Safety

TextCleaner instances are thread-safe for concurrent use, but sharing instances across threads requires proper synchronization if configuration is modified during processing.