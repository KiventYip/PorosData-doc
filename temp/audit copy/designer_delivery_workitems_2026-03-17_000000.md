# Designer 交付整改工作项清单

> Historical reference notice
>
> - doc_type: audit
> - status: historical_reference
> - created_at: 2026-03-17 00:00:00
> - updated_at: 2026-03-18 09:39:32
> - current_repo_layout: `data/raw`, `data/processed`, `data/structured`, `tests/`
> - current_effective_docs: `docs/usage_guide.md`, `docs/deployment_guide.md`, `docs/ai_ready_and_datamining_designer.md`
> - compatibility_notice:
>   - historical paths like `data/mineru_output_raw_data`, `data/processed_data`, `data/structured_data` have been renamed.
>   - historical test path `src/porosdata_designer/tests/` has moved to `tests/`.
>   - historical script `scripts/audit_structured.py` should be read as `scripts/audit_structured_data.py`.
>   - current structured output contract centers on `*_structured.json`; `*_structured.txt` remains as the readable companion export.


> 日期：2026-03-17
> 基准标准：`docs/ai_ready_and_datamining_designer.md`（2026-03-17 修订版）
> 审计范围：`data/structured/` 下 19 篇文档全量

---

## 一、整改背景

对照 `ai_ready_and_datamining_designer.md` 交付标准，对 `data/structured` 全量 19 篇文档执行深度审计后，
发现以下问题并已在本轮整改中修复：

| 问题类型 | 整改前 | 整改后 |
|---------|--------|--------|
| datamining 空标题 section | 7 篇 / 11 处 | 0 |
| chemical_formulas 语义噪声 | 2 篇 / 5+ 项 | 0 |
| 截断公式残留于 formulas | 3 篇 / 4 项 | 0（已过滤） |
| 审计脚本与实际格式不匹配 | .jsonl + structured 字段 | 已适配 .json + datamining 分离 |

---

## 二、已完成的修改

### P0-1：化学式过滤器强化

**文件**：`src/porosdata_designer/reorganizers/text_aggregator.py` — `_is_valid_chemical_formula()`

新增过滤规则：
1. **含 `=` 的表达式**判定为方程，不归入化学式（修复 `$T = 67 \bar{3} \mathrm{K}$` 等温度赋值）
2. **含数学 LaTeX 命令**（`\int`、`\frac`、`\sum`、`\Gamma`、`\approx` 等）判定为公式，不归入化学式（修复积分/热力学表达式）
3. **函数记号** `S(q)`、`F(x)` 形式判定为物理函数，不归入化学式
4. **单元素 + 非化学计量下标**（含字母变量 `i,j,k` 或分数 `/,`）判定为物理量符号（修复 `$S_{ij}(q)$`、`$F_{i,1/2}$`）
5. **单元素 + `\mathrm{}` 单位** 不再作为化学式正向信号（修复 `$T = ... \mathrm{K}$`）

### P0-2：空标题 section 修复

**文件**：`src/porosdata_designer/reorganizers/text_aggregator.py` — `_merge_document_order_sections()`

- 当 MAIN_TEXT 在无当前 section 时创建隐式 `poros_section_section`：
  - 短文本（≤80 字符、无换行）视为文章类型标签（如 `Short communication`、`Review`），用作 section 标题
  - 长文本仍开启 section 并保留空标题标签

**文件**：`src/porosdata_designer/data_mining_mapper.py` — `_to_structured_json()`

- 兜底逻辑：若 section 无 title 标签或标题为空，从第一段文本截取前 80 字符作为标题

### P0-3：截断公式过滤

**文件**：`src/porosdata_designer/data_mining_mapper.py` — `_to_structured_json()`

- 在 `formulas` 去重后，过滤以 `-` / `–` 结尾的截断公式（上游 Processor 断裂遗留）

### P0-4：审计脚本重写

**文件**：`scripts/audit_structured_data.py`

- 全面适配当前分文件交付格式：
  - `full_text/{doc_id}_structured.json`（`doc_id` / `content` / `pure_text_stream`）
  - `datamining/{doc_id}_datamining.json`（`doc_id` / `sections` / `formulas` / `chemical_formulas` / `asset_refs`）
  - `multimodal/{doc_id}_index.json`
- 新增审计项：空标题检查、化学式噪声检查（含模式匹配 + 缩写词表）、截断公式检查
- 移除对旧 `.jsonl` 格式和 `structured` 字段的依赖

---

## 三、审计结果

```
Total documents: 19
Passed: 285  Failed: 0
```

### 审计覆盖项（每篇 15 项，共 285 项）：

| 审计维度 | 检查内容 | 19/19 通过 |
|---------|---------|-----------|
| Schema | Poros 标签闭合与嵌套 | ✓ |
| LaTeX | 公式 `$` 定界符平衡 | ✓ |
| EOS | 文档末尾 `</s>` | ✓ |
| TagPrefix | 根标签 `<poros_doc>` 存在 | ✓ |
| ContentView | section 开闭匹配、单例不重复 | ✓ |
| TagDensity | 标签字符占比 ≤ 25% | ✓ |
| FullTextJSON | `doc_id` / `content` / `pure_text_stream` 三字段 | ✓ |
| PureTextView | `pure_text_stream` 无 poros_* 标签 | ✓ |
| DataminingJSON | `doc_id` / `sections` 必选字段 | ✓ |
| StructuredView | sections 非空 | ✓ |
| BlankTitle | 所有 section 有非空标题 | ✓ |
| ChemNoise | chemical_formulas 无非化学缩写/公式噪声 | ✓ |
| TruncatedFormula | formulas 无截断残片 | ✓ |
| Multimodal | 索引 schema 完整 | ✓ |
| Assets | 图片拷贝与索引一致 | ✓ |

### section 类型分布（全量 19 篇）：

| section_type | 出现次数 |
|-------------|---------|
| header | 35 |
| abstract | 15 |
| introduction | 15 |
| experimental | 11 |
| results | 10 |
| discussion | 3 |
| conclusion | 14 |
| acknowledgements | 8 |
| references | 18 |
| section (通用) | 31 |

---

## 四、交付判定

基于上述审计结果，Designer 包当前状态满足 `ai_ready_and_datamining_designer.md` 的所有交付要求：

1. **结构完整**：19/19 文档 Schema / 标签闭合 / EOS / 根标签 全通过
2. **视图分离**：`content`（结构感知训练）、`pure_text_stream`（纯文本训练）、`datamining`（数据挖掘）三视图字段完整且语义不混淆
3. **标签稳定**：采用稳定大类 section 标签，不稳定块统一回落到 `section`，标签密度合理
4. **语义纯净**：`chemical_formulas` 无已知噪声，`formulas` 无截断残片
5. **多模态一致**：索引与资产对齐

**结论：Designer 包达到可交付状态。**

---

## 五、已知上游遗留（Processor 职责范围）

以下问题源于上游 Processor 的输出质量，不在 Designer 修复范围内，但 Designer 已做最大程度隔离：

| 问题 | 影响文档 | Designer 处理方式 |
|------|---------|-----------------|
| `$Zr-$` 截断公式 | 00001, 00017, 00021 | 已从 datamining.formulas 过滤 |
| `$Z \mathrm{r}_{66}-$` 截断公式 | 00001 | 已从 datamining.formulas 过滤 |
| `[N]` 方括号引用残留于正文 | 16/19 篇 | 保留原文，不改写 |
| `\bar{N}` 上划线数值 | 4 篇 | 保留原文，不改写 |

建议后续在 Processor 层面修复上述断裂/噪声问题。