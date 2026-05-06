# PorosData-Parser

`Parser` is the **extraction** stage of the PorosData pipeline: it turns source PDFs and sidecar assets into reusable text blocks, figures, captions, and light metadata. The stage is optimised for **traceability and re-run**, not for a self-contained delivery package.
{: .lead}

## Current implementation

Work is anchored on **[MinerU](https://github.com/opendatalab/MinerU)** as the upstream PDF/OCR engine. PorosData treats MinerU’s content lists, extracted images, and metadata as the canonical input to the `data/raw/` tier that [PorosData-Processor](../processor/index.md) consumes.

## Roadmap

`PorosData-Parser` is expected to ship as a **packaged CLI** that normalises multiple upstream engines behind one content-list contract, so Processor and Designer never branch on vendor specifics. Until that release, run MinerU (or a compatible engine) and land artefacts under `data/raw/{doc_id}/` exactly as laid out under [Dataset layout](dataset-layout.md).

## What Parser provides

| Output | Description |
|--------|-------------|
| Text blocks | Body paragraphs, headings, captions |
| Figures and assets | Image files aligned with in-text mentions |
| Content lists | `*_content_list.json` with block order and types |
| Light metadata | Document-level fields when the engine exposes them |

## Input–output boundary

- **In** — PDFs and, where relevant, supplementary layout or OCR artefacts.
- **Out** — `*_content_list.json` plus image assets under `data/raw/{doc_id}/`. The bundle stays **engine-shaped**; do not hand-edit it to “fix” downstream issues.
- **Consumer** — [PorosData-Processor](../processor/index.md) reads the list, performs cleaning and repair, and writes `data/processed/`.
- **Contract** — Field-level layout and naming across `raw`, `processed`, and `structured` are defined in [Dataset layout](dataset-layout.md).

## Related

[Dataset layout](dataset-layout.md) · [End-to-End Workflow](../get_started/end-to-end-workflow.md) · [Processor overview](../processor/index.md) · [Designer overview](../designer/index.md)
