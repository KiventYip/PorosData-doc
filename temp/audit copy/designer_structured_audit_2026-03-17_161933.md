# Designer 结构化数据审计报告

> Historical reference notice
>
> - doc_type: audit
> - status: historical_reference
> - created_at: 2026-03-17 16:19:33
> - updated_at: 2026-03-18 09:39:32
> - current_repo_layout: `data/raw`, `data/processed`, `data/structured`, `tests/`
> - current_effective_docs: `docs/usage_guide.md`, `docs/deployment_guide.md`, `docs/ai_ready_and_datamining_designer.md`
> - compatibility_notice:
>   - historical paths like `data/mineru_output_raw_data`, `data/processed_data`, `data/structured_data` have been renamed.
>   - historical test path `src/porosdata_designer/tests/` has moved to `tests/`.
>   - historical script `scripts/audit_structured.py` should be read as `scripts/audit_structured_data.py`.
>   - current structured output contract centers on `*_structured.json`; `*_structured.txt` remains as the readable companion export.


## 基本信息

- 审计对象：`data/structured`
- 对照规范：`docs/ai_ready_and_datamining_designer.md`
- 审计范围：`full_text`、`multimodal`、JSONL 三层视图、处理耗时
- 审计时间：`2026-03-17 16:19:33`
- 审计方式：
  - 运行 `scripts/audit_structured_data.py`
  - 实测 `examples/run_all.py --input_dir data/processed`
  - 结合当前实现检查潜在性能放大点

## 审计结论

当前 `structured` 已基本满足规范中的 `Structure-Aware Training Ready`、`Plain-Text Training Ready` 与 `Data Mining Ready` 要求，整体可作为现阶段正式交付数据使用。

- 当前总检查项：`228`
- 通过：`225`
- 失败：`3`
- 警告：`0`
- 综合结论：`有条件通过`

“有条件通过”的原因不是结构损坏，而是 3 份文档的 `content` 标签密度略高于当前 25% 阈值，属于训练 token 成本提醒，不影响 `pure_text_stream` 与 `structured` 的正常消费。

## 与规范对照结果

### 1. `content` 结构感知训练视图

已满足：

- `19/19` 文档包含 `<poros_doc>` 根标签。
- `19/19` 文档标签闭合和嵌套合法。
- `19/19` 文档以 `</s>` 结尾。
- `19/19` 文档的 `content` 具备稳定 section 边界。
- `19/19` 文档 LaTeX 定界符平衡。

剩余问题：

- `00003`：标签密度 `25.44%`
- `00019`：标签密度 `25.58%`
- `00020`：标签密度 `26.06%`

判断：

- 以上问题属于“结构标签略密”，不是标签损坏。
- 若下游以 `content` 做结构感知训练，建议持续监控标签收益与 token 成本。

### 2. `pure_text_stream` 纯文本训练视图

已满足：

- `19/19` 文档通过纯净性检查。
- 未发现 `poros_*` 标签残留。
- 可直接服务 Embedding、纯文本继续预训练与检索。

判断：

- 当前 `pure_text_stream` 已符合规范中“去标签纯文本流”的定义。

### 3. `structured` 数据挖掘视图

已满足：

- `19/19` 文档都具备 `structured.sections`。
- `sections`、`paragraphs`、`formulas`、`chemical_formulas`、`asset_refs` 已可稳定落盘。
- `chemical_formulas` 未发现已知非化学缩写噪声。

仍可优化：

- 部分文档仍存在泛化 section，如空标题 `section`、重复 `header`、`Article info` 等宽泛章节。
- 这些问题不阻断交付，但会影响后续章节级检索、规则抽取和知识对齐精度。

### 4. multimodal 视图

已满足：

- `19/19` 文档索引结构合法。
- 图片资产与 Markdown 文件保持一致。
- 当前批次总图片数：`113`

判断：

- 在当前数据规模下，多模态结果正确性良好。

## 数据画像

- 文档总数：`19`
- 图片总数：`113`
- 平均 `content` 长度：`29656.5`
- 平均 `pure_text_stream` 长度：`24117.6`
- 平均 section 数：`9.6`
- 平均 formula 数：`54.2`
- 平均 chemical formula 数：`58.7`
- 平均 asset reference 数：`8.1`
- 最大 `content` 长度：`68157`
- 最小 `content` 长度：`9284`

## 处理耗时评估

本次实测命令：

```bash
python examples/run_all.py --input_dir data/processed
```

实测结果：

- `full_text`：`19/19 ok`，总耗时 `0.28s`，吞吐约 `68.5 docs/s`
- `multimodal`：`19/19 ok`，`113 images`，总耗时 `0.43s`，吞吐约 `43.9 docs/s`

性能结论：

- 在当前规模下，整体处理耗时表现优秀。
- 当前不存在必须立即处理的性能瓶颈。

## 是否需要为大批量场景提前优化

结论：`需要考虑，但不必立刻为了当前 19 篇数据重构全部链路。`

原因：

- 当前小规模数据的运行速度已经足够快。
- 但现有实现里已经存在在“大批量文档 + 多图长文档”场景下会明显放大的模式。

## 主要性能风险点

### 1. 多模态重复扫描 `content_list`

当前 `multimodal` 主流程仍按“每张图单独扫描全文”工作：

```109:129:src/porosdata_designer/reorganizers/multimodal_interleaver.py
# 1. 提取所有图片
images = self._extract_images(content_list)

# 2. 为每个图片建立完整的关联信息
multimodal_items = []
for image in images:
    item = self._build_multimodal_item(image, content_list)
    if item:
        multimodal_items.append(item)
```

而单图处理中又分别做 caption、mentions、semantic anchor 扫描：

```219:230:src/porosdata_designer/reorganizers/multimodal_interleaver.py
caption = self._find_precise_caption(fig_id, content_list)
mentions = self._find_precise_mentions(fig_id, content_list)
semantic_anchors = self._extract_semantic_anchors(fig_id, registry_info['first_seen_page'], content_list)
```

风险：

- 当前复杂度近似 `O(图像数 × 文本块数)`。
- 在百篇以上、每篇十几到几十图时，multimodal 侧会先于 full_text 成为主瓶颈。

### 2. 多模态导出为串行 IO

图片复制和 Markdown 写入逐图串行执行：

```732:783:src/porosdata_designer/reorganizers/multimodal_interleaver.py
for item in items:
    ...
    asset_copied = self.safe_copy_image(source_image_path, asset_dest_path)
    ...
    with open(markdown_path, 'w', encoding='utf-8') as f:
        f.write(markdown_content)
```

风险：

- 当前 `113` 张图时问题不大。
- 若扩展到数千张图，文件复制和写盘会变为明显 IO 成本。

### 3. 文本聚合末端存在多轮全文正则扫描

`TextAggregator` 在实体屏蔽阶段对全文执行多轮 `re.sub`：

```355:391:src/porosdata_designer/reorganizers/text_aggregator.py
result = re.sub(r'\\{1,2}\$\s*[\d,.][\d,.\-–~]*(?:\s*(?:billion|million|trillion|thousand))?', _protect_currency, result)
result = re.sub(r'\$\$([^\$]*?)\$\$', extract_double_dollar, result, flags=re.DOTALL)
result = re.sub(r'\$([^$\n]+?)\$', extract_single_dollar, result)
result = re.sub(chem_pattern, replace_chemical, result)
```

风险：

- 当前平均 3 万字符量级下代价可接受。
- 在更长全文、更多公式、更多化学式的批量语料上，会形成 CPU 热点。

## 大批量场景下的优化建议

### P0. 建议优先做

1. 将 `multimodal_interleaver` 主流程切换到“注册表 + 二阶段提取”模式。
2. 复用一次扫描得到的 figure registry，不再对每张图重复遍历全文。
3. 将 caption、mentions、anchors 抽取合并到共享索引上。

理由：

- 这是最可能在大规模数据下放大的性能点。
- 改动收益最大，且不需要改变最终输出契约。

### P1. 规模继续扩大后再做

1. 为图片复制和 Markdown 写入增加轻量并发。
2. 对超长文档增加阶段性 profiling，识别 `TextAggregator` 的正则热点。
3. 把标签密度统计独立成批量指标，跟踪不同语料批次的 token 成本。

### P2. 质量与性能联合优化

1. 继续收紧 `structured.sections` 的语义化程度，减少空标题 `section` 和宽泛 `header`。
2. 将章节语义精度提升和性能 profiling 一起做，避免只追求速度而牺牲可挖掘性。

## 最终判断

### 当前交付判断

- 当前 `data/structured` 数据质量已达到可交付水平。
- 当前处理耗时已达到优秀水平。

### 面向大批量需求的判断

- 如果你接下来只是继续处理几十篇同量级文档，可以先不做性能重构。
- 如果你的目标是持续处理“大批量文档、长文本、图像密集型论文”，建议现在就开始做 `multimodal` 侧的结构性优化。

### 建议优先级

1. 先保留当前交付逻辑不变，确保质量口径稳定。
2. 优先优化 `multimodal_interleaver` 的重复扫描。
3. 再根据真实批量规模决定是否继续做 IO 并发和全文正则优化。