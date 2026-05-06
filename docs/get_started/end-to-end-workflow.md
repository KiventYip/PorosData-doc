# PorosData Workflow: From Raw Papers to Final Deliverables

This page describes the **delivery path** from literature inputs to packages suitable for training, structured extraction, retrieval, and review. It complements step-by-step commands on other pages by keeping the focus on stages, directories, and what to inspect.
{: .lead}

**Pipeline in one line** — raw sources and parser output are stabilised by the processor, then shaped into delivery views by the designer:

```text
Raw Literature -> Parser -> Processor -> Designer -> Final Delivery Package
```

| Stage | Primary work | What you get |
|-------|----------------|---------------|
| Parser | Extract blocks, figures, captions, light metadata | Reusable raw text and image assets |
| Processor | Remove noise, repair fragmentation, normalise expressions | Intermediate results and batch reports under `processed/` |
| Designer | Organise sections and export views | Full-text, structured JSON, and multimodal indexes under `structured/` |

**Directory contract** — PorosData assumes a three-layer tree; the usual flow is `raw -> processed -> structured`:

```text
data/
├── raw/          # upstream parser packages
├── processed/    # cleaned intermediates
└── structured/   # final delivery package
```

**`raw/`** holds the upstream bundle per document: PDFs, parser-generated Markdown or lists, page-level intermediates, and extracted images. The layer is for **traceability and re-run**, not for handing off as final product.

**`processed/`** is where the processor writes cleaned `*_content_list.json`, mirrored images where configured, and a batch summary such as `processing_report.json`. Typical repairs address broken numerals and units, corrupted terms, noisy captions or footnotes, and unstable citation or formula boundaries.

**`structured/`** is the designer output. A common shape is:

```text
data/structured/
├── full_text/
├── datamining/
└── multimodal/
```

| Directory | Role | Typical files |
|-----------|------|----------------|
| `full_text/` | Reading, review, structure-aware training | `_structured.json`, `_structured.txt` |
| `datamining/` | Extraction and retrieval | `_datamining.json` |
| `multimodal/` | Figure–text linkage | `_index.json`, `fig_*.md`, `assets/` |

**What a completed run should provide** — per-document folders under `structured/`, plain-text streams where configured, structured JSON for mining, multimodal indexes that resolve figure mentions to assets, and reports that support batch review and traceability.

**How to review results efficiently** — (1) confirm `raw/` is complete for each `doc_id`, (2) read `processing_report.json` and spot-check `processed/` for regressions, (3) open the appropriate subtree under `structured/` for your downstream task (reading vs mining vs multimodal).

**Typical motivations** — high-quality training text, stable inputs for rule-based or learned extraction, explicit links between body text and figures, and a single package shape for storage or knowledge organisation.

**Related:** [Installation](installation.md) · [Quick Start](quickstart.md) · [Examples](examples.md) · [Parser](../parser/index.md) · [Processor](../processor/index.md) · [Designer](../designer/index.md)
