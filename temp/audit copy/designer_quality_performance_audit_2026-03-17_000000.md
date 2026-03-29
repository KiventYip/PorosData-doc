# Designer 包审计报告

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


## 基本信息

- 审计对象：`src/porosdata_designer`
- 审计范围：`data/structured`、`data/processed`、`docs/ai_ready_and_datamining_designer.md`
- 审计主题：数据质量、性能耗时、审计工具有效性
- 审计时间：`2026-03-17`
- 审计人：Cursor Agent

## 审计结论

当前 `Designer` 包在本批次 `structured` 上表现为“设计方向合理，但视图契约与结构化实现尚未完全跟上”。

- 表层合规：19 份文档、19 份 full_text、19 份 multimodal 索引均已产出；官方审计脚本共计 152 项检查，通过 151 项，失败 1 项，通过率 `99.34%`。
- 设计合理项：`content` 中保留 Poros 标签、以 `section/title/subtitle` 表示专业结构、以 `</poros_section_*>` 表示块级强边界，这一方向与长文本结构感知训练目标一致。
- 视图契约问题：`pure_text_stream`、`structured` 字段与新定义仍存在系统性落差，说明现有实现和审计口径滞后于标签设计。
- 真实质量缺陷：LaTeX 失衡、章节重复/错位、化学式误报、旧验证脚本目录漂移仍然是需要修复的工程问题。
- 综合评级：`有条件通过`

## 审计依据

- 规范文档要求 `Designer` 交付 `doc_id`、`content`、`pure_text_stream`、`structured` 四个必选字段，且 `pure_text_stream` 应为“去标签后的纯净文本流”，`structured` 应服务于数据挖掘与检索。
- 现有自动化审计脚本：`scripts/audit_structured_data.py`
- 现有批处理性能日志：
  - `logs/run_all_2026-03-17.log`
  - `logs/run_text_standardization_2026-03-16.log`
  - `logs/run_multimodal_extraction_2026-03-03.log`

## 样本与量化结果

- full_text 文档数：`19`
- multimodal 文档数：`19`
- multimodal 图片总数：`113`
- `content` 平均长度：`27672.6` 字符
- `pure_text_stream` 平均长度：`25883.4` 字符
- `structured.paragraphs` 平均数：`29.5`
- `structured.formulas` 平均数：`50.7`
- `structured.chemical_formulas` 平均数：`57.7`
- `structured.asset_refs` 平均数：`8.1`

## 主要发现

### A. 设计合理项

#### A1. `content` 作为结构感知训练视图的方向成立

- 在带标签全文中保留 `poros_section_*`、`poros_title_*`、`poros_subtitle_*`，可以帮助模型识别摘要、方法、结果、结论等专业结构边界。
- `</poros_section_{type}>` 作为块级强边界信号，与全局 `</s>` 并存，是合理的长文本训练设计，而不是格式噪音本身。
- 用 `section` 替代一级/二级标题的纯排版外观，转而保留“结构语义”，符合当前专业文本训练目标。

#### A2. 现有审计应区分“标签存在”和“字段契约失败”

- 标签出现在 `content` 中不应被默认判为失败。
- 需要被判定为失败的是：标签错误进入 `pure_text_stream`，或标签闭合但语义错位、无法被稳定消费。

### B. 视图契约问题

#### B1. `pure_text_stream` 不满足“纯净文本流”定义

全量 19/19 文档都在 `pure_text_stream` 中残留 `poros` 标签，属于系统性问题，不是个别坏样本。

- 量化结果：`19/19` 文档存在标签残留。
- 抽样命中：`00001=255` 个标签、`00002=121` 个、`00003=157` 个、`00004=117` 个、`00005=28` 个。
- 直接影响：
  - 训练语料 token 被结构标签污染。
  - 下游若假定该字段为纯文本，将出现切词、索引、Embedding 质量偏差。
  - 与规范中“去标签后的纯净文本流”不一致。

代码原因：

- `DataMiningMapper._to_pure_text_stream()` 只移除固定标签：
  - `title/abstract/keywords/main_text/conclusion/references/abs/meth/res`
- 但当前聚合器实际产出大量动态标签：
  - `section_*`
  - `title_*`
  - `subtitle_*`
  - 以及部分 `equ/chem` 标签未被完全剥离

对应代码位置：

- `src/porosdata_designer/data_mining_mapper.py`
- `src/porosdata_designer/reorganizers/text_aggregator.py`

#### B2. `structured.sections` 全量为空

`structured` 字段虽然存在，但 section 层结构并未真正落盘。

- 量化结果：`19/19` 文档的 `structured.sections == []`
- 直接影响：
  - 结构化层丢失章节边界，降低数据挖掘、检索、段落定位和 section-aware 抽取的可用性。
  - 规范要求 `structured` 作为结构化 JSON 服务于数据挖掘，但当前更接近“段落/公式/化学式平铺表”。

代码原因：

- `DataMiningMapper._to_structured_json()` 初始化了 `sections`，但后续没有填充逻辑。

### C. 真实质量缺陷

#### C1. 化学式抽取存在明显误报

现有 semantic noise 审计只拦截固定缩写白名单，无法覆盖“单位、参数名、状态符号、生物计数”这类领域噪声。

- 量化结果：`8/19` 文档出现可疑化学式项。
- 抽样示例：
  - `00010`：`$50 ~ \mathrm{CFU/mL}$`、`$S_{\mathrm{m}}$`
  - `00010`：`ATCC13311`
  - `00002`：`$H_{\mathrm{v}}$`
  - `00003`：`$H_{\mathrm{c}}$`
  - `00012`：`$H_{Au - Si}^{m i x}$`
  - `00010`：`$\mathsf{Ag} / \mathsf{AgCl}$`、`$\mathtt { Cu / Cr }$`

风险判断：

- 这些条目并非都是真正的材料/化学式实体。
- 当前 `chemical_formulas` 字段同时混入单位、物理符号、实验参数、菌落计数与材料式，影响后续知识抽取与实体归并。

#### C2. 章节装箱存在重复与错位

自动化 Schema 校验通过，不代表章节语义正确。

- 重复 `conclusion`：`5/19` 文档
  - `00010`、`00012`、`00014`、`00020`、`00021`
- 重复 `references`：`1/19` 文档
  - `00010`
- 重复 `abstract`：`2/19` 文档
  - `00006`、`00019`

表现：

- 某些文档在正文后又生成空的 `conclusion` 或重复 `references` 区块。
- 个别文档把实验正文段落装入 `references` section。

影响：

- 虽然 XML 标签闭合合法，但 section 语义错位会破坏基于章节的抽取逻辑。

#### C3. 验证脚本存在目录漂移

`scripts/validate_structured_output.py` 与 `scripts/validate_multimodal_output.py` 仍指向旧目录 `data/output/...`，无法直接验证当前产物 `data/structured/...`。

- 实测结果：两脚本在本次审计中均直接报 “Output directory does not exist”
- 影响：
  - 自动化验收链路与当前产出目录脱节。
  - 容易造成“数据已更新，但验证脚本未覆盖”的假阳性/假阴性。

#### C4. 文档 `00010` 存在 LaTeX 定界符失衡

官方审计脚本唯一失败项来自 `00010`。

- 问题类型：单美元符号 `$` 未成对
- 影响：
  - 训练样本中的公式 token 边界被破坏
  - 公式抽取与渲染可能失败

从样本可见，该文档出现如下碎裂：

- `projected to reach $\\$ 14$billion`
- `resulted in$\\$2.9-56.7$ billion`

说明该问题更像上游文本/结构化阶段的边界切分缺陷，而不是审计脚本误报。

## 性能耗时审计

### 实测耗时

来自 `logs/run_all_2026-03-17.log` 的最近一次全量批处理结果：

- `full_text`：`19/19 ok`，总耗时 `0.34s`，吞吐 `55.1 docs/s`
- `multimodal`：`19/19 ok`，`113 images`，总耗时 `0.31s`，吞吐 `61.1 docs/s`

补充历史日志：

- `logs/run_text_standardization_2026-03-16.log`：4 文档 `0.07s`
- `logs/run_text_standardization_2026-03-03.log`：3 文档 `0.03s` 与 `0.08s`
- `logs/run_multimodal_extraction_2026-03-03.log`：3 文档、23 图 `0.14s`

### 性能结论

在当前 19 文档、113 图的小规模数据集上，`Designer` 包性能表现良好，暂无明显耗时瓶颈；CPU 与 IO 都处于可接受水平。

### 潜在扩展瓶颈

尽管当前速度快，但从实现上看，存在中大规模数据下的放大风险：

1. `MultimodalInterleaver` 存在重复扫描 `content_list` 的模式

- 每张图片都会再次执行 caption 查找、mention 查找、语义锚点提取。
- 这会形成近似 `O(图像数 × 文本块数)` 的重复遍历。
- 当前数据量小所以不明显，但在长文档、多图论文上会放大。

1. 多模态导出为串行文件 IO

- 每张图执行一次复制、一次 Markdown 写入。
- `shutil.copy2()` 与逐图 `open(...).write(...)` 在大批量资产时会转为 IO 主导。

1. `TextAggregator` 末端使用多轮正则替换

- `_apply_entity_shielding()` 对全文执行多次 `re.sub()`。
- 在当前平均 2.7 万字符文档下代价很低，但超长文档时会成为主要 CPU 成本之一。

### 性能风险评级

- 当前批次：`低`
- 扩展到百篇以上、多图长文档：`中`

## 综合判断

### 已满足项

- full_text 与 multimodal 目录产物完整。
- 根标签、EOS、JSONL 必选字段、multimodal 资产拷贝在本批次整体通过。
- 当前小样本批处理速度优秀。

### 未完全满足项

- `pure_text_stream` 尚不是真正纯文本。
- `structured` 章节层未落地。
- 化学式字段存在误报。
- 部分文档章节装箱重复或错位。
- 旧验证脚本与现行输出目录不一致。

## 建议整改顺序

1. 优先修复 `DataMiningMapper._to_pure_text_stream()`，确保动态 `poros_*` 标签全部剥离。
2. 为 `DataMiningMapper._to_structured_json()` 补齐 `sections` 填充逻辑，保留 section/title/subtitle 层级。
3. 收紧化学式抽取规则，区分材料式、单位、物理量符号、菌落计数、生物编号。
4. 在 `TextAggregator` 侧补充章节去重/纠偏逻辑，避免重复 `abstract/references/conclusion`。
5. 修正 `scripts/validate_structured_output.py` 和 `scripts/validate_multimodal_output.py` 的默认输出目录。
6. 若后续数据规模扩大，优先优化 `MultimodalInterleaver` 的重复扫描问题，可考虑先构建注册表后复用索引，减少按图全量遍历。

## 最终评级

- 数据质量：`中`
- 性能耗时：`优`
- 审计工具有效性：`中`
- 交付结论：`建议修复 P1 后作为正式 AI/Data Mining Ready 交付`

## 对应整改清单

- 本报告对应的可执行工作项已整理为：`audit/designer_remediation_workitems_2026-03-17_000000.md`
- 建议优先执行：
  1. 视图契约统一：明确 `content`、`pure_text_stream`、`structured` 的职责
  2. `pure_text_stream` 去标签纯净化
  3. `structured.sections` 落盘
  4. 章节重复/错位与 LaTeX 失衡回归修复
