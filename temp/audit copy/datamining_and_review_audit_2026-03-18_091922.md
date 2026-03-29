# 数据提交审计：Data Mining 与第三方 Review 就绪性

> Historical reference notice
>
> - doc_type: audit
> - status: historical_reference
> - created_at: 2026-03-18 09:19:22
> - updated_at: 2026-03-18 09:39:32
> - current_repo_layout: `data/raw`, `data/processed`, `data/structured`, `tests/`
> - current_effective_docs: `docs/usage_guide.md`, `docs/deployment_guide.md`, `docs/ai_ready_and_datamining_designer.md`
> - compatibility_notice:
>   - historical paths like `data/mineru_output_raw_data`, `data/processed_data`, `data/structured_data` have been renamed.
>   - historical test path `src/porosdata_designer/tests/` has moved to `tests/`.
>   - historical script `scripts/audit_structured.py` should be read as `scripts/audit_structured_data.py`.
>   - current structured output contract centers on `*_structured.json`; `*_structured.txt` remains as the readable companion export.


**审计日期**：2026-03-15  
**审计对象**：`data/`（含 `processed`、`structured`）  
**依据文档**：[ai_ready_and_datamining_designer.md](../ai_ready_and_datamining_designer.md)  
**审计目的**：判定当前数据是否可提交给数据挖掘（Data Mining）及第三方评审（Third-party Review）使用。

---

## 一、审计结论摘要

| 维度 | 结论 | 说明 |
|------|------|------|
| **Designer 交付（结构化）** | ✅ **符合** | 目录、Poros 标签、JSONL 必选字段、EOS、多模态索引与资产均满足文档要求 |
| **Data Mining Ready** | ⚠️ **有条件符合** | 结构就绪，但存在残留 OCR/实体一致性问题，可能影响实体抽取与归并 |
| **AI-Ready（文本质量）** | ⚠️ **部分符合** | 部分文档存在元素符号断裂、公式/化学式书写不一致，对 LLM/Embedding 有轻微噪音 |
| **第三方 Review 可提交性** | ✅ **可提交** | 建议附带本报告及“已知问题清单”，便于评审方按预期使用 |

**总体结论**：数据**可以提交**给数据挖掘与第三方评审使用；建议在提交说明中注明残留的 Processor 层问题（见下文），并在后续版本中修复以提升 Data Mining 与 AI 使用效果。

---

## 二、依据文档的逐项核对

### 2.1 Designer 交付要求（文档五、七、十一）

| 条款 | 要求 | 检查结果 |
|------|------|----------|
| 五.1 输出目录与产物 | full_text：`{doc_id}_structured.txt`、`{doc_id}_structured.jsonl`；multimodal：`{doc_id}_index.json`、fig_n.md、assets | ✅ 5 个文档（00001–00005）均存在上述文件 |
| 五.2 Poros 标签与 Schema | 根标签 `<poros_doc>`/`</poros_doc>` 存在，标签闭合与嵌套合法 | ✅ 抽样 00001、00002 及历史审计结论：符合 |
| 五.3 双视图与必选字段 | JSONL 含 doc_id、content、pure_text_stream、structured | ✅ 00001_structured.jsonl 抽样确认四字段齐全 |
| 五.4 公式、EOS、化学式语义 | 公式定界符平衡、文档末尾 EOS（如 `</s>`）、structured 中化学式无非化学缩写 | ✅ 全部 5 个 txt 末尾为 `</poros_doc></s>`；历史审计通过 LaTeX/化学式检查 |
| 五.5 多模态索引与资产 | 索引含 image_path、fig_id、caption、mentions、metadata、asset_copied、markdown_file；与 assets 一致 | ✅ 00001_index.json 等抽样：字段完整，asset_copied 与物理文件一致 |

Designer 交付部分满足《ai_ready_and_datamining_designer.md》要求，可用于下游消费与验收。

### 2.2 Processor 数据质量与 AI-Ready / Data Mining Ready（文档二、四、六、九）

- **AI-Ready（文档二.1）**：要求文本干净、语义主体清晰、数值/单位/术语可读、Token 效率合理。  
  **检查**：整体可读，但存在以下**残留问题**（属 Processor 职责范围）：
  - **元素符号断裂/混写**（违反文档六“化学实体纠错”、四“实体清晰性”）  
    - 示例（00001）：`<poros_equ>$Z \mathbf{r} -$</poros_equ>`（应为 Zr）、`<poros_chem>$\mathbf{Ni -}$</poros_chem> <poros_chem>$Nb {- Y}}$</poros_chem>`（Ni–Nb–Y 断裂且有多余 `}`）。  
    - 同一文档内 “Zr” 存在 `Z \mathbf{r}` 与正常写法混用，影响**实体一致性**与检索/聚类。
  - **公式/化学式局部噪音**：如 `$Nb {- Y}}$` 中 `{-` 与多余闭合括号，可能对 LaTeX 解析或规则抽取造成边缘影响。

- **Data Mining Ready（文档二.2、九）**：要求实体名称稳定、数值/单位可识别、属性-值关系未破坏、适合构造 JSON/表/知识图谱。  
  **检查**：  
  - 结构化输出（content、pure_text_stream、structured）**具备**上下文锚点与属性-值邻近关系，未因标签化打散。  
  - **实体完整性**：同一文档内材料名、化学式存在上述混写，可能增加归并与标准化成本，建议在提交说明中注明。

- **元数据字段（图注/表题）**（文档四.5）：图注等已进入多模态 caption 与索引，未发现明显遗漏。

### 2.3 禁止破坏项（文档十）

- 根标签缺失、标签闭合/嵌套错误、公式结构破坏、缺 EOS 或 JSONL 必选字段、化学式含非化学缩写、多模态缺字段或资产不一致：**未发现**。 ✅

---

## 三、已知问题清单（建议随数据一并提交）

以下问题不影响“可提交性”，但建议在提交包中附带说明，便于数据挖掘与第三方评审按预期使用与解释结果。

| 类型 | 位置示例 | 描述 | 建议 |
|------|----------|------|------|
| 元素符号断裂/混写 | 00001 全文 | Zr 写为 `$Z \mathbf{r} -$` 或 `Z \mathbf{r}`；Ni–Nb–Y 写为 `$\mathbf{Ni -}$` + `$Nb {- Y}}$` | Processor 层统一为 Zr、Ni–Nb–Y 等稳定写法 |
| 化学式/公式局部错误 | 00001 | `$Nb {- Y}}$` 多余 `}`、`{-` 连字符 | 修复为 `Nb–Y` 或等价规范形式 |
| 术语一致性 | 00001 | “Zr-based” 与 “Z \mathbf{r} -based” 等混用 | 文档内统一术语与连字符规范 |

---

## 四、数据范围与可交付物

- **processed**：5 个文档，processing_report.json 显示 5/5 成功，有控制字符清理等记录，无错误列表。  
- **structured**：  
  - **full_text**：5 个 doc_id，各含 `*_structured.txt`、`*_structured.jsonl`。  
  - **multimodal**：5 个 doc_id，各含 `*_index.json`、fig_*.md、assets 下图片。  

以上均可作为数据挖掘与第三方评审的交付范围。

---

## 五、建议的提交方式

1. **可提交**：将 `data/processed` 与 `data/structured` 按现有结构打包，提交给数据挖掘与第三方评审。  
2. **随包附带**：  
   - 本审计报告（`docs/audit/datamining_and_review_audit_2026-03-18_091922.md`）。  
   - 已知问题清单（上表），并说明属 Processor 层残留，不影响结构化约定与多模态一致性。  
3. **后续改进**：在 Processor 流水线中增加“元素符号纠错”与“同一文档术语一致性”处理，以更好满足文档二、四、六、九条，提升 Data Mining 与 AI 使用效果。

---

## 六、结论

- **数据挖掘**：当前数据**可以提交**；结构化与多模态满足文档要求，实体/术语层面有已知残留问题，建议在说明中注明并在后续版本修复。  
- **第三方 Review**：当前数据**可以提交**；建议附带本审计报告与已知问题清单，以便评审方理解数据边界与质量现状。

以上审计依据《ai_ready_and_datamining_designer.md》中的 Designer 交付要求、Processor 数据质量要求、AI-Ready 与 Data Mining Ready 定义及禁止破坏项执行。