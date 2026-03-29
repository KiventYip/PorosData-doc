# 规则治理 SOP

[English Version](rule_governance_sop.md)

## 目标

用一套可重复执行的流程，把审计发现转变为已验证的规则更新和可交付门禁。

## 日常流程

1. 运行 `python -m porosdata_processor audit --processed-dir data/processed --report-file docs/audit/aiready_data_audit_result.json`。
2. 从审计 `task_list` 中选定一个问题类型，例如 `decimal_break` 或 `ref_sticky_protocol`。
3. 运行 `python -m porosdata_processor bootstrap-candidate --audit-file docs/audit/aiready_data_audit_result.json --issue-type <issue_type>`。
4. 编辑生成在 `src/porosdata_processor/rules/candidates/` 下的候选 TOML。
5. 打开生成在 `data/samples/` 下的样本 JSON，补充 `expected_contains` / `expected_not_contains`。
6. 运行 `python -m porosdata_processor sample-validate --sample-file <sample_file> --candidate-pack <candidate_pack> --report-file <report_file>`。
7. 审阅生成的 Markdown diff 报告，确认没有引入回归。
8. 运行 `python -m porosdata_processor promote-rule --candidate-pack <candidate_pack>`。
9. 重新执行 `python -m porosdata_processor run --input-dir data/raw --output-dir data/processed`。
10. 运行 `python -m porosdata_processor delivery-gate --processed-dir data/processed --report-file docs/audit/delivery_gate_report.md --json-file docs/audit/delivery_gate_result.json`。
11. 如果门禁通过，在 `CHANGELOG.md` 中记录变更，并保留审计链路。

## 操作说明

- `bootstrap-candidate` 是初始化命令，不是自动修复命令；它负责生成候选起点和样本骨架。
- `promote-rule` 按规则 `id` 合并，因此一旦采纳后应尽量保持规则 ID 稳定。
- `delivery-gate` 应被视作交付或发布前的阻断检查。
- 如果自动推断的目标规包不正确，可重新运行 `bootstrap-candidate` 并加 `--target`。

## 推荐产物

- 审计 JSON：`docs/audit/aiready_data_audit_result.json`
- 候选规包：`src/porosdata_processor/rules/candidates/*_candidate.toml`
- 样本文件：`data/samples/*_candidate_samples.json`
- 验证报告：`docs/rules/reports/*.md`
- 交付门禁报告：`docs/audit/delivery_gate_report.md`
