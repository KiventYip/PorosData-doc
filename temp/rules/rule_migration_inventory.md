# Rule Migration Inventory

## First Principle: Declarative Rules Drive Cleaning Quality

This package serves data cleaning. When cleaning quality needs improvement, the approach is to incrementally add or update TOML rule files — not to modify Python code. Every item in "Still Hybrid" is a friction point where quality improvement still requires code changes instead of rule updates.

## Status

This inventory tracks which rule domains are already declarative and which remain code-driven.

## Declarative Now

- `src/porosdata_processor/rules/repair_ocr.toml`
  - low-to-medium risk OCR repair rules
  - executed by `scientific_ocr_repair`
- `src/porosdata_processor/rules/normalize_terms.toml`
  - term consistency, alloy names, unit and punctuation normalization
  - executed by `TermConsistencyEngine`
- `src/porosdata_processor/rules/normalize_citations.toml`
  - citation symbol rewrites and citation policy metadata
  - consumed by citation-related steps
- `src/porosdata_processor/rules/detect_audit.toml`
  - audit-only OCR and quality detection patterns
  - consumed by `scripts/audit_aiready_data.py`
- `src/porosdata_processor/rules/detect_delivery.toml`
  - delivery-gate blocking patterns
  - reserved for pre-delivery checks
- `src/porosdata_processor/rules/patterns_cleaning.toml`
  - generic text-cleaning patterns
  - executed through the shared pattern catalog used by `PatternCollection` and `PatternCache`

## Still Hybrid

- `src/porosdata_processor/steps.py`
  - citation bracket cleanup still uses custom Python post-processing
  - `scientific_ocr_repair` still retains the dynamic `Delta -> Ni...` alloy repair path
- `src/porosdata_processor/document_numbering_rules.py`
  - Roman numeral context handling remains code-driven

## Legacy Compatibility Only

- `src/porosdata_processor/rules/term_consistency.toml`
  - canonical replacement: `src/porosdata_processor/rules/normalize_terms.toml`
- `src/porosdata_processor/rules/citation_rules.toml`
  - canonical replacement: `src/porosdata_processor/rules/normalize_citations.toml`
- `src/porosdata_processor/rules/audit_rules.toml`
  - canonical replacement: `src/porosdata_processor/rules/detect_audit.toml`

## Next Migration Candidates

1. Retire or isolate compatibility-only legacy packs once downstream callers are gone
2. Basic document numbering rewrites without context-sensitive branching
3. Delivery-gate consumer wired into CI or release audit scripts
