# Processor 执行报告

> 仓库变更说明（2026-03-17 后）：当前仓库统一批处理入口为 `porosdata-processor` / `python -m porosdata_processor`，`academic_tools/` 已移除，源码仓运行入口保留 `examples/run_pipeline.py`，数据目录已统一为 `data/raw` 与 `data/processed`。本文为历史审计归档，正文若出现旧路径、旧脚本或旧目录命名，均表示审计发生时的仓库状态。

**执行时间：2026-03-15 13:45**

---

## 1. 报告目的

本报告用于记录本轮 `Processor` 修复、重处理、复验与交付判断的完整执行情况。

本报告与既有审计链路的关系如下：

- `processor_delivery_acceptance_and_rectification_requirements_20260315_1338.md`：记录初始问题、拒收结论与整改要求。
- `processor_reinspection_audit_report_20260315_1340.md`：记录修复后的复验结果与通过结论。
- **本报告**：记录本轮执行动作、正式处理结果、评估模式观察与性能思考。

---

## 2. 执行背景

本轮执行基于以下背景开展：

- 初始审计已确认旧版 `processed_data` 存在串档、测试污染、元数据未统一清洗、关键实体与结构损坏等问题；
- 按整改要求，已完成字段清洗路径统一、关键 OCR/术语规则补充、公式伪影修复、控制字符统计接入、单元测试补充；
- 本轮重点是对正式目录 `data/processed` 进行重新处理，并结合运行日志评估当前版本是否可交付。

---

## 3. 本轮执行内容

本轮实际完成的执行项如下：

### 3.1 质量修复落实

- 将 `image_caption`、`image_footnote`、`table_caption`、`table_footnote` 纳入共享清洗入口；
- 正式输出阶段移除非交付字段，如 `description`；
- 修复高价值实体与单位问题，包括：
  - `10-ray` -> `X-ray`
  - `1n` / `1 n` -> `In`
  - `K / min` / `K / m i n` -> `K/min`
  - `m l` -> `ml`
  - `a t . %` -> `at.%`
  - `m a s s %` -> `mass%`
- 修复恢复后残留的公式伪影；
- 修复 `$©$` 这类被错误包入数学环境的符号表达。

### 3.2 报告能力补充

- 将控制字符清理情况纳入 `processing_report.json`；
- 新增统计项：
  - `control_chars_removed_total`
  - `files_with_control_char_cleanup`

### 3.3 回归验证

- 执行全量单元测试：
  - `pytest tests/unit -q`
  - 结果：`96 passed`
- 对正式目录 `data/processed` 进行了重新处理；
- 对运行日志进行了性能与 warning 行为观察。

---

## 4. 正式处理结果

当前 `data/processed/processing_report.json` 显示：

| 指标 | 数值 |
|------|------|
| `total_files` | `5` |
| `processed_files` | `5` |
| `error_files` | `0` |
| `total_items` | `263` |
| `processed_items` | `263` |
| `control_chars_removed_total` | `137` |
| `files_with_control_char_cleanup` | `5` |
| `avg_compression_rate` | `0.0364` |

说明：

- 所有目标文件均已成功处理；
- 未出现文件级错误；
- 输出写入阶段共清理控制字符 `137` 个；
- 共有 `5` 个文件在写出时检测到控制字符并完成清理；
- Token 压缩率处于温和区间，未出现异常压缩。

---

## 5. 交付判断

## 5.1 当前结论

**当前 `processed_data` 满足现阶段交付要求，可以交付。**

**当前版本可进入 `Designer`。**

## 5.2 判断依据

当前版本已关闭此前阻塞交付的关键问题：

- `00005` 串档问题已消失；
- 正式输出已清除测试污染字段；
- `00001` 中 `Al/In`、`X-ray`、`©` 等关键问题已修复；
- `00004` 中图注/正文已统一清洗；
- `00004` 的结构性公式残留已修复；
- 形式化报告已纳入控制字符统计，不再只能依赖终端 warning 观察。

综合 `docs/ai_ready_and_data_mining_delivery_standard.md` 的交付标准，当前版本已经达到：

- 无明显 OCR 断裂数字；
- 无明显断裂单位；
- 无明显术语碎裂；
- 无关键元数据字段遗漏处理；
- 文本适合 AI 阅读与规则处理；
- 样本中的关键结构性损坏已收敛。

---

## 6. 运行日志观察

本轮在评估模式下执行了：

```bash
porosdata-processor --enable-evaluation --force-reprocess
```

根据运行日志，可观察到以下行为：

### 6.1 评估模式已正常工作

- `transformers package available`
- `TextCleaner initialized`
- `Average token compression rate` 已输出

说明：

- Token 评估链路已成功启用；
- 每个文档均生成了压缩率统计；
- 处理报告已包含 `token_efficiency` 区段。

### 6.2 控制字符 warning 现已可解释且可统计

日志中多次出现：

- `WARNING - Detected and cleaned N control characters`

这类 warning 现在表示：

- 在输出写入阶段检测到不可见控制字符；
- 程序已自动清除并继续写出；
- 最终结果仍然是成功处理；
- 且对应数量已经进入 `processing_report.json`，不是仅停留在终端告警。

### 6.3 长文本 tokenizer warning 不影响交付质量

日志中出现：

- `Token indices sequence length is longer than the specified maximum sequence length for this model (xxxx > 1024)`

说明：

- 某些文本超过 `gpt2` 的典型上下文长度；
- 这是 **评估器的长度提示**，不是清洗质量错误；
- 它不影响 JSON 产物质量，也不影响本轮交付结论；
- 它主要影响的是评估模式下的日志噪音与性能体验。

---

## 7. 性能执行结果

根据终端执行日志，本轮在 `--enable-evaluation` 模式下的正式处理表现为：

| 指标 | 数值 |
|------|------|
| 总文件数 | `5` |
| 总耗时 | `13.70s` |
| 平均每文件耗时 | `2.739s` |
| 文件吞吐 | `0.4 files/s` |
| 条目吞吐 | `19.2 items/s` |
| 平均 token 压缩率 | `0.036` |

日志还表明：

- 启用了 `8` 个并行 worker；
- 每个子进程都加载了 `gpt2` tokenizer；
- tokenizer 初始化耗时约 `4.7s ~ 4.9s`；
- 初始化阶段伴随多次 `HEAD/GET` 网络请求到 `hf-mirror.com`。

---

## 8. 性能思考

## 8.1 当前性能是否可接受

从“能否完成质量评估”的角度看，当前性能是**可接受的**：

- 5 个文件总耗时约 14 秒；
- 评估链路成功运行；
- 结果稳定、无文件级失败。

但从“常规生产处理”的角度看，当前 `--enable-evaluation` 模式**不适合作为默认生产模式**。原因不是清洗逻辑慢，而是：

- tokenizer 加载成本高；
- 并行子进程重复加载 tokenizer；
- 评估模式引入网络访问；
- 长文本 token 统计本身会产生额外日志和开销。

也就是说，当前瓶颈主要在 **评估链路**，而不是 **清洗链路**。

## 8.2 如果还要修，优先修什么

如果后续继续修复，优先级建议如下：

### 优先级 1：区分“生产模式”和“审计模式”

建议明确：

- 默认生产处理：不开启 `--enable-evaluation`
- 审计/抽检/分析：才开启 `--enable-evaluation`

这是收益最高、风险最低的选择。

### 优先级 2：降低评估模式下的重复 tokenizer 初始化

当前日志显示多个 worker 各自加载 `gpt2`，存在明显重复成本。

可以考虑：

- 在评估模式下降低并发 worker 数；
- 尽量依赖本地缓存；
- 减少首次评估时的网络握手成本。

### 优先级 3：优化评估日志噪音

`Token indices sequence length is longer than ... 1024` 这类提示目前不会影响交付，但会影响运行日志可读性。

后续如需优化，可考虑：

- 对超长文本分段统计 token；
- 或仅在调试模式下输出这类提示。

## 8.3 当前是否需要为了性能继续改代码

**当前不建议为了“可以交付”继续大改清洗规则。**

原因：

- 当前质量已经达到交付要求；
- 进一步修改核心清洗规则的收益有限；
- 回归风险反而会升高。

如果继续优化，应优先选择：

- **只优化评估模式性能**
- **不改动已经稳定的清洗主链路**

---

## 9. 最终结论

本轮执行结论如下：

- **质量结论：通过**
- **交付结论：当前 `processed_data` 可以交付**
- **下游结论：可进入 `Designer`**
- **性能结论：常规处理可接受，评估模式偏重，应作为审计模式使用**

本报告用于记录本轮执行结果、质量判断与性能思考，可作为当前阶段的正式执行归档。
