# 标题语义化与区块封装：修复步骤与逻辑

- doc_type: design_reference
- status: reference_only
- updated_at: 2026-03-18 09:37:49
- current_contract_note: if this document mentions historical JSONL or prior audit structure, use `docs/ai_ready_and_datamining_designer.md`, `docs/usage_guide.md`, and current `data/structured/*_structured.json` as the active contract.



**目标**：将原始的统一 `<poros_title>` 转化为带语义属性的嵌入式标签，并做区块封装，以支持长程逻辑链的 Mean NLL 评估。

---

## 一、结构化指令：Content-Level Semantic Wrapping（见题开箱，见新题封箱）

Designer 在处理时须遵循 **“见题开箱，见新题封箱”** 原则：

- **见题开箱**：当检测到某一级标题（如 Abstract、1. Introduction、2. Experimental）时，开启对应的 `<poros_section_{type}>`，并紧接着写入 `<poros_title_{type}>标题文本</poros_title_{type}>`。
- **吸纳内容**：将该标题之后、**下一个一级标题之前**的所有 `<poros_paragraph>`（以及若有子标题则 `<poros_subtitle_level2>` 等）全部收入当前 section 内。
- **见新题封箱**：在进入下一个一级标题之前，必须闭合当前 section：`</poros_section_{type}>`，作为该逻辑块的**强 EOS**；再为新标题开新箱。

### 以 Abstract 为例的完整指令

**[Instruction: Content-Level Semantic Wrapping]**

- **识别起点**：当检测到文本为 “Abstract” 时，开启 `<poros_section_abstract>`。
- **嵌入标题**：紧接着写入 `<poros_title_abstract>Abstract</poros_title_abstract>`。
- **吸纳内容**：将原文中属于摘要的所有 `<poros_paragraph>`（即到下一个一级标题如 “1. Introduction” 之前的所有内容）全部收入该 section 内。
- **强制闭合 (EOS)**：在进入 “1. Introduction” 之前，必须闭合 `</poros_section_abstract>`。

**目标结构**：

```xml
<poros_section_abstract>
  <poros_title_abstract>Abstract</poros_title_abstract>
  <poros_paragraph>Bulk metallic glasses developed in last 15 years... [cite: 213]</poros_paragraph>
  <poros_paragraph>The experimental results confirm... [cite: 226]</poros_paragraph>
</poros_section_abstract>
```

其他 section（Introduction、Experimental、Results、Conclusion、References 等）按同一规则：**见题开箱 → 嵌标题 → 吸纳至下一一级标题前 → 见新题封箱**。

---

## 二、需求规则摘要


| 规则                          | 要求                                                                                                                |
| --------------------------- | ----------------------------------------------------------------------------------------------------------------- |
| **标题语义化**                   | 识别 `<poros_title>` 内关键词（Abstract, Introduction, Experimental, Results, Conclusion 等），重命名为 `<poros_title_{type}>`。 |
| **原位保留**                    | 禁止将标题提升至文档头部；标题必须保留在其在正文中对应的物理位置之前，作为后续文本预测的 Context 锚点。                                                          |
| **区块封装 (Section Wrapping)** | 以标题为界，将后续段落封装在 `<poros_section_{type}>` 内；闭合符 `</poros_section_{type}>` 作为该逻辑块的强 EOS 标记。                          |
| **层级保留**                    | 子标题（如 3.1, 3.2）使用 `<poros_subtitle_level2>` 标注，保留知识推理的层级深度。                                                       |


---

## 三、当前状态与差距

### 2.1 当前输出结构（TextAggregator）

- 按**类型分组**输出：先输出**所有** `<poros_title>...</poros_title>`，再 `<poros_keywords>`，再 `<poros_main_text>`（内部为平铺的 `<poros_paragraph>`）。
- 标题与正文**物理顺序被打破**：例如 “2. Experimental” 出现在文档前部，而对应正文在 `poros_main_text` 中靠后，无法作为“后续段落”的 Context 锚点。
- 无 `<poros_section_*>`，无 `<poros_title_{type}>`，无 `<poros_subtitle_level2>`。

### 2.2 目标结构示例

```xml
<poros_section_experimental>
<poros_title_experimental>2. Experimental</poros_title_experimental>
<poros_paragraph>BMGs were prepared in form of rods... [cite: 36, 445, 638]</poros_paragraph>
<poros_paragraph>...</poros_paragraph>
</poros_section_experimental>
```

子标题示例（层级保留）：

```xml
<poros_section_results>
<poros_title_results>3. Results</poros_title_results>
<poros_subtitle_level2>3.1. Short-range order of bulk metallic glasses</poros_subtitle_level2>
<poros_paragraph>...</poros_paragraph>
<poros_subtitle_level2>3.2. Thermal behavior of bulk metallic alloys</poros_subtitle_level2>
<poros_paragraph>...</poros_paragraph>
</poros_section_results>
```

---

## 四、语义类型与关键词映射

建议在配置或代码中维护「标题文本/模式 → type」的映射，用于生成 `poros_title_{type}` 与 `poros_section_{type}`：


| type                  | 关键词/模式示例                                                     | 说明                                                                           |
| --------------------- | ------------------------------------------------------------ | ---------------------------------------------------------------------------- |
| `abstract`            | Abstract                                                     | 摘要                                                                           |
| `introduction`        | Introduction, 1 Introduction                                 | 引言                                                                           |
| `experimental`        | Experimental, 2 Experimental, Methods, Materials and Methods | 实验/方法                                                                        |
| `results`             | Results, 3 Results                                           | 结果                                                                           |
| `discussion`          | Discussion, 4 Discussion                                     | 讨论                                                                           |
| `conclusion`          | Conclusion(s), 5 Conclusion(s)                               | 结论                                                                           |
| `acknowledgements`    | Acknowledgement(s)                                           | 致谢                                                                           |
| `references`          | References, Bibliography                                     | 参考文献                                                                         |
| `title` 或 `doc_title` | 文档主标题（首条且无数字前缀）                                              | 可保留为 `<poros_title>` 或 `<poros_title_doc>`                                   |
| （未匹配）                 | 其他                                                           | 可落为 `section` 或 `subsection`，或保留 `poros_title` 并包在 `poros_section_section` 中 |


**子标题层级**：

- 匹配模式如 `^\d+\.\d+\.`（3.1., 3.2.）→ `<poros_subtitle_level2>`，其后续段落归属当前父 section，直至下一同级或更高级标题。
- 若有 `^\d+\.\d+\.\d+\.` → 可扩展 `<poros_subtitle_level3>`。

---

## 五、修复步骤与实现逻辑

实现时必须落实 **一、结构化指令** 中的“见题开箱，见新题封箱”及 Abstract 示例的四个动作（识别起点、嵌入标题、吸纳内容、强制闭合）。

### 步骤 1：在聚合阶段保留「文档顺序」与「标题–段落」归属

**逻辑**：

- 当前 `TextAggregator` 的 `_merge_parts` 按 `ParagraphType` 分组后，按固定类型顺序（TITLE → ABSTRACT → … → MAIN_TEXT）输出，导致标题与正文分离。
- **修改方向**：在聚合前或聚合时，产出**带顺序的流式结构**，使每个「标题 + 其后的段落」成组，且整体顺序与原文一致。

**可选实现**：

- **方案 A（推荐）**：在 `TextAggregator` 内，不再按 type 大块合并，而是按 **content_list 的遍历顺序** 输出。每遇到一个 TITLE/ABSTRACT/CONCLUSION/REFERENCES 或 MAIN_TEXT 中的“节标题”段落，就开启一个新的逻辑块；遇到正文段落则挂到当前块。这样天然满足「原位保留」。
- **方案 B**：保持现有“先标题后 main_text”的中间表示，再增加**后处理步骤**：根据标题文本与 main_text 内段落顺序，通过规则或简单匹配（如标题数量与“节”的对应关系）重新拼接成「标题 + 段落」序列。难度与脆弱度较高，仅作备选。

**输出中间表示建议**：  
`[(block_type, content)]`，其中 `block_type` 为 `"title"|"subtitle_l2"|"subtitle_l3"|"paragraph"|"abstract"|"keywords"|"conclusion"|"references"`，且每个 title/subtitle 后紧跟其所属 paragraph 列表，便于步骤 2、3。

---

### 步骤 2：标题语义化 —— 为每个标题打上 type

**逻辑**：

- 对每个标题块，取其**内部文本**（如 "2. Experimental"、"Abstract"、"3.1. Short-range order..."）。
- 用**关键词/正则**匹配上表，得到 `type`（如 `experimental`、`abstract`、`results`）。
- 子标题（如 3.1.）不参与 section 的 type 命名，仅标记为 `subtitle_level2`（或 level3）；其所属 section 的 type 由**前一个一级标题**决定（如 "3. Results" → `results`）。

**输出**：

- 一级标题：`<poros_title_{type}>原始标题文本</poros_title_{type}>`。
- 子标题：`<poros_subtitle_level2>3.1. ...</poros_subtitle_level2>`（不改为 `poros_title_`*，以保留层级语义）。

**边界**：

- 未匹配到任何 type 的标题：可统一为 `<poros_title_section>` 与 `<poros_section_section>`，或保持 `<poros_title>` 并包在 `poros_section_section` 中。

---

### 步骤 3：区块封装 —— 用 `<poros_section_{type}>` 包裹「标题 + 后续段落」

**逻辑**：

- 每个**一级标题**（或 abstract/conclusion/references 等单块）开启一个 `<poros_section_{type}>`。
- 该 section 内顺序为：  
`开标签` → `本标题（poros_title_{type} 或 poros_subtitle_level2）` → `后续段落（poros_paragraph）` → 若遇下一级子标题则 `poros_subtitle_level2` → 其段落 → … → `闭标签`。
- `</poros_section_{type}>` 即该逻辑块的**强 EOS**，用于 Mean NLL 时作为块边界。

**规则**：

- 遇到**新的一级标题**（新的 section type）时，先关闭上一个 `</poros_section_...>`，再开新的 `<poros_section_{type}>`。
- Abstract / Conclusion / References 通常为单块，各自一个 section；若原文中它们与前后有明确顺序，也按「原位保留」插入到正确位置，不提前、不拖后。

---

### 步骤 4：层级保留 —— 子标题不开启新 section，只插入 subtitle 标签

**逻辑**：

- 形如 "3.1.", "3.2." 的标题不开启新的 `<poros_section_*>`，只输出 `<poros_subtitle_level2>...</poros_subtitle_level2>`，其后的段落仍属于当前 section（如 `poros_section_results`）。
- 若存在 "3.1.1." 等，可用 `<poros_subtitle_level3>`，逻辑同上。

---

### 步骤 5：Schema 与审计适配

**逻辑**：

- `SchemaValidator` 的 `TAG_HIERARCHY` 需扩展：允许 `poros_doc` 下出现 `poros_section_`*；`poros_section_*` 内允许 `poros_title_*`、`poros_subtitle_level2`、`poros_subtitle_level3`、`poros_paragraph`（及既有 poros_chem、poros_equ、poros_asset）。
- 若保留 `poros_main_text` 等旧标签，需约定其与 `poros_section_*` 的兼容策略（二选一或并存）；若全面切到 section 流，则审计脚本与文档中“根下直接 main_text”的假设需同步改为“根下为若干 poros_section_*”。
- LaTeX/EOS 等校验仍作用于全文；`</poros_section_{type}>` 作为**块内**强 EOS，文档末尾仍保留全局 `</s>`。

---

## 六、实现顺序建议

1. **配置/常量**：在 `config` 或 `text_aggregator` 中定义「标题关键词/正则 → type」映射及子标题层级正则。
2. **顺序流**：修改 TextAggregator（或等价模块），使输出按**文档顺序**的「标题/子标题 + 段落」流，不再“所有标题在前、所有正文在后”。
3. **语义化**：对每个标题文本做 type 识别，写出 `<poros_title_{type}>` 或 `<poros_subtitle_level2>`。
4. **封装**：按上述规则在每段一级标题（及 abstract/conclusion/references）处插入 `<poros_section_{type}>` 与 `</poros_section_{type}>`。
5. **Schema 与审计**：更新 TAG_HIERARCHY 与审计脚本，使新标签合法且可校验。
6. **测试**：用现有 00001 等文档跑通 pipeline，检查输出满足示例结构，且 Mean NLL 评估能识别块边界。

---

## 七、示例：修复前后对比（片段）

**修复前（当前）**：

```xml
<poros_title>2. Experimental</poros_title>
<poros_title>3. Results</poros_title>
...
<poros_main_text>
<poros_paragraph>BMGs were prepared...</poros_paragraph>
...
</poros_main_text>
```

**修复后（目标）**：

```xml
<poros_section_experimental>
<poros_title_experimental>2. Experimental</poros_title_experimental>
<poros_paragraph>BMGs were prepared in form of rods...</poros_paragraph>
<poros_paragraph>...</poros_paragraph>
</poros_section_experimental>
<poros_section_results>
<poros_title_results>3. Results</poros_title_results>
<poros_subtitle_level2>3.1. Short-range order of bulk metallic glasses</poros_subtitle_level2>
<poros_paragraph>...</poros_paragraph>
...
</poros_section_results>
```

---

## 八、与现有交付标准的关系

- 本方案引入新标签（`poros_section_*`、`poros_title_*`、`poros_subtitle_level2/3`），与 `docs/ai_ready_and_datamining_designer.md` 中“Poros 骨架”的扩展一致，需在**五、七、十一**中补充或引用本文档，约定上述标签为可选或必选（视产品线要求）。
- 现有 JSONL 的 `content`、`pure_text_stream`、`structured` 若依赖当前标签集，需同步扩展解析与导出逻辑，使新标签被正确保留或映射。
