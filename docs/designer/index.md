# PorosData-Designer

`Designer` is the **structured-delivery** module. It consumes **processor-stabilised** input — itself derived from [Parser](../parser/index.md) output via [Processor](../processor/index.md) — and produces the full-text, datamining, and multimodal artefacts teams actually ship. It is **not** a substitute for large-scale OCR cleaning; it assumes major noise has already been addressed.
{: .lead}

Responsibilities include section and paragraph organisation, structured field assembly, text–image linking, and export of the three **core groups** below. A common on-disk layout:

```text
data/structured/
├── full_text/{doc_id}/
├── datamining/{doc_id}/
└── multimodal/{doc_id}/
```

| Group | Primary use | Typical files |
|-------|-------------|---------------|
| Full-text | Reading, review, structure-aware training prep | `_structured.json`, `_structured.txt` |
| Structured (“datamining”) | Extraction, retrieval, storage | `_datamining.json` |
| Multimodal | Figure–text linkage | `_index.json`, `fig_*.md`, `assets/` |

**`full_text`** carries a tag-rich structural stream and a parallel plain stream; **`datamining`** exposes sections, optional formula and chemistry lists, and asset references; **`multimodal`** supplies an index, per-figure cards, and renamed assets aligned with in-text mentions.

**Upstream expectations** — numerics, units, terms, and material names should already be consistent; captions, table titles, and footnotes usable; figure references not broken earlier in the chain.

**Design rules** — structure must **serve delivery**, not only mimic print layout; section hierarchy should stay stable within a document; assets must remain traceable to source context; one package should simultaneously support reading, extraction, and review.

## Package entry points and stage inputs

| Entry | When |
|-------|------|
| `porosdata-designer` | Installed CLI (preferred in production) |
| `python -m porosdata_designer` | Module mode when console scripts are absent |
| `python examples/run_pipeline.py` | Dev wrapper from a source checkout |

Internally: CLI dispatch, runtime orchestration (`run all | text | multimodal`, `audit`, `validate`), reorganisers, schema/LaTeX validators, asset and datamining mappers.

| Command | Reads from | Rationale |
|---------|--------------|-----------|
| `run all` | `data/processed/` | Text + multimodal paths both expect cleaned lists |
| `run text` | `data/processed/` | Built on cleaned `*_content_list.json` |
| `run multimodal` | `data/raw/` | Preserves original asset paths from the parser |

If `processed/` mirrors images, multimodal may also run from that layer; when uncertain, follow [Dataset layout](../parser/dataset-layout.md).

## Commands and server operations

```bash
porosdata-designer run all --input_dir data/processed
porosdata-designer run text --input_dir data/processed
porosdata-designer run multimodal --input_dir data/raw

porosdata-designer audit structured
porosdata-designer validate structured
porosdata-designer validate multimodal
porosdata-designer validate acceptance
```

Redirect outputs and logs without changing inputs:

```bash
porosdata-designer run all \
  --input_dir /path/to/inputs \
  --output_dir /path/to/results/structured \
  --log_dir /path/to/results/logs
```

**Server-style batches** — use a dedicated venv (`python3 -m venv venv && source venv/bin/activate`) and `pip install -e .` from the package root; run long jobs under `nohup`, `screen`, or `tmux` so SSH drops do not kill work. Default logs live under `logs/` (`run_all_*.log`, `run_text_standardization_*.log`, `validate_*_*.log`) unless `--log_dir` overrides. Verify with `python -c "import porosdata_designer; print('install ok')"` and `python -m porosdata_designer --help`. After a batch, run `audit structured` and the relevant `validate` targets; compare reports to [Delivery standards](delivery-standards.md).

## Full-text output

Normative schema, tagging vocabulary, and section-opening rules are centralised in [Delivery standards](delivery-standards.md). Operationally: `{doc_id}_structured.json` pairs Poros-tagged `content` with tag-free `pure_text_stream`; `{doc_id}_structured.txt` mirrors the plain stream. Treat `content` as the validated structure-aware training view—do not substitute a Markdown strip for that contract.

## Limits and relationship with Processor

`Designer` cannot repair wholesale OCR failure; where semantics are ambiguous it may prefer **usable** exports over **over-labelled** ones; customer-specific schemas may still need a thin mapping layer. Reliability rises and falls with [Processor](../processor/index.md) output—this module is the **organisation and export** layer on top of that gate.
