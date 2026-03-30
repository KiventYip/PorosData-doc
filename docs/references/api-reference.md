# Processor API Overview

This page is a practical reference entry for the current processing-facing interfaces. It is intended to answer three questions quickly:
{: .lead}

- what to call
- what to pass in
- what to expect back
{: .tight-list}

## Scope of This Page

The current repository documentation is centered on the processing layer. In practice, the public-facing entry points fall into four groups:

| Area | Responsibility | Typical Entry |
|------|------|------|
| `Processor` | text cleaning and quality preparation | `TextCleaner`, CLI `run` |
| batch processing | process multiple source documents into `processed` outputs | `python -m porosdata_processor run` |
| review and acceptance | inspect processed outputs before handoff | audit and delivery-gate style commands |
| `Designer` handoff | take stable `processed` results into final delivery outputs | documented as a downstream stage, not a primary API in this page |

If you are looking for final structured delivery outputs, start with the `Designer` documentation after the processing stage is complete.

## Typical Call Path

The most common usage path is:

```text
Raw paper or parser output
-> TextCleaner or batch run
-> processed outputs
-> review and acceptance
-> downstream structured delivery
```

## Most Common Entry Points

### `TextCleaner`

Use `TextCleaner` when you want to clean one piece of scientific text inside Python code.

#### Constructor

```python
TextCleaner(pipeline=None, clean_options=None)
```

| Parameter | Type | Meaning |
|------|------|------|
| `pipeline` | `list | None` | ordered list of cleaning plugins |
| `clean_options` | `dict | None` | additional cleaning switches |

#### Typical Methods

##### `clean(text)`

Clean one text string with the configured pipeline.

| Item | Value |
|------|------|
| Input | `text: str` |
| Return | `str` |
| Use case | inline cleaning, local testing, rule verification |

```python
from porosdata_processor import TextCleaner

cleaner = TextCleaner()
result = cleaner.clean("The α phase appears in Fig. 1.")
print(result)
```

##### `clean_file(input_path, output_path, encoding="utf-8")`

Clean one file and write the result to disk.

| Parameter | Type | Meaning |
|------|------|------|
| `input_path` | `str` | source file path |
| `output_path` | `str` | target file path |
| `encoding` | `str` | file encoding, default `utf-8` |

| Return | Meaning |
|------|------|
| written file | cleaned file output at `output_path` |

### Batch CLI

Use the CLI when you want to process a directory instead of one text string.

#### Typical Command

```bash
python -m porosdata_processor run \
  --input-dir data/raw \
  --output-dir data/processed \
  --max-workers 4
```

#### Input and Output

| Item | Meaning |
|------|------|
| `--input-dir` | source directory with raw or upstream parser outputs |
| `--output-dir` | target directory for processed results |
| `--max-workers` | batch concurrency for multi-file runs |

| Output | Meaning |
|------|------|
| cleaned content lists | quality-ready intermediate outputs |
| copied assets | reusable image assets |
| `processing_report.json` | batch summary for review |

### Review and Acceptance Commands

Use these commands when the batch is complete and you need to inspect whether the outputs are ready to hand off.

#### Quality Review

```bash
python -m porosdata_processor audit \
  --processed-dir data/processed \
  --report-file docs/audit/aiready_data_audit_result.json
```

#### Delivery Gate

```bash
python -m porosdata_processor delivery-gate \
  --processed-dir data/processed \
  --report-file docs/audit/delivery_gate_report.md \
  --json-file docs/audit/delivery_gate_result.json
```

These commands are most useful in project handoff, batch review, or recurring quality checks.

## Parameters and Behavior at a Glance

### Common Processing Options

| Option | Where It Appears | Meaning |
|------|------|------|
| `pipeline` | `TextCleaner(...)` | choose or order cleaning plugins |
| `clean_options` | `TextCleaner(...)` | enable or tune specific cleaning behavior |
| `--input-dir` | CLI | source data location |
| `--output-dir` | CLI | processed output location |
| `--max-workers` | CLI | number of parallel workers |

### Expected Return Types

| Entry | Returns or Produces |
|------|------|
| `clean(text)` | one cleaned string |
| `clean_file(...)` | one cleaned file |
| `run` | processed directory outputs and batch report |
| `audit` | review report |
| `delivery-gate` | acceptance report and machine-readable result |

## Exceptions and Failure Signals

The Python API may raise runtime exceptions when configuration or processing is invalid. The two most common documented categories are:

| Exception | Meaning | Typical Cause |
|------|------|------|
| `ProcessingError` | text processing failed | invalid input, unsupported text case, or processing failure |
| `ConfigurationError` | configuration is invalid | wrong option shape or unsupported config value |

```python
try:
    cleaner = TextCleaner()
    result = cleaner.clean(text)
except ProcessingError as e:
    print(f"Processing failed: {e}")
except ConfigurationError as e:
    print(f"Configuration error: {e}")
```

For batch runs, the main failure signals are more often found in logs, processing reports, and delivery-gate outputs than in a direct Python exception.

## Available Plugin Examples

Common plugin names include:

- `citation_rules`
- `greek_to_latex`
- `normalize_whitespace`
- `latex_math_spaces`
{: .tight-list}

## When to Use Which Entry

| If you need to... | Use this entry |
|------|------|
| clean one string in code | `TextCleaner.clean()` |
| clean one file locally | `TextCleaner.clean_file()` |
| process many source files | CLI `run` |
| inspect processed outputs before handoff | CLI `audit` |
| check delivery readiness | CLI `delivery-gate` |

## Related Reading

- [Quick Start](../get_started/quickstart.md)
- [Examples](examples.md)
- [Processor](../tools/processor/index.md)
- [Designer](../tools/designer/index.md)