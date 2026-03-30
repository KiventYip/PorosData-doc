# PorosData 工作流：从原始论文到最终交付结果

本页说明 PorosData 如何把原始科研文献整理为可用于训练、结构化抽取、检索和人工复核的标准化结果。重点不是单个函数调用，而是用户如何理解整条交付链路。
{: .lead}

## 整体流程

```text
原始文献 -> Parser -> Processor -> Designer -> 最终交付目录
```
{: .section-intro}

| 阶段 | 主要任务 | 交付结果 |
|------|------|------|
| `Parser` | 提取正文、图表、图注和基础元数据 | 可继续处理的原始内容与图片资源 |
| `Processor` | 清理噪音、修复断裂、统一表达 | 高质量中间结果与处理报告 |
| `Designer` | 组织章节、生成结构化视图与索引 | 全文结果、结构化 JSON、多模态结果 |

## 输入与输出目录

PorosData 推荐按三层目录组织数据：
{: .section-intro}

```text
data/
├── raw/          # 上游原始结果
├── processed/    # 清洗后的中间结果
└── structured/   # 最终交付目录
```

数据流向为 `raw -> processed -> structured`。

## 阶段 1：原始输入进入 `raw`

`raw` 层保存上游解析结果和原始图片资源，典型内容包括：
{: .section-intro}

- 原始 PDF
- 解析得到的 Markdown 或内容列表
- 页面级中间文件
- 从文献中切出的图片资源
{: .tight-list}

这一层的目标不是直接交付，而是完整保留上游输入，方便追溯和复查。

## 阶段 2：`Processor` 生成 `processed`

`Processor` 负责把原始内容整理成稳定、清晰、可继续消费的中间结果。这里通常会处理以下问题：
{: .section-intro}

- 数字、小数点和单位被异常空格打断
- 术语、材料名和化学式出现断裂或误写
- 图注、表题和脚注中存在明显噪音
- 长文本中混入控制字符、格式残影和无意义碎片
{: .tight-list}

这一阶段的标准交付通常包括：

- 清洗后的 `*_content_list.json`
- 图片资源的可复用拷贝
- `processing_report.json` 形式的处理报告
{: .tight-list}

## 阶段 3：`Designer` 生成 `structured`

`Designer` 在高质量输入基础上组织最终交付结果。常见输出包括：
{: .section-intro}

```text
data/structured/
├── full_text/
├── datamining/
└── multimodal/
```

其中三类结果分别面向不同用途：

| 目录 | 作用 | 常见文件 |
|------|------|------|
| `full_text/` | 交付可阅读、可复核的全文结果 | `_structured.json`, `_structured.txt` |
| `datamining/` | 交付适合抽取、检索和入库的结构化结果 | `_datamining.json` |
| `multimodal/` | 交付图文关联清晰的索引与图片资产 | `_index.json`, `fig_*.md`, `assets/` |

## 用户最终会得到什么

完成一轮标准处理后，用户通常会获得以下结果：
{: .section-intro}

1. 一套按文档编号组织的交付目录
2. 一份适合训练使用的纯文本结果
3. 一份适合抽取和检索的结构化结果
4. 一套可用于图文联动的多模态索引
5. 一份可用于批处理复盘的处理报告
{: .tight-list}

## 典型使用顺序

对于批量项目，推荐按以下顺序理解和使用结果：
{: .section-intro}

1. 先查看 `raw/` 是否完整，确认原始输入没有缺失
2. 再检查 `processed/` 的处理报告，确认清洗阶段是否稳定完成
3. 最后进入 `structured/`，按具体用途读取全文、结构化结果或多模态索引
{: .tight-list}

## 适合的使用场景

- 为训练准备高质量文本
- 为结构化抽取准备稳定输入
- 为图表与正文联动准备可索引资产
- 为后续数据库建设或知识组织提供统一交付目录
{: .tight-list}

## 相关页面

- [安装指南](installation.md)
- [快速开始](quickstart.md)
- [使用示例](../references/examples.md)
- [Processor](../tools/processor/index.md)
- [Designer](../tools/designer/index.md)
{: .tight-list}
