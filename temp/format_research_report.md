# 输入格式调研报告

- doc_type: research_note
- status: reference_only
- updated_at: 2026-03-18 09:37:49
- current_contract_note: if this document mentions historical JSONL or prior audit structure, use `docs/ai_ready_and_datamining_designer.md`, `docs/usage_guide.md`, and current `data/structured/*_structured.json` as the active contract.



**调研日期**: 2025-03-03  
**数据目录**: `data/raw`、`data/processed`  
**关联包**: `porosdata_designer`

---

## 一、两种格式目录结构对比

### 1.1 raw（MinerU 原始输出）

```
data/raw/
├── {doc_id}/                              # 文档 ID（如 00001、00004、00005）
│   ├── state.json                         # 文档级元信息
│   └── mineru_2.1.10_output/
│       └── {doc_id}/
│           └── auto/
│               ├── {doc_id}.md            # Markdown 正文
│               ├── {doc_id}_model.json    # 布局检测输出
│               ├── {doc_id}_middle.json   # 中间表示
│               ├── {doc_id}_content_list.json  # 内容列表
│               └── images/                # 图片资源（如存在）
│                   └── *.jpg
├── 00001/
├── 00004/
└── 00005/
```

**特点**:
- 完整的 MinerU 2.1.10 输出
- 包含 `state.json`、`md`、`model.json`、`middle.json`、`content_list.json`
- 图片路径在 `img_path` 中为相对路径（如 `images/xxx.jpg`），相对于 `auto/` 目录

---

### 1.2 processed（文本标准化后输出）

```
data/processed/
├── processing_report.json                 # 批处理统计报告
├── {doc_id}/
│   └── mineru_2.1.10_output/
│       └── {doc_id}/
│           └── auto/
│               └── {doc_id}_content_list.json  # 仅此文件
├── 00001/
├── 00004/
└── 00005/
```

**特点**:
- 只保留 `content_list.json`
- **不包含** `state.json`、`md`、`model.json`、`middle.json`
- **不包含** `images/` 图片目录
- 包含 `processing_report.json`（整体统计、token 效率等）

---

## 二、content_list.json 结构对比

### 2.1 Raw 版本（raw）

```json
{
  "type": "text",
  "text": "原始 OCR 抽取文本",
  "text_level": 1,
  "page_idx": 0
}
```

- 类型: `text` / `image` / `equation` / `table` / `code` / `list` 等
- 图片项: `img_path`, `image_caption`, `image_footnote`, `page_idx`
- 无 `original_text` 字段

### 2.2 处理后版本（processed）

```json
{
  "type": "text",
  "text": "标准化后的文本",
  "page_idx": 0,
  "original_text": "原始 OCR/抽取 文本"
}
```

- 在 raw 基础上，部分文本项增加 `original_text` 字段
- `text` 为标准化后的内容，`original_text` 用于对比与审计
- 图片项结构相同，但 `img_path` 指向的图片**物理上不存在**（processed 下无 images 目录）

---

## 三、designer 包使用现状

### 3.1 输入来源

| 组件 | 输入来源 | 说明 |
|------|----------|------|
| `run_text_standardization.py` | 仅 `raw` | 硬编码 |
| `run_multimodal_extraction.py` | 仅 `raw` | 硬编码 |
| `ContentListAdapter` | 任意 JSON 文件路径 | 不区分格式 |
| `MiddleJsonAdapter` | 任意 middle.json 路径 | 需 raw 目录才有 middle.json |

### 3.2 路径假设

- 示例脚本均假设输入在 `project_root / "data" / "raw"`
- `MultimodalInterleaver._generate_markdown_and_copy_assets` 中图片源路径**硬编码**为：
  ```python
  source_image_path = Path("data") / "raw" / doc_id / "mineru_2.1.10_output" / doc_id / "auto" / image_path
  ```

---

## 四、潜在 Bug 与风险

### 4.1 高优先级

| 编号 | 问题 | 影响 | 位置 |
|------|------|------|------|
| B1 | **processed 无法用于多模态任务** | 若以 processed 的 content_list 作为输入，`img_path` 指向的图片不存在，复制图片会失败 | `MultimodalInterleaver` |
| B2 | **图片源路径硬编码且依赖 CWD** | 使用 `Path("data")` 相对当前工作目录，若从其他目录运行脚本会找不到图片 | `multimodal_interleaver.py:731-732` |
| B3 | **示例脚本不支持 processed 作为输入** | 用户无法指定使用 processed，只能使用 raw | `run_*.py` |

### 4.2 中优先级

| 编号 | 问题 | 影响 | 位置 |
|------|------|------|------|
| B4 | **original_text 未被显式处理** | TextAggregator/ContentFilter 使用 `block.get("text","")`，会使用标准化后的 `text`，逻辑正确，但 `original_text` 完全被忽略，无法用于对比或审计 | `content_filter.py`, `text_aggregator.py` |
| B5 | **processed 目录结构与 raw 不一致** | processed 缺少 state.json，若未来有组件依赖 state.json 会报错 | 全项目 |

### 4.3 低优先级

| 编号 | 问题 | 影响 | 位置 |
|------|------|------|------|
| B6 | **空 text 块** | processed 中存在 `"text": ""` 的块，ContentFilter 会过滤，但可能影响 item 数量统计 | `content_filter.py:86-88` |
| B7 | **img_path 解析** | 若 MinerU 版本变化导致 img_path 格式改变（如绝对路径），当前逻辑可能失效 | `image_processor.py`, `multimodal_interleaver.py` |

---

## 五、建议修复方向

1. **支持双输入源**：示例脚本增加 `--input-base` 或环境变量，允许指定 `raw` 或 `processed`。
2. **图片路径解析**：将 `MultimodalInterleaver` 的图片源路径改为基于 content_list 文件所在目录解析（即 `content_file.parent / image_path`），而非硬编码 raw 路径。
3. **processed 多模态说明**：若 processed 设计上不包含图片，应在文档中明确说明：多模态任务必须使用 raw 数据。
4. **original_text 可选利用**：在需要审计/对比的场景，可提供选项使用 `original_text` 而非 `text`。

---

## 六、格式关系小结

```
raw (完整 MinerU 输出)
        │
        ├── 文本标准化/清洗流程
        │         │
        │         ▼
        │   processed (仅 content_list.json + original_text)
        │
        └── designer 当前输入
                 │
                 ▼
        run_text_standardization / run_multimodal_extraction
                 │
                 ▼
        data/output/structured_text | data/output/multimodal_images
```

- **raw**：designer 的**当前唯一正式输入**，包含图片资源。
- **processed**：上游文本标准化流程的输出，结构为 raw 的子集，**无图片**，designer 示例未支持。