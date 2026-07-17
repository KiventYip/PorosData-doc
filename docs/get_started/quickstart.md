# Quick Start

This page walks from installation to a configurable cleaner and file-oriented runs. It assumes you already have `porosdata-processor` available in the active Python environment.
{: .lead}

**Install** — from PyPI:

```bash
pip install porosdata-processor
```

From a source tree:

```bash
git clone https://github.com/KiventYip/porosdata-processor.git
cd porosdata-processor
pip install -e .
```

Confirm the import:

```python
import porosdata_processor
print(f"Version: {porosdata_processor.__version__}")
```

**Default cleaning with `TextCleaner`** — the class applies the default plugin pipeline and preserves LaTeX-style segments where configured:

```python
from porosdata_processor import TextCleaner

cleaner = TextCleaner()
raw_text = "The energy equation is $E = mc^2$, involving α particles and β rays."
cleaned_text = cleaner.clean(raw_text)
print(cleaned_text)
# Example output: Greek letters normalised to LaTeX forms where rules apply
```

**Custom plugin order** — pass an explicit pipeline when you need citation normalisation, Greek-to-LaTeX conversion, or whitespace rules in a particular order:

```python
cleaner = TextCleaner(pipeline=[
    "citation_rules",
    "greek_to_latex",
    "normalize_whitespace",
])

text = "See reference 【1】 for α particle data."
result = cleaner.clean(text)
```

**LaTeX spacing options** — optional `clean_options` tighten math spacing when safe:

```python
cleaner = TextCleaner(clean_options={
    "clean_latex_math_spaces": True,
})

text = "Formula: $\\mathbf { X } + \\frac { a }{ b }$"
result = cleaner.clean(text)
```

**Single file on disk** — read the file, clean the string, then write:

```python
from pathlib import Path
from porosdata_processor import TextCleaner

cleaner = TextCleaner()
path = Path("document.md")
cleaned = cleaner.clean(path.read_text(encoding="utf-8"))
path.with_name("clean_document.md").write_text(cleaned, encoding="utf-8")
```

**Batch processing** — for a full **Raw Database** tree, the CLI is the supported entry point (see [Examples](examples.md) and [CLI reference](../processor/cli-reference.md)):

```bash
porosdata-processor cleaning \
  --input-dir "data/Raw Database" \
  --output-dir "data/Processed Database" \
  --max-workers 4
```

**YAML configuration (optional)** — project layouts often keep defaults under `config/processing_config.yaml`:

```yaml
cleaning:
  convert_greek: true
  apply_rules: true
  apply_patterns: true
  normalize_whitespace: true
  remove_extra_spaces: true

processing:
  concurrency: 0  # 0: sequential
  verbose: true
```

Tokenisation or chunking settings, when used, may live in a separate `config/token_config.yaml` (model family, BOS/EOS markers, chunk size, overlap). Align those files with the version of the processor you run; fields can change between releases.

**Where to read next** — [API Reference](../community/api-reference.md) · [Examples](examples.md) · [Contributing](https://github.com/KiventYip/PorosData-doc/blob/main/CONTRIBUTING.md) (process for doc changes in this site)
