# Processor

`Processor` is the **quality-preparation** stage: it does not emit the final structured package, but it turns [Parser](../parser/index.md) output in the **Raw Database** into **cleaner, more stable** intermediates in the **Processed Database** that downstream tooling can trust. In the delivery chain, it answers whether content is **fit to proceed**; [Designer](../designer/index.md) answers how that content should be **organised for handoff**.
{: .lead}

It is aimed at recurring extraction-stage failure modes: OCR noise, irregular spacing, corrupted terms and units, damaged chemistry or formulas, noisy captions and footnotes, and unstable citation boundaries. **Inputs** are body blocks, captions, table titles, image metadata, and upstream `*_content_list.json`. **Outputs** land under the configured output root (CLI default `data/Processed Database`)—cleaned lists, mirrored images when configured, `processing_report.json`, and review-oriented signals. When a run succeeds, numerics and formula boundaries read more clearly, entities stay more stable, and body, caption, and footnote fields are safer to export.

**Operational detail:** [CLI reference](cli-reference.md) lists entry points, flags, and exit codes; [Configuration and runtime](configuration-and-runtime.md) covers `Config`, environment variables, batch limits, and the default pipeline order.

## Typical repairs

| Type | Example problem | Target |
|------|-----------------|--------|
| Numerical repair | `0 . 0 1 0 n m` | `0.010nm` |
| Element repair | `N i` | `Ni` |
| Line-break repair | `110 \n s` | `110s` |
| Term normalisation | `Zr based` / `Zr-based` | one stable in-document form |
| Citation normalisation | `[2,3]`, `[1-3]` | one stable protocol |

## Runtime characteristics

Linux is the preferred host for long batch jobs. Python 3.8 or newer is required, and **no GPU** is expected. Fast storage (SSD or NVMe) materially helps I/O-heavy passes. As a rough guide: small validation sets often fit ~4 vCPU / 16 GB RAM; routine batches ~8 vCPU / 32 GB RAM; large sustained jobs ~16 vCPU / 64 GB RAM. Keep default concurrency conservative, enable evaluation or audit tooling deliberately, and lower worker counts when individual documents are very large. Throughput is **CPU-bound** and sensitive to formula density, worker count, optional evaluators, and the host OS; steady logs together with a moving `processing_report.json` usually indicate a healthy run, even when a handful of files lag.

## Internal architecture

Each text block follows a **fixed** pipeline:

```text
input text
  -> pre-shield processing
  -> Shield.protect          (LaTeX, code, citations → placeholders)
  -> Pipeline.execute        (ordered plugins on protected text)
  -> Shield.restore
  -> post-shield processing
  -> quality-ready text
```

**Shield** isolates math, code, and citations so destructive rules never see protected spans. **Pipeline** resolves an ordered plugin list (normalisation, OCR repair, terms, patterns, citations, numbering, Greek→LaTeX, whitespace, etc.). **DataSentinel** (audit-style) can check structural conservation, compression ratios, and quarantine suspicious files. The stage order and module skeleton are **frozen**; new behaviour arrives through **declarative rules** and registered steps—see [Data governance](data-governance.md).

## Batch execution: streaming and workers

**Streaming JSON** kicks in above a size threshold when `ijson` is installed, so large `*_content_list.json` files avoid a single `json.load`. **Multiprocessing** caps workers from CPU and free memory, applies per-file and overall timeouts, and downgrades risky blocks through an isolated subprocess path. Tokenisers and `TextCleaner` instances are cached per process. Numbers, defaults, and fallback order are summarised in [Configuration and runtime](configuration-and-runtime.md).

## Formula space repair

OCR often injects spurious spaces inside LaTeX. The implementation names only an **aggressive** region (e.g. `\mathrm`, `\mathbf`, `\mathsf`, `\mathit`, `\boldsymbol`, `\ce`, `\unit` brace arguments) for recursive collapse; other spans still receive structural normalisation, selective semantic folding, and numeric fixes, but without that inner aggressive pass. Work proceeds in phases—structure first, then guarded collapse, then numeric cleanup—with iteration caps, explicit protection for `\cite`, `\ref`, `\label`, `\text`, and spacing commands, and **rollback** when validation fails. The passes aim for stability on real inputs but are **not** a formal fixed point when limits trip.

## Token evaluation (optional)

Audits may compare token counts before and after cleaning. For large corpora, cost is dominated by **tokenizer calls**; recommended practice is **sampled** encoding with explicit sample metadata, **batched** calls (e.g. 32–64 items), and optional **character-level** estimators for coarse dashboards. Routine delivery leaves evaluation off; sampled runs feed the governance loop in [Data governance](data-governance.md).

## Quality loop, limits, and handoff to Designer

Real projects iterate: batch → inspect suspicious patterns → adjust rules or config → re-batch until outputs meet the gate. `Processor` **does not** define final business schemas or replace domain field design; on pathological math it prefers **structural safety** to aggressive rewriting. The more trustworthy the **Processed Database** is, the more reliable [Designer](../designer/index.md) becomes—treat this stage as the **quality gate**, not the terminal product layer.
