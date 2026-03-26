# PorosData-Designer

## 定位

`Designer` 是 PorosData 中负责**结构化组织与重构**的模块。它建立在 `Processor` 已完成质量清洗的前提上，将高质量文本进一步转换为**结构化对象、字段、关系和可交付产物**，用于训练视图、数据挖掘视图与多模态索引。

换言之：

- `Processor` 负责提升数据质量
- `Designer` 负责结构化表达

`Designer` 不应再承担大规模 OCR 清洗职责，它的任务重点是：章节重构、字段映射、公式与化学式保护、图文资产锚定，以及结构化结果的稳定导出。

## Designer 要交付什么

`Designer` 的核心任务包括但不限于：

- 实体识别与标准化映射
- 属性-值对抽取
- 条件与上下文归属绑定
- 结构化记录生成
- JSON / 表格 / Knowledge Graph 等目标格式输出

现阶段推荐的交付分为三类视图：

- 结构感知训练视图：带 Poros 标签的 `content`
- 纯文本训练视图：去标签后的 `pure_text_stream`
- 数据挖掘视图：面向抽取、检索与入库的 `datamining` 结果

## 什么是“就绪”

### Structure-Aware Training Ready

指数据允许在训练视图中保留稳定、可解释、可闭合的结构标签，用作长文本训练时的显式语义边界信号。

其关键要求包括：

- `section`、`title`、`subtitle` 标签用于表达结构语义，而不是模拟原始排版
- `</poros_section_{type}>` 可视为逻辑块强边界
- 只有当标签稳定、语义一致、嵌套安全时，才应作为训练增强信号

### Plain-Text Training Ready

指文本可直接作为自然语言序列输入模型，而不依赖任何 `poros_*` 结构标签才能被理解。

其关键要求包括：

- `pure_text_stream` 不得残留 XML 包装或结构控制标记
- 公式、化学式、图表引用在纯文本视图中的保留策略须全语料一致
- 结构信息应通过自然分段或统一纯文本占位体现，而不是依赖标签泄漏

### Data Mining Ready

指结构化结果已经适合实体抽取、关系抽取、属性映射与知识组织。

其关键要求包括：

- 实体名称稳定
- 数值、单位、属性可稳定识别
- 属性与上下文关系未被标签化或导出过程破坏
- 输出可进一步消费为 JSON、表结构、知识图谱或索引对象

## 输出目录与产物

现阶段 `Designer` 的交付以**分文件视图**为准，而不是单文件聚合。

- `structured/full_text/{doc_id}/`
- `structured/datamining/{doc_id}/`
- `structured/multimodal/{doc_id}/`（若启用）

推荐产物包括：

- `full_text/{doc_id}_structured.txt`
- `full_text/{doc_id}_structured.json`
- `datamining/{doc_id}_datamining.json`
- `multimodal/{doc_id}_index.json`
- `multimodal/assets/` 与按图拆分的 Markdown 文件

其中：

- `structured.txt` 面向人工检查与直接阅读
- `structured.json` 面向训练视图消费，承载 `content` 与 `pure_text_stream`
- `datamining.json` 面向结构化抽取、检索与入库

## Poros 标签与层级规划

结构化文本应符合 Poros 骨架约定，并采用**粗粒度、稳定优先**的标签体系。

- 必须包含根标签 `<poros_doc>` 与 `</poros_doc>`
- `poros_section_*` 的闭合标签承担逻辑块结束信号
- 优先使用稳定的大类 section：`header`、`abstract`、`introduction`、`experimental`、`results`、`discussion`、`conclusion`、`acknowledgements`、`references`
- 对语义不稳定的块一律回落到 `poros_section_section`
- 稳定大类可使用 `poros_title_header`、`poros_title_abstract`、`poros_title_introduction` 等
- 非稳定章节统一使用 `poros_title_section`
- 子标题层以 `poros_subtitle_level2`、`poros_subtitle_level3` 为主
- 行内语义标签维持轻量集合：`poros_paragraph`、`poros_equ`、`poros_chem`、`poros_asset`、`poros_keywords`
- 不得出现未闭合标签、错位嵌套或非法子节点

## 分视图契约与必选字段

### `full_text/{doc_id}_structured.json`

必须至少包含以下字段：

- `doc_id`
- `content`
- `pure_text_stream`

其中：

- `content` 是带 Poros 标签的完整文本，可作为结构感知训练视图
- `pure_text_stream` 是去标签后的纯净文本流，可作为纯文本训练、Embedding 或索引视图

### `datamining/{doc_id}_datamining.json`

必须至少包含以下字段：

- `doc_id`
- `title`
- `sections`

推荐同时交付：

- `formulas`
- `chemical_formulas`
- `asset_refs`

`sections` 中每一项应表达章节标题、段落与子标题层级；当章节语义不稳定时，可回退到 `section_type = "section"`。

## 公式、EOS 与化学式语义

必须保证训练就绪与语义一致：

- 行内公式定界符（如 `$...$`）须成对平衡
- 文档末尾须带项目约定的 EOS token，例如 `</s>`
- `</poros_section_{type}>` 作为块级边界信号，不替代全局 EOS
- `datamining.chemical_formulas` 只保留化学元素、化合物或稳定材料式
- 普通公式、积分表达式、热力学表达式、仪器名、方法名等不得混入 `chemical_formulas`

## 多模态索引与资产一致性

若交付 multimodal 产物，须满足：

- 索引文件为 JSON 数组
- 每项至少包含 `image_path`、`fig_id`、`caption`、`mentions`、`metadata`、`asset_copied`、`markdown_file`
- 索引条目数与实际拷贝到 `assets/` 的图片数一致
- 若存在 `fig` 级 Markdown，其路径或标识须与物理文件一致

## 结构化标准

| 维度 | 结构化要求 | 错误示例 (Bad) | 预期输出 (Good) |
|------|------------|----------------|-----------------|
| Poros 根标签 | 全文须被 `<poros_doc>` / `</poros_doc>` 包裹 | 缺失根标签 | `<poros_doc>...</poros_doc>` |
| 标签闭合 | 所有 Poros 标签须成对闭合、嵌套正确 | `</poros_paragraph>` 缺失或错位 | 开闭一一对应、嵌套合法 |
| 标签粒度 | 优先使用稳定大类；不稳定块回落到 `poros_section_section` | 为 `Declaration` 等继续发明新标签 | 使用通用 `section` 容器 |
| Section 语义 | `section/title/subtitle` 须稳定表达章节层次 | 章节正文游离于 section 之外 | section 边界清晰 |
| EOS 结尾 | 文档末尾须带 EOS token | 正文结束无 EOS | `...text</s>` |
| `full_text` 字段 | 须含 `doc_id`、`content`、`pure_text_stream` | 缺少 `pure_text_stream` | 三字段齐全 |
| `datamining` 字段 | 须含 `doc_id`、`title`、`sections` | 缺少 `sections` | 结构字段可消费 |
| 纯文本纯净性 | `pure_text_stream` 不得残留 `poros_*` 标签 | 仍含结构标签 | 仅保留自然文本 |
| 化学式语义 | `chemical_formulas` 不得混入非化学缩写或普通公式 | 含 `TEM`、`XRD` 等 | 仅保留化学元素或化合物 |
| 多模态索引 | 索引项须含约定字段 | 缺少 `fig_id` 或 `asset_copied` | 字段完整且与资产一致 |

## 训练与数据挖掘就绪要求

`Designer` 交付的 `content`、`pure_text_stream` 与 `datamining` 不得混淆语义职责。

### 1. 视图职责分离

- `content` 面向结构感知训练
- `pure_text_stream` 面向纯文本训练、Embedding、索引与通用语言建模
- `datamining` 面向数据挖掘与检索

### 2. 实体完整性

在 `content` 与 `datamining` 中，材料名称、实验名、关键术语在同一文档内拼写须保持高度一致，不得在聚合、打标签或导出过程中引入新的混用写法。

### 3. 上下文锚点

必须保留实验条件、温度区间、设备环境、前后限定语等锚点信息，不得在结构化过程中误判为噪音删去。

### 4. 属性-值对对齐

须确保测量属性与其对应数值、单位在 `content` 或 `datamining.sections` 中保持合理邻近关系，不能因分段或字段抽取把属性与数值打散。

### 5. 结构化噪音最小化

`pure_text_stream` 与 `datamining` 不得放大上游噪音，例如断裂数字、异常空格、不一致术语、损坏公式或多余引用符号。

## 禁止破坏项

以下情况属于不可接受的质量回退：

- 缺失根标签或破坏 Poros 标签闭合与嵌套
- 破坏公式结构、上下标结构或 LaTeX 定界符平衡
- 缺少 `full_text` / `datamining` 约定产物及其必选字段
- 将应保留在 `content` 中的结构标签错误复制到 `pure_text_stream`
- 在语义不稳定时继续发明更细粒度标签，而不是回退到通用 section
- 在 `datamining.chemical_formulas` 中混入非化学缩写、普通公式或工程表达式
- 文档末尾缺少 EOS
- 多模态索引缺少约定字段，或与 `assets/` 不一致
- 在导出过程中误删图注、表题、脚注中的编号或关键语义

## 质量验收标准

### 交付验收

`Designer` 交付结果至少应满足：

- Poros 根标签存在且标签闭合、嵌套符合约定
- 行内公式定界符成对平衡
- 文档末尾带 EOS
- `full_text/{doc_id}_structured.json` 包含 `doc_id`、`content`、`pure_text_stream`
- `datamining/{doc_id}_datamining.json` 至少包含 `doc_id`、`title`、`sections`
- `content` 中的标签能够稳定表达章节、标题、子标题与逻辑块边界
- `pure_text_stream` 为真正去标签后的纯文本流
- `datamining` 至少能够表达章节、段落、公式、化学式与资产引用
- 若产出多模态结果，索引字段与资产数量一致

### 拒收条件

出现以下任一情况，可判定当前版本不满足要求：

- 根标签缺失或标签闭合/嵌套错误
- 公式定界符不平衡或 LaTeX 结构被破坏
- 缺少 EOS 或缺少约定产物及其必选字段
- `pure_text_stream` 中残留大量 `poros_*` 标签
- `content` 中 section/title/subtitle 边界严重错位
- 语义不稳定时仍使用过细标签
- `datamining.chemical_formulas` 中混入非化学缩写、普通公式或工程表达式
- 多模态索引缺字段或资产未正确拷贝

## 技术路径说明

本页面约束的是 `Designer` 的**输出质量**，而不限定具体实现技术。实现可采用以下一种或多种方式：

- 基于规则的 Poros 标签生成与校验
- `content`、`pure_text_stream` 与 `datamining` 的分文件导出器
- 术语表与化学式 / 单位白名单
- 标签与公式的结构保护与局部修复
- 以“稳定大类 + 通用 section 回退”为原则的标签归一化策略
- 插件化流水线与导出器
- 审计脚本与自动化验收

无论采用何种技术路径，最终都必须服务于以下目标：

- `Processor` 负责数据质量交付
- `Designer` 负责数据结构化表达
- 两个包职责分离，但质量链路必须闭环
