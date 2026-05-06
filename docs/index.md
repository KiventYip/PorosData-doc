---
hide:
  - toc
---

# PorosData

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PyPI version](https://img.shields.io/pypi/v/PorosData-Processor.svg)](https://pypi.org/project/porosdata-processor/)

PorosData is a framework for processing scientific documents and delivering structured, reviewable outputs. It takes PDFs, OCR output, and parser artefacts and turns them into data assets that are easier to validate, reuse, and hand off downstream.
{: .lead}

In fields such as materials science, source documents routinely carry corrupted numerals, spacing noise, damaged terms, broken formulas, and figure references that no longer line up with captions. Those defects propagate into training data, extraction pipelines, retrieval, and manual review. PorosData is intended to suppress that noise while preserving scientific meaning and leaving a traceable path from input to delivery.

## Overview and scope

PorosData sits between raw literature and delivery-ready assets. Typical uses include preparing corpora for model training, supplying stable inputs for structured extraction and semantic retrieval, and packaging body text, captions, tables, and images into a single delivery layout for databases, knowledge organisation, or multimodal workflows.
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
    For a full path from papers to packaged outputs, see [End-to-End Workflow](get_started/end-to-end-workflow.md).

## Pipeline, modules, and capabilities

PorosData organises work around a three-stage pipeline for scientific documents. The diagram illustrates how storage, processing modules, and delivery-facing outputs connect in one system.
{: .section-intro}

![PorosData functional architecture](assets/images/DESIGN.jpg)

```text
[Raw Literature] -> Parser -> Processor -> Designer -> [Training Text / Structured Outputs / Multimodal Index]
```

| Module | Role |
|--------|------|
| **Parser** | Extracts reusable text blocks and assets from PDFs and parser output |
| **Processor** | Cleans noise, repairs fragmentation, and stabilises terms and numerical expressions |
| **Designer** | Shapes quality-ready text into full-text views, extraction-oriented outputs, and multimodal indexes |

**Typical cleaning and repair coverage** includes intelligent text cleaning (control characters, index noise, token fragmentation), scientific term validation (e.g. OCR corruption such as `X-ray` misread as `10-ray`), numerical and unit repair, entity stabilisation for chemical and material names, and cross-modal anchoring between figure references, images, and captions.

## What a delivery usually contains

PorosData aims at packaged outputs, not only “cleaner text.” A standard delivery often includes full-text material for reading and review, plain-text streams for training, structured JSON for extraction and retrieval, multimodal indexes linking text to image assets, and reports or logs that support batch review and traceability.
{: .section-intro}

## Where to go next

Terminology, integration detail, and design rationale sit under **Community**—start with the [Glossary](community/glossary.md), [Design Philosophy](community/design-philosophy.md), and [API Reference](community/api-reference.md). Essay-length background stays on the [Blog](blog/index.md) ([Research Review](blog/posts/2026-05-06-research-review.md), [Design Insights](blog/posts/2026-05-06-design-insights.md)).
{: .section-intro}

If you intend to contribute or follow releases, use the [Contributing Guide](community/contributing.md), [Roadmap](community/roadmap.md), and [Changelog](community/changelog.md).
{: .section-intro}
