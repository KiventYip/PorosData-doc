# Poros tags

Tag vocabulary emitted by the text aggregator and consumed by validators and the datamining mapper. Unless noted, names use the configured prefix (**`poros_`** by default).
{: .lead}

## Root and document shell

| Tag | Role | Children | Attributes |
|-----|------|----------|--------------|
| `poros_doc` | Document root | Sections, keywords, paragraphs, inline content | None |

`SchemaValidator` checks that opening and closing `poros_doc` markers exist for the full serialised document string.

## Sections and titles

Sections use paired tags:

`<poros_section_{type}>…</poros_section_{type}>`

Inside a section, a title uses:

`<poros_title_{type}>…</poros_title_{type}>`

Body text is split into:

`<poros_paragraph>…</poros_paragraph>`

### Section `type` vocabulary

First-class section types are derived from heading patterns (non-exhaustive list aligned with the classifier):

`highlights`, `graphical_abstract`, `article_info`, `keywords`, `abstract`, `introduction`, `theory`, `experimental`, `results`, `discussion`, `conclusion`, `author_info`, `acknowledgements`, `funding`, `conflict_of_interest`, `declaration`, `ethics`, `data_availability`, `supplementary`, `appendix`, `notes`, `abbreviations`, `nomenclature`, `references`.

**Fallbacks**

- `header` — first top heading that does not match a known pattern is downgraded here.  
- `other` — generic bucket when no better label applies (`FALLBACK_SECTION_TYPE` in code paths).

### Subtitles (same section)

`<poros_subtitle_level2>…</poros_subtitle_level2>`  
`<poros_subtitle_level3>…</poros_subtitle_level3>`

Subtitles do **not** open a new `poros_section_*`; they nest inside the current section.

## Standalone blocks

| Tag | Role |
|-----|------|
| `poros_keywords` | Keyword list block (logical child of `poros_doc`) |

## Paragraph and inline entities

| Tag | Typical parent | Role |
|-----|----------------|------|
| `poros_paragraph` | `poros_section_*` | Paragraph wrapper |
| `poros_chem` | Inside paragraphs | Chemistry / alloy notation; may appear as `$…$` |
| `poros_equ` | Inside paragraphs | Mathematics; `$$…$$` or `$…$` |
| `poros_asset` | Inside paragraphs | Figure/table anchor |

`poros_asset` carries attributes **`uuid`**, **`type`**, **`ref`** so downstream JSON can resolve figures and tables.

## `SchemaValidator.TAG_HIERARCHY`

The validator ships a static parent/child table that still mentions legacy containers (`poros_main_text`, `poros_abstract`, …). **`validate()` does not enforce that table for nesting**; it focuses on document root presence, global open/close stack consistency for every `<poros_*>` tag, and optional math-delimiter parity warnings.

Therefore, **treat the aggregator output as the real contract**, not every edge implied by the hierarchy table alone.

## Training end-of-sequence

After aggregation, training configuration may append an EOS token (default **`</s>`**) when `append_eos` is enabled. The same token must appear at the end of joined `content` lines when `validate structured` runs.

## Closing rules

Every `<poros_*>` opener (including forms with attributes) is pushed on a stack; the matching close tag must pop the same name. Violations surface as schema validation issues (often logged as warnings during `run` when validation does not hard-stop the pipeline).

## Related

- [Output artefacts](output-artifacts.md) — JSON mirrors of these tags  
- [Delivery standards](delivery-standards.md) — readiness language across Processor and Designer  
