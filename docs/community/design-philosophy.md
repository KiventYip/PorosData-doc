# Design Philosophy

Scientific writing is not ordinary prose. It encodes specialised terms, units, notation, figures, and cross-references that must survive transformation if downstream training, extraction, or peer review is to stay trustworthy. PorosData is designed around that constraint instead of treating papers as informal text to be simplified away.
{: .lead}

The objective is to make sources **more stable and easier to reuse structurally**, while **sacrificing as little scientific meaning as the workload permits**. Three design commitments follow.

**Academic atomicity** — content is treated as a unit that should not be torn apart casually. At character level, formulas, chemistry, and symbols should not be structurally damaged by cleaning. At relation level, numbers, units, conditions, and claims should stay linked. At structure level, section hierarchy, figure references, and surrounding context should remain traceable in delivered artefacts.

**Knowledge-constrained processing** — normalisation is not “make it pretty”; it is **meaning-aware**. Citation cleanup, unit consistency, term protection, and chemical-expression handling exist to keep outputs closer to what the author intended, not only to satisfy a formatter. Recurring domain choices should migrate into **reusable rule packs and strategies** so batch runs converge on a stable standard.

**Layered delivery** — parsing, quality preparation, and structured export are **separate responsibilities** in sequence. The parser preserves recoverable content and assets; the processor stabilises text and metadata so later steps are not fighting OCR residue; the designer then organises that stable input into full-text, structured, and multimodal packages. The chain is meant to move literature into training, extraction, retrieval, and human review **without** diluting the rigour expected in research communication.

Essay-length research commentary and design trade-offs appear in the [Blog](../blog/index.md)—for instance [Research Review](../blog/posts/2026-05-06-research-review.md) and [Design Insights](../blog/posts/2026-05-06-design-insights.md)—rather than in this brief.
