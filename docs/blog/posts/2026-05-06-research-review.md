---
description: >-
  Scientific text quality for training versus mining, and where PorosData sits in the delivery chain.
date:
  created: 2026-05-06
slug: 2026-05-06-research-review
categories:
  - Engineering
tags:
  - Research
  - Data Quality
  - Processor
authors:
  - kiventyip
---

!!! abstract "Note"
    Exploratory note on architecture and open questions around scientific data processing. Not a stable product commitment.

# Research Review

Scientific papers encode terminology, numerals, notation, figures, and qualifiers in ways that **general-purpose** text tools rarely preserve. Once PDF or OCR pipelines emit machine-readable text, small formatting defects propagate into training corpora, extractors, and review tools—so preparation standards must be **domain-aware**, not merely “spell-checked.”

<!-- more -->

**Quick links:** [Home](../../index.md) · [Quick Start](../../get_started/quickstart.md)

## Failure modes and why they differ by task

Typical breakage includes split numbers and units, corrupted terms, damaged math delimiters, captions that no longer align with figures, and contextual qualifiers (temperature, method, condition) that drift away from the values they modify. **Training-oriented** workflows care about **token purity**, **term accuracy**, and **long-range coherence**: noise steals context window budget and teaches spurious patterns; systematic mis-readings (e.g. `X-ray` rendered as `10-ray`) corrupt concepts; hyphenation and line-break artefacts inflate vocabulary and fragment phrases. **Mining-oriented** workflows care about **determinate values**, **stable entities**, and **explicit anchors** between text and assets: if magnitudes or chemical names are ambiguous, extraction and linking fail even when the prose “looks fine” to a human skimmer.

## PorosData as a layered response

Rather than treating “cleaning” and “packaging” as unrelated chores, PorosData chains **parse → stabilise → export**:

| Stage | Responsibility | Why it matters |
|-------|----------------|----------------|
| Parser | Preserve recoverable content and assets | Keeps a defensible source-of-truth package |
| Processor | Remove noise and stabilise text | Reduces failure rates for both training and mining |
| Designer | Emit full-text, structured, and multimodal views | Matches heterogeneous downstream consumers without re-deriving structure from scratch |

## Target quality profiles (sketch)

**Training-facing** — sequences should read continuously; scientific vocabulary should remain semantically faithful; inline math and references should survive well enough for later tooling. **Mining-facing** — attributes and units should be machine-recoverable; entities should normalise predictably within and across documents; figure and table references should resolve to captions and files. Both profiles assume Processor output meets the bar described in [Delivery standards](../../designer/delivery-standards.md) before Designer contracts apply.

## Open questions

Important tensions remain: how far automatic repair may go before it alters meaning; how to normalise irregular formulas without structural damage; how large terminology resources can grow before maintenance dominates; how multimodal anchors stay stable across parser versions and layout styles. These are not cosmetic—they determine whether a delivery package can be **reused across projects** or only as a one-off.

**Further reading:** [Design Insights](2026-05-06-design-insights.md) · [Processor](../../processor/index.md) · [Designer](../../designer/index.md) · [API Reference](../../community/api-reference.md)
