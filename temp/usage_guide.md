# Usage Guide

[中文版本](usage_guide_cn.md)

## Positioning

PorosData-Processor converts MinerU OCR outputs into LLM-ready scientific text while preserving formulas, citations, and structural cues.

## Quick Start

### Python API

```python
from porosdata_processor import TextCleaner

cleaner = TextCleaner()
result = cleaner.clean("The α phase appears in Section IV.")
print(result)
```

### Batch Processing

```bash
porosdata-processor \
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

## Rule Workflow Commands

### Bootstrap a Candidate Pack

```bash
python -m porosdata_processor bootstrap-candidate \
    --audit-file docs/audit/aiready_data_audit_result.json \
    --issue-type decimal_break
```

Use this command to infer the target canonical pack from an audit issue and generate:

- a candidate TOML pack
- a seeded sample JSON file

### Validate Candidate Rules

```bash
python -m porosdata_processor sample-validate \
    --sample-file data/samples/rule_eval_samples.template.json \
    --candidate-pack src/porosdata_processor/rules/candidates/normalize_terms_candidate.toml \
    --report-file docs/rules/reports/normalize_terms_candidate.md
```

### Promote Validated Rules

```bash
python -m porosdata_processor promote-rule \
    --candidate-pack src/porosdata_processor/rules/candidates/normalize_terms_candidate.toml
```

`promote-rule` incrementally merges validated rules by rule ID and keeps a backup under `docs/rules/backups/`.

### Audit Processed Data

```bash
python -m porosdata_processor audit \
    --processed-dir data/processed \
    --report-file docs/audit/aiready_data_audit_result.json
```

### Run the Delivery Gate

```bash
python -m porosdata_processor delivery-gate \
    --processed-dir data/processed \
    --report-file docs/audit/delivery_gate_report.md \
    --json-file docs/audit/delivery_gate_result.json
```

PowerShell shortcut:

```powershell
scripts/run_delivery_gate.ps1
```

## Processing Flow

```text
Raw text
 -> _pre_shield_processing
 -> Shield.protect
 -> Pipeline steps
 -> Shield.restore
 -> _post_shield_processing
 -> LLM-ready text
```

`local_text_compression` runs before Shield because it needs direct access to raw `$...$` math spans.

## Notes

- Quality-assurance and token-evaluation modes increase runtime.
- `clean_stream` is intended for simpler streaming scenarios and does not provide full Shield behavior.
- Validate configuration changes on samples before large batch runs.
- Use `docs/deployment_guide.md` for server deployment details.
