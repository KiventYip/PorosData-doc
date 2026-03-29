# PorosData-Designer

## Positioning

`Designer` is the structured-delivery module in PorosData. It works on top of the quality-prepared output from `Processor` and turns text, figures, and context into final deliverables that support training, extraction, retrieval, and review.

In short:

- `Processor` makes the content stable
- `Designer` organizes it into delivery-ready outputs
{: .tight-list}

## Main Responsibilities

`Designer` focuses on:
{: .section-intro}

- section and paragraph organization
- structured field assembly
- text-image linking
- export of full-text and structured outputs
- multimodal index generation
{: .tight-list}

It is not intended to take over large-scale OCR cleaning. Its role is to turn already-stable intermediate inputs into usable delivery products.

## Three Core Output Groups

At the current stage, `Designer` mainly delivers three output groups:
{: .section-intro}

| Output Group | Main Use | Common Files |
|------|------|------|
| Full-text outputs | reading, review, training preparation | `_structured.txt`, `_structured.json` |
| Structured outputs | extraction, retrieval, storage | `_datamining.json` |
| Multimodal outputs | figure-text linking and asset management | `_index.json`, `fig_*.md`, `assets/` |

## Output Layout

A typical output layout looks like this:
{: .section-intro}

```text
data/structured/
├── full_text/{doc_id}/
├── datamining/{doc_id}/
└── multimodal/{doc_id}/
```

Each document is stored by `doc_id`, which makes batch delivery, spot checks, and backtracking easier.

## What Users Receive

In a standard delivery run, `Designer` organizes one paper into several reusable result types:
{: .section-intro}

- a readable full-text result
- a plain-text stream for training use
- a structured JSON result for extraction and retrieval
- a multimodal index that links text references back to image assets
{: .tight-list}

## Key Output Notes

### `full_text`

`full_text` is the full-document delivery layer and usually includes:
{: .section-intro}

- a complete text with structural markers
- a plain-text stream without those markers
- a human-readable text version for inspection
{: .tight-list}

### `datamining`

`datamining` is the structured-use layer and usually includes:
{: .section-intro}

- title
- section content
- formula lists
- chemical or material expressions
- figure and table references
{: .tight-list}

### `multimodal`

`multimodal` is the figure-linking layer and usually includes:
{: .section-intro}

- an image index file
- figure-level description cards
- image assets connected to text references
{: .tight-list}

## Input Expectations

To produce stable outputs, `Designer` expects:
{: .section-intro}

- major noise has already been handled upstream
- numbers, units, terms, and material names are reasonably consistent
- captions, table titles, and footnotes are already usable
- text-to-figure references have not been broken earlier in the pipeline
{: .tight-list}

## Design Principles

`Designer` follows a few practical rules:
{: .section-intro}

- structure should serve delivery, not merely mimic layout
- section hierarchy should stay as stable as possible within one document
- image assets should remain traceable to their original context
- one delivery package should support reading, extraction, and review together
{: .tight-list}

## Known Boundaries

When using `Designer`, keep in mind:
{: .section-intro}

- it depends on upstream quality and cannot replace pre-cleaning
- for semantically unstable sections, it favors overall usability over overly fine labels
- final business schemas may still require an extra mapping layer
{: .tight-list}

## Relationship with `Processor`

`Designer` is not an isolated module. It relies on the stable input prepared by `Processor` and turns that quality-ready content into delivery directories and structured results for downstream users.