# Examples

This page provides copyable starter examples for common delivery scenarios. Each example includes a minimal command, an input layout, an expected output, and where to look first if something goes wrong.
{: .lead}

## Example 1: Trial Run on One Paper

Use this when you want to verify one source document before starting a larger batch.

### Applicable Scenario

- one paper needs a first-pass quality check
- you want to confirm terms, formulas, and figure references before scaling up

### Minimal Command

```bash
python -m porosdata_processor run \
  --input-dir data/raw \
  --output-dir data/processed \
  --max-workers 1
```

### Input Layout

```text
data/
└── raw/
    └── 00001/
        ├── 00001.pdf
        └── ...upstream parser files...
```

### Expected Output

```text
data/
└── processed/
    ├── processing_report.json
    └── 00001/
        └── ...cleaned intermediate outputs...
```

### What You Should Get

- one cleaned intermediate result set
- one processing report for quick review

### If It Fails, Check Here First

- whether `data/raw` contains a complete source package
- whether the command can write to `data/processed`
- whether the processing report or logs show missing source files

## Example 2: Batch Processing

Use this when you need to process multiple papers into one consistent intermediate batch.

### Applicable Scenario

- a project contains many papers
- the team needs one stable `processed` batch before final delivery

### Minimal Command

```bash
python -m porosdata_processor run \
  --input-dir data/raw \
  --output-dir data/processed \
  --max-workers 4
```

### Input Layout

```text
data/
└── raw/
    ├── 00001/
    ├── 00002/
    └── 00003/
```

### Expected Output

```text
data/
└── processed/
    ├── processing_report.json
    ├── 00001/
    ├── 00002/
    └── 00003/
```

### What You Should Get

- one processed directory for each document
- one batch report summarizing the run

### If It Fails, Check Here First

- whether all source folders follow one consistent structure
- whether worker count is too high for the current machine
- whether the batch report shows skipped or failed items

## Example 3: Build a Review-Oriented Delivery Package

Use this when the receiving team needs readable outputs as well as structured delivery artifacts.

### Applicable Scenario

- product, data, and research teams need the same delivery package
- the handoff must support reading, extraction, and review together

### Minimal Commands

```bash
python -m porosdata_processor run \
  --input-dir data/raw \
  --output-dir data/processed \
  --max-workers 4
```

```bash
porosdata-designer run all --input_dir data/processed
```

### Input Layout

```text
data/
├── raw/
└── processed/
```

### Expected Output

```text
data/
└── structured/
    ├── full_text/
    ├── datamining/
    └── multimodal/
```

### Expected Deliverables

- readable full-text outputs
- plain-text streams
- structured JSON outputs
- multimodal indexes for figure-text linking
- batch reports for traceability

### If It Fails, Check Here First

- whether `processed` outputs are complete and stable before running `Designer`
- whether the final `structured` directories were created as expected
- whether processing reports and validation outputs show unresolved quality issues

## Related Reading

- [Installation](../get_started/installation.md)
- [Quick Start](../get_started/quickstart.md)
- [End-to-End Workflow](../get_started/end-to-end-workflow.md)
- [Processor](../tools/processor/index.md)
- [Designer](../tools/designer/index.md)

## Quick Links

- [Home](../index.md)
- [Quick Start](../get_started/quickstart.md)
{: .tight-list}
