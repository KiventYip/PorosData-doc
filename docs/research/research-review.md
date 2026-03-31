---
status: exploratory
author: KiventYip
date: 2024-03-09
hide:
  - toc
---

!!! abstract "Research Note"
    This page belongs to the **PorosData Research & Thinking** series. It records architectural evolution, unfinished algorithmic explorations, and open questions around scientific data processing. It should not be interpreted as a final or stable product commitment.

# Research Review

## Quick Links

- [Home](../index.md)
- [Quick Start](../get_started/quickstart.md)
{: .tight-list}

## Problem Background

Scientific literature is rich in terminology, numbers, formulas, figures, and contextual qualifiers. Once papers are converted from PDF or OCR outputs into machine-readable text, small formatting errors quickly become downstream data problems.

Typical failures include:

- broken numbers and units
- corrupted scientific terms
- damaged formula boundaries
- captions and figure references losing their links
- context such as temperature, condition, or method drifting away from the value it describes

Because of this, scientific data preparation needs a different quality standard from general-purpose text processing.

## Why Training Preparation and Data Mining Need Different Standards

The two major downstream scenarios care about different failure modes.

### 1. Training Preparation

Training preparation is sensitive to sequence quality and semantic continuity.

- **Token purity** matters because control characters, page residue, and non-semantic fragments waste sequence budget and disturb learning.
- **Terminology accuracy** matters because corrupted terms such as `X-ray -> 10-ray` teach the wrong concept.
- **Long-text coherence** matters because broken words and damaged punctuation reduce the stability of long scientific passages.

### 2. Data Mining

Data mining is sensitive to structural precision and contextual binding.

- **Values and units** must stay determinate, or downstream extraction cannot recover the right magnitude.
- **Entity names** must stay stable, or matching, linking, and normalization become unreliable.
- **Text-image anchors** must remain explicit, or figures and captions cannot be reused in structured delivery.

## Where PorosData Fits

PorosData addresses these two scenarios through a layered delivery chain:

| Stage | Main Responsibility | Why It Matters |
|------|------|------|
| `Parser` | preserve usable source content and assets | keeps the source package intact enough for later recovery |
| `Processor` | remove noise and stabilize text quality | prepares content for reliable downstream use |
| `Designer` | export delivery-ready structures | turns stable inputs into full-text, structured, and multimodal outputs |

In other words, PorosData does not treat cleaning and delivery as separate concerns. It treats them as one connected path from source material to reusable outputs.

## What Kind of Data Quality Do We Need?

The target quality profile can be summarized in two views.

### Training Preparation View

- the text should be readable and structurally continuous
- scientific terms should stay semantically correct
- formulas and inline references should remain intact enough for downstream use

### Data Mining View

- values, units, and attributes should remain identifiable
- entities should stay stable within and across documents
- figure references, captions, and other metadata should remain connected to the main text

## Current Limits and Open Questions

Even with a stable processing pipeline, several questions remain open:

- how far should automatic repair go before it risks changing source meaning
- how should highly irregular formulas be normalized without damaging structure
- how much domain dictionary coverage is enough before maintenance cost becomes too high
- how should multimodal anchoring be kept stable across different parser outputs

These are not just implementation details. They directly affect whether a delivery package remains reusable across projects.

## Further Reading

- [Design Insights](design-insights.md)
- [Processor](../tools/processor/index.md)
- [Designer](../tools/designer/index.md)
- [API Reference](../references/api-reference.md)

