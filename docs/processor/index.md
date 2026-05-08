# PorosData-Processor

`Processor` is the **quality-preparation** stage: it does not emit the final structured package, but it turns [Parser](../parser/index.md) output into **cleaner, more stable** intermediates that downstream tooling can trust. In the delivery chain, it answers whether content is **fit to proceed**; [Designer](../designer/index.md) answers how that content should be **organised for handoff**.
{: .lead}

It is aimed at recurring parser failure modes: OCR noise, irregular spacing, corrupted terms and units, damaged chemistry or formulas, noisy captions and footnotes, and unstable citation boundaries. **Inputs** are body blocks, captions, table titles, image metadata, and upstream `*_content_list.json`. **Outputs** are written under `data/processed/`—cleaned lists, mirrored images when configured, `processing_report.json`, and review-oriented signals. When a run succeeds, numerics and formula boundaries read more clearly, entities stay more stable, and body, caption, and footnote fields are safer to export.

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

**Streaming JSON** yields content-list items incrementally so huge files need not load fully into memory (small files may use a fast path). **Multiprocessing** spreads documents across workers with CPU/memory-aware caps and **per-block / per-file timeouts**; on timeout the original text is retained and processing continues. Tokenisers and `TextCleaner` instances are **reused per worker** to amortise setup.

## Formula space repair

OCR often injects spurious spaces inside LaTeX. Repair is **conservative** and **zoned**: an **aggressive** region (e.g. `\mathrm`, `\mathbf`, `\ce`, `\unit`, nested braces) may collapse character-level noise; **Zone-O** (remaining math) follows **fix numbers, not letters** so operator spacing such as `a \ b` survives. Three phases—structural normalisation, semantic collapse (aggressive only, inside-out), numerical fixing—run in order; steps are **idempotent**, and failed validation **rolls back** changes. Citation commands, `~`, binary operators, and `\text{...}` are left untouched.

## Token evaluation (optional)

Audits may compare token counts before and after cleaning. For large corpora, cost is dominated by **tokenizer calls**; recommended practice is **sampled** encoding with explicit sample metadata, **batched** calls (e.g. 32–64 items), and optional **character-level** estimators for coarse dashboards. Routine delivery leaves evaluation off; sampled runs feed the governance loop in [Data governance](data-governance.md).

## Quality loop, limits, and handoff to Designer

Real projects iterate: batch → inspect suspicious patterns → adjust rules or config → re-batch until outputs meet the gate. `Processor` **does not** define final business schemas or replace domain field design; on pathological math it prefers **structural safety** to aggressive rewriting. The more trustworthy `processed/` is, the more reliable [Designer](../designer/index.md) becomes—treat this stage as the **quality gate**, not the terminal product layer.
