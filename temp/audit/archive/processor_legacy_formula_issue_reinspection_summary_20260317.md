# Processor 遗留公式问题复验摘要

> 仓库变更说明（2026-03-17 后）：当前仓库统一批处理入口为 `porosdata-processor` / `python -m porosdata_processor`，`academic_tools/` 已移除，源码仓运行入口保留 `examples/run_pipeline.py`，数据目录已统一为 `data/raw` 与 `data/processed`。本文为历史审计归档，正文若出现旧路径、旧脚本或旧目录命名，均表示审计发生时的仓库状态。

**复验时间**：2026-03-17  
**复验范围**：`data/processed` 全量 19 篇文档  
**对应实现**：
- `src/porosdata_processor/steps.py`
- `src/porosdata_processor/text_cleaner.py`
- `scripts/audit_aiready_data.py`

---

## 1. 复验结论

本轮已完成计划中的代码修复、专项测试、全量重跑与审计复验。

可确认关闭或明显收敛的问题：

- inline 坏 `array` 环境：已从代表样本中清除
- 假 `\Delta` 并入合金名：`Ni-Nb-Y` 代表样本已恢复
- 半截材料式：`Zr-` / `Cu_60-...` 已从“半个公式”收敛到可读文本或更稳定材料链
- citation 正向验收：`ref[...]` 已可单独计数，不再被审计误判为原始 `[n]`

仍有剩余任务，但已从“结构性坏公式”转为“局部样本清理与审计精炼”。

---

## 2. 全量运行结果

来自 `data/processed/processing_report.json`：

- 总文件数：19
- 成功处理：19
- 错误文件：0
- 总 item 数：1083
- 总耗时：117.96s
- 平均每文件耗时：6.21s
- 吞吐：0.161 files/s
- item 吞吐：9.18 items/s
- 平均 token compression rate：0.113

说明：

- 本轮全量处理成功，无错误文件
- 末段 4 个超长文本块触发了 90s 隔离子进程超时后轻量回退，但整体任务成功完成

---

## 3. 审计结果

来自 `docs/audit/aiready_data_audit_result.json`：

- `segments_with_ocr_issues`: 2
- `segments_with_quality_issues`: 64
- `segments_with_unbalanced_dollar`: 0
- `normalized_ref_count`: 441
- `raw_citation_count`: 40

当前任务清单 Top 项：

1. `semantic_latex_pollution`
   - 3 次，涉及 `00007`、`00013`、`00017`
2. `formula_hyphen_spacing`
   - 101 次，涉及 12 篇文档
3. `digit_internal_space`
   - 4 次，涉及 `00012`、`00019`
4. `raw_citation_protocol`
   - 40 次，涉及 `00010`、`00013`、`00021`

重要变化：

- `broken_inline_environment` 已不再出现在任务清单中
- `ref[...]` 已作为正向协议被单独计数，不再与原始 citation 残留混淆

---

## 4. 代表样本复验

### 4.1 `00001` inline 坏 `array`

原始输入：

- `$\begin{array} ... \end{array}$` 被错误带入正文

当前输出：

- 已恢复为 `$(q = 4 \pi \mathrm{sin} \theta / \lambda)$`
- 不再命中 `broken_inline_environment`

### 4.2 `00001` 假 `\Delta` 合金名

当前输出已恢复为：

- `$\mathrm{Ni-Nb-Y}$`

说明：

- `\DeltaNi` / `\DeltaNb` 这类假前缀代表问题已闭环

### 4.3 `00011` 半截材料式

原始输入：

- `$\mathbf{Zr-}$ and $\mathbf{Mg}$-based ...`

当前输出：

- `Zr- and $\mathrm{Mg}$-based ...`

说明：

- 已不再保留“半个公式”
- 对无法安全合并的样本，已降级为普通文本

### 4.4 `00020` 半截链式材料式

当前输出已收敛为：

- `($\mathrm{Cu_60-Zr}_{30} \mathrm{Ti}_{10})_{100 - x} \mathrm{Sn}_{x}$`

说明：

- 原先的 `$\mathrm{Cu_60 -}$ $...$` 半截链已被合并

### 4.5 `00021` 坏 environment 样本

当前输出：

- `with $\mathsf{q} = \frac{4 \pi}{\lambda} \mathsf{sin} \theta$ ...`

说明：

- inline `array` 已降级为普通行内公式

---

## 5. 剩余问题判断

### 已关闭

- inline 坏 `array` / 残缺 environment 结构问题
- 假 `\Delta` 并入合金名的核心历史问题
- 典型半截材料式保留为“半个公式”的问题
- `ref[...]` 被审计脚本误判为原始 citation 的问题

### 仍需后续收尾

- `formula_hyphen_spacing` 仍较多，但其中包含：
  - 合法或可接受的 `Zr-` / `X-ray` / `$...$-based`
  - 仍值得进一步细分的轻量残形
- `semantic_latex_pollution` 仍残留在 `00007`、`00013`、`00017`
- `raw_citation_protocol` 仍有 40 次，集中在 `00010`、`00013`、`00021`
- 个别材料式仍保留较保守的 LaTeX 结构，如 `$\mathrm{Cu_60-Zr}_{30} ...$`，可在后续继续追求更规范形态

---

## 6. 结论

本轮计划已经按步骤实现并完成复验。  
从上游遗留问题角度看，`Processor` 已完成最关键的三类闭环：

- 结构性坏公式降级
- 假 `\Delta` 合金污染修复
- 半截材料链的修复或保守降级

下一轮优化重点应从“堵大洞”转为：

- 细分 `formula_hyphen_spacing` 的误报与真问题
- 清理低频 `semantic_latex_pollution`
- 收尾剩余原始 citation 样本
