# Designer

`Designer` is the **structured-delivery** stage. It reads **processor-stabilised** lists from the **Processed Database** (sourced from [Parser](../parser/index.md) output via [Processor](../processor/index.md)) and writes per-document JSON, plain text where applicable, figure assets, and small Markdown cards into the **Designed Database**. It does **not** replace large-scale OCR repair; it assumes upstream text is already usable.
{: .lead}

## What lands on disk

The reference CLI defaults to a single tree under the project `data/` directory. Each document is one folder named after `doc_id`:

```text
data/Designed Database/{doc_id}/
├── {doc_id}.content.json      # structure-aware lines + plain stream
├── {doc_id}.structure.json    # datamining / section view
├── {doc_id}.assets.index.json # multimodal index (JSON array)
├── {doc_id}.content.txt       # optional plain export; used by audit when present
└── images/                    # copied figures; Markdown sidecars may sit here too
```

Override the base path with `--output_dir` on `run` / `validate` commands, or `--root_dir` on `audit structured` / `validate delivery`. The default directory name `Designed Database` comes from the package config constant `DEFAULT_DESIGNED_OUTPUT_DIR_NAME`.

| View | Primary files | Typical use |
|------|---------------|-------------|
| Full-text (tagged) | `{doc_id}.content.json` → `content` | Structure-aware training, review |
| Plain stream | `pure_text_stream` in the same JSON (and optional `.content.txt`) | Tag-free models and retrieval |
| Datamining | `{doc_id}.structure.json` | Sections, formulas, chemistry, asset refs |
| Multimodal | `{doc_id}.assets.index.json`, `images/*`, `*.md` cards | Figure–text linkage, layout metadata |

**Upstream expectations** — numerics, units, terms, and material names should already be consistent; captions, table titles, and footnotes readable; figure references not broken earlier in the chain.

**Design rules** — structure must **serve delivery**, not only mimic print layout; section typing should stay stable within a document; assets must remain traceable to source context; one pass should support reading, extraction, and review together.

## How runs are wired

| Command | What it runs |
|---------|----------------|
| `designer run all` | Text standardisation, then multimodal extraction |
| `designer run text` | Text path only (`content` / `structure` outputs) |
| `designer run multimodal` | Multimodal path only (expects lists and image paths the extractor can resolve) |

Discovery is driven by `*_content_list.json` anywhere under `--input_dir`; `doc_id` is the file stem with `_content_list` removed (for example `00001_content_list.json` → `00001`).

For exact flags, defaults, exit codes, and logging file patterns, see [CLI reference](cli-reference.md). For field-level contracts, see [Output artefacts](output-artifacts.md). Poros tag vocabulary and nesting behaviour are in [Poros tags](tags-reference.md). Operational checks are covered under [Validation and audit](validation-and-audit.md).

## Package entry points

| Entry | Notes |
|-------|--------|
| `designer` | Console script → `designer.cli:main` (`[project.scripts]` in the package) |
| `python -m designer` | Delegates to the same CLI via `designer/__main__.py` |

Install and import name follow the **`designer`** Python package (not `porosdata_designer`).

## Documentation map

- [Delivery standards](delivery-standards.md) — readiness levels and cross-stage obligations  
- [CLI reference](cli-reference.md) — commands, flags, logs, exit codes  
- [Output artefacts](output-artifacts.md) — JSON and Markdown file contracts  
- [Poros tags](tags-reference.md) — tag set, section vocabulary, EOS  
- [Configuration](configuration.md) — code-level defaults (`runtime/config.py`)  
- [Validation and audit](validation-and-audit.md) — `audit` / `validate` subcommands  
- [Multimodal](multimodal.md) — filenames, paths, known edge cases  
- [Python API](python-api.md) — public constructors and helpers  
- [Troubleshooting](troubleshooting.md) — common failures and log messages  

## Limits and relationship with Processor

Designer cannot repair wholesale OCR failure; where semantics stay ambiguous it may prefer **usable** exports over **over-labelled** ones. Quality is **bounded** by [Processor](../processor/index.md) output—this stage is the **organisation and export** layer on top of that gate.
