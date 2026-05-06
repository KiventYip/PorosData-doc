# Glossary

Shared vocabulary used across workflow, tool, and delivery pages so you can move between sections without reconciling conflicting terms.
{: .lead}

## Pipeline modules and data layers

| Term | Meaning |
|------|---------|
| **Parser** | Upstream stage that turns papers into reusable text blocks, figures, captions, and metadata. |
| **Processor** | Quality stage that cleans parser output so downstream steps see stable text and fields. |
| **Designer** | Delivery stage that organises stable input into full-text, structured, and multimodal outputs. |
| **`raw/`** | Layer retaining originals and parser packages for traceability. |
| **`processed/`** | Layer holding cleaned intermediates and processing reports. |
| **`structured/`** | Layer holding final full-text, datamining, and multimodal artefacts. |

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
