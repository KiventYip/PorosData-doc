# Output artefacts

Per-document files under `{output_base}/{doc_id}/`. Names below use `{doc_id}` as a literal prefix (for example `00001.content.json`).
{: .lead}

## `{doc_id}.content.json`

Structured **text** view: line-oriented arrays produced after aggregation and mapping.

| Field | Type | Required | Meaning |
|-------|------|----------|---------|
| `doc_id` | string | Yes | Same as directory name and content-list stem |
| `content` | `string[]` | Yes | Structure-aware view: one string per line; joined text includes `<poros_doc>…</poros_doc>` and ends with the configured EOS token (default `</s>` from `TRAINING_CONFIG`) |
| `pure_text_stream` | `string[]` | Yes | Tag-stripped stream for plain-text consumers; chemistry and math handling follows mapper rules |

The pair `content` vs `pure_text_stream` is produced in code by writing aggregated Poros text and the mapper’s `_to_pure_text_stream` output, each split on newlines for stable diffing and streaming I/O.

## `{doc_id}.structure.json`

**Datamining** view: hierarchical JSON. Keys are ordered on write as `doc_id`, optional `title`, optional `abstract`, then `sections`, `formulas`, `chemical_formulas`, `asset_refs`.

Document-level fields:

| Field | Type | Required on write | Notes |
|-------|------|-------------------|--------|
| `doc_id` | string | Yes | Identifier |
| `title` | string | No | Omitted when empty; from title headers or legacy `<poros_title>` handling |
| `abstract` | string | No | Omitted when empty; built from abstract sections with copyright-style noise filtered |
| `sections` | array | Yes | May be an empty list |
| `formulas` | string[] | Yes | Parsed from `<poros_equ>…</poros_equ>`; trailing hyphen / truncation patterns filtered in mapper |
| `chemical_formulas` | string[] | Yes | Parsed from `<poros_chem>…</poros_chem>` with validity filtering |
| `asset_refs` | object[] | Yes | Parsed from `<poros_asset …>` in body text |

Before serialisation, each `asset_refs[]` element receives a **`link`** field:

`images/{type}_{ref}.jpg`  
where `type` defaults to `fig` when missing, and `ref` is the in-text reference token.

### `sections[]` element

| Field | Type | Meaning |
|-------|------|---------|
| `section_type` | string | Normalised section label (for example `introduction`, `results`) |
| `title` | string | Section title; may be empty but the field exists |
| `subtitles` | array | Objects `{ "level": "level2" or "level3", "text": "…" }` |
| `paragraphs` | `string[]` | Paragraph text with inner tags stripped |
| `section_path` | `string[]` | Current implementation uses `[title]` or `[]` |
| `section_index` | int | Zero-based index |
| `total_sections` | int | Count of sections in the document |
| `position_ratio` | float | `round(idx / max(1, total_sections - 1), 3)` between `0.0` and `1.0` |

### `asset_refs[]` element

| Field | Type | Meaning |
|-------|------|---------|
| `uuid` | string | Stable id (for example UUID5 from `doc_id` and key material) |
| `type` | string | `fig` or `table` |
| `ref` | string | Figure or table number token |
| `text` | string | Visible anchor text inside the tag (for example `Fig. 1`) |
| `link` | string | Added at write time; relative path under the document folder |

## `{doc_id}.assets.index.json`

Top-level value is a **JSON array** (not an object). Each item describes one figure (or table image) after interleaving and materialisation.

| Field | Type | Required | Notes |
|-------|------|----------|--------|
| `image_path` | string | After materialisation | Often `images/fig_1.jpg` or a hashed name for long ids (see [Multimodal](multimodal.md)) |
| `fig_id` | string | Yes | Registry key; may be `1`, `1a`, `2.1`, … |
| `caption` | string | Yes | Defaults to `"Figure {fig_id}"` when missing |
| `mentions` | `string[]` | Yes | May be empty; sentence-level hits |
| `metadata` | object | Yes | Includes layout fields such as `page_idx`, `bbox`, caption/footnote text, spatial and semantic anchors |
| `asset_copied` | bool | Yes | `false` until a successful copy |
| `markdown_file` | string | Yes | Sidecar path such as `images/fig_1.md` |

`validate multimodal` enforces a **subset**: each entry must contain `fig_id`, `caption`, and `mentions` (as a list).

## Figure Markdown cards

Sidecars (for example `images/fig_{fig_id}.md`) follow a small template:

- Top-level heading: `# PorosFigure {fig_id}` (prefix derives from `TAG_PREFIX`).
- Image line: `![PorosFigure {fig_id}](relative-path)`.
- `### PorosCaption` plus body text.
- `### PorosMentions in Text` — bullet list, or a single “no mentions” placeholder when empty.
- Trailing HTML comment block with document id, page, figure id, and copy status.

`fig_id` may contain letters or dots; the filename base is not always `fig_{n}` (see [Multimodal](multimodal.md)).

## `{doc_id}.content.txt`

When present, **audit structured** splits this file on `====` boundaries and runs the same structural checks as on the reconstructed text stream. Emitting this file is optional depending on pipeline settings; validators focus on the JSON arrays for `validate structured`.

## Related

- [Poros tags](tags-reference.md) — where `<poros_*>` labels come from  
- [Validation and audit](validation-and-audit.md) — which checks apply to each file  
- [Multimodal](multimodal.md) — path resolution and filename hashing  
