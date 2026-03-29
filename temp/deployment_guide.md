# Deployment Guide

[中文版本](deployment_guide_cn.md)

## Environment

- Python 3.8+
- Recommended memory: 8 GB or more
- Multi-core CPU recommended for parallel batch processing

## What to Copy

Copy the repository root when possible. The essential runtime items are:

- `src/porosdata_processor/`
- `run_processor.py`
- `examples/run_pipeline.py`
- `pyproject.toml`
- `scripts/`
- `data/` as needed

You can usually exclude:

- `tests/`
- `.pytest_cache/`
- `__pycache__/`
- `.git/`

## Installation

```bash
git clone <repo-url> /opt/datapreprocessing
cd /opt/datapreprocessing
python3 -m venv venv
source venv/bin/activate
pip install .
```

For editable installation during debugging:

```bash
pip install -e .
```

## Basic Run

Preferred formal entrypoints:

- `porosdata-processor`
- `python -m porosdata_processor`

Example:

```bash
python -m porosdata_processor run \
    --input-dir data/raw \
    --output-dir data/processed \
    --max-workers 4
```

Equivalent source-repo entry:

```bash
python examples/run_pipeline.py \
    --input-dir data/raw \
    --output-dir data/processed
```

## Logs and Output

Default output root:

- processed data: `data/processed`
- processing report: `data/processed/processing_report.json`

Default log root:

- `logs/processor.log`

Custom log directory:

```bash
export POROS_LOGS_PATH=/var/log/porosdata
```

## Recommended Operations

### Audit Processed Data

```bash
python -m porosdata_processor audit \
    --processed-dir data/processed \
    --report-file docs/audit/aiready_data_audit_result.json
```

### Run Delivery Gate Before Handoff

```bash
python -m porosdata_processor delivery-gate \
    --processed-dir data/processed \
    --report-file docs/audit/delivery_gate_report.md \
    --json-file docs/audit/delivery_gate_result.json
```

## Long-Running Server Jobs

### `nohup`

```bash
nohup python -m porosdata_processor run \
    --input-dir /data/mineru_raw \
    --output-dir /data/cleaned \
    --max-workers 8 \
    > nohup_output.log 2>&1 &
```

### `screen` or `tmux`

Run the same command inside a managed terminal session for long-running jobs.

### `systemd`

Use a service wrapper for stable production execution when you need restart-on-failure behavior.

## Troubleshooting

- If `transformers`-related evaluation fails, remove `--enable-evaluation` or install the missing package.
- If memory usage is high, reduce `--max-workers`.
- If a batch is interrupted, rerun the same command. Incremental processing will skip unchanged outputs unless `--force-reprocess` is used.
