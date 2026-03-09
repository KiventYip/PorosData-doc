PorosData Documentation
========================

.. image:: https://img.shields.io/badge/python-3.8+-blue.svg
   :alt: Python 3.8+
   :target: https://www.python.org/downloads/

.. image:: https://img.shields.io/badge/License-MIT-yellow.svg
   :alt: License: MIT
   :target: https://opensource.org/licenses/MIT

.. image:: https://img.shields.io/pypi/v/PorosData-Processor.svg
   :alt: PyPI version
   :target: https://pypi.org/project/porosdata-processor/

**PorosData: A Comprehensive End-to-End Framework for Scientific Data Orchestration**

PorosData is an **AI4S data orchestration framework** specifically engineered for the materials Science and related empirical fields. By providi**ng a full-lifecycle solution - form parsing and refinement to data synthesis - it serves as the bridge between raw scientific literature and AI models, safeguarding the semantic integrity, fidelity, and end-to-end provenance of scientific data

框架核心特性：  
- **数据完整性保证**: 保护数学公式、引用体系和科学语义的原子性  
- **模块化架构**: 三大核心工具包协同工作，覆盖科研数据处理全流程  
- **学术导向设计**: 优先考虑学术规范和科研工作流的需求  

**学术原子性宣言**

在 AI for Science 时代，数据不仅是信息载体，更是学术话语的基础。PorosData 秉持"学术原子性"原则：每份数据都承载不可分割的学术价值，我们致力于在数据精炼过程中保护数学公式、引用体系和科学语义的原子完整性。

原子性保证包括：
- **语义保真**: 数学表达式永不失真，引用链条永不断裂
- **可追溯性**: 每个清洗决策都有明确的学术依据
- **可扩展性**: 新组件和插件无缝集成原子性契约

我们相信，真正的 AI for Science 不仅是技术创新，更是学术传统的传承。

.. note::
   **🚀 完整工作流案例**: 想要了解从PDF论文到AI训练数据集的完整流程？请查看 :doc:`end-to-end-workflow`。

PorosData-Parser
----------------

🔍 数据提取引擎

从 PDF 论文、LaTeX 源码等非结构化文献中智能提取结构化科学数据。

.. toctree::
   :maxdepth: 1
   :caption: Parser Documentation
   :titlesonly:

   PorosData-Parser/introduction
   PorosData-Parser/tool-usage
   PorosData-Parser/research-insights

PorosData-Processor
-------------------

🧹 数据清洗流水线

基于学术原子性原则，进行数据标准化、质量控制和预处理。

.. toctree::
   :maxdepth: 1
   :caption: Processor Documentation
   :titlesonly:

   PorosData-Processor/introduction
   PorosData-Processor/tool-usage
   PorosData-Processor/research-insights

PorosData-Designer
------------------

🎯 数据合成设计器

将清洗后的数据重组为适合大模型训练的指令数据集和实验设计方案。

.. toctree::
   :maxdepth: 1
   :caption: Designer Documentation
   :titlesonly:

   PorosData-Designer/introduction
   PorosData-Designer/tool-usage
   PorosData-Designer/research-insights

快速上手
--------

.. toctree::
   :maxdepth: 1
   :caption: 快速上手
   :titlesonly:

   installation
   quickstart
   examples

深度参考
--------

.. toctree::
   :maxdepth: 1
   :caption: 深度参考
   :titlesonly:

   design-philosophy
   research-review
   design-insights
   glossary
   api-reference

项目生态
==================

.. toctree::
   :maxdepth: 1
   :caption: 项目生态
   :titlesonly:

   contributing
   roadmap
   changelog

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`