# Audit Reports

[中文版本](readme_cn.md)

This directory stores audit results and scripts for processor quality assessment, rule adoption tracking, and delivery acceptance.

## Current Audit Results

| File | Description |
|------|-------------|
| [`aiready_data_audit_result.json`](./aiready_data_audit_result.json) | Latest machine-readable audit result (auto-generated) |
| [`ocr_audit_stats.json`](./ocr_audit_stats.json) | OCR repair statistics snapshot |
| [`unknown_pattern_mining.json`](./unknown_pattern_mining.json) | Unrecognized pattern candidates for rule expansion |

## Archived Historical Reports

Historical audit reports from the 2026-03-15 to 2026-03-17 development cycle have been moved to [`archive/`](./archive/).

See [`archive/INDEX.md`](./archive/INDEX.md) for a full chronological index with summaries.

Key archived reports for reference:

| Report | Date | Summary |
|--------|------|---------|
| [`rectification_acceptance_audit_report_20260317_1605.md`](./archive/rectification_acceptance_audit_report_20260317_1605.md) | 2026-03-17 | Final rectification acceptance |
| [`full_acceptance_audit_report_20260316.md`](./archive/full_acceptance_audit_report_20260316.md) | 2026-03-16 | Full acceptance audit |
| [`ai_ready_data_quality_audit_report_20260315.md`](./archive/ai_ready_data_quality_audit_report_20260315.md) | 2026-03-15 | AI-Ready data quality baseline |

## Reproducible Audit Scripts

- AI-ready audit: `scripts/audit_aiready_data.py`
- Inline formula pairing audit: `scripts/audit_inline_math_pairing.py`
- OCR statistics snapshot: `scripts/ocr_audit_stats.py`

## Governance

- Each audit run produces timestamped results. File-level artifacts must include `_YYYYMMDD` in their names.
- The data governance loop (`audit -> identify gap -> add rule -> reprocess -> re-audit -> delivery-gate`) is documented in `docs/guides/data_governance_playbook.md`.
- New audit documents should follow the bilingual documentation rule: English primary file plus `_cn` companion file.
