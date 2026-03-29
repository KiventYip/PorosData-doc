# Cursor Skill 使用说明

## 目的

本文档面向仓库使用者，说明本项目内置 Cursor skill 的用途、触发方式与推荐提问入口。

对应的 AI skill 位于：

- `.cursor/skills/datapreprocessing-project/SKILL.md`

该 skill 主要服务于 AI 模型，不是给用户直接阅读的主说明文档。

## 什么时候用

当你希望 AI 在本仓库中按既有架构和规则治理标准开展工作时，应让它进入项目 skill 语境。典型场景包括：

- 先理解仓库架构，再开始改代码
- 新增、调整、迁移某条清洗规则
- 判断一个改动应该放在 TOML 规则包还是 Python 算法里
- 检查仓库改动是否符合当前开发约束
- 继续收口 canonical 与 legacy rule pack
- 解释本包的处理流程、治理流程、交付门禁

## 推荐提问方式

你不需要手动“执行 skill 文件”，更推荐直接在需求里显式带上仓库上下文和目标。建议使用以下提问方式：

### 1. 架构理解入口

```text
先按这个仓库现有架构理解项目，再开始修改。
```

### 2. 规则开发入口

```text
这是一个新清洗需求，请先判断它应该落在哪个 canonical TOML 里，再实施。
```

### 3. 方案咨询入口

```text
请按本仓库现有开发约束，给我一个实施方案，再执行。
```

### 4. 治理扫描入口

```text
请按当前项目标准扫描仓库，指出哪些地方还不符合单一真源和规则文件化。
```

### 5. 使用说明入口

```text
请按这个项目的标准，说明这个包该如何开发、如何应用、如何验证。
```

## 推荐关键词

在提问中包含以下关键词，更容易让 AI 进入项目 skill 的正确语境：

- `datapreprocessing`
- `porosdata_processor`
- `rule pack`
- `TOML`
- `pipeline`
- `audit`
- `delivery gate`
- `canonical`
- `legacy`
- `term consistency`
- `citation`

## 你可以期待 AI 做什么

当 skill 被正确应用时，AI 应该：

1. 先用本仓库的固定架构来理解问题，而不是给出通用型建议。
2. 先判断改动属于 canonical 规则包、legacy 兼容层，还是 Python 算法边界。
3. 在实施时同步考虑测试、样本、changelog 与治理文档更新。
4. 解释方案时优先围绕这几个维度展开：
   - pipeline 固定
   - 规则文件化
   - 算法留代码
   - 单一真源
   - 治理闭环

## 相关文档

- `docs/rules/canonical_rule_pack_matrix.md`
- `docs/rules/rule_externalization_plan.md`
- `docs/rules/repository_constraint_scan_20260319_cn.md`
- `ARCHITECTURE_LEDGER_cn.md`
- `docs/guides/project_development_workflow_cn.md`
