# Delivery Standards

Named **readiness levels** and concrete obligations on Processor and Designer before data is consumed downstream. Levels are not always sequential: a project may target one or several depending on the task.
{: .lead}

| Level | Guarantee | Typical consumer |
|-------|-----------|------------------|
| **AI-Ready** | Text is usable by LLM/embedding models without heavy format noise; numbers, units, and inline math remain legible | Generative and embedding workflows |
| **Structure-Aware Training Ready** | Stable, closed Poros tags supply explicit semantic boundaries | Long-document, structure-aware training |
| **Plain-Text Training Ready** | Tag-free natural language stream | Pre-training, embeddings, retrieval without tag awareness |
| **Data Mining Ready** | Entities and attribute–value relations stay recoverable | Extraction, retrieval, knowledge graphs |

Shared rule: **quality precedes structure**; tags elaborate stable text rather than compensating for broken text.

**Processor vs Designer** — Processor ships the **quality package** (clean, stable, computable text without final business records). Designer ships the **structure package** (views, indexes, multimodal linkage). Designer quality is **bounded** by Processor output; Processor is expected to **lower disambiguation cost** for Designer rather than leaving ambiguous attribute pairing.

## Processor obligations

Processor output should meet **AI-Ready** and **Data Mining Ready** minima across six dimensions:

| Dimension | Requirement |
|-----------|---------------|
| **Text continuity** | Repair OCR fragmentation in numbers, decimals, units, and element symbols |
| **Entity clarity** | Protect and stabilise materials, methods, instruments, and scientific names within a document |
| **Numbers and units** | Preserve magnitudes, decimals, superscripts, and unit notation |
| **Formula safety** | Repair only when structurally safe; never destroy math or chemistry boundaries |
| **Citations** | Normalise in-text numeric citations; do not rewrite reference lists or fuse citations into words |
| **Metadata fields** | Apply the same rigour to captions, table titles, and footnotes as to body text |

Implementation detail lives on the [Processor](../processor/index.md) page.

## Designer obligations

Designer must emit the `data/structured/` tree described in [Dataset layout](../parser/dataset-layout.md) and satisfy the structure-aware, plain-text, and mining views **per file contract**.

**Deliverable groups**

| Group | Files | Role |
|-------|-------|------|
| `full_text/{doc_id}/` | `_structured.json`, `_structured.txt` | `content` + `pure_text_stream`; `.txt` mirrors tag-free stream |
| `datamining/{doc_id}/` | `_datamining.json` | Sections plus optional `formulas`, `chemical_formulas`, `asset_refs` |
| `multimodal/{doc_id}/` | `_index.json`, `fig_*.md`, `assets/` | Consistent figure index, cards, and assets |

Consumers must be able to choose `content`, `pure_text_stream` / `.txt`, or `_datamining.json` without contradictions.

**Poros tagging** — coarse-grained and stability-first. Root `<poros_doc>...</poros_doc>` is mandatory. Section tags draw from a **small fixed set** (`header`, `abstract`, `introduction`, `experimental`, `results`, `discussion`, `conclusion`, `acknowledgements`, `references`); unmapped sections fall back to `poros_section_section`. Title tags align to that vocabulary; subtitles keep **level** only (`poros_subtitle_level2/3`). Inline tags stay minimal (`poros_paragraph`, `poros_equ`, `poros_chem`, `poros_asset`, `poros_keywords`). Tags must nest and close; section closers are strong boundaries but **do not** replace document EOS tokens.

**View separation** — `content` may contain `poros_*`; `pure_text_stream` and `_structured.txt` must contain **none**; `_datamining.json` encodes structure as **fields**, not flattened pseudo-text; inline math delimiters stay balanced and structurally valid.

## Acceptance and rejection

**Accept** when Processor passes the six dimensions without regression; Designer emits required files and fields per `doc_id`; Poros trees validate; `pure_text_stream` / `.txt` contain no tag leakage; `_datamining.chemical_formulas` holds only chemical/material expressions; multimodal indexes reference assets that exist on disk; body and metadata fields are treated **consistently** within a document.

**Reject** on persistent OCR damage or broken formulas/citations in Processor output; missing required files or fields; invalid or unbalanced Poros trees; tag leakage into plain streams; mismatched multimodal assets; inconsistent treatment across body vs captions vs footnotes.

**Further reading:** [Dataset layout](../parser/dataset-layout.md) · [Processor](../processor/index.md) · [Designer](index.md) · [Data governance](../processor/data-governance.md) · [Glossary](../community/glossary.md)
