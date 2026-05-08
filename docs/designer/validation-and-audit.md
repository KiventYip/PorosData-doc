# Validation and audit

Commands that prove a Designed Database tree is internally consistent before you hand it to training, storage, or review teams.
{: .lead}

## `audit structured`

**Implementation** — builds a structured audit report, then walks each `doc_id` directory.

**When `{doc_id}.content.txt` exists** — the tool splits segments on `====`, runs `SchemaValidator`, `LaTeXValidator`, EOS checks, root tag presence, counts of `poros_section_*` open/close pairs, duplicate singleton sections, tag-density heuristics (for example `TagDensity` ≤ 25%), and related rules.

**`{doc_id}.content.json`** — requires `doc_id`, `content`, `pure_text_stream`; the plain stream must not contain `poros_*` substrings.

**`{doc_id}.structure.json`** — requires `doc_id`, `title`, `sections` with **non-empty** `sections`, non-empty section titles, no legacy `section_type == "section"`, chemical-formula noise checks, and `formulas` as a list without suspicious truncation patterns.

**Multimodal slice** — index file presence, required fields per entry, files under `images/`, `asset_copied` all `true`, and similar disk-level checks.

**Outputs** — human-readable console summary plus `audit_report.json` at the audit `--root_dir`. Summary counts include `total_docs`, `passed`, `failed`, `warnings`, `docs_passed`, `docs_failed`; each document entry carries `category`, `passed`, `message`, and `details`.

**Exit code** — `0` if `summary.failed == 0`, otherwise `1`.

## `validate structured`

Lightweight JSON checks in `_validate_structured_file`:

- Top-level keys exist.  
- `content` and `pure_text_stream` are **arrays of strings** (not a single concatenated string).  
- Joined `content` ends with `</s>` (or the configured EOS), includes `<poros_doc>`, and must not contain `<br>`.  
- `pure_text_stream` is non-empty after join.

**Gap note** — some docstrings claim `<br>` is stripped during aggregation, but a repository-wide search may show **no** replacement step. If upstream HTML still carries `<br>`, this validator will **fail** until the input or a preprocessing step removes it.

## `validate multimodal`

Ensures each `{doc_id}.assets.index.json` exists and that every element includes **`fig_id`**, **`caption`**, and **`mentions`** (list). Logs caption and mention coverage statistics; stricter than a quick smoke test but lighter than the full structured audit path for assets.

## `validate acceptance`

Randomised sampling: up to **five** documents and up to **three** index entries per document. Intended as a **weak** final gate—failures are rare unless the corpus has no valid multimodal rows.

## `validate delivery`

Calls the same report builder as `audit structured`, then writes `delivery_acceptance_report.json` under the log root. Use it when you want a **named delivery artefact** separate from `audit_report.json`.

## Related

- [CLI reference](cli-reference.md) — flags for each subcommand  
- [Output artefacts](output-artifacts.md) — fields validators expect  
- [Troubleshooting](troubleshooting.md) — how to fix common rejections  
