# Processor 遗留公式问题映射与优化步骤

> 仓库变更说明（2026-03-17 后）：当前仓库统一批处理入口为 `porosdata-processor` / `python -m porosdata_processor`，`academic_tools/` 已移除，源码仓运行入口保留 `examples/run_pipeline.py`，数据目录已统一为 `data/raw` 与 `data/processed`。本文为历史审计归档，正文若出现旧路径、旧脚本或旧目录命名，均表示审计发生时的仓库状态。

**形成时间**：2026-03-17  
**对照文档**：
- `docs/audit/processor_upstream_formula_legacy_issues_20260317.md`
- `docs/ai_ready_and_data_mining_delivery_standard.md`

---

## 1. 目的

本说明用于把上游遗留公式问题映射到 `Processor` 当前实现中，判断：

- 问题是否仍存在于 `Processor`
- 当前是已覆盖、部分覆盖还是未覆盖
- 后续应如何落实为具体优化步骤

---

## 2. 问题映射总表

| 问题类型 | 上游文档结论 | Processor 当前状态 | 判断 |
| --- | --- | --- | --- |
| inline 残缺 `array` 环境 | 明确存在 | 之前缺少专门降级逻辑，现已补 inline 降级修复 | 部分覆盖后转为已落实修复 |
| `\\Delta` 并入合金名 | 明确存在 | 已有假 `\\Delta` 识别，但复杂残形需要上下文收尾 | 部分覆盖后转为已落实修复 |
| 半截连字符材料式 | 明确存在 | 已有若干收紧规则，但跨片段/跨公式链合并不稳定 | 部分覆盖后转为已落实修复 |
| citation -> `ref[...]` 协议 | 标准要求必须统一 | 主链路已覆盖，但旧审计口径把 `ref[1]` 中的 `[1]` 误当作残留 | 已覆盖，审计脚本需补正向验收 |
| `wordref[1]` / `ref[1]word` 粘连 | 标准要求必须禁止 | 主流程已有空格修复，但审计脚本之前未显式验收 | 审计补齐 |
| 物理量 `\\Delta T/H/G/...` 保护 | 标准要求不得误伤 | 当前逻辑可区分物理量与合金名污染 | 已覆盖 |

---

## 3. 逐项判断

### 3.1 inline 残缺 `array` 环境

上游文档中的代表问题：

- `\\begin{array} ... \\end{array})` 被错误带入正文
- 原本只是普通括号说明，却被误升格为坏掉的 LaTeX 环境

当前判断：

- 问题**确实存在于 Processor 历史输出中**
- 之前 `Processor` 更偏向处理 display formula，对 inline 坏环境没有专门降级
- 现已在 `steps.py` 中补充 inline 坏 `array` 降级逻辑，把这类结构恢复成普通行内公式

优化落地：

1. 识别 `$...$` 中残缺的 `\\begin{array}` / `\\end{array}`
2. 若不含真正矩阵结构（无 `&`、无 `\\\\`），则降级为普通 inline math
3. 保留后续公式空格修复链路继续清洗

### 3.2 `\\Delta` 并入合金名

上游文档中的代表问题：

- `\\mathrm{\\DeltaNi - Nb {- Y}}`
- `\\mathrm{\\DeltaNb {- Y}}`

当前判断：

- 问题**确实存在于 Processor 历史输出中**
- 但它与真实 `\\Delta T`、`\\Delta H`、`\\Delta G` 必须严格区分
- 当前已在 `text_cleaner.py` 中加入“假 `\\Delta` 合金前缀剥离”逻辑，并保留真实物理量差值

优化落地：

1. 仅在合金式/元素链上下文删除假 `\\Delta`
2. 不对真实物理量 `\\Delta T / \\Delta H / \\Delta G / \\bar{\\Delta V}` 做删除
3. 对删除后的材料式继续做连字符与链式拼接修复

### 3.3 半截连字符材料式

上游文档中的代表问题：

- `$\\mathbf{Ni -}$ $...$`
- `$\\mathrm{Zr -}$ Cu`
- `$\\mathrm{Cu_60 -}$ $\\mathrm{Zr}_{30} ...$`

当前判断：

- 问题**确实存在于 Processor 历史输出中**
- 旧规则能处理部分空格污染，但不能稳定恢复跨公式链材料式
- 当前已在 `text_cleaner.py` 中补充后恢复阶段合并逻辑，用于修复：
  - `$\\mathrm{Zr-}$ Cu`
  - `$\\mathrm{Ni-}$ $\\mathrm{Nb-Y}$`
  - `$\\mathrm{Cu_60-}$ $\\mathrm{Zr}...$`

优化落地：

1. 合并“半截公式 + 后续元素 token”
2. 合并“半截公式 + 后续公式链”
3. 避免保留“半个公式”进入交付文本

### 3.4 citation / `ref[...]` 协议

当前判断：

- 主清洗链路中 `citation_to_ref` 已在默认 pipeline 启用
- 之前审计脚本存在一个明显口径问题：会把 `ref[1][2]` 中的 `[1]`、`[2]` 再次算成原始 citation 残留

优化落地：

1. 审计时先剔除合法 `ref[...]` 再统计残留 `[n]`
2. 增加 `normalized_ref_count`
3. 保留 `raw_citation_count`
4. 后续可继续扩展 `wordref[1]` / `ref[1]word` 的正向验收

---

## 4. 已落实的具体步骤

### 步骤 A：公式修复

- 在 `src/porosdata_processor/steps.py` 新增 inline 坏 `array` 降级逻辑
- 在 `local_text_compression()` 中接入该逻辑

### 步骤 B：语义污染修复

- 在 `src/porosdata_processor/text_cleaner.py` 强化假 `\\Delta` 识别
- 保留真实物理量 `\\Delta`
- 增加跨片段材料式、连字符链的后恢复合并

### 步骤 C：专项测试

- 在 `tests/unit/test_cleaner.py` 补充：
  - inline 坏 `array` 样例
  - 假 `\\Delta` 合金前缀样例
  - 半截材料链样例
  - 真 `\\Delta` 保留样例
- 保留 `tests/unit/test_equation_display_repair.py` 对 display formula 的既有保障

### 步骤 D：审计升级

- 在 `scripts/audit_aiready_data.py` 中补充：
  - `broken_inline_environment`
  - `ref_sticky_protocol`
  - `normalized_ref_count`
  - `raw_citation_count`
- 修复旧的 `raw_citation_protocol` 误报逻辑

---

## 5. 仍需重点复验的点

以下问题虽然已进入修复链，但仍需要在全量输出中复验：

- `00001`：坏 `array` 是否完全消失
- `00001`：`Ni-Nb-Y` 链是否完全恢复
- `00011`、`00013`、`00020`：半截材料式是否仍残留
- citation 审计结果是否还把 `ref[...]` 误判成原始 `[n]`

---

## 6. 最终结论

结合两份文档与当前代码实现，可以确认：

- 上游文档识别的核心问题**确实存在于 Processor 历史输出中**
- 其中 `假 Delta`、常见 `tt/textsf/Ii` 污染、citation 主链路已经具备较强修复能力
- 真正需要继续闭环的是：
  - inline 坏环境降级
  - 半截材料链的跨 token 合并
  - 审计脚本从“抓坏样本”升级为“交付验收”

当前已将上述问题落实为可执行的代码修复、测试补充与审计升级步骤；下一步应以全量重跑与复验结果来判断是否还有残余样本需要继续收尾。
