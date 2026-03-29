# 规则治理

[English Version](rule_governance.md)

## 目标

把规则更新从零散的正则修改，转变为可追踪、可复验的数据治理闭环。

## 第一原则：声明式规则改善清洗质量

本包服务于数据清洗。当需要改善清洗质量时，应增量更新 TOML 规则文件，而不是修改 Python 代码。代码修改仅限于声明式规则无法安全表达的结构性算法。规则创建与晋升的操作流程见 `rule_governance_sop_cn.md`。

## 工作流

1. 运行 `python -m porosdata_processor audit ...` 从处理结果中发现问题。
2. 记录问题类型、受影响样本数量和风险等级。
3. 判断该变更属于：
   - `repair`
   - `normalize`
   - `detect`
4. 新增或更新对应的 TOML 规包。
5. 补充 `source_audit`、优先级和 target 元数据。
6. 补充或更新回归测试与样本断言。
7. 运行 `python -m porosdata_processor bootstrap-candidate ...` 从审计结果初始化候选规包和样本 JSON。
8. 运行 `python -m porosdata_processor sample-validate ...` 对比正式规包与候选规包输出。
9. 如通过评审，运行 `python -m porosdata_processor promote-rule ...` 增量合并到正式规包。
10. 重新运行 `python -m porosdata_processor run ...` 处理新数据或复跑样本。
11. 在交付或移交前运行 `python -m porosdata_processor delivery-gate ...`。
12. 运行单元测试、集成测试和审计脚本。
13. 在 `CHANGELOG.md` 中记录规包变更。

操作层 SOP 请见 `docs/rules/rule_governance_sop_cn.md`。

## 编写原则

- 当行为本质上是纯模式替换时，优先使用声明式 TOML 规则，而不是继续增加硬编码正则。
- 高风险结构逻辑在能够安全外置前，可以继续保留在 Python 中。
- 不要在同一个执行 target 中混合 detect-only 规则与会改写文本的规则。
- 所有交付阻断规则都应具有清晰的 `priority` 与 `source_audit`。

## 规包归属

- `repair_ocr.toml`：清洗阶段使用的 OCR 与语义修复规则
- `normalize_terms.toml`：术语、合金命名、单位与一致性规则
- `normalize_citations.toml`：引用符号归一与引用策略元数据
- `detect_audit.toml`：仅用于审计的 OCR 与质量检测规则
- `detect_delivery.toml`：用于交付门禁的阻断规则

## Canonical 与 Legacy

- canonical 归属矩阵见 `docs/rules/canonical_rule_pack_matrix.md`
- `term_consistency.toml`、`citation_rules.toml`、`audit_rules.toml` 属于 legacy 兼容规包
- 新增业务规则应写入 canonical 的 `rule-pack.v1` 规包，而不是继续写入 legacy 规包

## 规则冲突防护

向 canonical 规包添加新规则时，需逐项验证：

1. **ID 唯一性**：每条规则的 `id` 在其所属规包内必须唯一。命名约定为 `{域}.{target}.{描述}`。
2. **Pattern 重叠**：新规则的 pattern 不应与同一 target 下已有规则匹配相同文本，除非优先级排序是有意为之。
3. **替换链风险**：新规则的 replacement 不应产生能触发其他规则的文本。通过 `sample-validate` 检测级联效应。
4. **Target 归属**：每条规则只应使用其所属规包拥有的 target，不允许跨包注入 target。
5. **验证门禁**：添加规则后必须运行 `sample-validate`，基线与候选的对比是捕捉规则交互的主要机制。

## 发布要求

每次规包发布至少应留下：

- 更新后的 TOML 规包
- 更新后的回归测试或样本
- 更新后的 `CHANGELOG.md`
- 如有需要，更新审计说明或迁移清单
