# Parser

**Parser** turns scientific PDFs into structured JSON through **[MinerU](https://github.com/opendatalab/MinerU)**, and adds a **web dashboard** plus **SLURM-oriented batch controls** so you can drive extraction and monitor jobs from one place. It is the **extraction** stage: it lands reusable text blocks, figures, captions, and light metadata under the **Raw Database** tree (default layout `data/Raw Database/{doc_id}/`; legacy layouts may use a lowercase `raw/` segment), optimised for **traceability and re-run**, not for a self-contained delivery package.
{: .lead}

## Naming in this manual

The reference implementation lives in the **`gen-sci-data`** source repository; this manual names the stage **Parser** so it lines up with **Processor** and **Designer** in navigation.

## Relationship to Processor

Work is anchored on MinerU as the upstream PDF/OCR engine. Parser treats MinerU’s content lists, extracted images, and metadata as the canonical input to the **Raw Database** that [Processor](../processor/index.md) consumes.

## Roadmap

Parser is expected to ship as a **packaged CLI** that normalises multiple upstream engines behind one content-list contract, so Processor and Designer never branch on vendor specifics. Until that release, run MinerU (or a compatible engine) and land artefacts under the Raw Database path layout in [Dataset layout](dataset-layout.md).

## What Parser provides

| Output | Description |
|--------|-------------|
| Text blocks | Body paragraphs, headings, captions |
| Figures and assets | Image files aligned with in-text mentions |
| Content lists | `*_content_list.json` with block order and types |
| Light metadata | Document-level fields when the engine exposes them |

## Input–output boundary

- **In** — PDFs and, where relevant, supplementary layout or OCR artefacts.
- **Out** — `*_content_list.json` plus image assets under `data/Raw Database/{doc_id}/` (or your configured raw root). The bundle stays **engine-shaped**; do not hand-edit it to “fix” downstream issues.
- **Consumer** — [Processor](../processor/index.md) reads the list, performs cleaning and repair, and writes **Processed Database** (default root `data/Processed Database/`).
- **Contract** — Field-level layout and naming across **Raw Database**, **Processed Database**, and **Designed Database** are defined in [Dataset layout](dataset-layout.md).

## Checkout and commands

The reference web app and dashboard in **`gen-sci-data`** may use their own product naming. **UVicorn invocations, CLI script names, and environment layout** are maintained in that repository’s README so this manual stays aligned with whatever that tree ships.

## Related

[Dataset layout](dataset-layout.md) · [End-to-end workflow](../get_started/end-to-end-workflow.md) · [Processor overview](../processor/index.md) · [Designer overview](../designer/index.md)
