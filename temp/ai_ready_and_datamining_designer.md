## 科学数据处理参考文档：AI-Ready 与 Data Mining 交付标准

### 一、文档目标

本标准用于定义科学文献数据在进入 AI 与数据挖掘链路前的质量要求，明确 `Processor` 与 `Designer` 两个包的职责边界，并给出可执行、可验收、可追溯的数据交付标准。

本标准强调：

- `Processor` 是**数据质量包**，负责把原始 OCR / MinerU 输出清洗成**清晰、稳定、可读、可计算**的数据。
- `Designer` 是**数据结构化包**，负责把 `Processor` 输出进一步转换为**结构化对象、字段、关系和数据库记录**。

换言之：

- `Processor` 解决的是“数据是否干净、是否可靠、是否适合进一步处理”。
- `Designer` 解决的是“数据如何被建模、抽取、映射和组织成结构化结果”。

`Processor` 不以生成最终数据库结构为目标，但必须为 `Designer` 提供足够高质量、低歧义、低噪音的输入。

---

### 二、核心定义：什么是“就绪”？

#### 1. AI-Ready

AI-Ready 指数据满足以下条件：

- 文本足够干净，能够直接输入 LLM 或 Embedding 模型而不会产生明显格式噪音干扰。
- 语义主体清晰，不因 OCR 断裂、错位空格、乱码、异常引用符号而降低模型理解质量。
- 数值、单位、术语、行内公式保持可读，且不会因清洗引入新的歧义。
- Token 使用效率合理，不因重复噪音或非语义碎片造成无意义膨胀。

#### 2. Structure-Aware Training Ready

Structure-Aware Training Ready 指数据满足以下条件：

- 允许在训练视图中保留稳定、可解释、可闭合的结构标签，用作大模型长文本训练时的显式语义边界信号。
- `section`、`title`、`subtitle` 等标签的设计目标是保留专业文献的结构语义，而不是模拟原始排版外观。
- `</poros_section_{type}>` 可视为段级或块级的**强边界信号**，其作用类似逻辑块的 EOS，但不替代文档末尾的全局 EOS token。
- 标签的价值在于帮助模型识别“哪一部分属于摘要、方法、结果、结论、图表引用或公式语义”，而不是增加无意义格式噪音。
- 只有当标签稳定、语义一致、嵌套安全时，才可将其作为训练增强信号；若标签损坏或漂移，则应视为质量问题。

#### 3. Plain-Text Training Ready

Plain-Text Training Ready 指数据满足以下条件：

- 文本可直接作为自然语言序列输入模型，而不依赖任何 `poros_*` 结构标签才能被理解。
- `pure_text_stream` 中不得残留 XML 包装、section/title/subtitle 标签或其他结构控制标记。
- 公式、化学式、图表引用在纯文本视图中的保留方式须全语料一致，避免同一语义在不同文档中采用不同转写策略。
- 纯文本视图中的结构信息应通过自然分段、稳定空白或约定好的纯文本占位体现，而不是依赖结构标签泄漏。
- 若下游任务是 Embedding、纯文本继续预训练、检索或通用语言建模，应优先消费 Plain-Text Training Ready 的视图。

#### 4. Data Mining Ready

Data Mining Ready 指数据满足以下条件：

- 实体名称稳定，术语、材料名、实验名在同一文档内尽量保持一致。
- 数值、单位、属性可以被规则或模型稳定识别。
- 属性与对应值、条件、上下文之间的关系未被清洗破坏。
- 文本适合进一步构造 JSON、表结构、知识图谱、关系三元组或其他结构化表达。

---

### 三、Processor 与 Designer 的职责边界

#### 1. Processor 的职责：数据质量交付

`Processor` 的核心任务不是“生成结构化结果”，而是交付高质量基础数据。其最低要求包括：

- 消除 OCR 造成的非语义空格、断裂、错字和格式噪音。
- 保持材料名、物理量、单位、术语、公式和引用结构的稳定性。
- 保护文本中的上下文锚点，避免因清洗破坏实验条件、属性归属和语义关系。
- 输出适合 AI 阅读、适合规则匹配、适合后续抽取的统一文本。

`Processor` 的交付对象包括但不限于：

- 正文 `text`
- 图注与图脚注 `image_caption`, `image_footnote`
- 表题与表脚注 `table_caption`, `table_footnote`
- 含行内公式的文字片段
- 后续会进入实体抽取或属性抽取的任何文本字段

#### 2. Designer 的职责：结构化组织与重构

`Designer` 的核心任务是在高质量文本基础上进行结构化重构，包括但不限于：

- 实体识别与标准化映射
- 属性-值对抽取
- 条件与上下文归属绑定
- 结构化记录生成
- JSON / 表格 / Knowledge Graph 等目标格式输出

#### 3. 两包之间的协作原则

为了确保包间职责清晰，必须遵守以下原则：

- `Processor` 负责提升数据质量，不应承担最终结构建模职责。
- `Designer` 负责结构化表达，不应再承担大规模 OCR 清洗职责。
- `Processor` 输出必须尽量降低 `Designer` 的歧义解析成本。
- `Designer` 的抽取质量上限，取决于 `Processor` 是否交付了足够清晰的数据。

---

### 四、数据质量交付要求：Processor 必须保证什么

#### 1. 文本连续性

必须修复 OCR 造成的非语义断裂，包括但不限于：

- 数字内部空格：`2 0 0` -> `200`
- 小数点断裂：`0 . 5` -> `0.5`
- 数值与单位断裂：`0 . 0 1 0 n m` -> `0.010nm`
- 元素符号断裂：`N i` -> `Ni`
- 非语义换行导致的碎裂：`110 \n s` -> `110s`

#### 2. 实体清晰性

必须优先保护和修正以下内容：

- 材料名称
- 化学元素与化合物符号
- 物理量名称
- 实验方法与设备名称
- 领域术语

同一术语在同一文档内不得出现会显著影响检索、聚类或识别的混乱写法，例如：

- `Zr based`
- `Zr-based`
- `Zr based BMG`

若这些形式语义相同，`Processor` 应尽可能输出更一致的写法。

#### 3. 数值与单位清晰性

数值与单位必须满足以下要求：

- 数值连续，不允许被 OCR 空格打断。
- 小数结构完整，不允许出现分离式小数点。
- 指数、上下标、符号尽可能保持正确结构。
- 单位必须采用统一协议，不得在同一语料中混乱输出。

#### 4. 公式与符号保护

`Processor` 可以修复公式中的 OCR 冗余空格，但必须遵守“修复优先服从结构安全”的原则：

- 行内公式优先保证结构不损坏。
- 显示公式优先保证块级结构不损坏。
- 上下标、希腊字母、引用命令、LaTeX 命令边界必须被保护。
- 任何无法确认安全的复杂显示公式，不应强行做激进清洗。

#### 5. 元数据字段同样属于质量交付范围

图注、脚注、表题、表脚注虽然不是正文，但同样是数据质量交付的一部分。`Processor` 不应只清洗正文而忽略这些字段，因为它们往往包含：

- 图表编号
- 材料名称
- 实验条件
- 单位与数值
- 行内公式
- 结构化抽取的重要上下文

这些字段若保留大量 OCR 噪音，会直接影响后续 `Designer` 的结构化质量。

---

### 五、数据结构化交付要求：Designer 必须保证什么

#### 1. 输出目录与产物

现阶段 `Designer` 的交付以**分文件视图**为准，而不是单文件 `JSONL` 聚合交付。

- **full_text**：须在 `structured/full_text/{doc_id}/` 下提供 `{doc_id}_structured.txt` 与 `{doc_id}_structured.json`。
- **datamining**：须在 `structured/datamining/{doc_id}/` 下提供 `{doc_id}_datamining.json`，作为数据挖掘视图主产物。
- **multimodal**（若启用）：须在 `structured/multimodal/{doc_id}/` 下提供图文关联索引（如 `{doc_id}_index.json`）、单图 Markdown（`fig_n.md`）及拷贝后的图片资源（`assets/`）。

其中：

- `full_text/{doc_id}_structured.txt` 面向可读检查与直接消费的标签文本。
- `full_text/{doc_id}_structured.json` 面向训练视图消费，承载 `content` 与 `pure_text_stream`。
- `datamining/{doc_id}_datamining.json` 面向结构化抽取、检索与入库，承载章节、公式、化学式与资产引用等结构化结果。

#### 2. Poros 标签与层级规划

必须保证结构化文本符合 Poros 骨架约定，并采用**较粗粒度、稳定优先**的标签体系。

- 须包含根标签 `<poros_doc>` 与 `</poros_doc>`，且成对闭合。
- `poros_section_*` 的闭合标签承担逻辑块结束信号的作用，可作为训练时的块级强边界；文档级结束仍以全局 EOS token 为准。
- 现阶段优先使用少量稳定的大类 section 标签：`header`、`abstract`、`introduction`、`experimental`、`results`、`discussion`、`conclusion`、`acknowledgements`、`references`。
- 对语义不稳定、跨期刊差异大、难以稳定归类的块，一律上收为通用容器 `poros_section_section`，不要继续细分出更多专用标签。
- `Article info`、`Full length article`、`Declaration`、`Supplementary material`、`Appendix`、`Note` 等非稳定章节，默认落入 `poros_section_section`，并在标题文本中保留原始语义。
- 标题标签与 section 粗粒度对齐：稳定大类可用 `poros_title_header`、`poros_title_abstract`、`poros_title_introduction` 等；非稳定章节统一使用 `poros_title_section`。
- 子标题层只保留层级，不再承载细粒度语义类别，现阶段以 `poros_subtitle_level2`、`poros_subtitle_level3` 为主。
- 行内语义标签维持轻量集合：`poros_paragraph`、`poros_equ`、`poros_chem`、`poros_asset`、`poros_keywords`。
- 不得出现未闭合标签、错位嵌套或非法子节点。

#### 3. 分视图契约与必选字段

现阶段三层表达分散在两个主文件中交付：

- `full_text/{doc_id}_structured.json` 须包含字段：`doc_id`、`content`、`pure_text_stream`。
- `content` 为带 Poros 标签的完整文本，是**结构感知训练视图**；允许以字符串数组形式保存。
- `pure_text_stream` 为去标签后的纯净文本流，是**纯文本训练视图**；允许以字符串数组形式保存。
- `datamining/{doc_id}_datamining.json` 为**数据挖掘视图**；须至少包含 `doc_id`、`title`、`sections`，并应同时交付 `formulas`、`chemical_formulas`、`asset_refs` 等辅助结构字段。
- `sections` 中每项用于表达章节标题、段落与子标题层级；当章节语义不稳定时，可使用通用 `section_type = "section"`。
- 若下游训练需要显式结构边界，应优先消费 `content`；若只需要自然文本，应消费 `pure_text_stream`；若需要结构化抽取与索引，应消费 `datamining` 产物。

#### 4. 公式、EOS 与化学式语义

必须保证训练就绪与语义一致：

- 行内公式定界符（如 `$...$`）须成对平衡，不得出现未闭合或错位，经 LaTeX 校验无结构性错误。
- 文档末尾须带项目约定的 EOS token（如 `</s>`），满足下游训练脚本对全局结尾符的期望。
- 当 `content` 使用 `poros_section_*` 时，`</poros_section_{type}>` 用于保留块级语义边界；该信号不替代 `</s>`。
- `datamining` 中的 `chemical_formulas` 须保持高精度语义，只保留化学元素、化合物或稳定材料式。
-  fragility 参数、积分表达式、热力学公式、力学表达式、仪器名、方法名等不得混入 `chemical_formulas`，此类内容应保留在 `formulas`、`sections` 或正文中。

#### 5. 多模态索引与资产一致性（若产出）

若交付 multimodal 产物，须满足：

- 索引文件为 JSON 数组，每项须包含 `image_path`、`fig_id`、`caption`、`mentions`、`metadata`、`asset_copied`、`markdown_file` 等约定字段。
- 索引条目数与实际拷贝到 `assets/` 的图片数一致；若有 `fig` 级 Markdown，其路径或标识须与物理文件对应。
- 不得出现索引有图但资产未拷贝，或字段缺失导致下游无法关联的情况。

---

### 六、文本清洗标准 (Cleaning Standards)


| 维度         | 处理要求                         | 错误示例 (Bad)              | 预期输出 (Good)    |
| ---------- | ---------------------------- | ----------------------- | -------------- |
| **物理量聚合**  | 数字、小数点、单位之间必须消除非语义空格         | `0 . 0 1 0 n m`         | `0.010nm`      |
| **化学实体纠错** | 修复断裂的元素符号，匹配领域术语表            | `Z \mathbf{r}`, `N i -` | `Zr`, `Ni`     |
| **数值连续性**  | 消除数字内部因 OCR 产生的换行或连字符        | `110 \n s`              | `110s`         |
| **术语一致性**  | 同类实体在同一文档内输出尽量一致             | `Zr based`, `Zr-based`  | `Zr-based`     |
| **元数据清晰性** | 图注/表题中的数值、单位、实体不应保留明显 OCR 断裂 | `Fig. 1. 1 0 n m`       | `Fig. 1. 10nm` |


---

### 七、文本结构化标准 (Structuring Standards)

与“文本清洗标准”相对应，`Designer` 在产出结构化文本、`full_text` JSON 与 `datamining` JSON 时须遵守以下结构化标准，以便验收与下游消费一致。


| 维度 | 结构化要求 | 错误示例 (Bad) | 预期输出 (Good) |
| --- | --- | --- | --- |
| **Poros 根标签** | 全文须被 `<poros_doc>` / `</poros_doc>` 包裹 | 无根标签或仅有一侧标签 | `<poros_doc>…</poros_doc>` |
| **标签闭合** | 所有 Poros 标签须成对闭合、嵌套正确 | `</poros_paragraph>` 缺失或错位 | 开闭一一对应、嵌套合法 |
| **标签粒度** | 优先使用稳定大类；不稳定块统一回落到 `poros_section_section` | 为 `Article info`、`Declaration` 等继续发明新专用标签 | 用通用 `section` 容器承载，原始标题保留在文本中 |
| **Section 语义** | `poros_section_*`、`poros_title_*`、`poros_subtitle_level2/3` 须稳定表达章节层次 | 章节正文游离于 section 之外，或 section 重复错位 | section 边界清晰、层级一致 |
| **EOS 结尾** | 文档末尾须带约定 EOS token（如 `</s>`） | 正文结束无 EOS | `…text</s>` |
| **块级强边界** | `</poros_section_{type}>` 可作为逻辑块强边界，且不得损坏闭合 | section 未闭合或跨节串联 | 每节闭合明确，可作块级 EOS |
| **full_text JSON 字段** | `full_text/{doc_id}_structured.json` 须含 `doc_id`、`content`、`pure_text_stream` | 缺少 `pure_text_stream` | 三字段齐全且可用 |
| **datamining JSON 字段** | `datamining/{doc_id}_datamining.json` 须含 `doc_id`、`title`、`sections`，并应含 `formulas`、`chemical_formulas`、`asset_refs` | 缺少 `sections` 或仅有平铺文本 | 章节与辅助结构字段可消费 |
| **纯文本视图纯净性** | `pure_text_stream` 不得残留 `poros_*` 标签 | `pure_text_stream` 仍含 `<poros_section_*>` | 纯文本流仅保留自然文本 |
| **化学式语义** | `datamining.chemical_formulas` 不得含非化学缩写或普通公式 | 含 `TEM`、`XRD`、`F_{i,1/2}` 或积分表达式 | 仅化学元素、化合物、稳定材料式 |
| **多模态索引** | 索引项须含 `image_path`、`fig_id`、`caption` 等约定字段 | 缺少 `fig_id` 或 `asset_copied` | 约定字段完整、与资产一致 |


---

### 八、符号与单位协议 (Symbol & Unit Protocol)

Designer 在产出结构化文本、`full_text` JSON 与 `datamining` JSON 时，须在输出中遵守以下符号与单位约定，以保证下游训练与抽取一致。

#### 1. 单位对齐原则

- 输出中的数值与单位须采用统一的 `Value + Unit` 表达协议，可为无空格或统一单空格，但项目内不得混用。
- 单位写法必须稳定，例如：`mm`, `nm`, `°C`, `s`, `min`, `keV`；在 `content` 与 `datamining` 中不得改写为不一致形式。
- 复合单位、指数单位、公式内单位须优先保证结构正确，再行输出，避免在结构化或标签化过程中引入断裂。

#### 2. 符号与结构保护原则

Designer 在生成 Poros 标签流与 `datamining` 字段时，必须保护以下结构不被破坏或误写：

- LaTeX 行内公式（定界符成对、内容不截断）
- LaTeX 显示公式与块级边界
- 上下标、希腊字母及引用命令与参考文献结构
- 化学元素和单位白名单中的写法，不得在 `datamining.chemical_formulas` 中混入非化学缩写

---

### 九、Designer 产出的训练与数据挖掘就绪要求

Designer 交付的 `content`、`pure_text_stream` 与 `datamining` 产物须按各自职责分别满足训练与数据挖掘要求，不得混淆字段语义。

#### 0. 视图职责分离 (View Contract Separation)

- `full_text/{doc_id}_structured.json.content` 面向结构感知训练，允许保留稳定的 Poros 标签作为语义边界信号。
- `full_text/{doc_id}_structured.json.pure_text_stream` 面向纯文本训练、Embedding、索引与通用语言建模，必须剥离全部结构标签。
- `datamining/{doc_id}_datamining.json` 面向数据挖掘与检索，必须将结构边界转译为可计算字段，而非只保留平铺文本。

#### 1. 实体完整性 (Entity Integrity)

在 `datamining` 与 `content` 中，材料名称、实验名、关键术语在同一文档内拼写须保持高度一致。不得在聚合、打标签或导出过程中引入会影响结构化归并的混用写法。

#### 2. 上下文锚点 (Contextual Anchors)

须在结构化输出中保留实验条件、温度区间、设备环境、前后限定语等锚点信息（如 `at elevated temperatures`、`at the high-energy beam-line`）。不得在生成 `content`、`pure_text_stream` 或 `datamining` 时将这些描述性条件误判为噪音删去。

#### 3. 属性-值对对齐 (Attribute-Value Pairing)

须确保测量属性与其对应数值、单位在 `content` 或 `datamining.sections` 中保持合理邻近关系（如 `diameter = 3mm`、`heating rate = 20 K/min`）。不能因标签化、分段或字段抽取把属性与数值打散，导致后续映射困难。

#### 4. 结构化噪音最小化

Designer 产出的 `pure_text_stream` 与 `datamining` 不得引入或放大以下问题：断裂数字、异常空格、同一实体的不一致术语、损坏的行内公式、多余引用符号噪音。若上游文本已存在上述问题，应在结构化时尽量隔离或标记，而非复制扩散到训练视图与挖掘视图。

#### 5. 结构感知训练视图约束

- `content` 中允许存在标签，但这些标签必须是稳定、闭合、可解释的结构信号，而不是随机格式噪音。
- `content` 中的 section 边界必须与正文语义一致，不得出现空节、重复节、章节错位或正文归属错误。
- 标签语义不稳定时，必须优先回退到更粗粒度的大类标签，而不是继续细分。
- 若将 `content` 直接用于长文本训练，则公式、化学式、图表引用和标题标签的策略须在整个语料集中保持一致。

---

### 十、禁止破坏项

以下情况属于 Designer 交付中不可接受的质量回退：

- 缺失根标签或破坏 Poros 标签闭合、嵌套，导致 Schema 校验不通过
- 破坏公式结构、上下标结构或 LaTeX 定界符平衡
- 缺少 `full_text/{doc_id}_structured.json`、`datamining/{doc_id}_datamining.json` 等约定产物，或缺少其必选字段
- 将应保留在 `content` 中的结构标签错误复制到 `pure_text_stream`，导致字段语义失配
- 在语义不稳定时继续发明更细粒度 section 标签，而不是回退到 `poros_section_section`
- 在 `datamining.chemical_formulas` 中混入已知非化学缩写、普通公式、积分表达式或物理量表达
- 文档末尾缺少约定 EOS token，导致下游训练脚本无法识别文档边界
- 多模态索引缺少约定字段，或索引条目与 `assets/` 拷贝不一致
- 在聚合、打标签或导出过程中误删或改写图注、表题、脚注中的编号或关键语义

---

### 十一、质量验收标准

#### 1. Designer 交付验收

Designer 交付结果至少应满足：

- Poros 根标签存在且标签闭合、嵌套符合约定，Schema 校验通过
- 行内公式定界符成对平衡，LaTeX 校验无结构性错误
- 文档末尾带约定 EOS token
- `full_text/{doc_id}_structured.json` 包含 `doc_id`、`content`、`pure_text_stream`，且格式可用
- `datamining/{doc_id}_datamining.json` 至少包含 `doc_id`、`title`、`sections`，并交付可用的 `formulas`、`chemical_formulas`、`asset_refs`
- `content` 中的结构标签能够稳定表达章节、标题、子标题与逻辑块边界
- `content` 在语义不稳定时已回退到更粗粒度的大类标签，而非继续细分
- `pure_text_stream` 为真正去标签后的纯文本流
- `datamining` 至少能表达章节、段落、公式、化学式、资产引用，并尽可能保留标题与子标题层信息
- `datamining.chemical_formulas` 中无已知非化学缩写或普通公式噪声
- 若产出多模态产物，索引具备约定字段且与 `assets/` 一致
- `content` 适合结构感知训练，`pure_text_stream` 适合纯文本训练与规则处理，`datamining` 适合数据挖掘与检索

#### 2. 拒收条件

出现以下任一情况，可判定当前 Designer 交付不满足要求：

- 根标签缺失或标签闭合/嵌套错误
- 公式定界符不平衡或 LaTeX 结构被破坏
- 缺少 EOS 或缺少 `full_text` / `datamining` 约定产物及其必选字段
- `pure_text_stream` 中残留大量 `poros_*` 标签，导致字段语义不成立
- `content` 中 section/title/subtitle 边界严重错位，导致标签虽闭合但语义不可消费
- 语义不稳定时仍使用过细标签，导致同类块在不同文档中映射标准不一致
- `datamining.chemical_formulas` 中混入非化学缩写、普通公式或工程表达式
- 多模态索引缺字段或资产未正确拷贝
- 同一文档内结构化产出在必选字段或标签映射标准上不一致

---

### 十二、技术路径说明

本标准约束的是 Designer 的**输出质量**，而不限定具体实现技术。Designer 实现可采用以下一种或多种方式：

- 基于规则的 Poros 标签生成与 Schema / LaTeX 校验
- 区分 `content`、`pure_text_stream` 与 `datamining` 的分文件导出器 / 映射器
- 术语表与化学式 / 单位白名单，用于 `datamining` 抽取与噪声过滤
- 标签与公式的结构保护与局部修复
- 以“稳定大类 + 通用 section 回退”为原则的标签归一化策略
- 插件化流水线与导出器（`full_text` / `datamining` / `multimodal`）
- 审计脚本与自动化验收（如 Schema、LaTeX、EOS、视图契约、化学式语义、多模态索引）

  
无论采用何种技术路径，最终都必须服务于以下目标：

- `Processor` 负责数据质量交付

- `Designer` 负责数据结构化表达

- 两个包职责分离，但质量链路必须闭环

