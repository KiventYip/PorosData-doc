# Rule Externalization Plan

## Goal

Move business-rule data out of Python modules into readable rule files, while keeping structural algorithms in code.

## First Principle: Declarative Rules Drive Cleaning Quality

This package serves data cleaning. When cleaning quality needs improvement, the approach is to incrementally add or update TOML rule files — not to modify Python code. Code changes are reserved for structural algorithms that cannot be safely expressed as declarative rules.

## Repository Constraints

The repository follows these development constraints:

1. Keep the pipeline graph fixed for default processing.
2. Externalize rule data into readable files whenever possible.
3. Keep structural and stateful algorithms in code.
4. Maintain a single source of truth for each rule family.
5. Keep step responsibilities narrow and explicit.
6. Preserve the rule-governance workflow: audit -> candidate -> validate -> promote -> gate.
7. Prefer consolidation before adding new abstraction layers.

## Design Boundary

- Keep in files:
  - regex-based normalize/repair/detect rules
  - label mappings
  - numbering mappings
  - Greek mappings
  - formula lexicon tables and whitelists
- Keep in code:
  - Shield lifecycle
  - formula parsing and brace matching
  - display/inline math structural repair
  - rule-pack loading, validation, promotion, and delivery-gate orchestration

## Phase 1 Executed

This change set externalizes three rule domains:

- `rules/normalize_metadata.toml`
  - front-matter labels
  - metadata punctuation cleanup
  - metadata line-break normalization
- `rules/normalize_numbering.toml`
  - chapter/section normalization regexes
  - Roman numeral mapping table
  - circled number mapping table
- `rules/normalize_greek.toml`
  - Unicode Greek to LaTeX mappings
  - variant normalization mappings
  - reverse LaTeX to Unicode mappings

Python modules updated to consume file-backed rule data:

- `steps.py`
- `document_numbering_rules.py`
- `greek_latex_converter.py`

## Phase 2 Executed

This change set externalizes higher-value cleanup domains and shared data tables:

- `rules/formula_lexicon.toml`
  - formula unit tables
  - function tables
  - element symbol tables
  - delta classification tables
- `rules/semantic_latex.toml`
  - pre-shield semantic OCR and LaTeX rewrites
- `rules/post_shield.toml`
  - restored-formula cleanup
  - hyphen-chain finishing rules
  - formula trailing-space cleanup
- `rules/patterns_cleaning.toml`
  - generic text cleanup patterns

Python modules updated to consume these files:

- `text_cleaner.py`
- `steps.py`

## Remaining High-Priority Externalization Targets

### Single-Source Consolidation

- completed: `patterns.py` and `tools.py` now share one canonical pattern catalog backed by `rules/patterns_cleaning.toml`
- completed: legacy compatibility packs are explicitly marked, and canonical ownership is listed in `docs/rules/canonical_rule_pack_matrix.md`

### Pipeline Consolidation

- make the default execution graph observable from a single canonical location
- reduce cross-layer duplication between `config.py`, `text_cleaner.py`, and batch-runtime entrypoints

### Public API Boundaries

- prevent batch/runtime code from depending on private helper functions in step modules
- keep step modules as the only public home for their rule-domain behavior

## Migration Rule

If a behavior can be expressed as:

- pattern
- replacement or detect action
- metadata such as phase / target / priority

then it should not remain hard-coded in Python business logic.

## Exception Rule

The following stay in Python by design:

- Shield lifecycle
- delimiter and brace matching
- display/inline formula structural repair
- reference-block recognition
- bounded iterative normalization passes
- workflow orchestration, validation, and delivery gating

## Verification Rule

Every externalized rule family must ship with:

- unit tests for positive and near-miss cases
- sample validation where candidate workflow applies
- delivery-gate coverage for blocking-quality issues when relevant

## Current Status Snapshot

Against the repository constraints, the current status is:

- `Pipeline fixed`: partially satisfied
- `Rules externalized`: partially satisfied, with major progress completed
- `Algorithms in code`: satisfied
- `Single source of truth`: mostly satisfied; remaining work is retirement of compatibility-only packs
- `Clear step ownership`: partially satisfied
- `Governance workflow`: satisfied in infrastructure, partially satisfied in coverage
- `Consolidate before abstracting`: partially satisfied
