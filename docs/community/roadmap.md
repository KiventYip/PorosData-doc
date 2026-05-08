# Roadmap

This roadmap is written for **external delivery and adoption**: what already ships, how the delivery package is expected to grow, and who the narrative is for.
{: .lead}

The toolchain is organised as **one continuous chain** — preserve sources in the **Raw Database**, stabilise text in the **Processed Database**, then export structured and multimodal views into the **Designed Database**:

| Module | Role today | Principal outputs |
|--------|------------|-------------------|
| Parser | Ingest papers and extraction artefacts | **Raw Database**: text blocks, images, basic metadata |
| Processor | Raise content quality | **Processed Database**: cleaned intermediates, reports, stable inputs for the next stage |
| Designer | Produce delivery layouts | **Designed Database**: full-text views, structured JSON, multimodal indexes |

The **target package** remains consistent across phases: a per-document result tree, plain-text streams for training preparation, structured artefacts for extraction and storage, multimodal indexes that preserve text–figure links, and reporting for review and traceability.

**Delivery phases (intent, not a dated contract)** — **Current focus:** end-to-end batch paths, the **Raw Database → Processed Database → Designed Database** layout (per-`doc_id` delivery folders), core full-text / datamining / multimodal groups, baseline audit and reporting, and an iterative loop of process → review → adjust → re-run. **Near term:** tighter consistency for terms, units, citations, and section layout; better behaviour on long documents, heavy formulas, and large batches; richer external-facing guides; stronger figure–text review; gradual formalisation of suspicious-pattern feedback into rules. **Longer term:** clearer acceptance standards for batch delivery, one coherent model across all output views, dependable reuse for training and retrieval, and improved project-level tracking and iteration.

**Audience** — teams building scientific literature datasets, engineering groups preparing corpora, application teams doing extraction or semantic retrieval, and product or data roles that need **reviewable** handoffs rather than opaque dumps.

**Continue from here:** [Home](../index.md) · [Quick Start](../get_started/quickstart.md) · [End-to-end workflow](../get_started/end-to-end-workflow.md)
