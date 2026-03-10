---
hide:
  - toc
---

# PorosData

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PyPI version](https://img.shields.io/pypi/v/PorosData-Processor.svg)](https://pypi.org/project/porosdata-processor/)

## 简介

在 Data-centric AI 的范式下，模型能力的上限往往由数据质量决定。然而，材料科学等领域的科研文献——PDF、LaTeX、OCR 产物——并非天然的模型食粮：控制字符、页码残影、断词错误、术语误识、拆散的数值表达式、断裂的图文引用……这些「脏数据」一旦进入训练流水线，轻则污染 token 分布，重则导致知识中毒，使模型习得错误的科学概念。

**PorosData** 面向这一痛点而生：它是专为实证科学设计的 AI4S 数据编排框架，将非结构化或半结构化的科研文献转化为语义可靠、结构一致、可追溯的 AI-Ready 数据集，覆盖从解析、精炼到合成的全生命周期。

## 核心价值

PorosData 秉持 **学术原子性**：将每一份科研数据视为不可分割的学术价值单元。

| 维度 | 承诺 |
|------|------|
| **语义保真** | 数学公式、引用链条在处理中保持完整，不做破坏性简化 |
| **可追溯性** | 每个清洗决策均可回溯到学术依据，支持审计与复现 |
| **场景适配** | 预训练关注 token 纯净与语义常识，数据挖掘关注实体精度与图文锚定 |

无论目标是大模型预训练还是知识图谱构建，PorosData 都围绕同一原则运作：**在提升可用性的同时，不牺牲科学严谨性**。

## 快速开始

- [安装指南](get_started/installation.md)
- [快速开始](get_started/quickstart.md)
- [使用示例](references/examples.md)

!!! tip "端到端示例"
    从 PDF 论文到 AI 训练数据集的完整转换流程，见 [端到端工作流](get_started/end-to-end-workflow.md)。

## 关键特性

### 面向预训练：Token 纯净与语义常识

预训练阶段模型学习的是世界知识与语言结构。若数据中混入控制字符、页码索引或断词错误（如 `short-range` → `shortrange`），将干扰上下文概率学习，甚至引入错误关联。

PorosData 通过 **智能文本清洗** 与 **科学术语一致性校验**，保证 token 流的纯净性与术语的语义准确性，降低知识中毒风险。

### 面向数据挖掘：实体精度与多模态锚定

数据挖掘需从文献中自动抽取合金成分、转变温度等结构化知识。此时数据质量的关键转为：数值与单位的确定性、化学元素等实体的稳健识别、文中「Fig. 1」与图片资产的硬链接。

PorosData 提供 **数值与单位修复**、**实体识别稳健化** 和 **图文资产锚定**，使后续的 NER、实体链接与知识图谱构建建立在可靠基础上。

### 五大能力一览

| 能力 | 解决的问题 |
|------|------------|
| 智能文本清洗 | 控制字符、索引噪声、断词与 token 断裂 |
| 科学术语校验 | OCR/解析导致的术语误写（如 X-ray → 10-ray） |
| 数值与单位修复 | 科学计数法、指数表达式的解析错误 |
| 实体识别稳健化 | 化学元素、合金名被误识为 LaTeX 符号 |
| 图文资产锚定 | 图表引用与图像、Caption 的跨模态索引 |

## 架构概览

PorosData 采用三位一体的模块化架构，覆盖科研数据处理的完整链路：

```
[文献] → Parser（提取） → Processor（精炼） → Designer（合成） → [AI-Ready 数据集]
```

| 模块 | 职责 |
|------|------|
| **PorosData-Parser** | 从 PDF、LaTeX 等非结构化文献中提取结构化科学数据 |
| **PorosData-Processor** | 在学术原子性约束下执行标准化、去噪与预处理 |
| **PorosData-Designer** | 将精炼后的数据重组为指令对、实验方案等训练就绪格式 |

各模块可独立使用，也可串联为端到端流水线；扩展与插件遵循同一原子性契约，保证生态内数据质量的一致性。

## 深度参考

- [设计哲学](concepts/design-philosophy.md)
- [研究综述](research/research-review.md)
- [设计洞察](research/design-insights.md)
- [术语表](concepts/glossary.md)
- [API 参考](references/api-reference.md)

## 社区与贡献

- [贡献指南](community/contributing.md)
- [路线图](community/roadmap.md)
- [更新日志](community/changelog.md)
