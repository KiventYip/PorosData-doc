---
status: exploratory
author: KiventYip
date: 2024-03-09
hide:
  - toc
---

!!! abstract "Research Note / 研发手记"
    本篇文档属于 **PorosData 研究与思考** 系列，主要记录架构演进的心路历程、尚未正式落地的算法推演或对特定 Data-centric AI 难题的探索。它不代表框架最终的稳定功能承诺。

# Design Insights.Zh

This page is under development.

## Overview

Content coming soon...

## Quick Links

- [Home](../index.md)
- [Quick Start](../get_started/quickstart.md)

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