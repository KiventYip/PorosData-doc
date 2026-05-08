---
description: >-
  Semantic stability, structural consistency, and minability across Processor and Designer.
date:
  created: 2026-05-06
slug: 2026-05-06-design-insights
categories:
  - Engineering
tags:
  - Research
  - Design
  - Processor
  - Designer
authors:
  - jianhonng
---

!!! abstract "Note"
    Exploratory note on architecture and open questions around scientific data processing. Not a stable product commitment.

# Design Insights

**Quick links:** [Home](../../index.md) · [Quick Start](../../get_started/quickstart.md)
{: .lead}

Model-centric pre-training and literature-scale mining impose **different** failure sensitivities. The pipeline therefore treats **semantic stability**, **structural consistency**, and **minability** as explicit design targets, implemented mainly through [Processor](../../processor/index.md) (quality) and [Designer](../../designer/index.md) (views and contracts). Executable detail on pipelines, tags, and acceptance tests now lives in those product docs rather than in this essay.

<!-- more -->

## Processor: text quality for sequence modelling

When text is consumed as **token sequences**, the objective is to let models learn world knowledge and linguistic regularities without absorbing artefacts that carry no scientific meaning. PDF and OCR paths routinely inject control symbols, running headers, and index debris; language models still tokenise those fragments, distorting conditional probabilities. **Token purity** therefore requires deliberate detection and removal of non-semantic material.

**Terminology accuracy** is equally critical: scientific terms behave like stable semantic units. Systematic corruption—`X-ray` misread as `10-ray`, for example—does not merely look wrong; it teaches the wrong concept. Domain lexica and contextual guards are part of the defence.

**Long-text coherence** suffers when hyphenation and line breaks split words (`short-range` → `short - range` or `shortrange`). Vocabulary inflates, stable phrases fragment, and modelling long scientific sentences becomes harder. Cleaning restores word continuity and predictable hyphenation so downstream models see linguistically plausible spans.

## Designer: structure and multimodal anchoring

Mining workflows care less about fluency than about **recoverable facts**: temperatures, pressures, compositions, and similar attributes must remain **numerically determinate**. OCR often fractures exponents (`$10^5$` → `$1 0 ^ { 5 }$`), which breaks magnitude extraction unless repaired.

**Entity stability** matters for chemical and materials names (`Ni`, `Au`, `Fe3C`). When those strings collapse into malformed pseudo-LaTeX, named-entity and linking stages fail, and knowledge graphs cannot anchor vertices reliably.

**Multimodal anchoring** goes beyond string mentions such as “Fig. 1.” Important evidence sits in figures, tables, and images; parsing must yield **indexable links** from in-text references to the corresponding assets and captions so multimodal training and retrieval do not stop at plain text.

## Technical landscape: complementary levers

No single technique covers scientific PDFs. In practice several layers stack:

| Approach | Core idea | Strengths | Limits | Typical contribution |
|----------|-----------|-----------|--------|----------------------|
| **Regex and deterministic rules** | Pattern-based repair | Fast, cheap, auditable | Weak on ambiguity (`Ni-` vs minus) | Removes spacing and header noise |
| **Lexica / dictionaries** | Multi-pattern attachment (e.g. Aho–Corasick) | Strong inside known vocabularies | Maintenance cost; novel compounds | Stabilises entities and formulas |
| **OCR / layout models** | Visual-to-markup (Nougat, Marker, classical OCR) | Better tables and math recovery | Compute cost; hallucination risk | Reduces upstream damage |
| **Small-model polish** | 1–3B LMs for semantic touch-up | Handles irregular residue | Latency; must not rewrite meaning | Final pass before embedding-heavy use |

| Summary | Cost | Flexibility | Accuracy focus |
|---------|------|-------------|----------------|
| Regex | Very low | Low | Known patterns |
| Dictionaries | Low | Medium | In-lexicon entities |
| Vision models | Medium–high | High | Layout + math |
| Small LMs | High | Very high | Contextual fixes |

## Limits that remain

Even with stacked strategies, difficult formulas, dictionary coverage, cross-parser anchor stability, and the trade-off between throughput and human review cost are **not solved once and for all**. How aggressively to “fix” ambiguous math, how broad lexica should grow, and how to regression-test multimodal links across parser upgrades remain active engineering questions.

**Further reading:** [Research Review](2026-05-06-research-review.md) · [Processor](../../processor/index.md) · [Designer](../../designer/index.md)
