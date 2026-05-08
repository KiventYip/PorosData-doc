# Glossary

Shared vocabulary used across workflow, tool, and delivery pages so you can move between sections without reconciling conflicting terms.
{: .lead}

## Pipeline modules and data layers

| Term | Meaning |
|------|---------|
| **Parser** | Extraction stage (implementation repo: `gen-sci-data`) that turns papers into reusable text blocks, figures, captions, and metadata under the **Raw Database**. |
| **Processor** | Quality stage that cleans Parser output into the **Processed Database** so downstream steps see stable text and fields. |
| **Designer** | Delivery stage that organises stable input into full-text, structured, and multimodal outputs under the **Designed Database**. |
| **Raw Database** | Layer retaining originals and Parser bundles for traceability (default root often `data/Raw Database/`; legacy docs may show a `raw/` segment). |
| **Processed Database** | Layer holding cleaned intermediates and processing reports (default root often `data/Processed Database/`). |
| **Designed Database** | Designer output root: per-`doc_id` folders with `*.content.json`, `*.structure.json`, `*.assets.index.json`, and `images/`. Override the path with `--output_dir`. |

## Output and field concepts

| Term | Meaning |
|------|---------|
| **`full_text`** | Human- and machine-readable full-document delivery (JSON + parallel plain text as documented). |
| **`datamining`** | Section-oriented structured JSON aimed at extraction, retrieval, and storage. |
| **`multimodal`** | Indexes and assets linking in-text figure references to image files and captions. |
| **`doc_id`** | Stable per-document identifier used across all layers. |
| **Caption** | Figure or table descriptive text, often critical for review and mining. |
| **Asset anchor** | Stable link between a mention in text and a concrete file in the delivery tree. |
| **`processing_report`** | Batch-level summary with status and quality signals for review. |
| **Academic atomicity** | Design rule: preserve scientific meaning, structure, and context during cleaning unless an explicit, reviewed rule says otherwise. |

**See also:** [Home](../index.md) · [Quick Start](../get_started/quickstart.md)
