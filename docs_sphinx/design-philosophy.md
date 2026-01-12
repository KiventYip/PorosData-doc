# Design Philosophy

## Plugin-Driven Architecture

PorosData-Processor is built on a flexible plugin system that allows developers to easily extend and customize text processing capabilities. This design separates core processing logic from specific cleaning rules, enabling:

### Benefits of Plugin Architecture

**Modularity**: Each cleaning operation is encapsulated in its own plugin, making the system easy to understand and maintain.

**Extensibility**: New cleaning rules can be added without modifying core code:

```python
@PluginRegistry.register("custom_academic_rule")
def my_rule(text: str) -> str:
    # Custom cleaning logic for specific domains
    return processed_text
```

**Customizability**: Users can create custom processing pipelines by selecting and ordering specific plugins:

```python
cleaner = TextCleaner(pipeline=[
    "unicode_normalization",
    "citation_rules",
    "greek_to_latex",
    "normalize_whitespace"
])
```

### Available Plugins

| Plugin | Purpose | Example |
|--------|---------|---------|
| `patterns_cleaning` | General text pattern cleanup | Fix punctuation spacing |
| `citation_rules` | Citation format normalization | `[1]` → `[1]` |
| `greek_to_latex` | Greek letter to LaTeX conversion | `α` → `\alpha` |
| `document_numbering_rules` | Document structure normalization | `Chapter II` → `Chapter 2` |
| `normalize_whitespace` | Whitespace standardization | Remove extra spaces |
| `remove_extra_spaces` | Space compression | Multiple spaces → single space |

## Shield Mechanism

The Shield mechanism is the cornerstone of our "cleaning without destruction" philosophy. It ensures that sensitive content remains untouched during aggressive text cleaning operations.

### How Shield Works

1. **Pre-Shield Phase**: Before applying cleaning rules, sensitive content is identified and temporarily replaced with unique placeholders.

2. **Safe Cleaning**: Cleaning operations are applied only to the "safe" text regions between placeholders.

3. **Post-Shield Restoration**: Original content is perfectly restored from placeholders.

### Protected Content Types

- **LaTeX Formulas**: Both inline (`$...$`) and display (`$$...$$`) mathematics
- **Code Blocks**: Markdown code blocks and inline code
- **Special Notation**: Academic symbols and formatting that should not be altered

### Technical Implementation

The Shield system uses cryptographically secure placeholders that are:

- **Unique**: Each placeholder is guaranteed to be unique within the document
- **Tamper-proof**: Impossible to accidentally generate matching placeholders
- **Efficient**: Minimal performance overhead during processing
- **Safe**: No risk of placeholder collision with document content

### Example

```python
# Input text
text = "The formula $E = mc^2$ is famous, and so is α particle physics."

# After Shield protection
protected = "The formula __SHIELD_abc123__ is famous, and so is α particle physics."

# After cleaning (only non-shielded text is processed)
cleaned = "The formula __SHIELD_abc123__ is famous, and so is \\alpha particle physics."

# After Shield restoration
final = "The formula $E = mc^2$ is famous, and so is \\alpha particle physics."
```

This approach ensures that even the most aggressive cleaning rules cannot damage critical scientific content, while still allowing comprehensive text normalization.