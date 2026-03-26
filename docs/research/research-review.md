---
status: exploratory
author: KiventYip
date: 2024-03-09
hide:
  - toc
---

!!! abstract "Research Note"
    This page belongs to the **PorosData Research & Thinking** series. It records architectural evolution, unfinished algorithmic explorations, and open questions around data-centric AI. It should not be interpreted as a final or stable product commitment.

# Research Review

## Quick Links

- [Home](../index.md)
- [Quick Start](../get_started/quickstart.md)

## What Kind of Data Quality Do We Need?

This page reviews data quality requirements from two perspectives: **AI-Ready** and **Data Mining Ready**.

### 1. AI-Ready Standards: Pre-training Requires Token Purity and Semantic Common Sense

Pre-training enables models to acquire general-purpose representations, semantic and syntactic understanding, and world knowledge by consuming large-scale natural text. If the data itself is wrong, the model can absorb false knowledge.

For that reason, pre-training data must preserve token purity.

- **Token Stream Purity**: The main text should not contain control characters, index residues, or other non-semantic fragments. Such artifacts waste tokens and disturb contextual learning.
- **Semantic Common Sense Accuracy**: Core scientific terminology must not be systematically corrupted. If `X-ray` becomes `10-ray`, the model learns a false scientific concept.
- **Long-Text Coherence**: Broken words and missing hyphens caused by line-break damage increase vocabulary entropy and reduce the model's ability to understand long and complex scientific sentences.

### 2. Data Mining Requirements: Entity Precision and Logical Linking

The goal of data mining is to extract structured knowledge from large document collections, such as alloy composition or transition temperature.

- **Certainty of Values and Units**: Scientific mining is highly sensitive to numerical form. OCR-broken expressions such as `$1 0 ^ { 5 }$` can destroy magnitude recognition and downstream attribute extraction.
- **Robustness of Entity Recognition**: Chemical elements such as `Ni` and `Au` must not be mistaken for LaTeX-like symbols. Otherwise, entity linking and graph construction fail because names are no longer reliable.
- **Anchoring of Multimodal Assets**: Mentions such as `Fig. 1` must not remain plain strings. They should become hard anchors that can point directly to the corresponding image asset and caption.

