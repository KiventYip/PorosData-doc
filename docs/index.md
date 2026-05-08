---
hide:
  - toc
---

# PorosData

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PyPI version](https://img.shields.io/pypi/v/PorosData-Processor.svg)](https://pypi.org/project/porosdata-processor/)

This site documents a document-processing toolchain that turns PDFs, OCR output, and **Parser** output into structured, review-ready assets. The goal is to make scientific content easier to validate, reuse, and hand off without rewriting the underlying research.
{: .lead}

In domains such as materials science, source files often arrive with corrupted numerals, irregular spacing, damaged terminology, fractured formulas, and figure references that no longer align with captions. Those issues travel quickly into training corpora, extraction workflows, retrieval indexes, and human review queues. The stack targets that class of noise: it stabilises text and structure while preserving meaning and maintaining an auditable path from **Raw Database** inputs through **Processed Database** work to **Designed Database** deliveries.

## Overview and scope

The pipeline sits between original PDF literature and delivery-ready packages. Typical workloads include building higher-quality training corpora, feeding stable inputs into structured extraction and semantic retrieval, and assembling body text, captions, tables, and images into one coherent layout for databases, knowledge organisation, or multimodal modelling.
{: .section-intro}

The project follows **Academic Atomicity**: usability and cleanliness are improved without stripping the substantive content of the original material.
{: .section-intro}

| Dimension | What it provides |
|-----------|------------------|
| **Reliable content** | Formulas, citations, units, and terminology kept as intact as practicable |
| **Clear structure** | Sections, blocks, figures, and fields easier for both systems and reviewers to follow |
| **Traceable process** | The route from raw input to delivered output remains inspectable |
| **Reusable delivery** | One output set can support training, extraction, retrieval, and storage |

## Getting started

If you are new to the stack, these pages give the shortest path from install to examples.
{: .section-intro}

- [Installation Guide](get_started/installation.md)
- [Quick Start](get_started/quickstart.md)
- [Usage Examples](get_started/examples.md)
{: .tight-list}

!!! tip "End-to-end walkthrough"
    For a full path from papers to packaged outputs, see [End-to-end workflow](get_started/end-to-end-workflow.md).

## Pipeline, modules, and capabilities

Work is organised around a three-stage pipeline for scientific documents. The diagram illustrates how the **Raw Database**, **Processed Database**, and **Designed Database** layers connect with Parser, Processor, and Designer.
{: .section-intro}

![Pipeline functional architecture](assets/images/DESIGN.jpg)

```text
[PDF literature] -> Raw Database (Parser) -> Processed Database (Processor) -> Designed Database (Designer) -> [Training text / structured outputs / multimodal index]
```

| Module | Role |
|--------|------|
| **[Parser](parser/index.md)** | Turns scientific PDFs into structured JSON (MinerU) and lands per-document trees under **Raw Database** for Processor |
| **Processor** | Cleans noise, repairs fragmentation, and stabilises terms and numerical expressions into **Processed Database** |
| **Designer** | Shapes quality-ready text into full-text views, extraction-oriented outputs, and multimodal indexes under **Designed Database** |

**Typical cleaning and repair coverage** includes intelligent text cleaning (control characters, index noise, token fragmentation), scientific term validation (e.g. OCR corruption such as `X-ray` misread as `10-ray`), numerical and unit repair, entity stabilisation for chemical and material names, and cross-modal anchoring between figure references, images, and captions.

## What a delivery usually contains

Downstream consumers typically need packaged outputs rather than marginally cleaner prose. A typical delivery bundles full-text views for reading and review, plain streams for training, structured JSON for extraction and retrieval, multimodal indexes that bind mentions to assets, and batch-oriented reports that support traceability.
{: .section-intro}

## Where to go next

Terminology, integration detail, and design rationale sit under **Community**—start with the [Glossary](community/glossary.md), [Design Philosophy](community/design-philosophy.md), and [API Reference](community/api-reference.md). Essay-length background stays on the [Blog](blog/index.md) ([Research Review](blog/posts/2026-05-06-research-review.md), [Design Insights](blog/posts/2026-05-06-design-insights.md)).
{: .section-intro}

If you intend to contribute or follow releases, use the [Contributing Guide](community/contributing.md), [Roadmap](community/roadmap.md), and [Changelog](community/changelog.md).
{: .section-intro}
