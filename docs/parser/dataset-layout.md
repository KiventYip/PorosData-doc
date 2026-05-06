# Dataset layout

File-level contract for the **three-tier** `data/` model: what each directory holds, how `doc_id` is used, and how artefacts line up between stages. For the narrative path from install to handoff, see [End-to-End Workflow](../get_started/end-to-end-workflow.md).
{: .lead}

**Top-level shape** — flow is normally `raw → processed → structured`:

```text
data/
├── raw/          # parser bundles, traceability anchor
├── processed/    # Processor output
└── structured/   # Designer output
    ├── full_text/
    ├── datamining/
    └── multimodal/
```

**`raw/{doc_id}/`** — `{doc_id}` is a five-digit zero-padded id (e.g. `00001`). Expect the PDF, `state.json`, parser output such as `{doc_id}.md`, `{doc_id}_content_list.json`, layout PDFs, and `images/{sha256}.jpg`. **`{doc_id}_content_list.json` is the primary handoff artefact**; images are keyed by hash and referenced from list items.

**`processed/`** — `processing_report.json` plus per-document cleaned `*_content_list.json` and usually **mirrored** `images/`. If a legacy layout omits mirrored images, multimodal may read from `raw/`; end-to-end runs today assume lists and images are both available under `processed/` for Designer.

**`structured/`** — delivery subtree; shapes below.

**Full-text**

```text
data/structured/full_text/{doc_id}/
├── {doc_id}_structured.json
└── {doc_id}_structured.txt
```

JSON pairs tagged `content` with `pure_text_stream`; `.txt` mirrors the tag-free stream.

**Datamining**

```text
data/structured/datamining/{doc_id}/
└── {doc_id}_datamining.json
```

Section-organised JSON (optional formula, chemistry, asset-ref fields) for retrieval and graph-style work.

**Multimodal**

```text
data/structured/multimodal/{doc_id}/
├── {doc_id}_index.json
├── fig_{n}.md
└── assets/fig_{n}.jpg
```

Index links figures to captions, mentions, layout metadata, and files under `assets/`.

## Naming conventions

| Item | Rule | Example |
|------|------|---------|
| `doc_id` | five-digit numeric | `00001` |
| Raw list | `{doc_id}_content_list.json` | `00001_content_list.json` |
| Raw image | SHA-256 + `.jpg` | `07922a29…35e.jpg` |
| Full-text | `{doc_id}_structured.{json,txt}` | `00001_structured.json` |
| Datamining | `{doc_id}_datamining.json` | `00001_datamining.json` |
| Multimodal index | `{doc_id}_index.json` | `00001_index.json` |
| Figure card / asset | `fig_{n}.md`, `assets/fig_{n}.jpg` | `fig_1.md`, `assets/fig_1.jpg` |

**Onboarding** — allocate the next `doc_id`, populate `raw/{doc_id}/`, run Processor and confirm `processing_report.json` and `processed/{doc_id}/`, run Designer and verify all three `structured/` subtrees; **never rename** `doc_id` mid-pipeline.

**See also:** [End-to-End Workflow](../get_started/end-to-end-workflow.md) · [Processor](../processor/index.md) · [Designer](../designer/index.md) · [Delivery standards](../designer/delivery-standards.md) · [Glossary](../community/glossary.md)
