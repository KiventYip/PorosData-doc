# Glossary

This page collects the core terms used across the PorosData documentation so readers can move between workflow, tool, and delivery pages with one shared vocabulary.
{: .lead}

## Core Modules

### Parser

The upstream extraction stage that turns raw papers into reusable text blocks, figures, captions, and metadata.

### Processor

The quality-preparation stage that cleans noisy parser outputs and makes them stable enough for downstream use.

### Designer

The structured-delivery stage that organizes stable inputs into full-text outputs, structured JSON, and multimodal indexes.

## Delivery Layers

### `raw`

The source layer that keeps original papers and upstream parser results for traceability.

### `processed`

The intermediate layer that stores cleaned outputs and processing reports.

### `structured`

The final delivery layer that stores full-text results, extraction-ready outputs, and multimodal assets.

## Output Types

### `full_text`

The delivery form used for readable and reviewable full-document outputs.

### `datamining`

The delivery form used for structured extraction, retrieval, and storage-oriented workflows.

### `multimodal`

The delivery form used to connect figure references in text with image assets and related descriptions.

## Common Fields and Concepts

### `doc_id`

The document identifier used to organize outputs and keep the delivery structure consistent.

### Caption

The descriptive text attached to a figure or table and often required for downstream review and extraction.

### Asset Anchor

A stable reference that links a figure or table mention in text to the actual asset in the delivery package.

### `processing_report`

The batch summary file that records output status, progress signals, and quality-review clues.

### Academic Atomicity

The principle that scientific meaning, structural cues, and context should remain as intact as possible during processing.

## Quick Links

- [Home](../index.md)
- [Quick Start](../get_started/quickstart.md)
{: .tight-list}
