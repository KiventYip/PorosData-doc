---
hide:
  - toc
---

# PorosData

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PyPI version](https://img.shields.io/pypi/v/PorosData-Processor.svg)](https://pypi.org/project/porosdata-processor/)

## 简介

PorosData 是面向科研文献的数据处理与结构化交付框架，用于把 PDF、OCR 与解析结果整理成可复查、可复用、可进一步消费的数据资产。
{: .lead}

对于材料科学等实证研究场景，原始文献往往包含断裂数字、异常空格、术语误写、公式损坏和图文引用脱节等问题。这些问题会直接影响模型训练、结构化抽取、检索入库和人工复核。PorosData 的目标，就是把这些上游噪音收敛为稳定、清晰、可追溯的交付结果。

## 适用场景

PorosData 适合放在“原始论文进入可消费数据资产”之间的整理环节。
{: .section-intro}

- 将科研论文整理为可用于训练的数据文本
- 为结构化抽取、规则处理和语义检索准备稳定输入
- 将正文、图注、表题和图片资产组织成统一的交付目录
- 为后续数据库建设、知识组织和多模态利用提供标准化基础
{: .tight-list}

## 核心价值

PorosData 以 **学术原子性** 为原则，强调在提高可用性的同时保留科学表达的完整性。
{: .section-intro}

| 维度 | 价值说明 |
|------|------|
| **内容可靠** | 尽量保留公式、引用、单位和术语的原始语义 |
| **结构清晰** | 让正文、章节、图表和字段关系更容易被系统和人工共同理解 |
| **过程可追溯** | 从原始输入到最终产物的处理链路清晰可查 |
| **交付可复用** | 同一批结果可服务于训练、抽取、检索和入库等多种后续任务 |

## 快速开始

如果你希望先看整体流程，再决定从哪个模块开始，可以先浏览下面三份入口文档。
{: .section-intro}

- [安装指南](get_started/installation.md)
- [快速开始](get_started/quickstart.md)
- [使用示例](references/examples.md)
{: .tight-list}

!!! tip "端到端示例"
    从原始论文到最终交付目录的完整流程，见 [端到端工作流](get_started/end-to-end-workflow.md)。

## 产品框架

PorosData 采用三段式链路处理科研文献：
{: .section-intro}

![PorosData 功能架构图](assets/images/DESIGN.jpg)

下图展示了存储层、处理模块和面向交付的输出能力，如何被组织为一套完整的端到端系统。
{: .section-intro}

```text
[原始文献] -> Parser -> Processor -> Designer -> [训练文本 / 结构化结果 / 多模态索引]
```

| 模块 | 面向用户的作用 |
|------|------|
| **Parser** | 从 PDF 和解析产物中提取可继续处理的文本与图片资源 |
| **Processor** | 清理噪音、修复断裂、稳定术语与数值表达，形成高质量中间结果 |
| **Designer** | 将高质量文本重组为全文视图、结构化抽取视图和多模态索引 |

## 五类核心能力

| 能力 | 解决的问题 |
|------|------------|
| 智能文本清洗 | 控制字符、索引噪声、断词与 token 断裂 |
| 科学术语校验 | OCR/解析导致的术语误写（如 X-ray → 10-ray） |
| 数值与单位修复 | 科学计数法、指数表达式的解析错误 |
| 实体识别稳健化 | 化学元素、合金名被误识为 LaTeX 符号 |
| 图文资产锚定 | 图表引用与图像、Caption 的跨模态索引 |

## 最终交付内容

PorosData 的交付不止是一份清洗后的文本，而是一套面向后续使用的结果目录，通常包括：
{: .section-intro}

- 可直接阅读和复核的全文结果
- 适合训练使用的纯文本流
- 适合抽取与检索的结构化 JSON
- 图文对应关系清晰的多模态索引
- 可用于批处理复盘的处理报告与日志
{: .tight-list}

## 深度参考

如果你想理解这套框架为什么这样设计，可以继续阅读以下背景材料。
{: .section-intro}

- [设计哲学](concepts/design-philosophy.md)
- [研究综述](research/research-review.md)
- [设计洞察](research/design-insights.md)
- [术语表](concepts/glossary.md)
- [API 参考](references/api-reference.md)
{: .tight-list}

## 社区与贡献

以下页面更适合已经开始试用、准备参与迭代或希望跟踪项目演进的读者。
{: .section-intro}

- [贡献指南](community/contributing.md)
- [路线图](community/roadmap.md)
- [更新日志](community/changelog.md)
{: .tight-list}
