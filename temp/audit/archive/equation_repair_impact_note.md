# 本次 Equation/显示公式修复对其它模块的影响说明

> 仓库变更说明（2026-03-17 后）：当前仓库统一批处理入口为 `porosdata-processor` / `python -m porosdata_processor`，`academic_tools/` 已移除，源码仓运行入口保留 `examples/run_pipeline.py`，数据目录已统一为 `data/raw` 与 `data/processed`。本文为历史审计归档，正文若出现旧路径、旧脚本或旧目录命名，均表示审计发生时的仓库状态。

## 一、修改范围（仅公式修复链路）

| 位置 | 修改内容 |
|------|----------|
| `steps.py` | `_find_env_body` 在遇到 `\` 时先检查是否为 `\end{env}`，避免跳过 `\end{array}` |
| `steps.py` | `_repair_display_formula_content` 对结构化公式不再做整段括号数校验 |
| `steps.py` | `_apply_display_formula_repair` 去掉对 `part`/`repaired` 的二次括号校验 |
| `steps.py` | `_repair_structured_display_formula` 对“仅因 `\{-\}`→`-` 少 2 个括号”的单元格仍采用 repaired |

**未改动的部分**：非公式的正文流水线、Shield 保护逻辑、引用/术语/编号等插件、run_processor 的 text/table/image 分支。

---

## 二、对“校对/验证”的影响

### 1. run_processor 主流程（当前生产路径）

- **结论：无影响**
- run_processor **未使用** DataSentinel、Shield.verify_integrity，也没有“原文 vs 处理后”的逐字校对。
- equation 类型只走 `_normalize_equation_latex_item` → `_apply_display_formula_repair`，不经过 TextCleaner / Shield。
- 正文中的 `$$...$$` 在 TextCleaner 的 `_pre_shield_processing` 里通过 `local_text_compression` 调用 `_apply_display_formula_repair`，修复发生在 Shield 之前，与现有逻辑一致，只是现在更多 array 公式会被正确修好。

### 2. defensive_validator（LaTeX 配对与结构）

- **结论：无负面影响**
- 校验的是：`$` 个数为偶、`$$` 个数为偶、数学环境内括号/花括号平衡。
- 本次修复只改 `$$...$$` **内部**空格与括号收紧，不增删 `$`/`$$`，且修复后仍调用 `_validate_latex_structure(repaired)`，保证花括号平衡，因此不会引入“公式配对不完整”或“展示公式未闭合”等错误。

### 3. Shield.verify_integrity / DataSentinel（可选 QA 路径）

- **结论：设计上本就允许公式被改写，无新问题**
- `verify_integrity(original_text, processed_text)` 要求 `original_text == processed_text`（及 Unicode/可见字符一致）。
- 一旦流水线里包含**公式修复**（如 local_text_compression），公式内容本来就会从“原始 OCR”变为“收紧后”，即 `original != processed`，integrity 会不通过，这是**预期行为**，不是本次修改新引入的。
- run_processor 当前**未启用** Sentinel/Shield 的 integrity 校验，因此生产跑批不受影响。

### 4. 其它校验 / 自愈

- **结论：无直接依赖**
- `tools.py` 的 Shield 占位与还原、boundary integrity 等针对的是“占位符与还原后文本”的一致性，不依赖公式内部的括号数或 array 解析。
- 自愈（boundary healer）仅在 integrity 失败时尝试修复边界，不依赖 `_bracket_counts_match` 或本次改动的公式逻辑。

---

## 三、是否存在“明确问题”

### 已排除的问题

1. **array 列说明被误修**  
   - 已通过“跳过 `\begin{array}` 后空白 + `{ spec }`”修正，列说明 `{ r l }` 不再进入单元格修复，单元测试 `test_equation_array_spec_unchanged` 通过。

2. **非 array 的 $$...$$ 被误伤**  
   - 只有匹配 `\begin{array}` / `\begin{matrix}` / `\begin{aligned}` 的块才走“按单元格拆分 + 每格修复”，其它显示公式仍走整段 `_repair_formula_content`，逻辑未放宽。

3. **括号数校验被全面取消**  
   - 非结构化显示公式仍保留 `_bracket_counts_match(inner, repaired)`，只有“结构化公式”和“仅因 `\{-\}` 少 2 括号的单元格”两处放宽，其它不匹配仍回退原内容。

### 需要留意的边界（非 bug）

1. **结构化公式整段不再做括号数校验**  
   - 若某单元格因其它原因（非 `\{-\}`）导致括号数变化且我们误用了 repaired，理论上可能得到括号不平衡的一格；当前仍保留该格的 `_validate_latex_structure(repaired)` 和“仅允许 (2,2) + 含 `\{-\}`”的放宽条件，实际风险可控。

2. **`_find_env_body` 先检查 `\end`**  
   - 仅影响“能否正确找到 `\end{array}` 位置”，不改变非 array 内容，也不会把非 array 块当 array 处理。

---

## 四、结论

- **本次修复不会**改变 run_processor 的校对/验证逻辑（当前主路径本身无公式逐字校对）。
- **不会**破坏 defensive_validator 的 LaTeX 配对与结构校验；修复后仍保证 `$`/`$$` 配对与花括号平衡。
- **不会**引入对 Shield/Sentinel 的新依赖；若将来启用 Sentinel，公式被修复导致 integrity 不通过是既有设计，非本次修改引入。
- **无已知明确问题**；仅在“结构化公式 + 单元格内仅 `\{-\}` 导致括号差”处放宽校验，并增加对 `\end{env}` 的识别，风险可控且已有单元测试覆盖。

如后续在具体文档或流水线中看到异常（例如某类 equation 仍未被修、或某处校验误报），可针对该用例再做单点排查。
