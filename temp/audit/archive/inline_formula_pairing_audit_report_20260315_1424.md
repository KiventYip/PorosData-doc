# 行内公式配对审计报告

> 仓库变更说明（2026-03-17 后）：当前仓库统一批处理入口为 `porosdata-processor` / `python -m porosdata_processor`，`academic_tools/` 已移除，源码仓运行入口保留 `examples/run_pipeline.py`，数据目录已统一为 `data/raw` 与 `data/processed`。本文为历史审计归档，正文若出现旧路径、旧脚本或旧目录命名，均表示审计发生时的仓库状态。

**审计时间：** 2026-03-15 14:24

---

## 1. 审计说明

- **依据：** 交付标准「行内公式 `$...$` 须成对、平衡；所有 `$` 成对出现」。
- **方法：** 对每段交付文本统计 `$` 与 `$$`；若 `$` 总数为奇数或 `$$` 出现次数为奇数，判定该段存在未闭合/未配对。
- **范围：** `data/processed` 下所有 `*_content_list.json` 中字段：`text`、`image_caption`、`image_footnote`、`table_caption`、`table_footnote`。

---

## 2. 审计结果汇总

| 指标 | 数值 |
|------|------|
| 扫描文件数 | 5 |
| 总条目数 | 263 |
| 总文本段数 | 263 |
| 存在未闭合/未配对 $ 的文本段数 | 0 |
| 涉及文件数 | 0 |
| 问题段占比 | 0.00% |

**结论：当前数据中不存在「行内公式未闭合」问题。**

---

## 3. 问题明细

无。


---

## 4. 附录

- **校验规则：** 单段内 `dollar_count = text.count('$')`，`double_dollar_count = text.count('$$')`；若 `dollar_count % 2 != 0` 或 `double_dollar_count % 2 != 0` 则记为问题。
- **复现：** 执行 `python scripts/audit_inline_math_pairing.py`（默认从项目根目录，扫描 `data/processed`）。
