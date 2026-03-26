# PorosData

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PyPI version](https://img.shields.io/pypi/v/PorosData-Processor.svg)](https://pypi.org/project/porosdata-processor/)

## Introduction

In the data-centric AI paradigm, the upper bound of model capability is often determined by data quality. Scientific literature in materials science and related fields, especially PDFs, LaTeX sources, and OCR outputs, is not naturally ready for model pipelines. Control characters, page-shadow artifacts, broken words, term corruption, fragmented numerical expressions, and broken figure references can all become structural problems during training or data mining.

**PorosData** addresses this gap. It is an AI4S data orchestration framework designed for empirical science, turning unstructured or semi-structured scientific literature into semantically reliable, structurally consistent, and traceable AI-Ready and Data Mining Ready assets, across the full lifecycle from parsing to quality delivery and structured expression.

## Core Value

PorosData is built on **Academic Atomicity**, which treats each piece of scientific data as an indivisible unit of scholarly value.

| Dimension | Commitment |
|------|------|
| **Semantic Fidelity** | Mathematical expressions and citation chains stay intact during processing |
| **Traceability** | Each cleaning decision can be audited and traced back to academic rationale |
| **Task Awareness** | Pre-training emphasizes token purity and semantic commonsense, while data mining emphasizes entity precision and multimodal anchoring |

No matter whether the target is large-scale pre-training or scientific knowledge extraction, the framework follows the same rule: **improve usability without sacrificing scientific rigor**.

## Quick Start

- [Installation Guide](get_started/installation.md)
- [Quick Start](get_started/quickstart.md)
- [Usage Examples](references/examples.md)

!!! tip "End-to-End Example"
    See the [End-to-End Workflow](get_started/end-to-end-workflow.md) for a complete walkthrough from PDF papers to training and mining views.

## Key Capabilities

### For Pre-training: Token Purity and Semantic Common Sense

At the pre-training stage, models learn world knowledge and language structure. If the source data is noisy or semantically broken, the resulting model absorbs false correlations or even incorrect scientific concepts.

PorosData improves token purity and term stability through cleaning, normalization, and scientific terminology protection.

### For Data Mining: Entity Precision and Multimodal Anchoring

Data mining aims to extract structured knowledge from scientific documents, such as material compositions, transition temperatures, or processing conditions. This requires reliable values and units, stable entity recognition, and hard links between text references and multimodal assets.

PorosData provides numerical repair, entity stabilization, and text-image anchoring so that NER, entity linking, structured extraction, and knowledge graph construction can operate on a reliable substrate.

### Capability Overview

| Capability | Problem It Solves |
|------|------------|
| Intelligent text cleaning | Control characters, index noise, token fragmentation, and broken words |
| Scientific term validation | OCR-driven term corruption such as `X-ray -> 10-ray` |
| Numerical and unit repair | Broken scientific notation, decimal points, and units |
| Entity stabilization | Chemical elements and material names misread as LaTeX or symbols |
| Asset anchoring | Cross-modal indexing between figure references, images, and captions |

## Architecture Overview

PorosData uses a three-part modular architecture that covers the full scientific data pipeline:

```
[Literature] -> Parser (Extraction) -> Processor (Quality Delivery) -> Designer (Structured Expression) -> [Training / Mining Views]
```

| Module | Responsibility |
|------|------|
| **PorosData-Parser** | Extract processable base text and assets from PDFs, LaTeX, and other unstructured scientific sources |
| **PorosData-Processor** | Deliver high-quality text under academic atomicity, making input AI-Ready and Data Mining Ready |
| **PorosData-Designer** | Reconstruct high-quality text into `content`, `pure_text_stream`, `datamining`, and related indexable artifacts |

The modules can be used independently or chained as one end-to-end workflow. Extensions and plugins inherit the same atomicity contract so that quality remains consistent from parsing through cleaning and structured export.

## In-Depth Reference

- [Design Philosophy](concepts/design-philosophy.md)
- [Research Review](research/research-review.md)
- [Design Insights](research/design-insights.md)
- [Glossary](concepts/glossary.md)
- [API Reference](references/api-reference.md)

## Project Ecosystem

- [Contributing Guide](community/contributing.md)
- [Roadmap](community/roadmap.md)
- [Changelog](community/changelog.md)
