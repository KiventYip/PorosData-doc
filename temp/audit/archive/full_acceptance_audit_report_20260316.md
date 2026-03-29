# 全量验收审计报告

> 仓库变更说明（2026-03-17 后）：当前仓库统一批处理入口为 `porosdata-processor` / `python -m porosdata_processor`，`academic_tools/` 已移除，源码仓运行入口保留 `examples/run_pipeline.py`，数据目录已统一为 `data/raw` 与 `data/processed`。本文为历史审计归档，正文若出现旧路径、旧脚本或旧目录命名，均表示审计发生时的仓库状态。

**审计日期**：2026-03-16  
**审计依据**：`docs/ai_ready_and_data_mining_delivery_standard.md`  
**审计对象**：`data/processed` 下所有 `*_content_list.json`  
**执行命令**：`porosdata-processor --enable-evaluation --force-reprocess`  
**处理报告**：`data/processed/processing_report.json`  
**质量审计**：`scripts/audit_aiready_data.py` → `docs/audit/aiready_data_audit_result.json`

---

## 1. 审计目的与范围

依据《科学数据处理参考文档：AI-Ready 与 Data Mining 交付标准》，对 Processor 全量修复后的输出进行**量化验收**，确保：

- **AI-Ready**：文本干净、语义清晰、数值/单位/公式可读，Token 使用合理。
- **Data Mining Ready**：实体稳定、属性-值可识别、上下文锚点保留、噪音最小化。
- **交付范围**：正文 `text`，以及图注/图脚注、表题/表脚注、`table_body` 等元数据字段。

本报告结合**处理报告**、**质量审计脚本**与**日志记录**，量化输出验收结论。

---

## 2. 处理执行统计（量化）

### 2.1 处理报告摘要

| 指标 | 数值 | 说明 |
|------|------|------|
| 总文件数 | 4 | 成功处理 4 份 |
| 成功处理 | 4 | 100% |
| 跳过 | 0 | — |
| 错误 | 0 | — |
| 总条目数 | 229 | 229 条 content_list 项 |
| 已处理条目 | 229 | 100% |
| 总耗时（秒） | 19.82 | 约 20 秒 |
| 单文件平均耗时（秒） | 4.96 | — |
| 文件处理速度 | 0.20 文件/秒 | — |
| 条目处理速度 | 11.55 条/秒 | — |
| 控制字符移除 | 0 | 本次无 |
| 自愈触发数 | 0 | — |
| 自愈尝试数 | 0 | — |
| 自愈成功数 | 0 | — |

### 2.2 Token 效率（评估模式）

| 指标 | 数值 | 说明 |
|------|------|------|
| 平均压缩率 | 15.21% | 原始 token 压缩约 15% |
| 最小压缩率 | 8.97% | 单文件最低 |
| 最大压缩率 | 19.04% | 单文件最高 |

---

## 3. 质量审计结果（量化）

### 3.1 AI-Ready 审计摘要

| 指标 | 数值 | 说明 |
|------|------|------|
| 审计文件数 | 4 | 与处理文件一致 |
| 总文本片段数 | 229 | 含正文、公式、图注、表题等 |
| 存在 OCR 残留的片段数 | **0** | 较上轮 7 片段降为 0 |
| 存在未闭合 `$` 的片段数 | **0** | 公式结构完好 |
| 图片项数量 | 38 | — |
| 表格项数量 | 1 | — |
| 图片含 caption | 38 | 100% |

### 3.2 逐文档结果

| 文档 | 条目数 | OCR 问题 | 未闭合 `$` |
|------|--------|----------|------------|
| 00001 | 74 | 0 | 0 |
| 00002 | 62 | 0 | 0 |
| 00003 | 44 | 0 | 0 |
| 00004 | 49 | 0 | 0 |

**结论**：本次全量验收后，**无 OCR 残留**，**无公式结构损坏**。

---

## 4. 日志关键记录

### 4.1 最终验收轮次（2026-03-16 19:01）

```
2026-03-16 19:00:59,516 - porosdata_processor - INFO - _init_text_cleaner - transformers package available, enabling token efficiency evaluation in subprocess
2026-03-16 19:00:59,518 - porosdata_processor - INFO - _init_text_cleaner - TextCleaner initialized (token evaluation will be lazy-loaded in subprocess)
2026-03-16 19:00:59,518 - porosdata_processor - INFO - __init__ - Initialization completed - Input: data/raw, Output: data/processed
2026-03-16 19:00:59,518 - porosdata_processor - INFO - __init__ - Parallel workers: 4, Evaluation mode: True
2026-03-16 19:00:59,518 - porosdata_processor - INFO - __init__ - Memory limit: 2048MB, Initial memory usage: 208.6MB
2026-03-16 19:00:59,518 - porosdata_processor - INFO - __init__ - Target file pattern: *_content_list.json (MinerU raw output)
2026-03-16 19:00:59,519 - porosdata_processor - INFO - run - Starting data processing pipeline
2026-03-16 19:00:59,520 - porosdata_processor - INFO - _collect_files - Discovered 4 files to process
2026-03-16 19:00:59,520 - porosdata_processor - INFO - run - Starting parallel processing of 4 files
2026-03-16 19:01:15,966 - porosdata_processor - INFO - process_batch - Processing progress: 25.0% (1/4 files)
2026-03-16 19:01:16,732 - porosdata_processor - INFO - process_batch - Processing progress: 50.0% (2/4 files)
2026-03-16 19:01:17,422 - porosdata_processor - INFO - process_batch - Processing progress: 75.0% (3/4 files)
2026-03-16 19:01:19,341 - porosdata_processor - INFO - process_batch - Processing progress: 100.0% (4/4 files)
2026-03-16 19:01:19,343 - porosdata_processor - INFO - _save_report - Processing report saved to: data\processed_data\processing_report.json
2026-03-16 19:01:19,344 - porosdata_processor - INFO - _print_summary - Data processing completion report
2026-03-16 19:01:19,344 - porosdata_processor - INFO - _print_summary - Total files: 4
2026-03-16 19:01:19,344 - porosdata_processor - INFO - _print_summary - Successfully processed: 4
2026-03-16 19:01:19,344 - porosdata_processor - INFO - _print_summary - Skipped files: 0
2026-03-16 19:01:19,344 - porosdata_processor - INFO - _print_summary - Error files: 0
2026-03-16 19:01:19,344 - porosdata_processor - INFO - _print_summary - Processed data items: 229
2026-03-16 19:01:19,344 - porosdata_processor - INFO - _print_summary - Total time: 19.82s
2026-03-16 19:01:19,344 - porosdata_processor - INFO - _print_summary - Average file processing time: 4.956s
2026-03-16 19:01:19,345 - porosdata_processor - INFO - _print_summary - Processing speed: 0.2 files/second
2026-03-16 19:01:19,345 - porosdata_processor - INFO - _print_summary - Data item processing speed: 11.6 items/second
2026-03-16 19:01:19,345 - porosdata_processor - INFO - _print_summary - Average token compression rate: 0.152
2026-03-16 19:01:19,345 - porosdata_processor - INFO - _print_summary - Minimum token compression rate: 0.090
2026-03-16 19:01:19,345 - porosdata_processor - INFO - _print_summary - Maximum token compression rate: 0.190
2026-03-16 19:01:19,427 - porosdata_processor - INFO - run - Total memory usage change: +0.2MB (initial: 208.6MB, final: 208.7MB)
```

### 4.2 本次修复涉及的关键特性（日志可印证）

- **小文件标准路径**：`Input file ... is 47532 bytes, below streaming threshold 262144; using standard JSON path`
- **高风险块子进程隔离**：`Using isolated subprocess for high-risk text block (len=2303)`
- **控制字符清洗**：`Detected and cleaned 2 control characters` / `Output sanitization: removed 27 control characters`
- **文档结构校验**：`_validate_document_signatures` 通过，无条目漂移

---

## 5. 与验收标准对照

依据 `docs/ai_ready_and_data_mining_delivery_standard.md` 第九节“质量验收标准”与“拒收条件”：

| 验收项 | 要求 | 审计结果 |
|--------|------|----------|
| 无明显 OCR 断裂数字 | 数字内部/小数点/单位间无断裂 | **满足**：OCR 残留 0 片段 |
| 无明显断裂单位 | 单位连续、统一协议 | **满足**：`\mathrm{}` 等已收紧 |
| 无明显术语碎裂 | 材料名、元素符号等连续 | **满足**：无元素断裂检出 |
| 无结构性公式损坏 | 行内/显示公式结构完整、`$` 配对 | **满足**：未闭合 `$` 为 0 |
| 关键元数据字段已处理 | 图注/表题/脚注纳入清洗 | **满足**：图注 38/38，表题 1/1 |
| 文本适合 AI 与规则处理 | 可读、可抽取 | **满足**：整体可读 |
| table_body 可 mining | 表格内文本节点已清洗 | **满足**：保守 HTML 清洗已启用 |

**拒收条件检查**：

- “Processor 输出仍存在**大量**可见 OCR 断裂”——当前为 **0**，**未触发**。
- “公式、符号或编号结构被破坏”——**未触发**。
- “图注/表题/脚注等重要字段未进入质量清洗范围”——**未触发**。
- “相同类型问题在不同字段上处理标准不一致”——**未触发**。

---

## 6. 结论与建议

### 6.1 总体结论

- **总体结论**：当前 `data/processed` 在本次全量验收下 **符合** AI-Ready 与 Data Mining 文档的交付要求，未触发拒收条件。
- **量化指标**：
  - 处理成功率：4/4 (100%)
  - OCR 残留：0/229 片段 (0%)
  - 公式未闭合：0
  - 元数据覆盖：图注 100%、表题 100%
  - Token 平均压缩率：约 15.2%

### 6.2 复验建议

- 每次修改清洗逻辑后重新执行 `porosdata-processor --enable-evaluation --force-reprocess` 与 `python scripts/audit_aiready_data.py`，并对比 `docs/audit/aiready_data_audit_result.json`，确保无新增 OCR 残留或公式损坏。

---

*报告由 `processing_report.json`、`aiready_data_audit_result.json` 及 `logs/processor.log` 生成，审计标准以 `docs/ai_ready_and_data_mining_delivery_standard.md` 为准。*
