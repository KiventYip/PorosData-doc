# Designer 性能优化执行工作项

> Historical reference notice
>
> - doc_type: audit
> - status: historical_reference
> - created_at: 2026-03-17 16:59:26
> - updated_at: 2026-03-18 09:39:32
> - current_repo_layout: `data/raw`, `data/processed`, `data/structured`, `tests/`
> - current_effective_docs: `docs/usage_guide.md`, `docs/deployment_guide.md`, `docs/ai_ready_and_datamining_designer.md`
> - compatibility_notice:
>   - historical paths like `data/mineru_output_raw_data`, `data/processed_data`, `data/structured_data` have been renamed.
>   - historical test path `src/porosdata_designer/tests/` has moved to `tests/`.
>   - historical script `scripts/audit_structured.py` should be read as `scripts/audit_structured_data.py`.
>   - current structured output contract centers on `*_structured.json`; `*_structured.txt` remains as the readable companion export.


## 说明

本文将 `docs/audit/designer_structured_audit_2026-03-17_161933.md` 中关于性能与扩展性的判断，细化为可直接排期、实施、验证的执行任务。

规划原则：

- 先做“收益最大且不改变输出契约”的优化。
- 先建立性能基线与 profiling，再做结构改造，避免盲目优化。
- 每项任务都要同时给出基准数据、回归样本、验收标准。
- 优化不得破坏既有 `content`、`pure_text_stream`、`structured`、`multimodal` 的输出语义。

## 当前基线

当前实测基线：

- 输入规模：`19` 篇文档，`113` 张图片
- `full_text`：`0.28s`，约 `68.5 docs/s`
- `multimodal`：`0.43s`，约 `43.9 docs/s`

当前判断：

- 小规模下性能优秀。
- 若目标扩展到百篇以上、多图长文档，`multimodal` 侧的重复扫描会先成为主要风险点。

## P0 基线与观测

### PW1. 建立正式性能基线脚本

- 目标：让每次性能改造前后都有可比结果，而不是只看单次日志。
- 涉及文件：
  - `scripts/` 下新增性能基线脚本
  - 可选：`examples/run_all.py`
- 具体动作：
  - 固定统计 `full_text`、`multimodal` 的总耗时、文档吞吐、图片吞吐。
  - 记录文档数、图片数、平均 `content` 长度、平均 section 数。
  - 输出 JSON 或 Markdown 基线结果，便于后续 diff。
- 建议输出字段：
  - `docs_count`
  - `images_count`
  - `full_text_seconds`
  - `multimodal_seconds`
  - `docs_per_second`
  - `images_per_second`
  - `avg_content_length`
  - `avg_sections`
- 验收标准：
  - 同一批输入可重复运行并输出稳定基线。
  - 后续每项优化都能引用同一口径比对结果。

### PW2. 为关键路径增加 lightweight profiling

- 目标：确认 CPU 时间实际耗在何处，避免错误优化方向。
- 涉及文件：
  - `src/porosdata_designer/reorganizers/multimodal_interleaver.py`
  - `src/porosdata_designer/reorganizers/text_aggregator.py`
  - 可选新增 `profiling` 脚本
- 具体动作：
  - 为 `interleave()`、`_build_multimodal_item()`、`_find_precise_mentions()`、`_extract_semantic_anchors()` 增加阶段计时。
  - 为 `TextAggregator._apply_entity_shielding()` 增加单次耗时统计。
  - 将 profiling 开关做成可选，不污染默认日志。
- 验收标准：
  - 能输出方法级耗时占比。
  - 能明确区分 CPU 热点和 IO 热点。

## P1 高收益结构优化

### PW3. 将 `multimodal_interleaver` 主流程切换到“注册表 + 二阶段提取”

- 目标：消除“每张图重复扫描全文”的主瓶颈。
- 涉及文件：
  - `src/porosdata_designer/reorganizers/multimodal_interleaver.py`
- 当前现状：
  - `interleave()` 仍走 `_extract_images()` + `_build_multimodal_item(image, content_list)`。
  - 文件中已经存在 `_build_figure_registry()` 和 `_extract_all_figures_context()`，但未作为主流程使用。
- 具体动作：
  - 将 `interleave()` 主路径改为：
    1. 一次扫描 `content_list` 建立 figure registry
    2. 基于 registry 执行二阶段上下文提取
    3. 输出与旧逻辑保持一致的 multimodal items
  - 保留旧逻辑作为 fallback 或测试对照路径，便于回归。
- 回归样本：
  - `00001`
  - `00010`
  - `00014`
  - `00019`
- 验收标准：
  - 输出字段完全兼容现有格式。
  - 同批输入下 caption / mentions / markdown / asset 拷贝结果不回退。
  - 中大样本基线下 `multimodal` 总耗时明显下降。

### PW4. 合并 caption / mentions / semantic anchors 的重复扫描

- 目标：把每个 fig 的多次全文扫描压缩为共享索引访问。
- 涉及文件：
  - `src/porosdata_designer/reorganizers/multimodal_interleaver.py`
- 具体动作：
  - 在 registry 构建阶段缓存：
    - `fig_id -> caption_candidates`
    - `fig_id -> mention_blocks`
    - `page_idx -> text_blocks`
  - `_extract_single_figure_context()` 不再直接重新遍历 `content_list`。
  - `_find_precise_caption()`、`_find_precise_mentions()`、`_extract_semantic_anchors()` 改为优先消费缓存。
- 验收标准：
  - 单图上下文提取不再出现 3 次以上全文扫描。
  - profiling 显示相关方法累计耗时显著下降。

### PW5. 预构建页级文本索引与块邻接索引

- 目标：优化锚点提取与上下文邻接访问。
- 涉及文件：
  - `src/porosdata_designer/reorganizers/multimodal_interleaver.py`
- 具体动作：
  - 预构建：
    - `page_idx -> text_blocks`
    - `block_id/index -> previous/next blocks`
  - `_get_surrounding_blocks()` 不再每次现算 `page_blocks`。
  - `_extract_semantic_anchors()` 直接使用页索引和邻接索引。
- 验收标准：
  - 锚点提取不再在每次调用时重建页内块列表。
  - 大页数文档上锚点提取耗时稳定下降。

## P2 IO 与批量导出优化

### PW6. 为图片复制与 Markdown 写入增加受控并发

- 目标：降低大批量图片导出时的串行 IO 成本。
- 涉及文件：
  - `src/porosdata_designer/reorganizers/multimodal_interleaver.py`
- 具体动作：
  - 将 `_generate_markdown_and_copy_assets()` 拆为：
    - 路径与任务准备
    - 图片复制任务
    - Markdown 写入任务
  - 使用轻量线程池处理 IO 型任务。
  - 并发数做成可配置，避免在机械硬盘或低 IO 环境下过度争用。
- 风险控制：
  - 保证输出文件名稳定。
  - 保证 item 更新顺序稳定。
- 验收标准：
  - 结果文件数、文件内容、索引字段与串行版本一致。
  - 大图片批次下总耗时下降。

## P3 文本侧优化

### PW8. 压缩 `TextAggregator` 的多轮全文正则扫描

- 目标：减少超长文档下 `TextAggregator` 的 CPU 开销。
- 涉及文件：
  - `src/porosdata_designer/reorganizers/text_aggregator.py`
- 具体动作：
  - 评估 `_apply_entity_shielding()` 中多轮 `re.sub` 是否可合并。
  - 将高频正则预编译为类级常量，避免重复编译。
  - 对不需要跨段处理的逻辑，尽可能改为分块处理而非全文多轮扫描。
- 风险控制：
  - 不能破坏当前对货币符号、LaTeX、化学式的防御性处理。
- 回归样本：
  - `00001`
  - `00003`
  - `00010`
  - `00020`
- 验收标准：
  - `content` 输出不回退。
  - `LaTeX` 与 `chemical_formulas` 审计结果不恶化。
  - profiling 显示实体屏蔽阶段耗时下降。

### PW9. 为超长文档建立分档策略

- 目标：避免所有文档都走同一套重处理路径。
- 涉及文件：
  - `src/porosdata_designer/reorganizers/text_aggregator.py`
  - 可选新增配置文件
- 具体动作：
  - 按文档长度或公式密度分档：
    - 普通文档：现有逻辑
    - 超长文档：更保守、更少轮的实体处理策略
  - 将高成本处理只应用到真正需要的文档。
- 验收标准：
  - 超长文档平均耗时下降。
  - 普通文档输出不受影响。

## P4 质量与性能联合任务

### PW10. 清理低收益结构标签，降低 `content` 标签密度

- 目标：在不损害结构语义的前提下减少 token 膨胀。
- 涉及文件：
  - `src/porosdata_designer/reorganizers/text_aggregator.py`
  - `scripts/audit_structured_data.py`
- 具体动作：
  - 盘点低收益标签来源：
    - 空标题 `section`
    - 语义过弱的 `header`
    - 可合并的重复结构标签
  - 评估是否合并、降级或直接不输出。
- 回归样本：
  - `00003`
  - `00019`
  - `00020`
- 验收标准：
  - 当前 3 个标签密度超阈值样本回到阈值内，或至少明显下降。
  - 章节语义不被破坏。

### PW11. 建立大批量性能回归集

- 目标：让优化以真实扩展场景而不是小样本主观判断为依据。
- 涉及文件：
  - `scripts/` 下新增性能回归脚本
  - `docs/audit/` 下新增基准说明文档
- 具体动作：
  - 建立三档样本集：
    - 小样本：当前 `19` 篇
    - 中样本：约 `100` 篇
    - 大样本：约 `300+` 篇且包含高图密度文档
  - 记录每档的：
    - 文档数
    - 图片数
    - 平均全文长度
    - 总耗时
    - 峰值内存
    - docs/s
    - images/s
- 验收标准：
  - 后续每次性能改造都能在三档数据上复测。
  - 能明确看出优化对规模放大的影响是否被抑制。

## 建议执行顺序

1. `PW1-PW2`
   - 先建立基线和 profiling，统一观察口径。
2. `PW3-PW5`
   - 优先完成 `multimodal` 主流程改造，这是最大收益点。
3. `PW6`
   - 再处理 IO 侧优化。
4. `PW8-PW9`
   - 文本侧优化放在第二阶段，避免过早动高风险逻辑。
5. `PW10-PW11`
   - 最后做标签密度压缩和大批量回归体系。

## 每阶段交付标志

### 阶段一完成标志

- 已有可重复运行的性能基线脚本。
- 已有方法级 profiling 数据。

### 阶段二完成标志

- `multimodal_interleaver` 不再走“每图重复扫描全文”的主路径。
- 中样本上 `multimodal` 耗时明显下降。

### 阶段三完成标志

- 大图片批次下 IO 时间下降。

### 阶段四完成标志

- `TextAggregator` 热点被量化并得到针对性优化。
- 超长文档耗时下降且不损害质量。

### 阶段五完成标志

- 标签密度超阈值样本减少。
- 已具备中大规模批量性能回归能力。

## 最终建议

如果你明确有“大批量数据处理”需求，这套性能优化工作应当进入正式排期，且建议从 `PW3-PW5` 开始实施。  
原因不是当前已经慢，而是当前的实现复杂度在规模放大后会先恶化 `multimodal`，现在改动成本低、收益最大、风险也相对可控。