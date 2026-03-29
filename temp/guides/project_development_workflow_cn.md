# 项目开发工作流

## 目的

本文档面向仓库使用者，说明在 `datapreprocessing` 项目中，如何按现有标准推进需求分析、规则开发、代码修改、验证与文档更新。

如果你想让 AI 按本仓库既有约束开展工作，可先阅读：

- `docs/guides/cursor_skill_usage_cn.md`

如果你想了解规则治理命令级 SOP，可继续阅读：

- `docs/rules/rule_governance_sop_cn.md`

## 第一原则：声明式规则改善清洗质量

本包服务于数据清洗。当需要改善清洗质量时，应增量更新 TOML 规则文件，而不是修改 Python 代码。代码修改仅限于声明式规则无法安全表达的结构性算法。规则创建与晋升的操作流程见 `docs/rules/rule_governance_sop_cn.md`。

## 先理解再实施

在本项目里，建议先判断需求属于哪一类，再开始修改：

1. 规则类需求
   - 例如新增 OCR 清洗规则、术语归一规则、引用归一规则、门禁检测规则
2. 算法类需求
   - 例如 Shield 生命周期、公式结构修复、括号匹配、结构保守校验
3. 架构治理类需求
   - 例如 canonical 与 legacy 收口、默认 pipeline 真源、文档一致性

基本判断原则：

- 纯 pattern / mapping / detect 行为，优先进入 canonical TOML 规则包
- 结构性、状态性、解析型行为，继续保留在 Python
- 不要把新业务规则继续写入 legacy 兼容规包

## 标准实施路径

### 1. 明确改动归属

先回答四个问题：

1. 这个需求属于哪个规则域？
2. 它应该进入哪个 canonical pack？
3. 是否触及 Python 算法边界？
4. 是否需要同步更新治理文档？

常见 canonical pack 入口：

- `src/porosdata_processor/rules/normalize_terms.toml`
- `src/porosdata_processor/rules/normalize_citations.toml`
- `src/porosdata_processor/rules/detect_audit.toml`
- `src/porosdata_processor/rules/detect_delivery.toml`
- `src/porosdata_processor/rules/patterns_cleaning.toml`

完整矩阵见：

- `docs/rules/canonical_rule_pack_matrix.md`

### 2. 实施改动

按需求类型选择实施方式：

- 规则类需求：优先修改 canonical TOML 规包
- 算法类需求：修改 Python 代码，并保留边界说明
- 架构类需求：优先做收口，不新增新的抽象层

实施时建议检查规则冲突：

- **ID 唯一性**：新规则 `id` 在规包内必须唯一（命名约定：`{域}.{target}.{描述}`）
- **Pattern 重叠**：新 pattern 不应与同一 target 下已有规则匹配相同文本
- **替换链风险**：replacement 不应产生能触发其他规则的文本
- **Target 归属**：每条规则只应使用其所属规包拥有的 target
- 是否已有近似规则可复用
- 是否需要补样本或回归测试
- 是否需要补 canonical/legacy 说明

### 3. 验证改动

最小验证建议：

```bash
python -m compileall src
python -m pytest tests/unit/test_patterns.py tests/unit/test_installation_verification.py tests/unit/test_processor.py
```

如果改动涉及规则工作流，再补：

```bash
python -m pytest tests/unit/test_rule_pack_loader.py
```

如果改动涉及候选规则治理流程，再按 SOP 补充：

1. `audit`
2. `bootstrap-candidate`
3. `sample-validate`
4. `promote-rule`
5. `delivery-gate`

## 文档更新要求

当你做的是“规则归属、治理方式、架构收口、canonical 关系”相关改动时，通常需要检查这些文档是否同步：

- `docs/rules/canonical_rule_pack_matrix.md`
- `docs/rules/rule_externalization_plan.md`
- `docs/rules/repository_constraint_scan_20260319_cn.md`
- `docs/rules/rule_governance.md`
- `docs/rules/rule_governance_cn.md`
- `docs/rules/rule_migration_inventory.md`
- `ARCHITECTURE_LEDGER.md`
- `ARCHITECTURE_LEDGER_cn.md`
- `CHANGELOG.md`
- `CHANGELOG_cn.md`

## 用户提问建议

如果你希望 AI 更稳定地按本仓库标准执行，建议直接这样提问：

### 架构型问题

```text
先按这个仓库的固定 pipeline、规则文件化和算法边界来理解问题，再给出方案。
```

### 规则型问题

```text
请先判断这个需求应该落在哪个 canonical TOML 规包，再实施并补测试与文档。
```

### 治理型问题

```text
请按当前仓库约束扫描并收口 legacy 残留，同时更新 related 文档。
```

## 常见误区

### 1. 把 skill 当成用户文档

不建议直接把 `.cursor/skills` 当作用户说明阅读入口。

- `skill` 主要服务 AI
- `docs` 才是面向用户的说明层

### 2. 只改规则，不补治理文档

如果改动影响了 canonical 归属、执行入口或治理方式，就不应只修改代码或 TOML。

### 3. 把新规则写进 legacy pack

以下文件属于兼容保留，不应继续承接新业务规则：

- `src/porosdata_processor/rules/term_consistency.toml`
- `src/porosdata_processor/rules/citation_rules.toml`
- `src/porosdata_processor/rules/audit_rules.toml`

### 4. 遇到复杂结构问题仍强行规则化

对于公式结构修复、解析、保护、恢复和校验类问题，应优先保留在 Python。

## 相关文档

- `docs/guides/cursor_skill_usage_cn.md`
- `docs/usage_guide_cn.md`
- `docs/rules/rule_governance_sop_cn.md`
- `docs/rules/canonical_rule_pack_matrix.md`
- `ARCHITECTURE_LEDGER_cn.md`
