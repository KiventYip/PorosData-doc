# AI-Ready 与 Data Mining 数据质量审计报告

> 仓库变更说明（2026-03-17 后）：当前仓库统一批处理入口为 `porosdata-processor` / `python -m porosdata_processor`，`academic_tools/` 已移除，源码仓运行入口保留 `examples/run_pipeline.py`，数据目录已统一为 `data/raw` 与 `data/processed`。本文为历史审计归档，正文若出现旧路径、旧脚本或旧目录命名，均表示审计发生时的仓库状态。

**审计依据**：`docs/ai_ready_and_data_mining_delivery_standard.md`  
**审计对象**：`data/processed` 下所有 `*_content_list.json`  
**执行时间**：2026-03-15  
**审计脚本**：`scripts/audit_aiready_data.py`  
**结果数据**：`docs/audit/aiready_data_audit_result.json`

---

## 1. 审计目的与范围

依据《科学数据处理参考文档：AI-Ready 与 Data Mining 交付标准》，对 Processor 输出数据做一次 **code audit**，确保 `data` 符合以下要求：

- **AI-Ready**：文本干净、语义清晰、数值/单位/公式可读，Token 使用合理。
- **Data Mining Ready**：实体稳定、属性-值可识别、上下文锚点保留、噪音最小化。
- **交付范围**：正文 `text`，以及图注/图脚注、表题/表脚注（`image_caption`、`image_footnote`、`table_caption`、`table_footnote`）等元数据字段均属质量交付范围。

本报告对 **processed_data** 中 5 份文档的 content_list 进行自动化核查与人工可读结论汇总。

---

## 2. 核查维度与方法

| 维度 | 检查内容 | 方法 |
|------|----------|------|
| **文本连续性** | 数字内空格、小数点断裂、数值与单位断裂、元素符号断裂 | 正则匹配文档中的“错误示例”形态 |
| **公式与符号** | 行内/显示公式 `$` 配对、LaTeX 明显损坏 | `$` 奇偶性；`\mathrm{ x y }` 等残留空格 |
| **元数据覆盖** | 图/表项是否具备 caption、footnote 字段 | 统计 type=image/table 及对应字段存在性 |
| **拒收条件** | 大量 OCR 断裂、公式损坏、关键字段未清洗、处理不一致 | 汇总触发的规则与数量 |

脚本对每条 `text` 及 `image_caption`、`image_footnote`、`table_caption`、`table_footnote` 的每个片段执行上述检查，并汇总到文档级与全局。

---

## 3. 审计结果摘要

（以下数据来自 `aiready_data_audit_result.json` 最近一次运行。）

| 指标 | 数值 |
|------|------|
| 审计文件数 | 5 |
| 总文本片段数 | 263 |
| 存在 OCR 残留的片段数 | 7 |
| 存在未闭合 `$` 的片段数 | 0 |
| 图片项数量 | 41 |
| 表格项数量 | 1 |
| 图片含 caption | 41 |
| 图片含 footnote | 0 |
| 表格含 caption | 1 |
| 表格含 footnote | 0 |

**OCR 残留按类型**：

| 类型 | 说明 | 出现次数 |
|------|------|----------|
| `mathrm_space_letters` | 公式内 `\mathrm{ x y }` 形态（单位/字母间空格） | 11 |
| `mathrm_space_ll` | `\mathrm{ a b }` 小写字母间空格 | 6 |
| `element_like_break` | 疑似元素符号断裂（如 `N i`） | 1 |

**结论摘要**：

- **公式结构**：未发现未闭合 `$`，行内/显示公式配对检查通过。
- **元数据覆盖**：所有图片项均含 `image_caption`；唯一表格项含 `table_caption`。图脚注/表脚注在样本中多为空，属数据源特性，非遗漏清洗。
- **文本连续性**：仍有少量 OCR 残留，集中在 **公式内 `\mathrm{}` 字母间空格**（如 `\mathrm{r g}`、`\mathrm{k i}`、`\mathrm{a t}`）及 1 处疑似元素断裂（`N i`）。数量有限（7 个片段、18 处匹配），未达“大量可见 OCR 断裂”的拒收线，但需在后续迭代中修复以完全符合文档“物理量聚合/化学实体纠错”要求。

---

## 4. 逐文档结果

| 文档 | 路径片段 | 条目数 | OCR 问题类型 | 样例 | 未闭合 `$` |
|------|----------|--------|--------------|------|------------|
| 00001 | .../00001/auto/00001_content_list.json | 74 | mathrm_space_letters(3), element_like_break(1) | `\mathrm{r g`, `N i ` | 0 |
| 00002 | .../00002/auto/00002_content_list.json | 62 | mathrm_space_letters(6), mathrm_space_ll(4) | `\mathrm{k i ` | 0 |
| 00003 | .../00003/auto/00003_content_list.json | 44 | 无 | — | 0 |
| 00004 | .../00004/auto/00004_content_list.json | 49 | mathrm_space_letters(2), mathrm_space_ll(2) | `\mathrm{a t ` | 0 |
| 00005 | .../00005/auto/00005_content_list.json | 34 | 无 | — | 0 |

00003、00005 未检出 OCR 残留；00001、00002、00004 存在公式内单位/字母空格残留，建议在公式清洗规则中增加对 `\mathrm{ x y }` 的收紧（在保证结构安全前提下）。

---

## 5. 与验收标准对照

依据 `docs/ai_ready_and_data_mining_delivery_standard.md` 第九节“质量验收标准”与“拒收条件”：

| 验收项 | 要求 | 审计结果 |
|--------|------|----------|
| 无明显 OCR 断裂数字 | 数字内部/小数点/单位间无断裂 | **部分满足**：正文与元数据中数字级断裂已较少，公式内 `\mathrm{}` 仍有字母间空格 |
| 无明显断裂单位 | 单位连续、统一协议 | **部分满足**：单位断裂多为公式内 `\mathrm{ r g }` 等，需在公式清洗中统一 |
| 无明显术语碎裂 | 材料名、元素符号等连续 | **基本满足**：仅 1 处 `N i` 疑似元素断裂 |
| 无结构性公式损坏 | 行内/显示公式结构完整、`$` 配对 | **满足**：未闭合 `$` 为 0 |
| 关键元数据字段已处理 | 图注/表题/脚注纳入清洗 | **满足**：图注、表题字段存在且已参与同一套清洗链路 |
| 文本适合 AI 与规则处理 | 可读、可抽取 | **满足**：整体可读，残留为局部可修复点 |

**拒收条件检查**：

- “Processor 输出仍存在**大量**可见 OCR 断裂”——当前为少量（7 片段/18 处），未达“大量”，**未触发**。
- “公式、符号或编号结构被破坏”——**未触发**。
- “图注/表题/脚注等重要字段未进入质量清洗范围”——**未触发**；字段存在且与正文同流程。
- “相同类型问题在不同字段上处理标准不一致”——审计未发现正文与元数据字段间的规则不一致，**未触发**。

---

## 6. 结论与建议

- **总体结论**：当前 `data/processed` 在本次审计下 **基本符合** AI-Ready 与 Data Mining 文档的交付要求，未触发拒收条件；公式结构完好，元数据覆盖完整，OCR 残留为少量且集中在公式内 `\mathrm{}` 与个别元素书写。
- **建议**：
  1. **公式内 `\mathrm{}` 空格**：在保证 LaTeX 结构安全的前提下，对 `\mathrm{ x y }` 形态做收紧（如 `\mathrm{r g}` → `\mathrm{rg}`），以完全满足“数值与单位清晰性”和“符号与单位协议”。
  2. **元素符号**：对类似 `N i ` 的断裂做术语/白名单纠错，与文档“化学实体纠错”一致。
  3. **复现与回归**：每次修改清洗逻辑后重新执行 `python scripts/audit_aiready_data.py`，并对比 `docs/audit/aiready_data_audit_result.json`，确保无新增 OCR 残留或公式损坏。

---

*报告由 `scripts/audit_aiready_data.py` 生成结果并人工整理，审计标准以 `docs/ai_ready_and_data_mining_delivery_standard.md` 为准。*
