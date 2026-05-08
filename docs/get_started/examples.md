# Examples

Copyable starting points for common delivery scenarios. Each block states **when it applies**, gives a **minimal command**, sketches **layout**, notes **expected artefacts**, and lists **first checks** if something fails.
{: .lead}

After you complete [Quick Start](quickstart.md), the scenarios below add **batch sizing**, Designer-side validation hooks, and explicit ties to the export contract in [Delivery standards](../designer/delivery-standards.md); they assume you are already comfortable with the single-`doc_id` layout.

## Example 1: Single-document trial

**When to use** — you need a first-pass quality check on one paper before scaling a batch.

**Command**

```bash
porosdata-processor cleaning \
  --input-dir "data/Raw Database" \
  --output-dir "data/Processed Database" \
  --max-workers 1
```

**Input layout**

```text
data/
└── Raw Database/
    └── 00001/
        ├── 00001.pdf
        └── ... Parser / raw-tier files ...
```

**Expected output**

```text
data/
└── Processed Database/
    ├── processing_report.json
    └── 00001/
        └── ... cleaned intermediates ...
```

**You should see** — one cleaned bundle per source folder plus a processing report suitable for quick review.

**If it fails** — verify **Raw Database** is complete, the process can write to **Processed Database**, and logs or `processing_report.json` do not report missing inputs.

## Example 2: Batch processing

**When to use** — many papers must be normalised to a single **Processed Database** batch before design or handoff.

**Command**

```bash
porosdata-processor cleaning \
  --input-dir "data/Raw Database" \
  --output-dir "data/Processed Database" \
  --max-workers 4
```

**Input layout**

```text
data/
└── Raw Database/
    ├── 00001/
    ├── 00002/
    └── 00003/
```

**Expected output**

```text
data/
└── Processed Database/
    ├── processing_report.json
    ├── 00001/
    ├── 00002/
    └── 00003/
```

**You should see** — one processed directory per document and a batch-level report.

**If it fails** — check folder naming consistency, whether `--max-workers` exceeds what the host tolerates, and whether the report marks skipped or failed items.

## Example 3: Review-oriented delivery package

**When to use** — recipients need readable text, structured JSON, and multimodal linkage in one pass.

**Commands**

```bash
porosdata-processor cleaning \
  --input-dir "data/Raw Database" \
  --output-dir "data/Processed Database" \
  --max-workers 4
```

```bash
designer run all --input_dir "data/Processed Database"
```

**Input layout**

```text
data/
├── Raw Database/
└── Processed Database/
```

**Expected output**

```text
data/
└── Designed Database/
    ├── 00001/
    │   ├── 00001.content.json
    │   ├── 00001.structure.json
    │   ├── 00001.assets.index.json
    │   └── images/
    └── 00002/
        └── …
```

**Deliverables** — full-text views, plain streams where configured, structured JSON for mining, multimodal indexes, and traceability-oriented reports.

**If it fails** — confirm **Processed Database** is complete before invoking Designer; inspect whether each `doc_id` folder exists under the output root; resolve any quality flags in Processor output before treating the package as final.

## Fine-tuning formats: orientation

There is **no single canonical** fine-tuning file format. Layouts differ with model family (encoder-only, causal decoder, encoder–decoder), task shape (single-turn chat, tool use, classification), training-framework habits, and the templates that surround a given base checkpoint.

A typical delivery ships **three parallel views per document**. Most training stacks need only a thin adapter—field renaming, chunking, or turn packing—to align with local conventions:

| Need | Suggested view |
|------|----------------|
| Plain pre-training, embeddings, retrieval | `pure_text_stream` in `{doc_id}.content.json`, or optional `{doc_id}.content.txt` |
| Structure-aware long-context training | `content` in `{doc_id}.content.json` (Poros tags intact) |
| Extraction, KG-style assembly, instruction data prep | `{doc_id}.structure.json` |
| Multimodal / figure-grounded training | `{doc_id}.assets.index.json` plus `images/` and Markdown figure cards |

View contracts are specified in [Delivery standards](../designer/delivery-standards.md). A fuller catalogue of task-specific templates may appear in a later revision of this page.

**Related:** [Installation](installation.md) · [Quick Start](quickstart.md) · [End-to-end workflow](end-to-end-workflow.md) · [Processor](../processor/index.md) · [Designer](../designer/index.md) · [Home](../index.md)
