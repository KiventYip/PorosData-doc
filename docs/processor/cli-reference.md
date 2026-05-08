# CLI reference

Command-line behaviour described here matches **porosdata-processor 0.4.1**; confirm your install with `pip show porosdata-processor`. If this site and your checkout disagree, trust the package you run.
{: .lead}

## Entry points

| Invocation | Resolves to |
|------------|-------------|
| `python -m processor` | `processor.cli:main` (aggregated CLI) |
| `porosdata-processor` | `processor.cli:main` |
| `porosdata-cleaning` | `processor.cleaning.cleaning_cli:main` (same options as batch; **not** routed through the aggregated subcommand) |
| `porosdata-audit` | `processor.audit.audit_cli:main` |
| `porosdata-rulegovernance` | `processor.rulegovernance.rulegovernance_cli:main` |
| `porosdata-evaluation` | `processor.evaluation.evaluation_cli:main` |

Aggregated subcommands on `porosdata-processor`: `cleaning`, `audit`, `evaluation`, `rulegovernance`. There is **no** `run` subcommand—batch work maps to **`cleaning`** (or use `porosdata-cleaning` directly).

## `cleaning` / `porosdata-cleaning`

```bash
porosdata-processor cleaning [OPTIONS]
# or
porosdata-cleaning [OPTIONS]
```

| Option | Type | Default | Notes |
|--------|------|---------|--------|
| `--input-dir` | string | `data/Raw Database` | Input tree |
| `--output-dir` | string | `data/Processed Database` | Output tree |
| `--log-level` | enum | `INFO` | `DEBUG`, `INFO`, `WARNING`, `ERROR` |
| `--max-workers` | int | *(inferred)* | Cap parallel processes |
| `--enable-evaluation` | flag | off | Token-efficiency evaluation (`transformers`) |
| `--force-reprocess` | flag | off | Ignore “output newer than input” skip |
| `--memory-limit` | int | `2048` | RSS hint threshold (MB) for GC messaging |
| `--heartbeat-seconds` | int | `30` | Wait-loop heartbeat; runtime uses `max(5, value)` |
| `--diagnostic` | flag | off | Tier-2 diagnostics in `processing_debug.json`—**only** when `--enable-evaluation` is set; otherwise it has no effect |

**Exit codes**

- `0` — `report["summary"]["error_files"] == 0`
- `1` — any error files, or an uncaught failure
- `130` — `KeyboardInterrupt`

## `audit`

```bash
porosdata-processor audit [--processed-dir DIR] [--report-file PATH]
```

| Option | Default |
|--------|---------|
| `--processed-dir` | `data/Processed Database` |
| `--report-file` | `data/Rule Supplement Database/audit_report.json` |

Exit code is always `0`.

## `rulegovernance`

Subcommands: `bootstrap-candidate`, `sample-validate`, `promote-rule`, `delivery-gate`.

**`bootstrap-candidate`** — required: `--audit-file`, `--issue-type`. Optional: `--target`, `--candidate-pack`, `--sample-file`. Exits `0`.

**`sample-validate`** — required: `--sample-file`, `--candidate-pack`, `--report-file`. Optional: `--baseline-pack`. Exits `0` when all expectations pass, else `2`.

**`promote-rule`** — required: `--candidate-pack`. Optional: `--destination-pack`, `--backup-dir`. Exits `0`.

**`delivery-gate`**

| Option | Default |
|--------|---------|
| `--processed-dir` | `data/Processed Database` |
| `--report-file` | `data/Rule Supplement Database/delivery_gate.md` |
| `--json-file` | `data/Rule Supplement Database/delivery_gate.json` |

Exits `0` when `summary.blocking_documents == 0`, else `3`. The workflow uses rule pack `rules/detect_delivery.toml` unless you override it in code.

## `evaluation`

| Option | Default | Required |
|--------|---------|----------|
| `--input-file` | — | yes |
| `--model` | `gpt2` | |
| `--sample-rate` | `0.1` | |
| `--batch-size` | `64` | |

Exits `0` on success; a missing input file raises `FileNotFoundError`.

## Reports, logs, and artefacts

| Artefact | Location |
|----------|----------|
| Batch summary JSON | `<output-dir>/processing_report.json` |
| Optional diagnostics | `<output-dir>/processing_debug.json` (with evaluation + `--diagnostic`) |
| Default rotating file log | `logs/processor.log` (10 MB, five backups) when the runtime does not override `log_file` |

Shell wrappers may send logs elsewhere—for example `scripts/run_rulegovernance.sh` under `logs/rulegovernance/<run_id>/`—that layout is **script-level**, not the Python package default.

**See also:** [Configuration and runtime](configuration-and-runtime.md) · [Data governance](data-governance.md) · [Processor overview](index.md)
