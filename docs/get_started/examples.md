# Examples

Copyable starting points for common delivery scenarios. Each block states **when it applies**, gives a **minimal command**, sketches **layout**, notes **expected artefacts**, and lists **first checks** if something fails.
{: .lead}

After you complete [Quick Start](quickstart.md), the scenarios below add **batch sizing**, Designer-side validation hooks, and explicit ties to the export contract in [Delivery standards](../designer/delivery-standards.md); they assume you are already comfortable with the single-`doc_id` layout.

## Example 1: Single-document trial

**When to use** — you need a first-pass quality check on one paper before scaling a batch.

**Command**

```bash
python -m porosdata_processor run \
  --input-dir data/raw \
  --output-dir data/processed \
  --max-workers 1
```

**Input layout**

```text
data/
└── raw/
    └── 00001/
        ├── 00001.pdf
        └── ... upstream parser files ...
```

**Expected output**

```text
data/
└── processed/
    ├── processing_report.json
    └── 00001/
        └── ... cleaned intermediates ...
```

**You should see** — one cleaned bundle per source folder plus a processing report suitable for quick review.

**If it fails** — verify `data/raw` is complete, the process can write to `data/processed`, and logs or `processing_report.json` do not report missing inputs.

## Example 2: Batch processing

**When to use** — many papers must be normalised to a single `processed/` batch before design or handoff.

**Command**

```bash
python -m porosdata_processor run \
  --input-dir data/raw \
  --output-dir data/processed \
  --max-workers 4
```

**Input layout**

```text
data/
└── raw/
    ├── 00001/
    ├── 00002/
    └── 00003/
```

**Expected output**

```text
data/
└── processed/
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
python -m porosdata_processor run \
  --input-dir data/raw \
  --output-dir data/processed \
  --max-workers 4
```

```bash
porosdata-designer run all --input_dir data/processed
```

**Input layout**

```text
data/
├── raw/
└── processed/
```

**Expected output**

```text
data/
└── structured/
    ├── full_text/
    ├── datamining/
    └── multimodal/
```

**Deliverables** — full-text views, plain streams where configured, structured JSON for mining, multimodal indexes, and traceability-oriented reports.

**If it fails** — confirm `processed/` is complete before invoking the designer; inspect whether `structured/` subtrees exist; resolve any quality flags in processor output before treating the package as final.

## Fine-tuning formats: orientation

There is **no single canonical** fine-tuning file format. Layouts differ with model family (encoder-only, causal decoder, encoder–decoder), task shape (single-turn chat, tool use, classification), training-framework habits, and the templates that surround a given base checkpoint.

PorosData typically ships **three parallel views per document**. Most training stacks need only a thin adapter—field renaming, chunking, or turn packing—to align with local conventions:

| Need | Suggested PorosData view |
|------|---------------------------|
| Plain pre-training, embeddings, retrieval | `pure_text_stream` in `_structured.json`, or `_structured.txt` |
| Structure-aware long-context training | `content` in `_structured.json` (Poros tags intact) |
| Extraction, KG-style assembly, instruction data prep | `_datamining.json` |
| Multimodal / figure-grounded training | `multimodal/` index plus figure cards and assets |

View contracts are specified in [Delivery standards](../designer/delivery-standards.md). A fuller catalogue of task-specific templates may appear in a later revision of this page.

**Related:** [Installation](installation.md) · [Quick Start](quickstart.md) · [End-to-End Workflow](end-to-end-workflow.md) · [Processor](../processor/index.md) · [Designer](../designer/index.md) · [Home](../index.md)
