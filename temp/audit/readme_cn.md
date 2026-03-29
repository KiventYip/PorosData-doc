# 审计文档索引

[English Version](README.md)

本目录存放处理器质量评估、规则采纳跟踪和交付验收的审计结果与脚本。

## 当前审计结果

| 文件 | 说明 |
|------|------|
| [`aiready_data_audit_result.json`](./aiready_data_audit_result.json) | 最新的机器可读审计结果（自动生成） |
| [`ocr_audit_stats.json`](./ocr_audit_stats.json) | OCR 修复统计快照 |
| [`unknown_pattern_mining.json`](./unknown_pattern_mining.json) | 未识别模式候选，用于规则扩展 |

## 已归档历史报告

2026-03-15 至 2026-03-17 开发周期的历史审计报告已移至 [`archive/`](./archive/)。

完整的按时间排列的索引请见 [`archive/INDEX.md`](./archive/INDEX.md)。

关键归档报告供参考：

| 报告 | 日期 | 摘要 |
|------|------|------|
| [`rectification_acceptance_audit_report_20260317_1605.md`](./archive/rectification_acceptance_audit_report_20260317_1605.md) | 2026-03-17 | 最终整改验收 |
| [`full_acceptance_audit_report_20260316.md`](./archive/full_acceptance_audit_report_20260316.md) | 2026-03-16 | 全量验收审计 |
| [`ai_ready_data_quality_audit_report_20260315.md`](./archive/ai_ready_data_quality_audit_report_20260315.md) | 2026-03-15 | AI-Ready 数据质量基线 |

## 可复现审计脚本

- AI-ready 审计：`scripts/audit_aiready_data.py`
- 行内公式配对审计：`scripts/audit_inline_math_pairing.py`
- OCR 统计快照：`scripts/ocr_audit_stats.py`

## 治理说明

- 每次审计运行产生带时间戳的结果。文件级产物文件名中必须包含 `_YYYYMMDD`。
- 数据治理闭环（`审计 -> 识别差距 -> 添加规则 -> 重新处理 -> 再审计 -> 交付门禁`）的完整说明见 `docs/guides/data_governance_playbook_cn.md`。
- 新增审计文档应遵循双语规则：英文主文档 + `_cn` 中文对应文档。
