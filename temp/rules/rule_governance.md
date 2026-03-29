# Rule Governance

[中文版本](rule_governance_cn.md)

## Goal

Turn rule updates into a traceable data-governance loop instead of ad hoc regex edits.

## First Principle: Declarative Rules Drive Cleaning Quality

This package serves data cleaning. When cleaning quality needs improvement, the approach is to incrementally add or update TOML rule files — not to modify Python code. Code changes are reserved for structural algorithms that cannot be safely expressed as declarative rules. The operational workflow for rule creation and promotion is documented in `rule_governance_sop.md`.

## Workflow

1. Run `python -m porosdata_processor audit ...` to discover issues from processed outputs.
2. Record the issue type, affected sample count, and risk.
3. Decide whether the change belongs to:
   - `repair`
   - `normalize`
   - `detect`
4. Add or update the corresponding TOML rule pack.
5. Attach `source_audit`, priority, and target metadata.
6. Add or update regression tests and sample assertions.
7. Run `python -m porosdata_processor bootstrap-candidate ...` to seed a candidate pack and sample JSON from the audit result.
8. Run `python -m porosdata_processor sample-validate ...` to compare baseline and candidate outputs.
9. If accepted, run `python -m porosdata_processor promote-rule ...` to incrementally merge validated rules into the canonical pack.
10. Re-run `python -m porosdata_processor run ...` on new data or reprocessed samples.
11. Run `python -m porosdata_processor delivery-gate ...` before release or handoff.
12. Run unit tests, integration tests, and audit scripts.
13. Record the rule-pack change in `CHANGELOG.md`.

See `docs/rules/rule_governance_sop.md` for the operator-facing daily procedure.

## Authoring Principles

- Prefer declarative TOML rules over new hard-coded regex when the behavior is pure pattern replacement.
- Keep high-risk structural logic in Python until it can be safely modeled declaratively.
- Do not mix detect-only and mutating rules in the same execution target.
- Give every delivery-blocking rule a clear `priority` and `source_audit`.

## Pack Ownership

- `repair_ocr.toml`: OCR and semantic repair rules used during cleaning
- `normalize_terms.toml`: terminology, alloy naming, units, and consistency rules
- `normalize_citations.toml`: citation symbol normalization and citation policy metadata
- `detect_audit.toml`: audit-only quality and OCR detection patterns
- `detect_delivery.toml`: blocking delivery-gate checks

## Canonical vs Legacy

- Canonical ownership is defined in `docs/rules/canonical_rule_pack_matrix.md`.
- `term_consistency.toml`, `citation_rules.toml`, and `audit_rules.toml` are legacy compatibility packs.
- New business rules should land in canonical `rule-pack.v1` packs, not in legacy packs.

## Rule Conflict Prevention

When adding a new rule to a canonical pack, verify:

1. **ID uniqueness**: every rule `id` must be unique within its pack. Follow `{domain}.{target}.{description}`.
2. **Pattern overlap**: the new pattern must not match the same text as an existing rule in the same target unless priority ordering is intentional.
3. **Replacement chain risk**: the replacement text must not create patterns that trigger other rules unintentionally. Run `sample-validate` to detect cascading effects.
4. **Target ownership**: each rule should only use targets owned by its pack. Cross-pack target injection is not allowed.
5. **Validation gate**: always run `sample-validate` after adding rules. Baseline-vs-candidate comparison is the primary mechanism for catching rule interactions.

## Release Expectations

Every rule-pack release should leave behind:

- updated TOML pack
- updated regression test or sample
- updated `CHANGELOG.md`
- if applicable, updated audit explanation or migration inventory
