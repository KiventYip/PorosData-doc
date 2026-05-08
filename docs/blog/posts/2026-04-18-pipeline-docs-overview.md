---
description: >-
  How Processor and Designer docs fit the end-to-end Data-Centric AI workflow.
date:
  created: 2026-04-18
slug: 2026-04-18-pipeline-docs-overview
categories:
  - Engineering
tags:
  - Processor
  - Designer
  - Engineering
authors:
  - porosdata
---

# Mapping the pipeline to the docs

This documentation splits **operational detail** (how to run and validate) from **conceptual** pages (contracts, layout, governance). This note is a **map**, not a tutorial: it tells you where to read once you know which stage you care about.

<!-- more -->

**Processor** documentation emphasises batch cleaning, intermediate artefacts under **Processed Database**, and quality signals before handoff. **Designer** documentation explains how stable intermediates become per-`doc_id` delivery folders (default under **Designed Database**)—full-text JSON, structure JSON, multimodal indexes—and how those views relate to training and extraction consumers.

For a single narrative path from install through integration, start at [End-to-end workflow](../../get_started/end-to-end-workflow.md), then open [Processor](../../processor/index.md) and [Designer](../../designer/index.md) as needed.
