# Canonical Rule Pack Matrix

## Purpose

This matrix defines which rule packs are canonical, which are legacy-compatibility only, and where new work should land.

## Canonical Packs

| Concern | Canonical pack | Primary consumer | Notes |
|---|---|---|---|
| OCR repair | `rules/repair_ocr.toml` | `scientific_ocr_repair` | Keep only pattern-driven repair rules here. |
| Term consistency | `rules/normalize_terms.toml` | `TermConsistencyEngine` / `term_consistency_mapping` | New terminology, alloy, unit, and punctuation normalization rules go here. |
| Citation normalization | `rules/normalize_citations.toml` | citation-related steps in `steps.py` | Includes rewrite rules plus citation policy metadata. |
| Audit detection | `rules/detect_audit.toml` | audit workflow | Detect-only pack for audit and issue discovery. |
| Delivery gate | `rules/detect_delivery.toml` | delivery gate | Blocking checks only. No mutating rules. |
| Metadata cleanup | `rules/normalize_metadata.toml` | `metadata_signal_cleanup` | Front matter labels and metadata payload cleanup. |
| Numbering normalization | `rules/normalize_numbering.toml` | `DocumentNumberingRuleEngine` | Declarative numbering mappings and low-risk numbering rewrites. |
| Greek normalization | `rules/normalize_greek.toml` | `GreekLatexConverter` | Greek and LaTeX mapping tables. |
| Formula lexicon | `rules/formula_lexicon.toml` | `steps.py` / `text_cleaner.py` | Shared tables for formula and unit handling. |
| Semantic LaTeX cleanup | `rules/semantic_latex.toml` | `text_cleaner.py` | Pre-shield semantic OCR and LaTeX rewrites. |
| Post-shield cleanup | `rules/post_shield.toml` | `text_cleaner.py` | Restored-formula cleanup and hyphen-chain finishing. |
| Generic pattern cleaning | `rules/patterns_cleaning.toml` | `PatternCollection` / `PatternCache` | Single source for generic text-cleaning patterns. |

## Legacy Compatibility Packs

| Legacy pack | Canonical replacement | Status | Rule |
|---|---|---|---|
| `rules/term_consistency.toml` | `rules/normalize_terms.toml` | Compatibility only | Do not add new business rules here. |
| `rules/citation_rules.toml` | `rules/normalize_citations.toml` | Compatibility only | Keep only until all legacy callers are retired. |
| `rules/audit_rules.toml` | `rules/detect_audit.toml` | Compatibility only | Keep only for migration safety and normalized loading. |

## First Principle: Declarative Rules Drive Cleaning Quality

This package serves data cleaning. When cleaning quality needs improvement, the approach is to incrementally add or update TOML rule files — not to modify Python code. Code changes are reserved for structural algorithms that cannot be safely expressed as declarative rules.

## Decision Rule

1. If the behavior is a pure pattern or mapping, place it in the canonical TOML pack for that domain.
2. If the behavior is detect-only, place it in an audit or delivery pack, not in a mutating cleanup pack.
3. If the behavior is structural, stateful, or needs parsing, keep it in Python.
4. If a legacy pack must be touched for compatibility, update the corresponding canonical pack and document the reason.

## Rule Conflict Prevention

When adding a new rule:

1. **ID uniqueness**: every `id` must be unique within its pack. Follow `{domain}.{target}.{description}`.
2. **Pattern overlap**: verify the new pattern does not match the same text as an existing rule in the same target, unless priority ordering is intentional.
3. **Replacement chain risk**: verify the replacement text does not create patterns that trigger other rules. Run `sample-validate` to detect cascading effects.
4. **Target ownership**: each rule should only use targets owned by its pack. Cross-pack target injection is not allowed.
5. **Validation gate**: always run `sample-validate` after adding rules.

## Documentation Rule

When rule ownership changes, update:

- `docs/rules/rule_externalization_plan.md`
- `docs/rules/repository_constraint_scan_20260319_cn.md`
- `docs/rules/rule_governance.md`
- `docs/rules/rule_governance_cn.md`
- `docs/rules/rule_migration_inventory.md`
- `ARCHITECTURE_LEDGER.md`
- `ARCHITECTURE_LEDGER_cn.md`
- `CHANGELOG.md`
- `CHANGELOG_cn.md`
