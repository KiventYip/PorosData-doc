# PorosData-Processor

## Positioning

`Processor` is the PorosData module responsible for **data quality delivery**. Its goal is not to generate final database schemas or knowledge graphs. Instead, it transforms raw OCR, MinerU, and PDF parsing outputs into **clean, stable, readable, and computable** text, so that `Designer` receives low-noise, low-ambiguity input.

In short:

- `Processor` answers whether data is clean, reliable, and ready for further use
- `Designer` answers how that data should be modeled, extracted, mapped, and organized into structured outputs

## What Processor Must Deliver

At a minimum, `Processor` must:

- Remove non-semantic OCR noise, spacing errors, fragments, typos, and formatting artifacts
- Preserve the stability of material names, physical quantities, units, terminology, formulas, and citation structures
- Protect contextual anchors so cleaning does not break conditions, attribute ownership, or semantic relations
- Output text that is suitable for AI consumption, rule-based matching, and downstream extraction

Typical delivery targets include, but are not limited to:

- Main body `text`
- Figure captions and figure footnotes: `image_caption`, `image_footnote`
- Table captions and table footnotes: `table_caption`, `table_footnote`
- Text fragments containing inline formulas
- Any text field that will later enter entity or attribute extraction

## What "Ready" Means

### AI-Ready

AI-Ready means the text is clean enough to be fed directly into LLMs or embedding models without major degradation from broken spacing, garbage symbols, or term corruption.

Core properties include:

- The text is clean enough that the token stream is not polluted by non-semantic fragments
- The semantic subject remains clear and is not broken by OCR fragmentation
- Numbers, units, terms, and inline formulas remain readable
- Cleaning does not introduce new ambiguity

### Data Mining Ready

Data Mining Ready means the text is suitable as input for structured extraction.

Core properties include:

- Entity names remain stable, with material names and terms kept consistent within a document
- Numbers, units, and attributes can be reliably recognized by rules or models
- Relations among values, conditions, and context are preserved
- The text can be transformed further into JSON, tables, knowledge graphs, or triples

## Data Quality Delivery Requirements

### 1. Text Continuity

OCR-induced non-semantic fragmentation must be repaired, including but not limited to:

- Internal spaces inside numbers: `2 0 0` -> `200`
- Broken decimal points: `0 . 5` -> `0.5`
- Broken values and units: `0 . 0 1 0 n m` -> `0.010nm`
- Fragmented element symbols: `N i` -> `Ni`
- Non-semantic line-break fragmentation: `110 \n s` -> `110s`

### 2. Entity Clarity

The following classes must be explicitly protected and corrected when necessary:

- Material names
- Chemical elements and compounds
- Physical quantity names
- Experimental methods and instrument names
- Domain terminology

Within a single document, the same term should not appear in obviously divergent forms that harm search, clustering, or recognition, such as `Zr based`, `Zr-based`, and `Zr based BMG`. When the semantics are identical, `Processor` should normalize them toward a more consistent form.

### 3. Numerical and Unit Clarity

Numbers and units must satisfy these requirements:

- Numerical sequences must remain continuous
- Decimal structures must remain intact
- Exponents, subscripts, superscripts, and symbols should remain structurally correct
- Units must follow a unified project convention

### 4. Formula and Symbol Protection

`Processor` may remove OCR-generated redundant spaces inside formulas, but repairs must always obey structural safety:

- Inline formulas must keep their structure intact
- Display formulas must keep block-level integrity intact
- Subscripts, superscripts, Greek letters, citation commands, and LaTeX command boundaries must be protected
- Complex formulas should not be aggressively rewritten when structural safety cannot be guaranteed

### 5. Citation and Reference Stability

Citation normalization is part of data quality delivery, not an optional extra.

- Numeric citations should be normalized into stable forms such as `ref[1]`, `ref[2][3]`, and `ref[1][2][3]`
- Mixed forms such as `[1]`, `[2,3]`, `[1-3]`, and `[1, 2, 5-7]` should be normalized into one protocol
- Normalized citations must not stick to neighboring words and create dirty outputs such as `wordref[1]`
- Reference list entries at the end of the document must preserve their original structure, such as `[1] Author. Title...`
- Roman numeral or non-numeric references should only receive bracket and spacing normalization, not forced rewriting into `ref[...]`

### 6. Metadata Fields Are Also in Scope

Figure captions, footnotes, table titles, and table footnotes are not optional side fields. They are part of the quality delivery scope because they often contain:

- Figure or table identifiers
- Material names
- Experimental conditions
- Numbers and units
- Inline formulas
- Critical context for downstream structured extraction

## Cleaning Standards

| Dimension | Requirement | Bad | Good |
|------|----------|----------------|-----------------|
| Physical value aggregation | Remove non-semantic spaces among numbers, decimal points, and units | `0 . 0 1 0 n m` | `0.010nm` |
| Chemical entity repair | Fix fragmented element symbols with domain dictionaries | `Z \mathbf{r}`, `N i -` | `Zr`, `Ni` |
| Numerical continuity | Remove OCR-induced breaks inside numbers | `110 \n s` | `110s` |
| Terminology consistency | Keep equivalent entities in a document as consistent as possible | `Zr based`, `Zr-based` | `Zr-based` |
| Citation cleanliness | Normalize numeric citations and keep them separated from text | `1960 [1]`, `[2,3]`, `[1-3]` | `1960 ref[1]`, `ref[2][3]`, `ref[1][2][3]` |
| Metadata clarity | Figure/table metadata should not preserve obvious OCR fractures | `Fig. 1. 1 0 n m` | `Fig. 1. 10nm` |

## Symbol and Unit Protocol

### Unit Alignment Principles

- Use one consistent `Value + Unit` convention across the project, whether with no space or a single space
- Unit spellings must remain stable, such as `mm`, `nm`, `°C`, `s`, `min`, and `keV`
- Compound units, exponential units, and formula-embedded units must preserve structure before any spacing repair

### Symbol Protection Principles

The cleaning process must protect:

- LaTeX inline formulas
- LaTeX display formulas
- Subscripts and superscripts
- Greek letters
- Citation commands and reference structures
- Whitelisted chemical elements and units

## Preconditions for Designer

Before data is handed off to `Designer`, `Processor` output should already ensure:

- Entity names, experiment names, and key terms remain highly consistent within a document
- Contextual anchors such as temperature ranges, environments, and conditions are preserved
- Attributes remain close to their values and units, such as `diameter = 3mm`
- Large amounts of broken numbers, abnormal spacing, inconsistent terms, and damaged formulas are no longer present
- In-text citations and reference-list entries can be reliably distinguished

## Non-Negotiable Failures

The following are unacceptable regressions:

- Rewriting material names, physical quantities, or domain terms into wrong words
- Breaking formulas, subscript/superscript structures, or LaTeX boundaries
- Damaging identifiers in captions, titles, or footnotes
- Deleting key connective text between attributes and conditions
- Accidentally deleting reference list items
- Rewriting reference list items into `ref[...]`
- Incorrectly concatenating normalized citations with neighboring text, such as `wordref[1]`
- Introducing new ambiguous spellings or new OCR noise
- Cleaning only the body text while ignoring critical metadata fields

## Acceptance Criteria

### Delivery Acceptance

At minimum, accepted output should satisfy:

- No obvious OCR-broken numbers
- No obvious broken units
- No obvious fragmented terminology
- No structural formula corruption
- No important metadata fields left outside the cleaning scope
- Numeric citations in body text, captions, titles, and footnotes are normalized into `ref[n]` / `ref[n][m]...`
- Normalized citations do not stick to surrounding text, and reference lists remain in `[n] ...` form
- The text is ready for AI reading and rule-based processing

### Entry Criteria for Designer

Data should enter `Designer` only when:

- Basic quality cleaning is complete
- Numbers, units, and entities are stably recognizable
- Key fields such as captions, titles, and footnotes are usable
- Remaining noise no longer significantly disrupts structured extraction
- Citation structure is already stable

### Rejection Criteria

Any of the following should cause rejection:

- `Processor` output still contains large amounts of visible OCR fragmentation
- Formulas, symbols, or identifiers are structurally damaged
- Important metadata fields such as captions or footnotes are missing from the cleaning scope
- The data is readable but still not stable enough for extraction
- Numeric citations still mix incompatible formats instead of one unified protocol
- The reference list has been mistakenly rewritten, or opening body citations are misclassified as bibliography items
- Similar problems are treated inconsistently across different fields

## Technical Path

This page constrains **output quality**, not a single implementation strategy. Acceptable implementation paths may include:

- Regular-expression rules
- Terminology dictionaries and whitelists
- Structural protection and local repair
- OCR post-processing strategies
- Lightweight models or semantic assistance

Regardless of implementation, the end goals remain:

- `Processor` is responsible for data quality delivery
- `Designer` is responsible for structured expression
- The two packages stay separated in responsibility while the quality chain remains closed