# Designer 审计整改工作项

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


## 说明
本文将 `audit/designer_quality_performance_audit_2026-03-17_000000.md` 中的审计发现转化为可执行工作项。

执行原则：
- 先修正视图契约，再修正抽取质量，再修正验证链路。
- 不把“标签存在”本身视为缺陷；缺陷在于字段职责不清、标签语义错位、抽取精度不足。
- 所有工作项都应同时给出回归样本与验收标准。

## P0 视图契约

### W1. 明确 `content` / `pure_text_stream` / `structured` 的实现契约
- 目标：让实现与 `docs/ai_ready_and_datamining_designer.md` 的新定义一致。
- 涉及文件：
  - `src/porosdata_designer/data_mining_mapper.py`
  - `scripts/audit_structured_data.py`
- 具体动作：
  - 明确 `content` 为结构感知训练视图。
  - 明确 `pure_text_stream` 为纯文本训练视图。
  - 明确 `structured` 为数据挖掘视图。
- 验收标准：
  - 审计脚本能分别检查三类视图职责。
  - 不再把 `content` 含标签视为默认失败项。

### W2. 修复 `pure_text_stream` 残留动态标签
- 目标：`pure_text_stream` 真正成为纯文本流。
- 涉及文件：
  - `src/porosdata_designer/data_mining_mapper.py`
- 具体动作：
  - 剥离 `poros_section_*`、`poros_title_*`、`poros_subtitle_*` 等动态标签。
  - 明确公式、化学式、资产引用在纯文本视图中的保留策略。
- 验收标准：
  - `pure_text_stream` 中不再出现 `poros_*` 标签。
  - 全量 JSONL 抽查 `pure_text_stream` 时不含 XML 包装。

## P1 结构化质量

### W3. 为 `structured` 补齐 section 层信息
- 目标：让 `structured` 真正保留章节边界。
- 涉及文件：
  - `src/porosdata_designer/data_mining_mapper.py`
- 具体动作：
  - 为 `structured.sections` 填充 `section_type`、`title`、`paragraphs`、可选 `subtitles`。
  - 保证其与 `content` 中的 section 边界一致。
- 验收标准：
  - `structured.sections` 不再全量为空。
  - 任一文档都能从 `structured` 恢复章节顺序。

### W4. 修复章节重复与错位
- 目标：避免 `abstract`、`references`、`conclusion` 重复或正文归属错误。
- 涉及文件：
  - `src/porosdata_designer/reorganizers/text_aggregator.py`
- 具体动作：
  - 增加 section 去重与纠偏逻辑。
  - 对 `references`、`conclusion`、`abstract` 建立更稳定的开闭规则。
- 回归样本：
  - `00006`
  - `00010`
  - `00012`
  - `00014`
  - `00019`
  - `00020`
  - `00021`
- 验收标准：
  - 重复 `abstract/references/conclusion` 的样本回归通过。
  - section 闭合合法且语义归属正确。

### W5. 修复 LaTeX 定界符失衡
- 目标：消除已知公式边界破坏。
- 涉及文件：
  - `src/porosdata_designer/reorganizers/text_aggregator.py`
  - `src/porosdata_designer/latex_validator.py`
- 回归样本：
  - `00010`
- 具体动作：
  - 修复单美元符号切分错误。
  - 识别货币符号、区间数字、跨片段拼接导致的错误公式拆分。
- 验收标准：
  - `00010` 的 LaTeX 校验通过。
  - 不能因修复货币符号而破坏正常公式抽取。

### W6. 收回 `Designer` 中越界的 `\Delta` 文本修复
- 目标：把 `\Delta...` 的处理从“正文改写”收回到“解析期防御”，避免 `Designer` 对上游脏文本做破坏性修复。
- 问题归因：
  - `\DeltaNi-Nb-Y`、`\mathrm{\Delta ...}` 一类输入的根因在 `Processor` / 上游 OCR 清洗。
  - 当前 `Designer` 在 `text_aggregator.py` 中直接剥离 leading `\Delta`，已经越过“结构化组织”职责边界，并会制造 `Ni - Nb {- Y}}` 之类新脏数据。
- 涉及文件：
  - `src/porosdata_designer/reorganizers/text_aggregator.py`
  - `src/porosdata_designer/chemical_formula_parser.py`
  - `docs/ai_ready_and_datamining_designer.md`
- 具体动作：
  - 移除 `text_aggregator.py` 中对正文/标签输出直接执行的 leading `\Delta` 剥离逻辑。
  - 保留 `chemical_formula_parser.py` 中仅服务结构化解析的防御性归一化，且明确其不改写 `content` 原文。
  - 为 `Designer` 明确规则：遇到疑似 `\Delta` 脏输入时，允许“不误抽取”为化学式，但不允许“改写正文 token”。
  - 在规范或开发说明中补充职责边界：`Processor` 负责修复坏公式，`Designer` 仅做非破坏性容错。
- 回归样本：
  - `00001`
- 验收标准：
  - `content` 中不再因 `Designer` 的 `\Delta` 处理引入新增花括号失衡或残留 `}`。
  - `structured.chemical_formulas` 不再因 `\Delta` 前缀误识而污染。
  - `Designer` 的全文输出逻辑中不再存在“为纠正 `\Delta` 而直接改写正文”的实现。

### W7. 为不安全公式输入建立“保守降级”策略
- 目标：当上游已交付残缺 LaTeX 或坏公式时，`Designer` 不继续放大错误，而是保守输出或显式隔离。
- 问题归因：
  - 当前 `processed` 已存在不完整公式，如 `\begin{array} ... \end{array}` 内容残缺。
  - `Designer` 现状是继续包成 `<poros_equ>` 输出，缺少“不安全输入”识别与降级策略。
- 涉及文件：
  - `src/porosdata_designer/reorganizers/text_aggregator.py`
  - `src/porosdata_designer/latex_validator.py`
  - `scripts/audit_structured_data.py`
- 具体动作：
  - 为行内公式分类增加“结构安全”判断，识别残缺环境、异常括号、明显不闭合片段。
  - 对不安全公式采用保守策略：保留原文、降级为普通文本，或标记为低置信度公式；禁止激进修复。
  - 在审计脚本中增加“不安全公式被继续结构化输出”的专项检查。
  - 建立坏样本回归集，覆盖残缺 `array`、残缺括号、错误闭合等情况。
- 回归样本：
  - `00001`
  - `00010`
- 验收标准：
  - 残缺公式不会在 `Designer` 阶段被进一步改坏。
  - 审计报告能区分“上游坏输入”与“Designer 新引入损坏”。
  - 对坏公式的处理策略在全量样本中保持一致。

### W8. 收紧 `chemical_formulas` 抽取精度
- 目标：减少单位、参数符号、生物编号、计数项误入化学式列表。
- 涉及文件：
  - `src/porosdata_designer/reorganizers/text_aggregator.py`
  - `src/porosdata_designer/config.py`
  - `scripts/audit_structured_data.py`
- 具体动作：
  - 区分材料式、实验参数、单位、生物编号、物理量符号。
  - 扩展白名单/黑名单与上下文过滤规则。
- 回归样本：
  - `00001`
  - `00002`
  - `00003`
  - `00010`
  - `00012`
- 验收标准：
  - `CFU/mL`、`ATCC13311`、`S_m`、`H_c` 等不再误入高精度化学式字段。
  - 合法材料式不被误杀。

## P2 工具链与审计

### W9. 为跨包责任边界建立联动整改项
- 目标：把“根因修复”明确落到 `Processor`，避免问题长期滞留在 `Designer` 侧打补丁。
- 涉及文件：
  - `docs/ai_ready_and_datamining_designer.md`
  - `docs/audit/designer_remediation_workitems_2026-03-17_000000.md`
  - `data/processed` 生成链路对应仓库/脚本（需跨包协作）
- 具体动作：
  - 将本轮识别出的 `\Delta` 误识、残缺 LaTeX、异常花括号问题整理为上游输入质量缺陷清单。
  - 为 `Processor` 建立对应修复项：公式结构修复、材料式断裂修复、坏 token 隔离。
  - 在 `Designer` 整改清单中明确哪些项属于“本包止血”，哪些项需要上游彻底修复。
- 回归样本：
  - `00001`
- 验收标准：
  - 每类问题都能追溯到明确责任方：`Processor` 根因修复 / `Designer` 防御修复。
  - 不再把跨包问题长期固化为 `Designer` 内部规则堆积。

### W10. 修正验证脚本输出目录漂移
- 目标：让验证脚本默认检查当前真实产物目录。
- 涉及文件：
  - `scripts/validate_structured_output.py`
  - `scripts/validate_multimodal_output.py`
  - `scripts/final_acceptance_validation.py`
- 具体动作：
  - 将默认目录从 `data/output/...` 对齐到 `data/structured/...`，或改为参数化目录输入。
- 验收标准：
  - 不带参数运行时能直接检查当前交付目录。
  - 旧目录模式若仍需支持，应通过参数显式指定。

### W11. 重构审计口径
- 目标：把“标签设计合理性”和“字段契约失败”分开审。
- 涉及文件：
  - `scripts/audit_structured_data.py`
  - `audit/designer_quality_performance_audit_2026-03-17_000000.md`
- 具体动作：
  - 增加 `content` 的结构感知训练验收。
  - 增加 `pure_text_stream` 的纯净性验收。
  - 增加 `structured.sections` 的落盘完整性验收。
- 验收标准：
  - 审计报告可区分“设计合理项”“字段契约问题”“真实质量缺陷”。

## P3 性能与扩展性

### W12. 优化多模态重复扫描
- 目标：降低多图长文档下的重复遍历成本。
- 涉及文件：
  - `src/porosdata_designer/reorganizers/multimodal_interleaver.py`
- 具体动作：
  - 复用注册表或索引结果，减少按图重复扫描 `content_list`。
  - 评估 caption、mention、anchor 的共享扫描策略。
- 验收标准：
  - 在同等输入下结果不变。
  - 中大样本下总耗时下降，或至少不随图片数线性放大过快。

### W13. 为长文本训练建立标签密度审计
- 目标：确保结构标签提供语义收益，而不是造成无意义 token 膨胀。
- 涉及文件：
  - `scripts/audit_structured_data.py`
  - 可选新增 `scripts/` 下专项统计脚本
- 具体动作：
  - 统计 `content` 中标签 token 占比。
  - 统计 section 数、标题数、标签/正文长度比。
- 验收标准：
  - 审计报告可回答“标签是否过密”“结构收益是否值得 token 成本”。

## 建议执行顺序
1. W1-W2：先修视图契约，避免实现和规范继续错位。
2. W3-W8：再修结构化主质量问题，优先处理 `\Delta` 越界修复和不安全公式降级策略。
3. W9-W11：同步修复跨包责任划分、审计与验证链路。
4. W12-W13：最后处理性能与规模化问题。

## 交付完成标志
- 规范、实现、审计三者对 `content`、`pure_text_stream`、`structured` 的定义一致。
- `pure_text_stream` 真正纯净。
- `structured.sections` 可用。
- 主要坏样本回归通过。
- `\Delta` 类问题不再由 `Designer` 通过正文改写“修复”。
- 残缺 LaTeX 在 `Designer` 中不再被继续放大。
- 验证脚本可直接对当前 `structured` 运行。