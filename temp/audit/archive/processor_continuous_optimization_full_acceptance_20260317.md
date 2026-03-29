# Processor 持续优化全量验收

> 仓库变更说明（2026-03-17 后）：当前仓库统一批处理入口为 `porosdata-processor` / `python -m porosdata_processor`，`academic_tools/` 已移除，源码仓运行入口保留 `examples/run_pipeline.py`，数据目录已统一为 `data/raw` 与 `data/processed`。本文为历史审计归档，正文若出现旧路径、旧脚本或旧目录命名，均表示审计发生时的仓库状态。

时间：2026-03-17

## 验收范围

- `data/processed` 全量 19 篇文档
- 代码改动覆盖：
  - `src/porosdata_processor/steps.py`
  - `src/porosdata_processor/text_cleaner.py`
  - `scripts/audit_aiready_data.py`
  - `tests/unit/test_cleaner.py`
  - `tests/unit/test_audit_script.py`

## 验收结果

### 1. 全量 Processor

- 总文件：19
- 成功处理：19
- 错误文件：0
- 总 item：1083
- 总耗时：320.04s
- 平均每文件：16.84s
- item 吞吐：3.38 items/s
- 平均 token compression rate：0.127

说明：

- 全量处理成功，无失败文件
- 末段仍有超长块触发 `90s` 隔离子进程超时后 lightweight fallback，这是当前主要性能瓶颈

### 2. 全量 AIReady 审计

- `segments_with_ocr_issues`: 2
- `segments_with_quality_issues`: 28
- `segments_with_unbalanced_dollar`: 0
- `normalized_ref_count`: 481
- `raw_citation_count`: 0

### 3. 已确认关闭的问题

- inline 坏 `array` / 残缺 environment
- 假 `\Delta` 并入合金名
- citation 漏转导致的正文原始 `[n]` 残留
- `ref[...]` 二次处理导致的链式破坏
- `\tt at.%`、`X-ray`、`Mg-based`、`Pt-free` 一批常见残形

## 剩余问题量化

### DQ-001 `semantic_latex_pollution`

- 数量：2
- 文档：`00013`、`00017`
- 优先级：`P0`
- 说明：剩余的是低频语义级公式污染，已经不再是大面积系统性问题
- 建议动作：
  - 抽取两个样本做定点规则
  - 新增 2 个回归测试
  - 重跑目标文档复验

### DQ-002 `formula_hyphen_spacing`

- 数量：48
- 文档：11 篇
- 优先级：`P1`
- 说明：当前主要是公式化连字符术语残形，例如 `Zr-`、`$Zr$-b`、`$\\mathrm{cu}$-b` 一类
- 建议动作：
  - 先按样式聚类，区分“真问题”和“可接受写法/审计误报”
  - 优先清理高频样式：
    - `Zr-` / `Zr-based`
    - `X-ray`
    - 元素符号 + `-based/-free/-rich`
    - 二元材料式如 `Zr-Cu`
  - 补 4~6 个专项单测

### DQ-003 `digit_internal_space`

- 数量：4
- 文档：`00012`、`00019`
- 优先级：`P1`
- 说明：数量已很低，但仍需确认是真 OCR 残留还是图号/页码/参考条目误报
- 建议动作：
  - 对 4 个命中逐条抽样
  - 若属误报，收紧审计
  - 若属真问题，补定向数值修复规则

## 可执行工作任务

1. `P0` 清理 `00013`、`00017` 的 2 个残余语义污染样本，并补回归测试。
2. `P1` 对 48 个 `formula_hyphen_spacing` 命中做样式聚类，输出“真问题/误报/可接受写法”三类清单。
3. `P1` 基于聚类结果补一轮连字符术语清理规则，优先收敛 `Zr-`、`Zr-based`、`Zr-Cu`、`cu-based` 等高频残形。
4. `P1` 对 4 个 `digit_internal_space` 命中逐条复核，决定是修规则还是收紧审计。
5. `P2` 优化超长文本块的 fallback 策略，降低全量运行耗时与 lightweight fallback 比例。

## 结论

当前 `Processor` 已完成本轮主要数据质量闭环，关键结构性问题已关闭。  
全量验收通过的依据是：

- 0 个处理失败文件
- 0 个未闭合 dollar 残留
- 0 个正文原始 citation 残留
- 剩余问题集中在低频语义污染、连字符术语碎片与少量数字空格

后续优化应从“修大缺口”转入“低频样式收尾 + 性能收敛”。
