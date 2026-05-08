# Configuration and runtime

Runtime behaviour matches **porosdata-processor 0.4.1**. There is **no** checked-in `processing_config.yaml` or `token_config.yaml`; behaviour comes from Python types, environment variables, and CLI flags.
{: .lead}

## Where settings live

- **`Config` dataclass** — encoding, chunk sizes, extensions, Unicode form, `default_pipeline`, `debug_mode`, and related fields.
- **`RuntimeConfig` / paths** — environment variables: `POROS_QUARANTINE_PATH`, `POROS_LOGS_PATH`, `POROS_TEMP_DATA_PATH`, `POROS_CACHE_PATH`.
- **`DataProcessor` constructor** — input/output directories, worker count, memory limit, evaluation switches, and related batch controls.
- **`configure_runtime_env`** — optional Hugging Face client defaults such as `HF_ENDPOINT`, `HF_HUB_TIMEOUT`, `HF_HUB_DISABLE_TELEMETRY`.

## `Config` fields (schema-level summary)

| Field | Default | Role |
|-------|---------|------|
| `encoding` | `utf-8` | Text decoding |
| `chunk_size` | `4096` | Read chunk (bytes) |
| `max_file_size` | `100 * 1024 * 1024` | Per-file ceiling (bytes) |
| `supported_extensions` | `{.txt,.md,.tex,.latex,.json}` | Accepted suffixes |
| `unicode_normalization_form` | `NFC` | `unicodedata.normalize` target |
| `regex_precompilation` | `True` | Regex precompilation toggle |
| `debug_mode` | `False` | Per-step debug logging in `Pipeline` |
| `default_pipeline` | ordered list in code | Default cleaning step names |

Authoritative TOML rule-pack fields live with the package in `docs/rules/rule_pack_schema.md` (`schema`, `version`, `defaults`, per-rule `id`, `priority`, `pattern`, optional `kind`, `phase`, `target`, replacements, flags, and metadata).

## Pipeline and rule packs

- The cleaner resolves **step names** to **callables** on the `Pipeline` object (`globals().get(name)` or an instance method)—there is no separate plugin registry file.
- Declarative packs apply through helpers such as `apply_rule_pack` / `get_filtered_transform_rules`, filtered by `kind`, `phase`, `target`, and related columns.
- **Pre-shield extras** — `local_text_compression` runs before `Shield.protect` so raw `$...$` stays available.
- **Post-shield extras** — `citation_to_ref` and `term_consistency_mapping` also have post-shield passes where the implementation needs restored text.

Default ordered steps (1-based) follow `Config.default_pipeline`:

| # | Step | Role |
|---|------|------|
| 1 | `unicode_normalization` | NFC normalisation |
| 2 | `scientific_ocr_repair` | Science OCR repairs (`repair_ocr.toml` and friends); skipped when `apply_heavy_ocr_repair=False` |
| 3 | `term_consistency_mapping` | Terminology mapping (`normalize_terms.toml`, priorities P0–P2) |
| 4 | `patterns_cleaning` | Pattern passes plus full-width digit/letter folding |
| 5 | `metadata_signal_cleanup` | Metadata cleanup (`normalize_metadata.toml`) |
| 6 | `reference_symbol_cleanup` | Citation symbol hygiene |
| 7 | `citation_rules` | Inline citation rules (`normalize_citations.toml`) |
| 8 | `citation_to_ref` | Prose citation protocol (`ref[…]` when configured) |
| 9 | `document_numbering_rules` | Numbering and circled numerals |
| 10 | `greek_to_latex` | Greek Unicode → LaTeX macros |
| 11 | `normalize_whitespace` | Tabs and trailing spaces |
| 12 | `remove_extra_spaces` | Collapse repeated interior spaces |

Other callables (for example `inline_citation_removal`) exist for **custom** `pipeline=` lists.

## Shield coverage

`Shield.protect` wraps, in order: fenced Markdown code; inline code; LaTeX environments; display math (`$$…$$`, `\[…\]`, `\(…\)`); inline math `$…$` with `$$` disambiguation; and common `\cmd{…}` / `\cmd[…]` / `\cmd` forms. Citations are **not** a separate shield class—they are handled inside the pipeline and post-shield logic.

Placeholders use internal boundary prefixes/suffixes; `restore` walks placeholders **in reverse** with single-shot `replace`. Each `clean()` ends with `clear()` so workers can reuse one `Shield` instance safely.

## `TextCleaner` (high level)

Constructor parameters include `pipeline`, `config`, `sentinel`, `strict_mode`, and `apply_heavy_ocr_repair` (when `False`, the heavy pre-shield OCR chain is skipped, including streaming shortcuts).

- **`clean(text)`** — `None` becomes `""`; non-`str` input raises `TypeError`. The codebase does **not** ship documented `ProcessingError` / `ConfigurationError` types.
- **`clean_stream(iterable, chunk_size=8192)`** — lightweight chunk cleaning **without** cross-chunk shielding; treat it as a narrow tool, not a drop-in for full documents.
- **`clean_file`** — removed; read bytes yourself, then call `clean`.
- **Class method `with_quality_assurance(...)`** — builds an instance wired to `DataSentinel` (thresholds, quarantine path, strictness).
- **Pipeline errors** — unknown steps raise `ValueError`; `strict_mode=True` with a triggered sentinel may raise `RuntimeError` (“Quality circuit breaker…”). Non-strict failures roll back the failing step to its input and log a warning.

In batch mode, `Pipeline.audit_processing_result` currently passes `shield_instance=None`, so sentinel branches that expect a live `Shield` for integrity stats **do not run** even when a sentinel is attached.

## Batch I/O and limits

- **Large JSON** — files above `256 * 1024` bytes use **`ijson`** streaming when available; otherwise the loader falls back to `json.load` (install the `[batch]` extra if streaming matters).
- **Atomic writes** — outputs are written to `*.tmp` and renamed into place.
- **Worker count** — when unset, the runtime picks `min(cpu_count, floor(available_memory_mb / 512), 32)`.
- **Timeouts** — per-file default `600` s; overall budget scales with file count. Plain text blocks use `45` s without evaluation and `90` s with evaluation. Streamed JSON items call workers with `enable_evaluation=False`; metrics still flow through `MetricsEngine.consume_block` in-process. **High-risk** blocks (length ≥ 1200 or markers such as `$$`, `\begin{`, `\cfrac`) run isolated with a `120` s cap; on timeout the worker tries a light fallback, then the **original** text if that fails.
- **Memory** — RSS is tracked with `psutil` when present; crossing `memory_limit_mb` emits GC guidance rather than killing workers.

## `processing_report.json` and statuses

Per-file states include `processing` (initial), `success`, `skipped` (fresh output without `--force-reprocess`), and `error` (missing inputs, stream failures, timeouts, or hard exceptions).

When something fails, the runtime often **keeps the original text** (subprocess timeout path, direct-clean retry path, streamed-item fallback). Non-strict pipeline steps roll back to the previous step’s output; sentinel rollbacks can return the untouched source string.

## Formula repair (naming)

Only an **aggressive** region (e.g. `\mathrm`, `\mathbf`, `\mathsf`, `\mathit`, `\boldsymbol`, `\ce`, `\unit` brace arguments) runs the recursive collapse helper. The sources do **not** use a “Zone-O” label—treat everything else as more conservative structural and numeric passes. Iteration caps mean repairs are **not** a formal mathematical fixed point in pathological cases.

**See also:** [CLI reference](cli-reference.md) · [Processor overview](index.md) · [Data governance](data-governance.md)
