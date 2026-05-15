# Getting started

This section is the **documentation hub** for the PorosData document stack. The manuals for **Parser**, **Processor**, and **Designer** live here in **pipeline order** (raw extraction → quality preparation → structured delivery), together with shared setup pages that apply across stages.
{: .lead}

## Three-stage manuals

Work moves from PDFs and engine output to review-ready packages. Each stage has its own overview and reference pages under this same **Getting started** branch in the site navigation.

| Stage | Role | Start here |
|--------|------|------------|
| **Parser** | Extracts blocks, figures, and content lists into the **Raw Database** | [Parser overview](../parser/index.md) · [Dataset layout](../parser/dataset-layout.md) |
| **Processor** | Cleans and stabilises lists into the **Processed Database** | [Processor overview](../processor/index.md) · [CLI reference](../processor/cli-reference.md) · [Configuration and runtime](../processor/configuration-and-runtime.md) |
| **Designer** | Exports tagged views, structure JSON, and multimodal indexes into the **Designed Database** | [Designer overview](../designer/index.md) · [Delivery standards](../designer/delivery-standards.md) · [CLI reference](../designer/cli-reference.md) |

For a single narrative that walks the directories and artefacts from end to end, use [End-to-end workflow](end-to-end-workflow.md).

## Shared setup and examples

These pages focus on environment, first commands, and copyable scenarios. They often emphasise **Processor** and **Designer** CLIs because those packages ship on PyPI; **Parser** setup and dashboard commands are maintained in the upstream **`gen-sci-data`** repository (see the Parser overview).

- [Installation](installation.md) — Python environment, `porosdata-processor`, sanity checks  
- [Quick Start](quickstart.md) — `TextCleaner`, optional YAML config, batch cleaning CLI  
- [Examples](examples.md) — single-document trial, batch runs, Processor → Designer handoff  
- [End-to-end workflow](end-to-end-workflow.md) — **Raw / Processed / Designed Database** layout and what to inspect  

## Where to read next

Terminology and integration notes: [Glossary](../community/glossary.md) · [API Reference](../community/api-reference.md). Project home: [PorosData home](../index.md).
