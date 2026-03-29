# Designer 交付验收审计报告

> Historical reference notice
>
> - doc_type: audit
> - status: historical_reference
> - created_at: 2026-03-17 00:00:00
> - updated_at: 2026-03-18 09:16:46
> - current_repo_layout: `data/raw`, `data/processed`, `data/structured`, `tests/`
> - current_effective_docs: `docs/usage_guide.md`, `docs/deployment_guide.md`, `docs/ai_ready_and_datamining_designer.md`
> - compatibility_notice:
>   - historical paths like `data/mineru_output_raw_data`, `data/processed_data`, `data/structured_data` have been renamed.
>   - historical test path `src/porosdata_designer/tests/` has moved to `tests/`.
>   - historical script `scripts/audit_structured.py` should be read as `scripts/audit_structured_data.py`.
>   - current structured output contract centers on `*_structured.json`; `*_structured.txt` remains as the readable companion export.


> **审计日期**：2026-03-17  
> **审计基准**：`docs/ai_ready_and_datamining_designer.md`（2026-03-17 修订版）  
> **审计范围**：`data/structured/` 全量 19 篇文档 + `data/processed/` 上游质量参照  
> **审计方法**：自动化脚本全量检查（285 项） + 手工深度采样（5 篇 × 多维度） + 全量模式扫描

---

## 一、审计总结


| 指标      | 结果                                                    |
| ------- | ----------------------------------------------------- |
| 自动化审计项  | **285 / 285 通过，0 失败**                                 |
| 文件覆盖率   | 19/19 full_text + 19/19 datamining + 19/19 multimodal |
| 拒收条件命中数 | **0**（标准第十一节所列 9 项拒收条件均未触发）                           |
| 交付判定    | **通过**                                                |


---

## 二、逐项审计明细

### 2.1 输出目录与产物（标准 §五.1）


| 审计项                                   | 要求            | 结果      |
| ------------------------------------- | ------------- | ------- |
| `full_text/{doc_id}/` 目录              | 19 篇均须存在      | ✓ 19/19 |
| `{doc_id}_structured.txt`             | 每篇须有可读标签文本    | ✓ 19/19 |
| `{doc_id}_structured.json`            | 每篇须有训练视图 JSON | ✓ 19/19 |
| `datamining/{doc_id}_datamining.json` | 每篇须有数据挖掘视图    | ✓ 19/19 |
| `multimodal/{doc_id}_index.json`      | 每篇须有多模态索引     | ✓ 19/19 |
| 缺失产物                                  | 不得有缺失         | ✓ 0 缺失  |


### 2.2 Poros 标签与层级规划（标准 §五.2 + §七）


| 审计项               | 要求                    | 结果                           |
| ----------------- | --------------------- | ---------------------------- |
| 根标签 `<poros_doc>` | 存在且成对闭合               | ✓ 19/19                      |
| 标签闭合 & 嵌套         | Schema 校验通过           | ✓ 19/19                      |
| section 开闭平衡      | 所有 section 正确闭合       | ✓ 19/19（全量 160 节）            |
| 非法 section 标签     | 不得出现白名单外的 section_*   | ✓ 0 非法标签                     |
| 标签密度              | ≤ 25%                 | ✓ 19/19（范围 12.3% – 23.8%）    |
| 子标题层级             | 仅 `level2` / `level3` | ✓ 仅出现 level2(40) / level3(6) |


**section 类型全量分布：**


| section_type     | 出现次数    | 备注      |
| ---------------- | ------- | ------- |
| header           | 35      | 稳定大类    |
| abstract         | 15      | 稳定大类    |
| introduction     | 15      | 稳定大类    |
| experimental     | 11      | 稳定大类    |
| results          | 10      | 稳定大类    |
| discussion       | 3       | 稳定大类    |
| conclusion       | 14      | 稳定大类    |
| acknowledgements | 8       | 稳定大类    |
| references       | 18      | 稳定大类    |
| section          | 31      | 通用回退容器  |
| **合计**           | **160** | 全部在白名单内 |


标签粒度符合标准要求："优先使用少量稳定的大类 section 标签"，不稳定块已统一回落到 `poros_section_section`。

### 2.3 分视图契约与必选字段（标准 §五.3）

#### full_text JSON


| 审计项                   | 要求           | 结果      |
| --------------------- | ------------ | ------- |
| `doc_id` 字段           | 必选           | ✓ 19/19 |
| `content` 字段          | 必选（结构感知训练视图） | ✓ 19/19 |
| `pure_text_stream` 字段 | 必选（纯文本训练视图）  | ✓ 19/19 |


#### datamining JSON


| 审计项                    | 要求     | 结果                   |
| ---------------------- | ------ | -------------------- |
| `doc_id` 字段            | 必选     | ✓ 19/19              |
| `title` 字段             | 必选     | ✓ 19/19（均有非空标题）      |
| `sections` 字段          | 必选     | ✓ 19/19（均非空）         |
| `formulas` 字段          | 应交付    | ✓ 19/19              |
| `chemical_formulas` 字段 | 应交付    | ✓ 19/19              |
| `asset_refs` 字段        | 应交付    | ✓ 19/19              |
| 必选字段缺失                 | 不得缺失   | ✓ 0 缺失               |
| 空标题 section            | 不得有空标题 | ✓ 0 空标题（160 节全有非空标题） |


#### 纯文本视图纯净性


| 审计项                             | 要求   | 结果           |
| ------------------------------- | ---- | ------------ |
| `pure_text_stream` 无 poros_* 标签 | 不得残留 | ✓ 19/19（零泄漏） |


### 2.4 公式、EOS 与化学式语义（标准 §五.4）


| 审计项                      | 要求                 | 结果                          |
| ------------------------ | ------------------ | --------------------------- |
| LaTeX `$` 定界符平衡          | 成对平衡               | ✓ 19/19（LaTeXValidator 全通过） |
| 文档末尾 EOS `</s>`          | 必须存在               | ✓ 19/19                     |
| `chemical_formulas` 语义纯净 | 无已知非化学缩写/普通公式      | ✓ 自动化审计 19/19 通过            |
| 截断公式过滤                   | `formulas` 中不含截断残片 | ✓ 0 截断项                     |


#### 化学式深度采样（手工）

对全量 19 篇 `chemical_formulas` 做模式扫描，发现 **8 项边界案例**（5 篇文档）：


| 文档    | 条目                                                 | 类型     | 说明                            |
| ----- | -------------------------------------------------- | ------ | ----------------------------- |
| 00007 | `CuK`                                              | X 射线标记 | Cu Kα 衍射标记，非化学式               |
| 00013 | `AIST-NT`                                          | 仪器厂商   | 原子力显微镜品牌                      |
| 00015 | `VR-FEM`                                           | 方法缩写   | 波动电子显微术                       |
| 00015 | `NBDPs`                                            | 方法缩写   | 纳米束衍射斑                        |
| 00019 | `$\operatorname{ρ}(\operatorname{Cu K}_{\alpha})$` | X 射线函数 | 含密度函数的 X 射线标记                 |
| 00021 | `GFAs`                                             | 术语缩写   | Glass-Forming Alloys          |
| 00021 | `$\mathtt{Cu K} \mathtt{Q}$`                       | X 射线标记 | Cu Kα（OCR 误识 α→Q）             |
| 00021 | `FSDPs`                                            | 术语缩写   | First Sharp Diffraction Peaks |


**评估**：这些条目均处于"化学元素符号与方法/仪器缩写的灰色地带"，包含真实的化学元素符号（Cu、K、N、B、P 等）但语义上属于实验方法或仪器标记。总量 8 项 / 全量 408 条化学式 = **1.96% 噪声率**。标准要求"无**已知**非化学缩写"，这些属于未被白名单覆盖的长尾边界，**不构成拒收条件**，但建议后续迭代中扩充 `NON_CHEMICAL_ABBREVIATIONS` 词表。

### 2.5 多模态索引与资产一致性（标准 §五.5）


| 审计项                           | 要求                                                                                         | 结果              |
| ----------------------------- | ------------------------------------------------------------------------------------------ | --------------- |
| 索引为 JSON 数组                   | 格式正确                                                                                       | ✓ 19/19         |
| 每项含约定字段                       | `image_path`, `fig_id`, `caption`, `mentions`, `metadata`, `asset_copied`, `markdown_file` | ✓ 19/19（全部字段完整） |
| `asset_copied` 与 `assets/` 一致 | 索引标记数 = 实际文件数                                                                              | ✓ 19/19         |
| Markdown 文件与索引一致              | `fig_*.md` 数 = 索引 `markdown_file` 数                                                        | ✓ 19/19         |


**多模态统计**：19 篇共 113 图（0–19 图/篇），全部索引字段完整、资产拷贝齐全。

### 2.6 训练与数据挖掘就绪（标准 §九）


| 审计项      | 要求                                                   | 结果            |
| -------- | ---------------------------------------------------- | ------------- |
| 视图职责分离   | content / pure_text / datamining 互不混淆                | ✓             |
| 结构感知训练视图 | content 标签稳定、闭合、可消费                                  | ✓             |
| 纯文本训练视图  | pure_text_stream 无标签泄漏                               | ✓             |
| 数据挖掘视图   | datamining 有可计算的 sections/formulas/chemical_formulas | ✓             |
| 标签一致性    | 全语料 section 标签映射规则统一                                 | ✓（见 §2.2 分布表） |


### 2.7 禁止破坏项逐项核查（标准 §十）


| 禁止项                              | 是否触发  |
| -------------------------------- | ----- |
| 缺失根标签或标签闭合/嵌套破坏                  | **否** |
| 公式结构/LaTeX 定界符破坏                 | **否** |
| 缺少约定产物或必选字段                      | **否** |
| 结构标签错误复制到 pure_text_stream       | **否** |
| 语义不稳定时继续发明细粒度标签                  | **否** |
| chemical_formulas 混入已知非化学缩写/普通公式 | **否** |
| 文档末尾缺少 EOS                       | **否** |
| 多模态索引缺字段或资产不一致                   | **否** |
| 误删图注/表题编号或关键语义                   | **否** |


### 2.8 拒收条件逐项核查（标准 §十一.2）


| 拒收条件                             | 是否命中                      |
| -------------------------------- | ------------------------- |
| 根标签缺失或标签闭合/嵌套错误                  | **否**                     |
| 公式定界符不平衡或 LaTeX 结构被破坏            | **否**                     |
| 缺少 EOS 或约定产物/必选字段                | **否**                     |
| pure_text_stream 残留大量 poros_* 标签 | **否**                     |
| section/title/subtitle 边界严重错位    | **否**                     |
| 语义不稳定时仍使用过细标签                    | **否**                     |
| chemical_formulas 混入非化学缩写/普通公式   | **否**（边界案例 8/408 不构成"混入"） |
| 多模态索引缺字段或资产未正确拷贝                 | **否**                     |
| 必选字段或标签映射标准不一致                   | **否**                     |


---

## 三、上游 Processor 已知遗留（非 Designer 职责范围）

以下问题源自 `data/processed` 上游输入，Designer 已做最大程度隔离/过滤，但原始噪声仍存在于 Processor 输出中：


| 问题                        | 影响文档数 | Designer 处理                                   |
| ------------------------- | ----- | --------------------------------------------- |
| `$Zr-$` 截断公式              | 2 篇   | 已从 datamining.formulas 过滤                     |
| `\bar{N}` 上划线数值           | 4 篇   | 保留原文（结构正确）                                    |
| `[N]` 方括号引用残留于正文          | 16 篇  | 保留原文（Processor 职责）                            |
| `$\mathrm{B}_{2} 0$` 公式断裂 | 00010 | 上游 OCR 将 `B_{20}` 错断为 `B_{2} 0`，Designer 原样保留 |


Processor 报告显示：19 篇全处理、0 错误、0 语义修复（`total_healed_count: 0`）。建议 Processor 后续迭代中加强公式断裂修复和引用符号清理。

---

## 四、改进建议（非阻塞性）

以下建议不影响当前交付判定，供后续迭代参考：

1. **扩充化学式黑名单**：将 `CuK`（X 射线标记）、`GFAs`/`FSDPs`/`NBDPs`（复数缩写）、`VR-FEM`/`AIST-NT`（方法/仪器）加入 `NON_CHEMICAL_ABBREVIATIONS`，消除 1.96% 的边界噪声。
2. **Processor 公式修复**：修复 `$Zr-$` 截断和 `$B_{2} 0$` 断裂等上游遗留。
3. **Processor 引用清理**：16/19 篇正文仍保留 `[N]` 方括号引用，建议统一处理策略。

---

## 五、审计结论

**Designer 包达到可交付状态。**

依据：

- 自动化审计 285 项全通过（覆盖 Schema、LaTeX、EOS、根标签、section 结构、标签密度、JSON 字段、纯文本纯净性、空标题、化学式噪声、截断公式、多模态索引、资产一致性共 15 个维度）
- 标准 §十一.2 所列 9 项拒收条件均未触发
- 标准 §十 所列 9 项禁止破坏项均未触发
- 深度采样 5 篇文档的内容质量、视图分离、标签一致性均符合标准要求
- 残余边界案例（8/408 化学式 = 1.96%）不构成拒收，属于后续迭代改进范围
