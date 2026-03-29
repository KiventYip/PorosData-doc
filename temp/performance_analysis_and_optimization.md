# Processor 性能分析与优化说明

## 一、可能导致“整体性能下降”的原因

1. **启用 `--enable-evaluation` 时的额外开销**
   - 每个子进程会加载一次 GPT-2 tokenizer（网络/磁盘），用于 token 效率评估。
   - 多进程并行时，N 个 worker = N 次 tokenizer 加载（例如 5 个文件并行 ≈ 5 次加载），首轮会有明显延迟。
   - **已优化**：原先在**每条文本**处理时都新建 `TokenizerEvaluator` 和 `TextCleaner`，现已改为**进程内复用**带 evaluator 的 `TextCleaner`，仅首条会触发 tokenizer 加载，后续条目不重复创建对象。

2. **单文件内串行处理**
   - 每个文件在单个子进程内按条目顺序处理（流式读取 + 逐条清洗），文件内无并行。
   - 设计如此：保证顺序、内存可控；若单文件条目很多，该文件总耗时会线性增加。

3. **单条超时与单文件超时**
   - 单条文本处理超时 120s、单文件总超时 600s。若某条或某文件卡住，会拉长整体时间或触发超时报错，观感上像“变慢”。

4. **ijson 流式解析**
   - 流式解析适合大文件、省内存，但解析开销比一次性 `json.load` 略高；小文件若用 standard 路径（无 ijson 时）会整文件加载，二者各有取舍。

---

## 二、已实施的优化（本次）

- **进程级复用带 Evaluator 的 TextCleaner**
  - **位置**：标准批处理 CLI 内部调用的 `run_processor.py` 中 `_get_process_text_cleaner(enable_evaluation=True)` 与 `_do_processing()`。
  - **原问题**：`enable_evaluation=True` 时，每条文本都 `TokenizerEvaluator()` + `TextCleaner(evaluator=...)`，造成大量重复创建和潜在重复加载。
  - **现行为**：`enable_evaluation=True` 时，进程内只创建一次 `TextCleaner.with_tokenizer_evaluation("gpt2")` 并缓存；tokenizer 仍由 `TokenizerCache` 在进程内只加载一次。每条文本只调用 `cleaner.clean(text, eval_mode=True)`，不再新建 evaluator/cleaner。
  - **效果**：减少每条文本的对象创建与重复初始化，eval 模式下整体吞吐会提升，首条之后的条目不再承担 evaluator/cleaner 的创建成本。

---

## 三、可选的进一步优化空间

| 方向 | 说明 | 风险/成本 |
|------|------|------------|
| **eval 时减少并行度** | 例如 `--enable-evaluation` 时默认将 `max_workers` 调小（如 2），减少多进程同时拉 tokenizer 的争用与重复下载。 | 总墙钟时间可能略增，但首轮更稳、资源更可控。 |
| **小文件用 standard 路径** | 当输入 JSON 文件小于某阈值（如 5MB）时，用 `json.load` 整文件解析替代 ijson 流式，可能略快。 | 需测具体数据；大文件仍应用流式。 |
| **预下载 tokenizer** | 首次运行前在环境内执行一次 `AutoTokenizer.from_pretrained("gpt2")`，使缓存命中，避免多进程同时冷启动。 | 需文档说明或脚本封装。 |
| **单条/单文件超时可配置** | 通过 CLI 或配置暴露 `timeout_seconds`、`timeout_per_file`，便于对大数据集调大。 | 无逻辑风险，仅配置扩展。 |

---

## 四、如何确认“性能下降”是否缓解

- 使用 **相同数据集** 与 **相同参数**（如 `--enable-evaluation --force-reprocess`）跑一遍，对比优化前后的：
  - 总耗时（墙钟时间）；
  - 日志中 “Tokenizer loaded successfully” 出现次数（应为 **每进程 1 次**，而不是每条约 1 次）；
  - 是否仍出现单文件/单条超时。
- 若仍感觉慢，可重点看：
  - 单文件条目数是否特别多（如 00001 有 74 条）；
  - 是否触发了单文件 10 分钟超时或单条 2 分钟超时。

---

## 五、小结

- **包整体性能下降** 的主要原因已定位为：eval 模式下**每条文本都新建 Evaluator 和 TextCleaner**，带来多余对象创建与潜在重复初始化。
- **已做优化**：改为进程级复用带 evaluator 的 TextCleaner，tokenizer 继续由 TokenizerCache 在进程内只加载一次。
- **可选优化**：减少 eval 时并行度、小文件用 standard 解析、预下载 tokenizer、超时可配置等，可按需逐步采纳。
