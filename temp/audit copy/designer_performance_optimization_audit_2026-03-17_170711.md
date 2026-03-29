# Designer 性能优化审计报告

> Historical reference notice
>
> - doc_type: audit
> - status: historical_reference
> - created_at: 2026-03-17 17:07:11
> - updated_at: 2026-03-18 09:39:32
> - current_repo_layout: `data/raw`, `data/processed`, `data/structured`, `tests/`
> - current_effective_docs: `docs/usage_guide.md`, `docs/deployment_guide.md`, `docs/ai_ready_and_datamining_designer.md`
> - compatibility_notice:
>   - historical paths like `data/mineru_output_raw_data`, `data/processed_data`, `data/structured_data` have been renamed.
>   - historical test path `src/porosdata_designer/tests/` has moved to `tests/`.
>   - historical script `scripts/audit_structured.py` should be read as `scripts/audit_structured_data.py`.
>   - current structured output contract centers on `*_structured.json`; `*_structured.txt` remains as the readable companion export.


## 基本信息

- 审计对象：`src/porosdata_designer`
- 审计主题：在保障功能不变前提下，面向服务器部署和大批量数据场景的性能优化
- 审计时间：`2026-03-17 17:07:11`
- 对照数据：`data/processed` → `data/structured`
- 验证范围：
  - 全流程重跑
  - `structured` / `multimodal` 验证脚本
  - `structured` 审计脚本

## 本次实施的优化

本轮实际落地的优化聚焦在 `multimodal` 热路径，原则是“不改变默认输出契约，只减少重复扫描成本”。

已完成改造：

1. 将 `MultimodalInterleaver.interleave()` 从“逐图扫描全文”改为“单次建立 figure registry + processing index，再按图消费索引”。
2. 将 `caption`、`mentions`、`semantic_anchors` 的提取改为优先使用预构建索引，避免对 `content_list` 做重复全量遍历。
3. 保留原有输出字段与默认导出行为：
   - `image_path`
   - `fig_id`
   - `caption`
   - `mentions`
   - `metadata`
   - `asset_copied`
   - `markdown_file`

涉及文件：

- `src/porosdata_designer/reorganizers/multimodal_interleaver.py`

## 功能不变性验证

已执行：

- `python examples/run_all.py --input_dir data/processed`
- `python scripts/validate_structured_output.py`
- `python scripts/validate_multimodal_output.py`
- `python scripts/audit_structured_data.py`

验证结果：

- `validate_structured_output.py`：`19/19` 通过
- `validate_multimodal_output.py`：`19/19` 通过
- `multimodal` 图片总数：`113`
- 图片带 caption 比例：`100%`
- 图片带 mentions 比例：`88.5%`

判断：

- 本次优化未破坏现有输出格式。
- 默认功能保持可用。
- 现有交付链路在回归后仍可正常运行。

## 审计结果

优化后重新审计 `data/structured`：

- 总检查项：`228`
- 通过：`227`
- 失败：`1`
- 警告：`0`

唯一剩余失败项：

- `00003` 的 `TagDensity = 25.44%`

说明：

- 该失败项与本轮性能优化无关。
- 它属于 `content` 结构标签密度提示，不是结构损坏或功能回退。

与优化前相比，当前审计结果从 `225` 通过 / `3` 失败提升到 `227` 通过 / `1` 失败。

## 性能对比

### 优化前基线

来自前一轮审计基线：

- `full_text`：`0.28s`，约 `68.5 docs/s`
- `multimodal`：`0.43s`，约 `43.9 docs/s`

### 优化后实测

本次回归重跑结果：

- `full_text`：`0.21s`，约 `92.2 docs/s`
- `multimodal`：`0.24s`，约 `79.5 docs/s`

### 对比结论

- `multimodal` 总耗时下降：`44.2%`
- `multimodal` 文档吞吐提升：`81.1%`

说明：

- `full_text` 本轮没有做针对性算法改造，其波动更可能来自运行噪声、文件系统缓存或测量抖动，不应把其提升归因于本次优化。
- `multimodal` 的下降幅度与改动位置一致，说明热路径优化已经生效。

## 面向服务器部署场景的判断

### 当前是否足够部署

结论：`可以部署当前版本。`

原因：

- 小到中等规模数据下，当前吞吐已经足以支撑服务器端批处理任务。
- 默认输出契约未变，回归和审计均通过。
- 当前风险主要不是功能稳定性，而是大规模扩展后的线性放大成本。

### 对大批量数据的意义

本次优化的意义主要体现在：

- 把最明显的 `O(图数 × 文本块数)` 重复扫描削弱为“单次建索引 + 按图消费”。
- 在图像密集型文档上，`multimodal` 侧的扩展性显著改善。
- 后续如果扩到百篇以上、多图长文档，这一版比优化前更适合做服务器批量任务。

### 仍需关注的服务器侧瓶颈

1. 图片复制与 Markdown 写入仍是串行 IO。
2. 超长全文下，`TextAggregator` 的多轮全文正则仍可能成为 CPU 热点。
3. 若后续接入并发任务队列，需要进一步评估：
   - 单机磁盘 IO
   - Python 进程并发策略
   - 每批次文档大小分布

## 剩余优化建议

### 建议尽快继续做

1. 为 `multimodal` 导出阶段增加受控并发，优化图片复制和 Markdown 写入。
2. 建立正式性能基线脚本，固定记录 `docs/s`、`images/s`、总耗时和输入规模。

### 建议在数据量继续扩大后做

1. 对 `TextAggregator` 做 profiling，确认正则扫描的真实热点。
2. 继续压缩低收益结构标签，降低 `content` 的标签密度。
3. 建立中样本 / 大样本性能回归集，而不是只用当前 `19` 篇文档评估。

## 最终结论

本轮性能优化是有效的，而且符合“功能不变、面向服务器部署”的要求。

- 输出契约未变
- 回归全部通过
- 当前审计结果未回退，反而略有提升
- `multimodal` 实测耗时下降明显

因此，本次优化可以视为：

`可合并、可部署、可作为后续大批量性能优化的第一阶段成果`