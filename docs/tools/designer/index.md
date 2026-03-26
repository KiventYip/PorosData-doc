# PorosData-Designer

## Positioning

`Designer` is the PorosData module responsible for **structured organization and reconstruction**. It operates on top of text that has already been quality-cleaned by `Processor`, and converts that high-quality input into **structured objects, fields, relations, and deliverables** for training views, data-mining views, and multimodal indexing.

In short:

- `Processor` improves data quality
- `Designer` expresses that data in structured form

`Designer` should not absorb large-scale OCR cleaning work. Its responsibilities center on section reconstruction, field mapping, formula and chemical-form protection, text-image anchoring, and stable export of structured outputs.

## What Designer Must Deliver

Core tasks include, but are not limited to:

- Entity recognition and normalized mapping
- Attribute-value extraction
- Binding of conditions and context
- Structured record generation
- Export to JSON, tables, knowledge graphs, and related target formats

At the current stage, the preferred outputs are divided into three views:

- Structure-aware training view: tagged `content`
- Plain-text training view: cleaned `pure_text_stream`
- Data-mining view: `datamining` results for extraction, retrieval, and storage

## What "Ready" Means

### Structure-Aware Training Ready

This means the training view may retain stable, interpretable, and properly closed structural tags as explicit semantic boundary signals for long-context training.

Key requirements:

- `section`, `title`, and `subtitle` tags should express structure, not mimic layout
- `</poros_section_{type}>` may serve as a strong logical block boundary
- Tags may be used as training signals only when they are stable, semantically consistent, and safely nested

### Plain-Text Training Ready

This means the text can be fed directly into models as natural language without depending on `poros_*` structural tags for interpretation.

Key requirements:

- `pure_text_stream` must not retain XML wrappers or structural control markers
- Formulas, chemical expressions, and figure/table mentions must follow one stable rendering policy across the corpus
- Structure should be conveyed through natural segmentation or agreed plain-text placeholders, not through leaked tags

### Data Mining Ready

This means the structured output is suitable for entity extraction, relation extraction, attribute mapping, and downstream knowledge organization.

Key requirements:

- Entity names remain stable
- Numbers, units, and attributes are reliably identifiable
- Relations between attributes and context are not broken during tagging or export
- The output can be consumed as JSON, tables, knowledge graphs, or index objects

## Output Directories and Artifacts

At this stage, `Designer` delivery is based on **per-view files**, not a single aggregated file.

- `structured/full_text/{doc_id}/`
- `structured/datamining/{doc_id}/`
- `structured/multimodal/{doc_id}/` when enabled

Recommended artifacts include:

- `full_text/{doc_id}_structured.txt`
- `full_text/{doc_id}_structured.json`
- `datamining/{doc_id}_datamining.json`
- `multimodal/{doc_id}_index.json`
- `multimodal/assets/` plus per-figure Markdown files

Among them:

- `structured.txt` is intended for readable inspection
- `structured.json` serves training views and carries `content` and `pure_text_stream`
- `datamining.json` serves structured extraction, retrieval, and storage

## Poros Tags and Hierarchy

Structured text should follow the Poros skeleton contract and use a **coarse-grained, stability-first** tag system.

- The root tags `<poros_doc>` and `</poros_doc>` must be present
- Closing `poros_section_*` tags serve as logical block-end signals
- Stable section classes should be preferred: `header`, `abstract`, `introduction`, `experimental`, `results`, `discussion`, `conclusion`, `acknowledgements`, and `references`
- Semantically unstable blocks should fall back to `poros_section_section`
- Stable top-level titles may use tags such as `poros_title_header`, `poros_title_abstract`, and `poros_title_introduction`
- Unstable sections should use `poros_title_section`
- Subtitle layers should mainly use `poros_subtitle_level2` and `poros_subtitle_level3`
- Inline semantic tags should remain lightweight: `poros_paragraph`, `poros_equ`, `poros_chem`, `poros_asset`, and `poros_keywords`
- Unclosed tags, broken nesting, and illegal child structures are not allowed

## View Contracts and Required Fields

### `full_text/{doc_id}_structured.json`

This file must contain at least:

- `doc_id`
- `content`
- `pure_text_stream`

Where:

- `content` is the fully tagged Poros text for structure-aware training
- `pure_text_stream` is the de-tagged clean text stream for plain-text training, embedding, or indexing

### `datamining/{doc_id}_datamining.json`

This file must contain at least:

- `doc_id`
- `title`
- `sections`

It should also preferably include:

- `formulas`
- `chemical_formulas`
- `asset_refs`

Each item in `sections` should represent section titles, paragraphs, and subtitle hierarchy. When section semantics are unstable, `section_type = "section"` is the correct fallback.

## Formulas, EOS, and Chemical Semantics

Training-readiness and semantic consistency require:

- Inline formula delimiters such as `$...$` must remain balanced
- The document must end with the project EOS token, such as `</s>`
- `</poros_section_{type}>` acts as a block-level boundary signal and does not replace the global EOS
- `datamining.chemical_formulas` should contain only chemical elements, compounds, or stable material formulas
- Ordinary formulas, integrals, thermodynamic expressions, instrument names, and method names must not leak into `chemical_formulas`

## Multimodal Indexing and Asset Consistency

When multimodal outputs are produced, they must satisfy:

- The index file is a JSON array
- Each item contains at least `image_path`, `fig_id`, `caption`, `mentions`, `metadata`, `asset_copied`, and `markdown_file`
- The number of index entries matches the number of copied assets under `assets/`
- If figure-level Markdown files exist, their paths or identifiers must align with physical files

## Structuring Standards

| Dimension | Structuring Requirement | Bad | Good |
|------|------------|----------------|-----------------|
| Poros root tag | Entire content must be wrapped by `<poros_doc>` / `</poros_doc>` | Missing root tag | `<poros_doc>...</poros_doc>` |
| Tag closure | All Poros tags must close correctly and nest safely | Missing or misplaced `</poros_paragraph>` | One-to-one closure with valid nesting |
| Tag granularity | Prefer stable coarse types; unstable blocks fall back to `poros_section_section` | Inventing new tags for `Declaration` and similar blocks | Use the generic `section` container |
| Section semantics | `section/title/subtitle` must stably encode hierarchy | Body text drifting outside section containers | Clear section boundaries |
| EOS ending | Document must end with EOS | No EOS at the end | `...text</s>` |
| `full_text` fields | Must include `doc_id`, `content`, `pure_text_stream` | Missing `pure_text_stream` | All three fields present |
| `datamining` fields | Must include `doc_id`, `title`, `sections` | Missing `sections` | Fields are structurally consumable |
| Plain-text purity | `pure_text_stream` must not retain `poros_*` tags | Structural tags remain | Natural text only |
| Chemical semantics | `chemical_formulas` must not include non-chemical abbreviations or general formulas | Includes `TEM`, `XRD`, etc. | Only chemical elements or compounds |
| Multimodal index | Index items must include the agreed fields | Missing `fig_id` or `asset_copied` | Complete fields aligned with assets |

## Training and Data Mining Readiness

The three `Designer` outputs, `content`, `pure_text_stream`, and `datamining`, must not blur their responsibilities.

### 1. Separation of View Responsibilities

- `content` is for structure-aware training
- `pure_text_stream` is for plain-text training, embedding, indexing, and general language modeling
- `datamining` is for data mining and retrieval

### 2. Entity Integrity

Within `content` and `datamining`, material names, experiment names, and key terms must remain highly consistent inside a document. Aggregation, tagging, or export must not introduce new mixed spellings.

### 3. Contextual Anchors

Experimental conditions, temperature ranges, environments, and preceding or trailing qualifiers must be preserved. They must not be deleted as if they were noise during structuring.

### 4. Attribute-Value Alignment

Measured attributes and their values and units must remain reasonably adjacent inside `content` or `datamining.sections`. Structuring must not separate them in ways that make downstream mapping unreliable.

### 5. Minimal Structured Noise

`pure_text_stream` and `datamining` must not amplify upstream noise such as broken numbers, abnormal spacing, inconsistent terms, damaged formulas, or stray citation artifacts.

## Non-Negotiable Failures

The following are unacceptable regressions:

- Missing the root tag or breaking Poros tag closure and nesting
- Breaking formulas, subscript/superscript structure, or LaTeX delimiter balance
- Missing required `full_text` / `datamining` artifacts or required fields
- Copying structural tags into `pure_text_stream`
- Inventing overly fine-grained tags when semantics are unstable instead of falling back to generic sections
- Mixing non-chemical abbreviations, general formulas, or engineering expressions into `datamining.chemical_formulas`
- Missing the final EOS
- Producing multimodal indexes with missing required fields or mismatched copied assets
- Deleting identifiers or key semantics from captions, table titles, or footnotes during export

## Acceptance Criteria

### Delivery Acceptance

At minimum, accepted `Designer` output should satisfy:

- Poros root tags exist and close correctly with valid nesting
- Inline formula delimiters remain balanced
- The document ends with EOS
- `full_text/{doc_id}_structured.json` contains `doc_id`, `content`, and `pure_text_stream`
- `datamining/{doc_id}_datamining.json` contains at least `doc_id`, `title`, and `sections`
- `content` tags stably represent sections, titles, subtitles, and logical block boundaries
- `pure_text_stream` is truly de-tagged plain text
- `datamining` can represent sections, paragraphs, formulas, chemical formulas, and asset references
- If multimodal artifacts are produced, index fields and asset counts remain consistent

### Rejection Criteria

Any of the following should cause rejection:

- Missing root tags or broken nesting/closure
- Unbalanced formula delimiters or broken LaTeX structure
- Missing EOS or missing required artifacts and fields
- Large amounts of `poros_*` tags remain in `pure_text_stream`
- Section, title, or subtitle boundaries are severely misplaced in `content`
- Tagging remains over-granular even when semantics are unstable
- `datamining.chemical_formulas` contains non-chemical abbreviations, ordinary formulas, or engineering expressions
- The multimodal index is missing fields or assets were not copied correctly

## Technical Path

This page constrains **output quality**, not one implementation style. Valid implementations may include:

- Rule-based Poros tagging and validation
- Split exporters for `content`, `pure_text_stream`, and `datamining`
- Terminology lists and whitelists for chemical formulas and units
- Structural protection and local repair for tags and formulas
- Tag normalization strategies based on "stable coarse classes + generic section fallback"
- Plugin-based pipelines and exporters
- Audit scripts and automated acceptance checks

Regardless of implementation, the end goals remain:

- `Processor` is responsible for data quality delivery
- `Designer` is responsible for structured expression
- The two packages remain separated in responsibility while the quality chain stays closed