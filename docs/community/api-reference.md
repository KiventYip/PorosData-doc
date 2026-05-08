# Processor API

This page answers **what to call**, **what to pass**, and **what you get back** for the processing layer. Final structured delivery is documented under [Designer](../designer/index.md).
{: .lead}

**Scope** — three surfaces matter: in-process cleaning (`TextCleaner`), directory-scale work through the **`cleaning`** CLI (or `porosdata-cleaning`), and review or gate commands (`audit`, `rulegovernance`). Treat Designer as a **downstream** step once the **Processed Database** looks stable.

**Typical path**

```text
Raw paper or Parser output (Raw Database)
  -> TextCleaner or batch run
  -> Processed Database
  -> review / gate
  -> Designed Database (Designer)
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

**File I/O** — the current `TextCleaner` API is string-oriented. Read a file yourself, call `clean`, then write the result (see [Quick Start](../get_started/quickstart.md)).

## Batch CLI

Directory-oriented processing uses the **`cleaning`** subcommand (same options as `porosdata-cleaning`):

```bash
porosdata-processor cleaning \
  --input-dir "data/Raw Database" \
  --output-dir "data/Processed Database" \
  --max-workers 4
```

| Flag | Role |
|------|------|
| `--input-dir` | Root of **Raw Database** (Parser output) |
| `--output-dir` | Root for **Processed Database** artefacts |
| `--max-workers` | Parallelism for file-level work |

Typical artefacts: cleaned content lists, copied assets where configured, `processing_report.json`. Exit codes and the full flag list are in [CLI reference](../processor/cli-reference.md).

## Review and acceptance commands

**Audit** — pattern and structural signals over **Processed Database**:

```bash
porosdata-processor audit \
  --processed-dir "data/Processed Database" \
  --report-file "data/Rule Supplement Database/audit_report.json"
```

**Delivery gate** — blocking checks with human-readable and machine-readable reports:

```bash
porosdata-processor rulegovernance delivery-gate \
  --processed-dir "data/Processed Database" \
  --report-file "data/Rule Supplement Database/delivery_gate.md" \
  --json-file "data/Rule Supplement Database/delivery_gate.json"
```

## Options, returns, and errors

| Option / entry | Appears on | Role |
|----------------|------------|------|
| `pipeline`, `clean_options` | `TextCleaner(...)` | Plugin order and toggles |
| `--input-dir`, `--output-dir`, `--max-workers` | CLI `cleaning` | IO roots and concurrency |

| Call | Result |
|------|--------|
| `clean(text)` | One string |
| `cleaning` | Processed tree + report |
| `audit` / `rulegovernance delivery-gate` | Review artefacts |

`clean` raises `TypeError` on non-string input. Unknown pipeline steps raise `ValueError`; strict sentinel settings may raise `RuntimeError`. Batch problems usually show up in logs and `processing_report.json` rather than as one catch-all exception type.

```python
from porosdata_processor import TextCleaner

cleaner = TextCleaner()
result = cleaner.clean(text)
```

**Common plugin identifiers** — e.g. `citation_rules`, `greek_to_latex`, `normalize_whitespace`, `latex_math_spaces` (exact set depends on version).

**Choosing an entry**

| Goal | Entry |
|------|--------|
| Clean one string | `TextCleaner.clean` |
| Clean one file | Read text, `clean`, write (string API) |
| Many documents | CLI `cleaning` (or `porosdata-cleaning`) |
| Inspect batch quality | CLI `audit` |
| Release-style gate | CLI `rulegovernance delivery-gate` |

**See also:** [Quick Start](../get_started/quickstart.md) · [Examples](../get_started/examples.md) · [Processor](../processor/index.md) · [Designer](../designer/index.md)
