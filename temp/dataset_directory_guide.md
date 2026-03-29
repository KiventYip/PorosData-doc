# dataset directory guide

- doc_type: dataset_directory_guide
- status: active
- updated_at: 2026-03-19 00:00:00

## 概述

`data/` 目录承载 PorosData-Designer 流水线的全部数据资产，按处理阶段划分为三层：

```
data/
├── raw/                  ← 上游原始数据（MinerU 完整解析产物）
├── processed/            ← 中间处理数据（标准化清洗后的 Designer 输入）
└── structured/           ← 最终结构化产物（Designer 交付输出）
    ├── full_text/        ←   全文结构化（AI 训练）
    ├── datamining/       ←   数据挖掘（检索 / 知识图谱）
    └── multimodal/       ←   多模态图文交织
```

数据流向为 **raw → processed → structured**。

---

## 一、raw — 上游原始数据

### 目录结构

```
data/raw/{doc_id}/
├── {doc_id}.pdf
├── state.json
└── mineru_2.1.10_output/{doc_id}/auto/
    ├── {doc_id}.md
    ├── {doc_id}_content_list.json
    ├── {doc_id}_middle.json
    ├── {doc_id}_model.json
    ├── {doc_id}_layout.pdf
    ├── {doc_id}_origin.pdf
    ├── {doc_id}_span.pdf
    └── images/
        └── {sha256}.jpg
```

`{doc_id}` 采用 5 位零填充编号（如 `00001`）。

### 文件说明

| 文件 | 说明 |
|------|------|
| `{doc_id}.pdf` | 原始科学论文 PDF 文件 |
| `state.json` | 文档解析状态元数据，记录 PDF 是否存在、MinerU 版本号、是否有 OCR / auto 输出 |
| `{doc_id}_content_list.json` | MinerU 逐块解析的内容列表，是整个 Designer 流水线的**核心输入** |
| `{doc_id}.md` | MinerU 自动生成的 Markdown 格式全文 |
| `{doc_id}_middle.json` | MinerU 中间层表示，包含段落级与块级解析结构 |
| `{doc_id}_model.json` | 模型推理元信息，包括检测框坐标与分类置信度 |
| `{doc_id}_layout.pdf` | 布局分析可视化 PDF，在原 PDF 上叠加检测框标注 |
| `{doc_id}_origin.pdf` | 原始 PDF 的拷贝 |
| `{doc_id}_span.pdf` | 文本 span 级别可视化 PDF |
| `images/{sha256}.jpg` | 从 PDF 中提取的图片，以文件内容 SHA256 哈希值命名 |

### state.json 字段

```json
{
    "has_pdf": true,
    "mineru": [
        {
            "mineru_version": "2.1.10",
            "has_mineru_ocr": false,
            "has_mineru_auto": true
        }
    ]
}
```

| 字段 | 类型 | 说明 |
|------|------|------|
| `has_pdf` | bool | 原始 PDF 是否存在 |
| `mineru` | array | MinerU 解析记录列表 |
| `mineru[].mineru_version` | string | MinerU 引擎版本号 |
| `mineru[].has_mineru_ocr` | bool | 是否存在 OCR 模式输出 |
| `mineru[].has_mineru_auto` | bool | 是否存在 auto 模式输出 |

> **特例**：`00018/` 仅包含 `00018.xml`，无 PDF 和 MinerU 输出。

---

## 二、processed — 中间处理数据

### 目录结构

```
data/processed/
├── processing_report.json
└── {doc_id}/mineru_2.1.10_output/{doc_id}/auto/
    ├── {doc_id}_content_list.json
    └── images/
        └── {sha256}.jpg
```

### 文件说明

| 文件 | 说明 |
|------|------|
| `processing_report.json` | 全局处理报告，汇总所有文档的批处理统计信息 |
| `{doc_id}_content_list.json` | 经标准化清洗后的 content_list（去除控制字符、统一格式），是 Designer 的直接输入 |
| `images/{sha256}.jpg` | 与 raw 对应的图片资源拷贝，供多模态流水线引用 |

### processing_report.json 字段

```json
{
  "summary": {
    "total_files": 19,
    "processed_files": 19,
    "skipped_files": 0,
    "error_files": 0,
    "total_items": 1083,
    "processed_items": 1083,
    "total_healed_count": 0,
    "total_healing_attempts": 0,
    "total_healing_successes": 0,
    "control_chars_removed_total": 15,
    "files_with_control_char_cleanup": 4,
    "temp_files_removed_total": 0
  },
  "performance": {
    "total_time_seconds": 108.63,
    "avg_time_per_file_seconds": 5.72,
    "files_per_second": 0.17,
    "items_per_second": 9.97
  },
  "errors": []
}
```

| 字段路径 | 类型 | 说明 |
|----------|------|------|
| `summary.total_files` | int | 待处理文件总数 |
| `summary.processed_files` | int | 成功处理的文件数 |
| `summary.skipped_files` | int | 跳过的文件数 |
| `summary.error_files` | int | 出错的文件数 |
| `summary.total_items` | int | content_list 中的条目总数 |
| `summary.processed_items` | int | 成功处理的条目数 |
| `summary.control_chars_removed_total` | int | 清除的控制字符总数 |
| `summary.files_with_control_char_cleanup` | int | 涉及控制字符清理的文件数 |
| `performance.total_time_seconds` | float | 批处理总耗时（秒） |
| `performance.avg_time_per_file_seconds` | float | 平均每文件耗时（秒） |
| `performance.files_per_second` | float | 处理速度（文件/秒） |
| `performance.items_per_second` | float | 处理速度（条目/秒） |
| `errors` | array | 错误记录列表 |

---

## 三、structured — 最终结构化产物

`data/structured/` 是 Designer 的交付目录，包含三类输出。

### 3.1 full_text — 全文结构化

#### 目录结构

```
data/structured/full_text/{doc_id}/
├── {doc_id}_structured.json
└── {doc_id}_structured.txt
```

#### {doc_id}_structured.json

带 Poros 标签体系的完整结构化全文，面向 AI 结构感知训练。

必选字段：

| 字段 | 类型 | 说明 |
|------|------|------|
| `doc_id` | string | 文档编号（5 位零填充） |
| `content` | string[] | 带 Poros 标签的结构化文本数组。标签包括 `<poros_doc>`、`<poros_section_{type}>`、`<poros_title_{type}>`、`<poros_subtitle_level2/3>`、`<poros_paragraph>`、`<poros_equ>`、`<poros_chem>`、`<poros_asset>`、`<poros_keywords>` 等 |
| `pure_text_stream` | string[] | 去除所有 Poros 标签后的纯文本流数组 |

规范要求：
- 文档根标签 `<poros_doc>` 必须存在且闭合
- 所有标签成对闭合、嵌套正确
- 文档末尾带 `</s>` EOS token
- `pure_text_stream` 中不得残留任何标签

#### {doc_id}_structured.txt

去除所有 Poros 标签后的干净纯文本流，适合通用语言模型训练。内容与 `_structured.json` 中 `pure_text_stream` 字段对应。

### 3.2 datamining — 数据挖掘

#### 目录结构

```
data/structured/datamining/{doc_id}/
└── {doc_id}_datamining.json
```

#### {doc_id}_datamining.json

面向数据挖掘、语义检索和知识图谱构建的结构化 JSON。

必选字段：

| 字段 | 类型 | 说明 |
|------|------|------|
| `doc_id` | string | 文档编号 |
| `title` | string | 论文标题 |
| `sections` | array | 按章节拆分的段落集合，每个 section 包含类型标签与文本内容 |

推荐字段：

| 字段 | 类型 | 说明 |
|------|------|------|
| `formulas` | array | 数学公式列表（LaTeX 格式） |
| `chemical_formulas` | array | 化学式 / 材料式列表，仅限化学元素 / 化合物 / 材料式，不混入机构或仪器缩写 |
| `asset_refs` | array | 图表资产引用列表，每项包含 `type`（图/表）、`ref`（引用标识）、`link`（指向 multimodal 资产的路径） |

### 3.3 multimodal — 多模态图文交织

#### 目录结构

```
data/structured/multimodal/{doc_id}/
├── {doc_id}_index.json
├── fig_{n}.md
└── assets/
    └── fig_{n}.jpg
```

#### {doc_id}_index.json

多模态图片索引清单，每张图一条结构化记录。

| 字段 | 类型 | 说明 |
|------|------|------|
| `image_path` | string | 图片相对路径（如 `./assets/fig_1.jpg`） |
| `fig_id` | string | 图片编号 |
| `caption` | string | 图注文本 |
| `mentions` | string[] | 正文中引用该图的句子列表 |
| `metadata` | object | 图片元数据 |
| `metadata.page_idx` | int | 图片所在页码（0-based） |
| `metadata.bbox` | array | 边界框坐标 |
| `metadata.image_footnote` | array | 图片脚注 |
| `metadata.image_caption` | array | 原始图注 |
| `metadata.spatial_info` | object | 空间位置信息（页码、位置、是否有边界框） |
| `metadata.semantic_anchors` | object | 语义锚点，包含 `before`（前文上下文）、`after`（后文上下文）和 `anchor_type`（锚定方式） |
| `asset_copied` | bool | 图片是否已成功拷贝到 assets 目录 |
| `markdown_file` | string | 对应的 Markdown 描述卡片路径（如 `./fig_1.md`） |

#### fig_{n}.md

每张图的 Markdown 描述卡片，便于人工审阅和多模态训练数据构建。结构如下：

```markdown
# Poros_Figure {n}

![Poros_Figure {n}](./assets/fig_{n}.jpg)

### Poros_Caption

{图注文本}

### Poros_Mentions in Text

- {正文引用句 1}
- {正文引用句 2}

<!--
Document: {doc_id}
Page: {page}
Fig ID: {n}
Asset copied: {True/False}
-->
```

#### assets/fig_{n}.jpg

规范化命名的图片文件，由原始 SHA256 哈希命名的图片重命名拷贝而来，与 `fig_{n}.md` 和 `{doc_id}_index.json` 中的引用路径一一对应。

---

## 四、命名约定汇总

| 约定项 | 规则 | 示例 |
|--------|------|------|
| doc_id | 5 位零填充数字编号 | `00001`, `00014` |
| content_list 输入文件 | `{doc_id}_content_list.json` | `00001_content_list.json` |
| 原始图片命名 | SHA256 哈希 + `.jpg` | `07922a29...35e.jpg` |
| 结构化全文 | `{doc_id}_structured.json` / `.txt` | `00001_structured.json` |
| 数据挖掘 | `{doc_id}_datamining.json` | `00001_datamining.json` |
| 多模态索引 | `{doc_id}_index.json` | `00001_index.json` |
| 多模态图片描述 | `fig_{n}.md` | `fig_1.md` |
| 多模态图片资产 | `fig_{n}.jpg`（在 `assets/` 下） | `assets/fig_1.jpg` |

---

## 五、当前数据规模

| 数据层 | 文档数 | 备注 |
|--------|--------|------|
| `raw/` | 19 个文件夹 | 00001–00021（缺 00016），含 18 篇 PDF + 1 篇 XML (00018) |
| `processed/` | 19 个文件夹 | 全部标准化完成，processing_report 显示 0 错误 |
| `structured/full_text/` | 19 个文件夹 | 每个含 `_structured.json` + `_structured.txt` |
| `structured/datamining/` | 19 个文件夹 | 每个含 `_datamining.json` |
| `structured/multimodal/` | 19 个文件夹 | 图片数量 1–19 张/篇不等，00013 仅有 index 无图片 |
