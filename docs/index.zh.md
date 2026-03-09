# PorosData

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PyPI version](https://img.shields.io/pypi/v/PorosData-Processor.svg)](https://pypi.org/project/porosdata-processor/)

PorosData 是专为材料科学等实证领域设计的 AI4S 数据编排框架。它提供从解析、精炼到数据合成的全生命周期解决方案，连接原始科研文献与 AI 模型，保障科学数据的语义完整性、忠实度和端到端溯源性。

## 核心特性

- **保障数据完整性**: 维持数学公式、引用体系和科学语义的原子级完整
- **协同模块化架构**: Parser、Processor 和 Designer 三大工具包覆盖科研数据处理全流程
- **遵循学术规范**: 设计逻辑优先满足科研工作流需求

## 学术原子性契约

PorosData 将每份数据视为不可分割的学术价值单元。在数据精炼过程中，我们承诺：

- **保持语义保真**: 确保数学表达式不失真，引用链条不断裂
- **提供可追溯性**: 记录每个清洗决策的学术依据
- **支持无缝扩展**: 允许新组件和插件继承原子性契约

## AI-Ready 数据标准

为了确保数据真正适用于大模型，PorosData 严格遵循以下 AI-Ready 数据处理要求：

### 1. Pre-training 的要求：Token 纯净度与语义常识

预训练的目标是让模型学习世界知识（如物理、化学规律）。如果数据本身包含错误，模型就会产生“知识中毒”。

- **Token 流的纯净性**：正文中不应包含与语义无关的控制字符或索引。该类与语义、语法结构无关的数据在训练时属于干扰噪音，会破坏模型对上下文概率的预测。
- **语义常识的准确性**：核心术语不能有系统性误识。如果将 X-ray 识别为 10-ray，模型会学习到错误的科学概念，导致它在后续任务中无法理解射线衍射的逻辑。
- **长文本的连贯性**：换行符处理不当导致的单词断裂（如 shortrange 缺失连字符变为 short - range）会增加模型词表的熵，降低其对长难句的理解能力。

### 2. Data Mining 的要求：实体精度与逻辑链接

数据挖掘的目标是从海量文档中自动化提取结构化知识（如：合金成分、转变温度）。

- **数值与单位的确定性**：科学挖掘对数字极其敏感。被 OCR 拆散的数字（如 $1 0 ^ { 5 }$）会导致挖掘算法无法识别出正确的数量级，直接废掉自动化的属性提取任务。
- **实体识别的稳健性**：化学元素（如 Ni, Au）不能被误识为 LaTeX 符号（如 $\Delta$, \Au），否则在构建知识图谱时，实体链接（Entity Linking）会由于名称错误而失败。
- **多模态资产的锚定**：挖掘工作往往需要“图文穿透”。AI-Ready 要求文中的“Fig. 1”不仅仅是几个字符，而是一个能够直接索引到图片资产和对应 Caption 的硬链接锚点。

!!! note "案例研究"
    查看 [端到端工作流](get_started/end-to-end-workflow.md) 了解从 PDF 论文到 AI 训练数据集的转换过程。

## PorosData-Parser

🔍 数据提取引擎

从 PDF 论文、LaTeX 源码等非结构化文献中智能提取结构化科学数据。

## PorosData-Processor

🧹 数据清洗流水线

基于学术原子性原则，进行数据标准化、质量控制和预处理。

## PorosData-Designer

🎯 数据合成设计器

将清洗后的数据重组为适合大模型训练的指令数据集和实验设计方案。

## 快速上手

- [安装指南](get_started/installation.md)
- [快速开始](get_started/quickstart.md)
- [使用示例](references/examples.md)

## 深度参考

- [设计哲学](concepts/design-philosophy.md)
- [研究综述](research/research-review.md)
- [设计洞察](research/design-insights.md)
- [术语表](concepts/glossary.md)
- [API 参考](references/api-reference.md)

## 项目生态

- [贡献指南](community/contributing.md)
- [路线图](community/roadmap.md)
- [更新日志](community/changelog.md)
