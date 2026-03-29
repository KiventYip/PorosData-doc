# Token Evaluation 高性能方案设计

## 1. 当前方案的性能瓶颈分析

### 1.1 调用链与调用次数

当前流程（MinerU JSON → TextCleaner → token 评估）中：

- **每块文本**：`evaluate_step(raw_text, processed_text)` 内部调用 `_tokenize(raw_text)` 与 `_tokenize(processed_text)`，即 **2 次 `tokenizer.encode()`**。
- **多进程**：每个 worker 进程内 Tokenizer 通过 `TokenizerCache` 只加载一次，但 **encode 仍按块串行调用**，无批量。
- **规模**：
  - 1 PDF ≈ 500 text blocks → 1,000 次 encode
  - 10,000 PDF ≈ 5,000,000 blocks → **10,000,000 次 encode**

### 1.2 瓶颈归纳

| 瓶颈类型 | 说明 | 影响 |
|----------|------|------|
| **encode 调用次数** | 每块 2 次，与块数线性放大 | 大规模下 CPU/内存带宽成为瓶颈 |
| **无批量化** | 单条 `encode(str)`，无法利用 batch API | 无法摊薄 Python 调用与 tokenizer 内部固定开销 |
| **Tokenizer 初始化** | 每进程首次加载 GPT2（网络/磁盘） | 冷启动 3–5 秒 × worker 数 |
| **与清洗强耦合** | 每块清洗完立即评估，无法跨块合并 | 难以做采样或延迟批处理 |

### 1.3 当前代码位置

- `TokenizerEvaluator.evaluate_step()`：内层两次 `self._tokenize()`（evaluator.py）
- `_tokenize()`：`self.tokenizer.encode(text, add_special_tokens=False)`（evaluator.py）
- 调用入口：标准批处理 CLI 最终会进入 `run_processor.py`，其中每个 text item 调用 `_process_single_item_worker()`，内部 `cleaner.clean(text, eval_mode=True)` 最终调用 `evaluate_pipeline`，即每块 2 次 encode。

---

## 2. 推荐的优化架构（总体）

- **评估与清洗解耦**：清洗阶段只产出 `(raw_text, cleaned_text)` 流，评估阶段对“流”做采样/批处理后再调 tokenizer。
- **分层统计**：支持“全量清洗 + 采样评估”，保证压缩率等指标仍具统计意义（见下节）。
- **单进程内**：Tokenizer 仍只加载一次；通过 **批量 encode** 或 **采样 + 批量** 降低调用次数与总耗时。

---

## 3. 三种优化策略

### 策略 A：采样评估（Sampling）

**思路**：仅对一部分文本块做 token 评估，用样本均值/分位数估计整体压缩率。

- **实现要点**：
  - 每 N 块评估 1 块（或按块 ID 哈希取模），或每文件随机采样 K 块。
  - 仅对采样块调用 `tokenizer.encode(raw)` 与 `tokenizer.encode(cleaned)`，其余块不调用。
- **调用次数**：若采样率 10%，则 encode 次数降为原来的 **10%**（例如 10M → 1M）。
- **统计意义**：在块数足够、采样随机或分层时，样本压缩率均值、分位数可估计整体；可报告置信区间（如 bootstrap）。

**优点**：实现简单、与现有清洗逻辑兼容、降幅大。  
**缺点**：不得到每块精确压缩率；需明确报告“基于 N 块采样”。

---

### 策略 B：字符级估计（Token Estimation）

**思路**：用“字符数 / 平均 token 长度”等启发式估计 token 数，不做真实 encode。

- **实现要点**：
  - 例如 `est_tokens = len(text) / 4`（英文约 4 字符/token），或对中文用不同系数；可先在小样本上标定系数。
  - 仅用于汇总指标（如整文件、整批的估计压缩率），不做逐块精确评估。
- **调用次数**：**0 次** tokenizer.encode（仅算术运算）。

**优点**：零 tokenizer 调用、极快、适合 TB 级粗筛。  
**缺点**：非真实 token 数，与真实 GPT 系 tokenizer 有偏差；仅适合趋势/规模估计，不适合精确报表。

---

### 策略 C：批量 Tokenization（Batch Tokenization）

**思路**：先收集多块 `(raw, cleaned)`，再对多段文本一次性调用 tokenizer 的批量接口。

- **实现要点**：
  - 使用 `tokenizer([text1, text2, ...], add_special_tokens=False, return_length=True)` 或分批 `encode` 列表，减少 Python 调用次数与 tokenizer 内部调度。
  - 在“评估阶段”按 buffer 大小（如 32/64 条）累积，满则批量 encode，再算每块压缩率。
- **调用次数**：从 2×块数 降为 **2×ceil(块数/batch_size)**（例如 batch=64 时约 1/64 的调用次数）。

**优点**：保留每块精确压缩率、统计与现有一致；适合多进程内每个 worker 本地批处理。  
**缺点**：需缓冲与延迟输出；超长文本需截断或拆分以控制内存。

---

## 4. 各策略优缺点对比

| 策略 | 优点 | 缺点 |
|------|------|------|
| **A 采样** | 实现简单、调用量线性下降、统计可解释 | 无逐块精确值、需标注“采样” |
| **B 估计** | 零 encode、极快、可 TB 级 | 非真实 token、仅宜粗筛 |
| **C 批量** | 每块精确、调用次数大幅下降 | 需缓冲、实现稍复杂 |

---

## 5. 推荐的最终架构

- **混合**：以 **采样 + 批量** 为主，可选 **估计** 做兜底或预筛。
  - **主路径**：清洗不变；评估侧对“块流”做 **采样**（例如 10% 或每文件至少 K 块），对采样块在进程内 **按 batch 调用 tokenizer**，得到真实压缩率与汇总统计。
  - **可选**：对未采样块或全量做一次 **字符级估计**，仅用于大盘监控（如“估计总 token 节省”），不写入逐块结果。
- **兼容**：保留“全量逐块评估”开关（如 `--eval-full`），用于小规模或调试；默认用“采样 + 批量”。
- **多进程**：每个 worker 仍持有一份 TokenizerCache；worker 内对“本进程处理的块”做采样与批处理，主进程只汇总各 worker 的统计（或再聚合置信区间）。

---

## 6. Python 示例代码实现

见仓库内：`src/porosdata_processor/evaluation_optimized.py`（或 `docs/examples/token_eval_optimized_example.py`）。下面给出核心接口与用法示例。

### 6.1 批量编码 + 采样评估（核心逻辑示例）

```python
# 批量编码：减少 encode 调用次数
def batch_tokenize(tokenizer, texts: List[str], batch_size: int = 64) -> List[int]:
    lengths = []
    for i in range(0, len(texts), batch_size):
        batch = texts[i : i + batch_size]
        # 使用 return_length 避免返回大列表，仅要长度时更省内存
        out = tokenizer(batch, add_special_tokens=False, return_length=True, truncation=True, max_length=8192)
        lengths.extend(out["length"])
    return lengths

# 采样：仅对部分块做真实评估
def should_evaluate_block(block_index: int, sample_rate: float = 0.1, seed: int = 42) -> bool:
    import random
    r = random.Random(seed + block_index)
    return r.random() < sample_rate
```

### 6.2 与现有 pipeline 的集成方式

- 在 `run_processor` 的流式循环中，对每个 text 块：
  - 若未开启评估：与现有一致，不调 tokenizer。
  - 若开启评估且为“采样+批量”模式：
    - 先执行 `clean(original)` 得到 `cleaned`；
    - 将 `(original, cleaned)` 放入进程内 buffer；
    - 若当前块被采样，则 buffer 中对应项标记为“待评估”；
    - 当 buffer 满或文件结束时，对“待评估”的 (raw, cleaned) 列表做 **batch_tokenize**，计算压缩率并更新汇总统计；
    - 未采样块不写入 compression_rate，或写入 None。
- 汇总层：对每个文件/每批报告“基于 N 块采样的平均压缩率”及可选置信区间。

完整可运行实现见：`src/porosdata_processor/evaluation_optimized.py`（`SamplingBatchEvaluator`、`batch_tokenize_lengths`、`TokenEstimator` 等）。

---

## 7. 对 TB 级语料的性能预估

### 7.1 假设

- 1 TB 纯文 ≈ 约 5×10^8 块（按每块约 2KB 计）。
- 当前方案：2×5×10^8 = **10^9 次** encode；若单次 encode 约 0.1 ms，约 **10^5 s ≈ 27.7 小时**（单进程），多进程可近似线性分摊。
- 优化后（采样 10% + batch_size=64）：
  - encode 次数：2 × (5×10^8 × 0.1 / 64) ≈ **1.56×10^6 次**；
  - 单次“批量 encode”约 64 条，耗时量级仍可按 64×0.1 ms 粗算，总耗时约 **1.56×10^6 × 6.4 ms ≈ 10^4 s ≈ 2.8 小时**（单进程），再乘以采样与 I/O 系数（例如 1.5），约 **4–5 小时** 单进程；多进程（如 16 worker）可到 **约 20 分钟内** 完成 token 评估部分。
- 若再启用“字符级估计”仅做大盘监控，评估侧几乎不再占时间，TB 级主要耗时在清洗与 I/O。

### 7.2 小结

- **当前方案**：TB 级评估以 10^9 次 encode 为主瓶颈，多进程下仍可能达数十小时。
- **采样 10% + batch 64**：评估部分可降到数小时内（多进程可到约 20 分钟量级），且统计仍有意义。
- **再叠加估计**：可用于全量“估计总节省”，评估侧延迟可忽略。

---

## 8. 文档与代码索引

- 本文档：`docs/token_evaluation_high_performance_design.md`
- 示例实现：`src/porosdata_processor/evaluation_optimized.py`
  - `SamplingBatchEvaluator`：采样 + buffer + 批量 encode，汇总统计
  - `batch_tokenize_lengths` / `batch_compression_rates`：批量编码与压缩率
  - `TokenEstimator`：字符级估计（零 tokenizer 调用）
  - `should_evaluate_block`：确定性采样
  - `evaluate_one_block`：单块评估（兼容现有逐块评估）
