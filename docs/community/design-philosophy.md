# Design Philosophy

Scientific literature is not generic prose: it encodes terms, units, notation, figures, and cross-references that must survive processing if downstream training, extraction, or review is to remain trustworthy. PorosData is built around that constraint rather than around “simplifying” papers into informal language.
{: .lead}

The aim is to make sources **more stable and more structurally usable** while **losing as little scientific meaning as the task allows**. Three commitments follow from that aim.

**Academic atomicity** — content is treated as a unit that should not be torn apart casually. At character level, formulas, chemistry, and symbols should not be structurally damaged by cleaning. At relation level, numbers, units, conditions, and claims should stay linked. At structure level, section hierarchy, figure references, and surrounding context should remain traceable in delivered artefacts.

**Knowledge-constrained processing** — normalisation is not “make it pretty”; it is **meaning-aware**. Citation cleanup, unit consistency, term protection, and chemical-expression handling exist to keep outputs closer to what the author intended, not only to satisfy a formatter. Recurring domain choices should migrate into **reusable rule packs and strategies** so batch runs converge on a stable standard.

**Layered delivery** — parsing, quality preparation, and structured export are **separate responsibilities** in sequence. The parser preserves recoverable content and assets; the processor stabilises text and metadata so later steps are not fighting OCR residue; the designer then organises that stable input into full-text, structured, and multimodal packages. The chain is meant to move literature into training, extraction, retrieval, and human review **without** diluting the rigour expected in research communication.

Essay-length research commentary and design trade-offs appear in the [Blog](../blog/index.md)—for instance [Research Review](../blog/posts/2026-05-06-research-review.md) and [Design Insights](../blog/posts/2026-05-06-design-insights.md)—rather than in this brief.
