# Rule Governance SOP

[中文版本](rule_governance_sop_cn.md)

## Goal

Use a single repeatable workflow to turn audit findings into validated rule updates and release gates.

## Daily Flow

1. Run `python -m porosdata_processor audit --processed-dir data/processed --report-file docs/audit/aiready_data_audit_result.json`.
2. Pick one issue type from the audit `task_list`, such as `decimal_break` or `ref_sticky_protocol`.
3. Run `python -m porosdata_processor bootstrap-candidate --audit-file docs/audit/aiready_data_audit_result.json --issue-type <issue_type>`.
4. Edit the generated candidate TOML under `src/porosdata_processor/rules/candidates/`.
5. Open the generated sample JSON under `data/samples/` and fill `expected_contains` / `expected_not_contains`.
6. Run `python -m porosdata_processor sample-validate --sample-file <sample_file> --candidate-pack <candidate_pack> --report-file <report_file>`.
7. Review the generated Markdown diff report and confirm there is no regression.
8. Run `python -m porosdata_processor promote-rule --candidate-pack <candidate_pack>`.
9. Re-run batch processing with `python -m porosdata_processor run --input-dir data/raw --output-dir data/processed`.
10. Run `python -m porosdata_processor delivery-gate --processed-dir data/processed --report-file docs/audit/delivery_gate_report.md --json-file docs/audit/delivery_gate_result.json`.
11. If the gate passes, record the change in `CHANGELOG.md` and keep the audit trail.

## Operator Notes

- `bootstrap-candidate` is a seed command, not an auto-fix command. It generates a candidate starting point and sample skeletons.
- `promote-rule` merges by rule `id`, so keep rule IDs stable once adopted.
- `delivery-gate` should be treated as a blocking check for release or handoff.
- If an issue is not mapped to the right pack automatically, rerun `bootstrap-candidate` with `--target`.

## Recommended Outputs

- Audit JSON: `docs/audit/aiready_data_audit_result.json`
- Candidate pack: `src/porosdata_processor/rules/candidates/*_candidate.toml`
- Seeded samples: `data/samples/*_candidate_samples.json`
- Validation report: `docs/rules/reports/*.md`
- Delivery gate report: `docs/audit/delivery_gate_report.md`
