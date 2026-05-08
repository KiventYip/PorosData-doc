# Processor API Overview

Fast answers for **what to call**, **what to pass**, and **what comes back**. Final structured delivery is documented under [Designer](../designer/index.md); this page centres on the processing layer.
{: .lead}

**Scope** — practical entry points fall into: in-process cleaning (`TextCleaner`), directory-scale batch runs (`python -m porosdata_processor run`), and review or gate commands (`audit`, `delivery-gate`). Handoff to the designer is a **downstream** step once `processed/` is trusted.

**Typical path**

```text
Raw paper or parser output
  -> TextCleaner or batch run
  -> processed outputs
  -> review / gate
  -> structured delivery (Designer)
```

## `TextCleaner`

In-process cleaning for strings or single files.

**Constructor** — `TextCleaner(pipeline=None, clean_options=None)`

| Parameter | Type | Role |
|-----------|------|------|
| `pipeline` | `list \| None` | Ordered plugin names |
| `clean_options` | `dict \| None` | Feature switches (e.g. math spacing) |

**`clean(text) -> str`** — run the configured pipeline on one string; suited to tests and inline use.

```python
from porosdata_processor import TextCleaner

cleaner = TextCleaner()
result = cleaner.clean("The α phase appears in Fig. 1.")
```

**`clean_file(input_path, output_path, encoding="utf-8")`** — read, clean, write.

| Parameter | Meaning |
|-----------|---------|
| `input_path` | Source path |
| `output_path` | Destination path |
| `encoding` | Text encoding (default UTF-8) |

## Batch CLI

Directory-oriented processing.

```bash
python -m porosdata_processor run \
  --input-dir data/raw \
  --output-dir data/processed \
  --max-workers 4
```

| Flag | Role |
|------|------|
| `--input-dir` | Root of raw or parser outputs |
| `--output-dir` | Root for processed artefacts |
| `--max-workers` | Parallelism for file-level work |

Typical artefacts: cleaned content lists, copied assets where configured, `processing_report.json`.

## Review and acceptance commands

**Audit** — pattern and structural signals over `processed/`:

```bash
python -m porosdata_processor audit \
  --processed-dir data/processed \
  --report-file docs/audit/aiready_data_audit_result.json
```

**Delivery gate** — blocking checks with human-readable and machine-readable reports:

```bash
python -m porosdata_processor delivery-gate \
  --processed-dir data/processed \
  --report-file docs/audit/delivery_gate_report.md \
  --json-file docs/audit/delivery_gate_result.json
```

## Options, returns, and errors

| Option / entry | Appears on | Role |
|----------------|------------|------|
| `pipeline`, `clean_options` | `TextCleaner(...)` | Plugin order and toggles |
| `--input-dir`, `--output-dir`, `--max-workers` | CLI `run` | IO roots and concurrency |

| Call | Result |
|------|--------|
| `clean(text)` | One string |
| `clean_file(...)` | File on disk |
| `run` | Processed tree + report |
| `audit` / `delivery-gate` | Review artefacts |

Documented exception families include `ProcessingError` (failed transform) and `ConfigurationError` (invalid options). Batch issues often surface in logs and reports rather than as a single Python exception.

```python
from porosdata_processor import TextCleaner

cleaner = TextCleaner()
# clean() may raise ProcessingError (transform failure) or ConfigurationError (invalid options).
result = cleaner.clean(text)
```

**Common plugin identifiers** — e.g. `citation_rules`, `greek_to_latex`, `normalize_whitespace`, `latex_math_spaces` (exact set depends on version).

**Choosing an entry**

| Goal | Entry |
|------|--------|
| Clean one string | `TextCleaner.clean` |
| Clean one file | `TextCleaner.clean_file` |
| Many documents | CLI `run` |
| Inspect batch quality | CLI `audit` |
| Release-style gate | CLI `delivery-gate` |

**See also:** [Quick Start](../get_started/quickstart.md) · [Examples](../get_started/examples.md) · [Processor](../processor/index.md) · [Designer](../designer/index.md)
