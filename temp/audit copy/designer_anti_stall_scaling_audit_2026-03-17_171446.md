# Designer 大数据量防卡死与扩展性审计报告

> Historical reference notice
>
> - doc_type: audit
> - status: historical_reference
> - created_at: 2026-03-17 17:14:46
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
- 审计目标：在功能不变前提下，降低大数据量处理时的卡顿、长时间无响应和单次任务过重风险
- 审计时间：`2026-03-17 17:14:46`
- 适用场景：
  - 服务器批处理
  - 大批量文档输入
  - 图像密集型论文批量处理

## 本轮新增优化与防卡死策略

本轮在上一轮热路径优化基础上，继续加入了“面向大数据量运行”的保护策略，但对外仍只保留默认全量交付链路。

### 已实施内容

1. 为 `MultimodalInterleaver` 增加内部受控并发 IO

- 默认使用保守线程数，不激进并发
- 目标是降低图片复制与 Markdown 写入在大批量下的串行阻塞风险
- 该能力作为内部实现保留，不再作为用户可选入口暴露

2. 对外入口仍保持单一全量交付模式

- `examples/run_multimodal_extraction.py` 仅保留标准全量导出流程
- `examples/run_all.py` 仅保留标准全流程交付流程
- 不再暴露额外控制开关，避免交付策略分叉

## 功能不变性验证

默认完整模式已重新回归验证：

- `python examples/run_all.py --input_dir data/processed`
- `python scripts/validate_multimodal_output.py`
- `python scripts/audit_structured_data.py`

结果：

- `validate_multimodal_output.py`：`19/19` 通过
- `audit_structured.py`：`227` 通过，`1` 失败
- 唯一失败仍是 `00003` 的 `TagDensity 25.44%`

判断：

- 本轮防卡死优化没有破坏默认输出契约。
- 完整模式仍可直接作为正式交付链路使用。

## 性能与稳定性判断

### 当前默认模式

默认完整模式仍可正常运行，适合正式产物生成。

### 当前新增的扩展保护

本轮新增的保护重点不是让小样本继续提速，而是让大样本更不容易出现：

- 单次任务过长
- IO 长时间阻塞
- 一次性全量处理导致的感知卡顿
- 服务器部署时“任务看起来卡住但其实只是没有进度反馈”

### 对“卡死风险”的实际改善

从工程视角看，本轮的改进重点是：在不引入额外交付入口的前提下，降低默认全量交付链路中的热路径与 IO 阻塞风险。

这类改动的意义是：

- 即使保持单一全量交付入口，图像复制与 Markdown 写入阶段也不再完全受制于串行热路径
- 不需要引入额外操作模式，就能获得更稳的服务器侧处理表现

## 推荐的服务器运行策略

### 1. 正式交付模式

用于生成最终完整产物：

```bash
python examples/run_all.py --input_dir data/processed
```

适用：

- 需要完整 `structured`
- 需要图片资产和 Markdown
- 统一正式交付口径

## 仍然存在的风险点

### 1. `TextAggregator` 仍有超长文档 CPU 热点风险

当前还没有针对全文正则链做第二阶段优化。

### 2. 还没有正式的性能基线脚本

当前仍依赖运行日志和手动复测，不利于后续持续评估大规模扩展效果。

## 下一步建议

### 优先建议

1. 新增独立的性能基线脚本，记录：
   - 文档数
   - 图片数
   - 总耗时
   - docs/s
   - images/s

2. 对 `TextAggregator` 增加 profiling 开关，定位超长全文热点。

### 运维建议

1. 保持单一正式交付入口，避免人为切换运行策略造成产物口径分叉。
2. 如需进一步扩容，优先继续做内部性能基线和热点 profiling，而不是增加新的外部入口分支。

## 最终结论

本轮不仅做了性能优化，也补上了“防卡死”的运行规划与工程护栏。

可以明确说，当前版本已经比原先更适合服务器和大批量场景，原因在于：

- 默认完整模式仍然可交付
- 已支持受控并发
- 已能在不改变默认输出契约的前提下降低大任务卡顿风险

如果你的核心目标是“不要因为数据量大而出现明显卡顿或单次任务卡死”，那么当前这一版已经完成了第一阶段工程化改造；下一步最值得继续做的是：

`建立正式性能基线 + TextAggregator profiling`