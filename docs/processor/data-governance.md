# Data Governance

How PorosData improves quality **over time** through a **closed loop**: audits yield evidence, rule changes are reviewed, and deliveries are gated against the same standards used in development. The processor’s **control flow stays frozen**; behaviour evolves mainly through **declarative rule packs** (TOML), with Python reserved for genuinely contextual or stateful logic.
{: .lead}

> Quality advances by **adding reviewed rules**, not by casually rewriting core pipeline code. Every cycle should leave a **trace**: timestamps, artefacts, and an explicit decision record.

## Governance loop

```text
┌─────────────────────────────────────────────────────────────────┐
│   Audit -> Identify gap -> Bootstrap candidate -> Sample validate │
│       ^                                    │                     │
│       └──────── Delivery gate <- Promote rule ──────────────────┘
└─────────────────────────────────────────────────────────────────┘
```

Each step feeds the next; a release typically starts a new audit pass for the following one.

**Audit** — run the project audit on current `processed/` data: pattern detectors surface OCR residue, odd formatting, and suspicious citations; structural checks cover delimiter balance, citation statistics, and metadata coverage. Results are **timestamped JSON** for diffing across runs. Operators still triage true vs false positives and mark blocking vs warning severity.

**Identify gap** — classify each finding:

| Finding | Response | Location |
|---------|----------|----------|
| Regex-fixable | Add rule | Canonical rule pack |
| Structural / algorithmic | Code change with review | Processor source |
| Detector false positive | Refine audit pattern | Audit pack |
| Accepted edge case | Document and skip | Audit notes |

**Bootstrap candidate** — when a gap warrants a declarative fix, author a candidate rule carrying `id`, `priority`, `target`, `pattern`, and `replacement`, and hold it in staging until review completes. IDs such as `{domain}.{target}.{description}` keep large packs navigable.

**Sample validate** — apply candidates to representative slices and examine three things together: match counts on intended cases, **replacement-chain** conflicts (one rule firing after another in unintended ways), and **semantic** fidelity on real sentences—not only whether the regex matched.

**Promote rule** — merge validated candidates into the canonical pack, archive the prior pack with a `YYYYMMDD_HHMMSS` timestamp, run the regression tests, and **reprocess** affected corpora so production data reflects the promoted rules.

**Delivery gate** — run blocking detectors across all `processed/` data. A single blocking hit fails the gate; warnings are reported but non-blocking. A successful gate, together with the audit trail and promotion record, constitutes the auditable **release trace** for that cut.

**Architecture boundaries** — declarative rules cover regex, replacements, normalisation maps; Python covers contextual algorithms and state; **pipeline order, Shield, and module skeleton are frozen** without explicit approval; rule files, detectors, tests, and docs evolve freely. Processor implementation detail lives upstream; this site links it from the [Processor](index.md) page.

**See also:** [Delivery standards](../designer/delivery-standards.md) · [Dataset layout](../parser/dataset-layout.md) · [Glossary](../community/glossary.md)
