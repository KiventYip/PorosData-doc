# Changelog

This log records **documentation and delivery-facing milestones** for this site: changes that affect how external readers understand scope, workflow, or outputs. Internal experiments stay out unless they alter public guidance.
{: .lead}

**What belongs here** — updates to site structure, recommended workflows, how deliveries should be interpreted, or major additions to user-facing guides. Ephemeral internal notes and historical audit-only material are omitted unless they change what the public docs assert.

**2026-05 — Documentation tree and URL realignment** — Markdown sources now sit in product folders under `docs/parser/`, `docs/processor/`, `docs/designer/`, together with expanded `docs/get_started/` (including [Examples](../get_started/examples.md)) and `docs/community/` ([Glossary](../community/glossary.md), [API Reference](../community/api-reference.md), [Design Philosophy](../community/design-philosophy.md), …). Legacy URL prefixes such as `/concepts/`, `/references/`, `/tools/`, and `/research/` are **not** published; refresh bookmarks and inbound links. Overlapping prose was trimmed while preserving contractual facts. Long-form research narrative remains on the [Blog index](../blog/index.md).

**2026-05 — Top-level navigation restructure** — Sidebar moved from abstract categories (**Tools** / **Concepts** / **Reference**) to a workflow order: **Home → Getting Started → PorosData Parser → PorosData Processor → PorosData Designer → Community → Blog**. Introduced [Parser overview](../parser/index.md); grouped Examples with Getting Started and reference-style pages with Community. Physical paths were later aligned with this model (see **Documentation tree and URL realignment**).

**2026-05 — Naming: databases and module prose** — User-facing body text standardises on **Parser**, **Processor**, and **Designer**; data layers are **Raw Database**, **Processed Database**, and **Designed Database** (PDF literature → Raw Database → … → Designed Database). Sidebar labels retain the **PorosData** prefix on the three product sections.

**2026-05 — Concepts consolidation and tool depth** — Internal `archive/` material was folded into the live site. Notable additions include [Dataset layout](../parser/dataset-layout.md), [Delivery standards](../designer/delivery-standards.md), [Data governance](../processor/data-governance.md); expanded [Processor](../processor/index.md) (architecture, workers, formula repair zones, token-evaluation strategy); expanded [Designer](../designer/index.md) (layout, CLI, deployment, full-text contract, section wrapping); and [Examples](../get_started/examples.md) with a fine-tuning primer. Retired mirror files and duplicate language copies are not republished; history remains in Git for traceability.

**2026-03 — Documentation refresh** — Home and overview rewritten from a delivery perspective; roles of Parser, Processor, and Designer clarified; roadmap added; placeholders replaced with installation, glossary, examples, and this changelog; vocabulary aligned around training preparation, extraction, and packaged outputs.

**How to use this page** — New readers should still begin at [Home](../index.md) and [Quick Start](../get_started/quickstart.md); return here when you need a concise record of how **published guidance** has moved.

**Links:** [Home](../index.md) · [Quick Start](../get_started/quickstart.md)
