# PorosData-Designer

## 定位

`Designer` 是 PorosData 中负责结构化交付的模块。它建立在 `Processor` 已完成质量整理的基础上，把文本、图表和上下文组织为适合训练、抽取、检索和复核使用的最终结果。

简而言之：

- `Processor` 负责把内容整理干净
- `Designer` 负责把内容组织成可交付结果
{: .tight-list}

## 主要职责

`Designer` 重点处理以下工作：
{: .section-intro}

- 章节与段落重组
- 结构化字段组织
- 图文资产关联
- 全文结果与结构化结果导出
- 多模态索引生成
{: .tight-list}

它不承担大规模 OCR 清洗，而是把已经稳定的中间结果进一步变成可交付产品。

## 三类核心产物

当前 `Designer` 主要输出三类结果：
{: .section-intro}

| 产物 | 面向用途 | 常见文件 |
|------|------|------|
| 全文结果 | 阅读、复核、训练准备 | `_structured.txt`, `_structured.json` |
| 结构化结果 | 抽取、检索、入库 | `_datamining.json` |
| 多模态结果 | 图文联动、图片索引、资产管理 | `_index.json`, `fig_*.md`, `assets/` |

## 输出目录

典型输出目录如下：
{: .section-intro}

```text
data/structured/
├── full_text/{doc_id}/
├── datamining/{doc_id}/
└── multimodal/{doc_id}/
```

每个文档按 `doc_id` 独立存放，便于批处理交付、抽查和回溯。

## 用户能获得什么

在标准交付中，`Designer` 会把同一篇文献整理为多种可复用结果：
{: .section-intro}

- 一份可直接阅读的全文结果
- 一份适合训练使用的纯文本流
- 一份适合结构化抽取和检索的 JSON 结果
- 一套图文引用关系清晰的多模态索引
{: .tight-list}

## 关键结果说明

### `full_text`

`full_text` 面向全文交付，通常包含：
{: .section-intro}

- 带结构标记的完整文本
- 去除结构标记后的纯文本流
- 便于人工审阅的文本版本
{: .tight-list}

### `datamining`

`datamining` 面向结构化利用，通常包含：
{: .section-intro}

- 标题
- 章节内容
- 公式列表
- 化学式或材料式
- 图表引用信息
{: .tight-list}

### `multimodal`

`multimodal` 面向图文联动，通常包含：
{: .section-intro}

- 图片索引文件
- 按图拆分的说明卡片
- 与正文引用对应的图片资产
{: .tight-list}

## 输入要求

为了得到稳定结果，`Designer` 依赖以下前置条件：
{: .section-intro}

- 文本中的主要噪音已经在上一步处理完成
- 数值、单位、术语和材料名具备较好一致性
- 图注、表题、脚注等关键字段可直接使用
- 正文与图表的引用关系没有被上游破坏
{: .tight-list}

## 设计原则

`Designer` 的组织方式遵循以下原则：
{: .section-intro}

- 结构优先服务交付，而不是复刻排版
- 同一文档的章节层级应尽量稳定
- 图文资产要能回到原始上下文
- 一套结果应同时支持阅读、抽取和复查
{: .tight-list}

## 已知边界

使用 `Designer` 时需要注意：
{: .section-intro}

- 它依赖上游输入质量，无法替代前置清洗
- 对语义极不稳定的章节，不追求过细标签，而优先保证整体可用
- 最终字段设计仍应结合具体业务需求做二次映射
{: .tight-list}

## 与 `Processor` 的关系

`Designer` 不是单独工作的模块。它建立在 `Processor` 提供的稳定输入之上，负责把质量结果进一步转换成面向最终使用者的交付目录和结构化成果。
