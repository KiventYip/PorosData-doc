# End-to-end workflow

This page traces the **delivery path** from literature inputs to packages you can use for training, structured extraction, retrieval, and review. It stays at the level of stages, directories, and what to inspect; exact commands live on the installation and reference pages.
{: .lead}

**Pipeline in one line** — sources land in the **Raw Database** via **Parser**, are stabilised into the **Processed Database** by **Processor**, then shaped into delivery views in the **Designed Database** by **Designer**:

```text
PDF literature -> Parser -> Raw Database -> Processor -> Processed Database -> Designer -> Designed Database
```

| Stage | Primary work | What you get |
|-------|----------------|---------------|
| Parser | Extract blocks, figures, captions, light metadata | **Raw Database**: reusable raw text and image assets |
| Processor | Remove noise, repair fragmentation, normalise expressions | **Processed Database**: intermediate results and batch reports |
| Designer | Organise sections and export views | **Designed Database**: per-`doc_id` folders by default (override with `--output_dir`) |

**Directory contract** — the usual flow is **Raw Database → Processed Database → Designed Database**:

```text
data/
├── Raw Database/         # Parser / upstream extraction packages
├── Processed Database/   # Processor output
└── Designed Database/      # Designer output (default folder name)
    └── {doc_id}/
```

**Raw Database** holds the upstream bundle per document: PDFs, Parser-generated Markdown or lists, page-level intermediates, and extracted images. The layer is for **traceability and re-run**, not for handing off as final product.

**Processed Database** is where Processor writes cleaned `*_content_list.json`, mirrored images where configured, and a batch summary such as `processing_report.json`. Typical repairs address broken numerals and units, corrupted terms, noisy captions or footnotes, and unstable citation or formula boundaries.

**Designed Database** (or your custom `--output_dir`) holds **one subdirectory per `doc_id`** with the JSON views, optional plain text, and an `images/` subtree. Typical files:

```text
data/Designed Database/00001/
├── 00001.content.json
├── 00001.structure.json
├── 00001.assets.index.json
└── images/
```

| Files | Role |
|-------|------|
| `{doc_id}.content.json` | Poros-tagged `content` plus `pure_text_stream` line arrays |
| `{doc_id}.structure.json` | Datamining JSON (`sections`, formulas, asset refs) |
| `{doc_id}.assets.index.json` | Multimodal index (JSON array) and pointers into `images/` |

**What a completed run should provide** — per-document folders under the chosen output root, plain-text streams where configured, structured JSON for mining, multimodal indexes that resolve figure mentions to assets, and reports that support batch review and traceability.

**How to review results efficiently** — (1) confirm **Raw Database** is complete for each `doc_id`, (2) read `processing_report.json` and spot-check **Processed Database** for regressions, (3) open the matching `{doc_id}` folder under **Designed Database** for your downstream task (reading vs mining vs multimodal).

**Typical motivations** — high-quality training text, stable inputs for rule-based or learned extraction, explicit links between body text and figures, and a single package shape for storage or knowledge organisation.

**See also:** [Installation](installation.md) · [Quick Start](quickstart.md) · [Examples](examples.md) · [Parser](../parser/index.md) · [Processor](../processor/index.md) · [Designer](../designer/index.md) · [Dataset layout](../parser/dataset-layout.md)
