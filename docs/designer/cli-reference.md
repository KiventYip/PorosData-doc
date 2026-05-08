# CLI reference

Command-line surface of the **`designer`** package: pipeline runs, structured audits, and validators. All paths accept `Path`-style strings on the shell.
{: .lead}

## Entry points

| Mode | Resolves to |
|------|-------------|
| `designer …` | `designer.cli:main` |
| `python -m designer …` | Same entry via `designer/__main__.py` |

## Command tree

Top-level subcommands: `run`, `audit`, `validate`. Each adds its own nested parser.

### `run`

| Subcommand | Role |
|------------|------|
| `run all` | Full text standardisation, then multimodal extraction |
| `run text` | Text standardisation only |
| `run multimodal` | Multimodal extraction only |

Shared arguments on every `run` variant:

| Flag | Required | Default | Meaning |
|------|------------|---------|---------|
| `--input_dir` | Yes | — | Root directory; the tool recursively collects `*_content_list.json` files |
| `--output_dir` | No | project `data/Designed Database` | Base directory for per-`doc_id` output folders |
| `--log_dir` | No | project `logs/` | Directory for rotating log files |

### `audit`

| Subcommand | Role |
|------------|------|
| `audit structured` | Deep audit of Designed Database-style outputs |

| Flag | Required | Default | Meaning |
|------|------------|---------|---------|
| `--root_dir` | No | same default as Designed Database root | Root that contains per-`doc_id` folders |

### `validate`

| Subcommand | Role |
|------------|------|
| `validate structured` | Checks `{doc_id}.content.json` contracts |
| `validate multimodal` | Checks `{doc_id}.assets.index.json` (lighter than full audit) |
| `validate acceptance` | Sampling-based smoke checks |
| `validate delivery` | Delivery-standard pass using the same report builder as audit |

`validate structured`, `validate multimodal`, and `validate acceptance` accept `--output_dir` (default: Designed Database root) and optional `--log_dir`.  
`validate delivery` mirrors `audit structured` flags: `--root_dir`, `--log_dir`.

## Copy-paste examples

```bash
designer run all --input_dir "/path/to/Processed Database"
designer run text --input_dir "/path/to/Processed Database" --output_dir /path/out --log_dir /path/logs
designer run multimodal --input_dir "/path/to/Processed Database"

designer audit structured
designer audit structured --root_dir /path/to/Designed\ Database

designer validate structured --output_dir /path/to/Designed\ Database
designer validate multimodal --output_dir /path/to/Designed\ Database
designer validate acceptance --output_dir /path/to/Designed\ Database
designer validate delivery --root_dir /path/to/Designed\ Database
```

## Input discovery

`--input_dir` is normalised to an absolute path and **must exist**. Under it, every `*_content_list.json` file becomes one document:

`doc_id = <stem of file> with the suffix "_content_list" removed`  
Example: `papers/00001_content_list.json` → `doc_id` `00001`.

Each list file is a **JSON array** of blocks (text, images, equations, and so on) as produced by the Processor / MinerU-style toolchain.

## Output and logging defaults

If `--output_dir` is omitted on `run` or `validate`, writers resolve to:

`get_project_root() / "data" / "Designed Database"`

Each document is written to `{output_base}/{doc_id}/`.

If `--log_dir` is omitted, logs go to `get_project_root() / "logs"`.

## Log files

Logging uses **loguru**. After setup, the process still prints `INFO` to stderr; file sinks use `DEBUG`, UTF-8 encoding, **10 MB** rotation, **7 days** retention, and a **daily** component in the filename pattern.

The file path pattern is:

`{log_dir}/{script_name}_{time:YYYY-MM-DD}.log`

where `{time:YYYY-MM-DD}` is expanded by loguru (not a fixed literal date). Typical `script_name` values include:

`run_all`, `run_text_standardization`, `run_multimodal_extraction`, `validate_structured_output`, `validate_multimodal_output`, `final_acceptance_validation`, `validate_delivery_output`.

## Exit codes

| Scenario | Code |
|----------|------|
| `run_*` finished without error | `0` |
| `KeyboardInterrupt` during `run_*` | `130` |
| Uncaught exception in `run_*` | `1` |
| `audit structured` — `report["summary"]["failed"] == 0` | `0` |
| `audit structured` — one or more failures | `1` |

Other validate subcommands follow their own logging and process exit conventions; treat non-zero exits as a failed check when the CLI prints errors.

## Related

Defaults that are not CLI flags (for example `TAG_PREFIX`, `TRAINING_CONFIG`) live in [Configuration](configuration.md). JSON field names are documented in [Output artefacts](output-artifacts.md).
