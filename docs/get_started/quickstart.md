# Quick Start

## Install PorosData

Install from PyPI (Recommended):

```bash
pip install porosdata-processor
```

Install from source:

```bash
git clone https://github.com/KiventYip/porosdata-processor.git
cd porosdata-processor
pip install -e .
```

Verify installation:

```python
import porosdata_processor
print(f"Version: {porosdata_processor.__version__}")
```

## Clean Text

Use `TextCleaner` to normalize scientific text while preserving formulas:

```python
from porosdata_processor import TextCleaner

# Initialize cleaner with default settings
cleaner = TextCleaner()

# Process text
raw_text = "The energy equation is $E = mc^2$, involving α particles and β rays."
cleaned_text = cleaner.clean(raw_text)

print(cleaned_text)
# Output: "The energy equation is $E = mc^2$, involving \alpha particles and \beta rays."
```

## Custom Pipeline

Configure a cleaner with specific plugins:

```python
# Create a cleaner with specific plugins
cleaner = TextCleaner(pipeline=[
    "citation_rules",      # Normalize citations
    "greek_to_latex",      # Convert Greek letters
    "normalize_whitespace" # Clean up spacing
])

text = "See reference 【1】 for α particle data."
result = cleaner.clean(text)
# Output: "See reference [1] for \alpha particle data."
```

## Advanced Options

Enable advanced LaTeX formula cleaning:

```python
# Enable advanced LaTeX formula cleaning
cleaner = TextCleaner(clean_options={
    "clean_latex_math_spaces": True  # Remove extra spaces inside formulas
})

text = "Formula: $\\mathbf { X } + \\frac { a }{ b }$"
result = cleaner.clean(text)
# Output: "Formula: $\\mathbf{X} + \\frac{a}{b}$"
```

## Process Files

### Process Single File

```python
# Clean a Markdown file
cleaner.clean_file(
    input_path="document.md",
    output_path="clean_document.md",
    encoding="utf-8"
)
```

### Batch Processing

```python
from processing.batch_processor import BatchProcessor

processor = BatchProcessor()
processor.process_text_data(
    input_dir="data/raw",
    output_dir="data/cleaned"
)
```

## Configuration

### Processing Configuration

Create a `config/processing_config.yaml`:

```yaml
cleaning:
  convert_greek: true
  apply_rules: true
  apply_patterns: true
  normalize_whitespace: true
  remove_extra_spaces: true

processing:
  concurrency: 0  # 0 for sequential processing
  verbose: true
```

### Token Configuration

For advanced tokenization settings, create `config/token_config.yaml`:

```yaml
model_type: "llama"  # or "gpt", "custom"

tokens:
  llama:
    bos: "<s>"
    eos: "</s>"
    inst_start: "[INST]"
    inst_end: "[/INST]"

splitting:
  max_chunk_tokens: 512
  split_by_paragraph: true
  preserve_paragraphs: true
  overlap_tokens: 50
```

## Next Steps

- Explore [API Reference](../references/api-reference.md) for detailed method documentation
- Check out [Examples](../references/examples.md) for real-world use cases
- Learn about [Plugin Development](../community/contributing.md) to extend functionality