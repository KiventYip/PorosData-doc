# PorosData Designer 审计报告

- doc_type: reference_report
- status: reference_only
- updated_at: 2026-03-18 09:37:49
- current_contract_note: if this document mentions historical JSONL or prior audit structure, use `docs/ai_ready_and_datamining_designer.md`, `docs/usage_guide.md`, and current `data/structured/*_structured.json` as the active contract.





**审计日期**：2025-03-04  
**审计范围**：`data/structured` 输出数据 + `porosdata_designer` 包功能  
**审计视角**：AI-ready 训练数据要求、数据挖掘（Data Mining）要求

---

## 一、数据产出审计

### 1.1 输出结构概览

| 路径 | 内容 | 用途 |
|------|------|------|
| `full_text/{doc_id}/*_structured.jsonl` | content, pure_text_stream, structured | 文本结构化 + 双视图 |
| `full_text/{doc_id}/*_structured.txt` | 同 content | 人工查看 |
| `multimodal/{doc_id}/*_index.json` | 图文关联索引 | 多模态检索 |
| `multimodal/{doc_id}/fig_*.md` | 单图 Markdown | 图文对 |
| `multimodal/{doc_id}/assets/*.jpg` | 图片资源 | 物理资产 |

### 1.2 AI-ready 数据要求审计

| 要求 | 现状 | 结论 |
|------|------|------|
| **纯净文本流** | `pure_text_stream` 仍含 `<poros_equ>`、`<poros_chem>` 标签 | ❌ 不符合 |
| **可训练格式** | 无 Llama/DeepSeek/JSONL 标准格式输出 | ❌ 缺失 |
| **EOS 终止符** | `content` 含 `</s>`，`pure_text_stream` 已移除 | ⚠️ 不一致 |
| **长度与分块** | 无分块、无 max_length 控制 | ⚠️ 待优化 |
| **多模态对齐** | 文本含 `<poros_asset uuid>`，但 multimodal 索引无 UUID | ❌ 无法跨任务关联 |

**问题详情**：

1. **pure_text_stream 非纯净**  
   - 仍保留 `<poros_equ>$...$</poros_equ>`、`<poros_chem>...</poros_chem>`  
   - AI 训练期望：公式可转为占位符（如 `[FORMULA]`）或自然语言描述，化学式可保留或占位

2. **ExporterRegistry 与流水线脱节**  
   - Llama3Exporter、DeepSeekExporter、MarkdownExporter 依赖 `DocumentModel`  
   - 当前流水线输出为 JSONL（content / pure_text_stream / structured），无 DocumentModel 桥接  
   - 导致 AI 格式导出器未被实际使用

### 1.3 数据挖掘（Data Mining）要求审计

| 要求 | 现状 | 结论 |
|------|------|------|
| **结构化 JSON** | 有 `structured` 字段 | ✅ 具备 |
| **段落/公式/化学式/资产引用** | paragraphs, formulas, chemical_formulas, asset_refs | ✅ 具备 |
| **title 提取** | 因嵌套标签，首个 `poros_title` 匹配失败，得到 "Abstract" | ❌ 错误 |
| **abstract 提取** | 正则未正确匹配含嵌套标签的 abstract | ❌ 为空 |
| **溯源剥离** | 正文中 `[1]`、`[2]` 等引用未剥离 | ❌ 未实现 |
| **full_text ↔ multimodal 关联** | full_text 有 asset uuid，multimodal 无 uuid | ❌ 无法关联 |

**问题详情**：

1. **structured 提取错误**  
   - `title`：正则 `[^<]*` 无法处理 `<poros_title>...<poros_equ>...</poros_title>`，导致匹配到下一个 "Abstract"  
   - `abstract`：`<poros_abstract>` 可能含 `<poros_equ>` 等嵌套，当前正则未考虑

2. **溯源未剥离**  
   - 需求：将 `[1]`、`[2,3]` 等从正文剥离并存入 metadata  
   - 现状：ProvenanceManager 已实现但未接入流水线，引用仍保留在正文

3. **full_text 与 multimodal 无法关联**  
   - full_text 中 `<poros_asset uuid="b90427b6-...">` 使用 uuid5(doc_id, fig_1)  
   - multimodal 的 `00001_index.json` 无 uuid 字段  
   - 无法通过 uuid 做跨任务检索（如文本→图、图→文本）

---

## 二、Designer 包功能审计

### 2.1 模块与流水线集成状态

| 模块 | 已实现 | 已接入流水线 | 说明 |
|------|--------|--------------|------|
| SchemaValidator | ✅ | ⚠️ 部分 | 仅日志告警，未阻断或写入 metadata |
| ChemicalFormulaParser | ✅ | ❌ | 未在 pipeline 中调用 |
| LaTeXValidator | ✅ | ❌ | 未用于段落质量标记 |
| AssetAnchoringEngine | ✅ | ✅ | 已接入 run_text_standardization |
| ProvenanceManager | ✅ | ❌ | 未接入 |
| DataMiningMapper | ✅ | ✅ | 已接入，但 pure_text 逻辑不完整 |
| DataAuditor | ✅ | ❌ | 依赖 DocumentModel，与当前输出不兼容 |
| ExporterRegistry | ✅ | ❌ | 未与 JSONL 输出桥接 |

### 2.2 核心职责达成情况

| 职责 | 达成度 | 说明 |
|------|--------|------|
| Schema 强制校验 | 60% | 有校验逻辑，结果未写入输出或阻断 |
| 多模态资产锚定 | 80% | 文本侧有 UUID 标签，multimodal 侧缺 UUID |
| 实体属性化 | 40% | ChemicalFormulaParser 未接入，poros_chem 未结构化 |
| 溯源管理 | 20% | ProvenanceManager 未接入 |

### 2.3 优化功能达成情况

| 功能 | 达成度 | 说明 |
|------|--------|------|
| 合金成分解析器 | 30% | 模块存在，未接入；Delta 修复在 TextAggregator 中 |
| 资产穿透引擎 | 85% | 文本替换完成，multimodal 无 uuid 回写 |
| 公式语法校验 | 20% | LaTeXValidator 未接入 |
| 数据挖掘字段映射 | 60% | 有双视图，pure_text 不纯净、structured 提取有误 |

---

## 三、待优化项汇总

### 3.1 高优先级（影响 AI-ready / 数据挖掘）

1. **pure_text_stream 真正纯净化**  
   - 将 `<poros_equ>...</poros_equ>` 转为占位符（如 `[FORMULA]`）或保留 LaTeX 原文（视训练需求）  
   - 将 `<poros_chem>...</poros_chem>` 转为占位符或保留原文  
   - 或提供「纯文本 / 保留公式」两种模式

2. **structured 提取修复**  
   - title：支持嵌套标签（如 `<poros_title>...<poros_equ>...</poros_title>`）  
   - abstract：同上，或使用递归/栈式解析

3. **full_text 与 multimodal 的 UUID 关联**  
   - 在 `00001_index.json` 每项增加 `uuid` 字段（与 AssetAnchoringEngine 的 uuid5 一致）  
   - 便于跨任务检索与多模态对齐

4. **DocumentModel 桥接或替代**  
   - 方案 A：从 content/structured 构建 DocumentModel，接入 ExporterRegistry  
   - 方案 B：新增直接基于 JSONL 的 AI 格式导出（Llama/DeepSeek JSONL），不依赖 DocumentModel

### 3.2 中优先级（增强功能完整性）

5. **ProvenanceManager 接入**  
   - 在聚合后对正文做 `extract_and_strip`  
   - 将引用列表写入 metadata，正文中移除 `[1]`、`[2]` 等

6. **LaTeXValidator 接入**  
   - 对段落做公式校验  
   - 将 `low_quality_paragraphs` 写入 metadata

7. **ChemicalFormulaParser 接入**  
   - 对 `poros_chem` 内容调用 parser，输出结构化字典  
   - 写入 structured 或单独 metadata 字段

8. **Schema 校验结果写入**  
   - 将 SchemaValidationResult 写入 JSONL 的 metadata  
   - 便于质量审计与过滤

### 3.3 低优先级（体验与扩展）

9. **multimodal fig_*.md 增加 uuid**  
   - 在 Markdown 中增加 doc_id、uuid 等元信息，便于检索

10. **分块与长度控制**  
    - 提供按 token 或字符的分块选项  
    - 支持 max_length 截断，便于长文档训练

11. **IFW 等机构缩写误标**  
    - 将 IFW 等加入 abbreviation_blacklist，避免误标为 poros_chem

---

## 四、审计结论

**整体评分**：**65/100**

- **AI-ready**：当前 `pure_text_stream` 仍含标签，且无标准 AI 格式输出，与训练就绪仍有差距。  
- **数据挖掘**：`structured` 字段具备，但 title/abstract 提取错误、溯源未剥离、跨任务关联缺失。  
- **Designer 包**：骨架定义与资产链接方向正确，但 ChemicalFormulaParser、LaTeXValidator、ProvenanceManager 未接入，ExporterRegistry 与流水线脱节。

**建议优先顺序**：  
1）修复 pure_text 与 structured 提取；  
2）建立 full_text ↔ multimodal 的 UUID 关联；  
3）接入 ProvenanceManager、LaTeXValidator；  
4）建立 DocumentModel 桥接或替代方案，打通 AI 格式导出。