# PorosData Workflow: From Raw Papers to Final Deliverables

This page explains how PorosData turns scientific literature into outputs that are ready for training, structured extraction, retrieval, and human review. The focus here is the delivery path, not a single code example.
{: .lead}

## Pipeline Overview

```text
Raw Literature -> Parser -> Processor -> Designer -> Final Delivery Package
```
{: .section-intro}

| Stage | Main Task | Output |
|------|------|------|
| `Parser` | Extract text blocks, figures, captions, and basic metadata | Reusable raw content and image assets |
| `Processor` | Remove noise, repair fragmentation, and normalize expressions | Quality-ready intermediate results and reports |
| `Designer` | Organize sections and export structured views and indexes | Full-text outputs, structured JSON, and multimodal assets |

## Input and Output Layout

PorosData works best with a three-layer directory structure:
{: .section-intro}

```text
data/
├── raw/          # upstream parser results
├── processed/    # cleaned intermediate results
└── structured/   # final delivery package
```

The standard data flow is `raw -> processed -> structured`.

## Stage 1: Raw Inputs in `raw`

The `raw` layer keeps the upstream source package intact. Typical contents include:
{: .section-intro}

- Original PDF files
- Parser-generated Markdown or content lists
- Page-level intermediate files
- Extracted image assets
{: .tight-list}

This layer is preserved for traceability and review rather than for direct downstream delivery.

## Stage 2: `Processor` Builds `processed`

`Processor` turns raw parser results into stable intermediate inputs. Typical issues handled at this stage include:
{: .section-intro}

- Numbers, decimal points, and units broken by spacing noise
- Fragmented or corrupted terms, material names, and chemical expressions
- Noisy captions, table titles, and footnotes
- Long text blocks polluted by control characters or formatting artifacts
{: .tight-list}

Standard outputs at this stage usually include:

- Cleaned `*_content_list.json`
- Reusable copies of image assets
- A processing report such as `processing_report.json`
{: .tight-list}

## Stage 3: `Designer` Builds `structured`

`Designer` converts quality-ready inputs into final delivery outputs. A typical result layout is:
{: .section-intro}

```text
data/structured/
├── full_text/
├── datamining/
└── multimodal/
```

These three output groups serve different downstream needs:

| Directory | Purpose | Common Files |
|------|------|------|
| `full_text/` | Readable and reviewable full-text delivery | `_structured.json`, `_structured.txt` |
| `datamining/` | Extraction-ready and retrieval-ready structured outputs | `_datamining.json` |
| `multimodal/` | Indexed image assets linked back to the text | `_index.json`, `fig_*.md`, `assets/` |

## What Users Receive

After a standard run, users typically receive:
{: .section-intro}

1. A delivery directory organized by document ID
2. Plain-text outputs suitable for training use
3. Structured outputs suitable for extraction and retrieval
4. Multimodal indexes that connect text references to image assets
5. Reports that support batch review and delivery tracking
{: .tight-list}

## Recommended Reading Order

For batch projects, the easiest way to review results is:
{: .section-intro}

1. Start with `raw/` and confirm the source package is complete
2. Check `processed/` and its report to confirm the cleaning stage completed cleanly
3. Open `structured/` and choose the full-text, structured, or multimodal outputs based on your downstream task
{: .tight-list}

## Typical Use Cases

- Prepare high-quality text for training workflows
- Provide stable inputs for structured extraction
- Create indexable links between figures and body text
- Deliver one consistent package for database building and knowledge organization
{: .tight-list}

## Related Reading

- [Installation](installation.md)
- [Quick Start](quickstart.md)
- [Examples](../references/examples.md)
- [Processor](../tools/processor/index.md)
- [Designer](../tools/designer/index.md)
{: .tight-list}