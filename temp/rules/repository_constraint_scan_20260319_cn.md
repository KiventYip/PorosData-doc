# 仓库开发约束扫描报告

## 第一原则：声明式规则改善清洗质量

本包服务于数据清洗。当需要改善清洗质量时，应增量更新 TOML 规则文件，而不是修改 Python 代码。所有约束扫描都以此为基准：每个仍然硬编码在 Python 中的纯模式替换，都是阻碍通过规则更新改善质量的摩擦点。

## 目标

依据当前仓库采用的 7 条开发约束，对实现层进行一次结构扫描，明确：

- 哪些点已经满足
- 哪些点部分满足
- 哪些点仍需继续整改
- 哪些保留项属于算法边界，不应被强行规则文件化

## 扫描依据

当前约束如下：

1. `Pipeline` 固定
2. 规则文件化
3. 算法留代码
4. 单一真源
5. `Step` 职责清晰
6. 规则治理闭环
7. 先收口再抽象

## 当前结论

- `Pipeline 固定`：部分满足
- `规则文件化`：部分满足，且已完成一轮高价值迁移
- `算法留代码`：满足
- `单一真源`：基本满足
- `Step 职责清晰`：部分满足
- `规则治理闭环`：满足
- `先收口再抽象`：部分满足

## 已满足项

- 大量业务规则已迁移到 `rules/*.toml`
- 公式结构修复、Shield 生命周期、括号/分隔符匹配等算法仍保留在 Python
- 审计、候选规则、验证、采纳、门禁的治理链路已存在并可执行
- 基础 text-cleaning pattern 已统一收口到 `patterns_cleaning.toml`，`patterns.py` 与 `tools.py` 共享同一 catalog
- `docs` 与 `.cursor/skills` 已形成“用户文档 vs AI skill”清晰分层
- 新增规则域已经覆盖：
  - `normalize_metadata.toml`
  - `normalize_numbering.toml`
  - `normalize_greek.toml`
  - `formula_lexicon.toml`
  - `semantic_latex.toml`
  - `post_shield.toml`
  - `patterns_cleaning.toml`

## 当前主要整改点

### 1. 仍保留 legacy 规则包用于迁移兼容

例如：

- `citation_rules.toml`
- `audit_rules.toml`
- `term_consistency.toml`

这些并非当前主执行真源，但仓库中仍保留，属于“迁移兼容状态”。
当前 canonical 对照已收口到 `docs/rules/canonical_rule_pack_matrix.md`。

影响：

- 新开发者可能误判真实入口
- 文档与代码需要持续强调 canonical pack

### 2. `steps.py` 仍然偏大

虽然大量规则已外置，但 `steps.py` 仍同时承载：

- step 入口函数
- 私有公式算法
- 引用处理逻辑
- 共享辅助函数

影响：

- 责任边界仍不够清晰
- 后续继续迁移或审查时成本较高

### 3. 默认执行图仍由多处共同表达

当前默认流程主要分布在：

- `config.py`
- `text_cleaner.py`
- `run_processor.py`

影响：

- “固定 pipeline” 这一约束已基本成立，但“单一可观测真源”仍不足
- `TextCleaner` 仍允许外部传入自定义 `pipeline`
- 运行时入口中仍有轻量 pipeline 表达，容易削弱默认执行图的唯一性

### 4. 公开入口/API 层仍存在并存表达

规则真源已基本收口，但公开入口层仍有兼容包装与并存导出，例如：

- `__init__.py`
- `pipelines/__init__.py`
- `pipelines/text_cleaner.py`
- `pipelines/steps.py`

影响：

- 新开发者不易判断真正主入口
- “单一真源” 在公开 API 层面仍是部分满足

## 算法边界保留项

以下内容应继续保留在代码中，而不是继续强行迁移到规则文件：

- Shield 保护/恢复
- 公式结构解析
- brace matching
- display formula 的 cell-wise repair
- reference block 识别
- 固定点迭代与结构校验

这些属于算法，不属于简单业务规则。

## 立即执行建议

1. 统一基础 pattern 真源，明确 `patterns.py` / `tools.py` / `patterns_cleaning.toml` 的关系。
2. 在文档中明确 canonical rule packs，并标注 legacy packs 仅为兼容保留；维护 `docs/rules/canonical_rule_pack_matrix.md`。
3. 后续拆分 `steps.py` 时按领域拆分，不新增新的抽象层。
4. 优先继续收口默认执行图与公开 API 并存表达，再考虑新一轮抽象。

## 结果说明

本次扫描后的仓库状态，不再适合描述为“明显半耦合”；更准确的表述是：

`规则基础设施已建立，主要业务规则已文件化，当前剩余问题主要集中在历史兼容残留与执行图收口。`
