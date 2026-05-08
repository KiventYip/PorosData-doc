# Dataset layout

File-level contract for the **three-tier** `data/` model: what each directory holds, how `doc_id` is used, and how artefacts line up between stages. For the narrative path from install to handoff, see [End-to-end workflow](../get_started/end-to-end-workflow.md).
{: .lead}

**Top-level shape** — flow is normally **Raw Database → Processed Database → Designed Database** (final delivery):

```text
data/
├── Raw Database/         # Parser bundles, traceability anchor
├── Processed Database/   # Processor output
└── Designed Database/    # Designer output (default name; configurable via --output_dir)
    └── {doc_id}/
```

The default **`Designed Database`** directory name matches `DEFAULT_DESIGNED_OUTPUT_DIR_NAME` in the Designer package. You may point `--output_dir` at any writable root; documentation still refers to this default for clarity.

**`Raw Database/{doc_id}/`** — `{doc_id}` is a five-digit zero-padded id (e.g. `00001`). Expect the PDF, `state.json`, Parser output such as `{doc_id}.md`, `{doc_id}_content_list.json`, layout PDFs, and `images/{sha256}.jpg`. **`{doc_id}_content_list.json` is the primary handoff artefact**; images are keyed by hash and referenced from list items.

**`Processed Database/`** — `processing_report.json` plus per-document cleaned `*_content_list.json` and usually **mirrored** `images/`. Designer discovers lists recursively; point `--input_dir` at **Processed Database** (or any tree that contains the lists you intend to ship). Image paths inside each JSON are resolved **relative to that list file’s directory**.

**Designer output (`Designed Database/` by default)** — one folder per document:

```text
data/Designed Database/{doc_id}/
├── {doc_id}.content.json
├── {doc_id}.structure.json
├── {doc_id}.assets.index.json
├── {doc_id}.content.txt          # optional; used by audit when present
└── images/
    ├── fig_1.jpg                 # or image_{md5prefix}.jpg for long ids
    ├── fig_1.md                  # figure card (naming follows fig_id rules)
    └── …
```

- **`content.json`** — line arrays `content` (Poros-tagged) and `pure_text_stream` (plain).  
- **`structure.json`** — datamining JSON (`sections`, formulas, chemistry, `asset_refs` with `link`).  
- **`assets.index.json`** — JSON **array** of multimodal rows (paths, captions, mentions, metadata).  

See [Designer output artefacts](../designer/output-artifacts.md) for field detail.

## Naming conventions

| Item | Rule | Example |
|------|------|---------|
| `doc_id` | five-digit numeric | `00001` |
| Raw list | `{doc_id}_content_list.json` | `00001_content_list.json` |
| Raw image | SHA-256 + `.jpg` | `07922a29…35e.jpg` |
| Full-text JSON | `{doc_id}.content.json` | `00001.content.json` |
| Datamining JSON | `{doc_id}.structure.json` | `00001.structure.json` |
| Multimodal index | `{doc_id}.assets.index.json` | `00001.assets.index.json` |
| Figure card / sidecar | under `images/`, often `fig_{fig_id}.md` | `images/fig_1.md` |
| Copied asset | under `images/`, `fig_{fig_id}.*` or hashed name | `images/fig_1.jpg` |

**Onboarding** — allocate the next `doc_id`, populate `Raw Database/{doc_id}/`, run Processor and confirm `processing_report.json` and `Processed Database/{doc_id}/`, run Designer and verify the per-`doc_id` folder under the chosen output root; **never rename** `doc_id` mid-pipeline.

**See also:** [End-to-end workflow](../get_started/end-to-end-workflow.md) · [Processor](../processor/index.md) · [Designer](../designer/index.md) · [Delivery standards](../designer/delivery-standards.md) · [Glossary](../community/glossary.md)
