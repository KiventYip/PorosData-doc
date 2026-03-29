# Project Development Workflow

## Purpose

This document is for repository users. It explains how to move work forward in `datapreprocessing` using the current project standards for requirement analysis, rule development, code changes, validation, and documentation updates.

If you want the AI to work under the repository's established constraints, read:

- `docs/guides/cursor_skill_usage.md`

If you want the command-level SOP for rule governance, read:

- `docs/rules/rule_governance_sop.md`

## First Principle: Declarative Rules Drive Cleaning Quality

This package serves data cleaning. When cleaning quality needs improvement, the approach is to incrementally add or update TOML rule files — not to modify Python code. Code changes are reserved for structural algorithms that cannot be safely expressed as declarative rules. The operational workflow for rule creation and promotion is documented in `docs/rules/rule_governance_sop.md`.

## Understand Before Implementing

In this project, first decide what kind of change you are making:

1. Rule-oriented work
   - for example OCR cleanup rules, terminology normalization, citation normalization, or delivery-gate detection rules
2. Algorithm-oriented work
   - for example Shield lifecycle, formula-structure repair, brace matching, or conservative structure checks
3. Architecture and governance work
   - for example canonical vs legacy consolidation, default-pipeline source of truth, or documentation consistency

Basic decision rules:

- Pure pattern, mapping, or detect behavior should go into a canonical TOML rule pack.
- Structural, stateful, or parsing-heavy behavior should remain in Python.
- New business rules should not be added to legacy compatibility packs.

## Standard Execution Path

### 1. Clarify change ownership

Answer these four questions first:

1. Which rule domain does this request belong to?
2. Which canonical pack should own it?
3. Does it cross a Python algorithm boundary?
4. Does it require governance-document updates?

Common canonical entry points:

- `src/porosdata_processor/rules/normalize_terms.toml`
- `src/porosdata_processor/rules/normalize_citations.toml`
- `src/porosdata_processor/rules/detect_audit.toml`
- `src/porosdata_processor/rules/detect_delivery.toml`
- `src/porosdata_processor/rules/patterns_cleaning.toml`

For the complete matrix, see:

- `docs/rules/canonical_rule_pack_matrix.md`

### 2. Implement the change

Choose the implementation path by change type:

- rule-oriented work: update the canonical TOML pack first
- algorithm-oriented work: update Python code and keep the boundary explicit
- architecture work: consolidate first and avoid introducing new abstraction layers

During implementation, check for rule conflicts:

- **ID uniqueness**: the new rule `id` must be unique within its pack (convention: `{domain}.{target}.{description}`)
- **Pattern overlap**: verify the new pattern does not match the same text as an existing rule in the same target
- **Replacement chain risk**: verify the replacement text does not create patterns that trigger other rules unintentionally
- **Target ownership**: each rule should only use targets owned by its pack
- whether an equivalent rule already exists
- whether samples or regression tests need updates
- whether canonical vs legacy ownership notes must be updated

### 3. Validate the change

Minimum validation baseline:

```bash
python -m compileall src
python -m pytest tests/unit/test_patterns.py tests/unit/test_installation_verification.py tests/unit/test_processor.py
```

If the change touches rule-workflow infrastructure, also run:

```bash
python -m pytest tests/unit/test_rule_pack_loader.py
```

If the change touches candidate-rule governance, continue through the SOP:

1. `audit`
2. `bootstrap-candidate`
3. `sample-validate`
4. `promote-rule`
5. `delivery-gate`

## Documentation Update Expectations

When your change affects rule ownership, governance, architecture consolidation, or canonical relationships, review whether these documents also need updates:

- `docs/rules/canonical_rule_pack_matrix.md`
- `docs/rules/rule_externalization_plan.md`
- `docs/rules/repository_constraint_scan_20260319_cn.md`
- `docs/rules/rule_governance.md`
- `docs/rules/rule_governance_cn.md`
- `docs/rules/rule_migration_inventory.md`
- `ARCHITECTURE_LEDGER.md`
- `ARCHITECTURE_LEDGER_cn.md`
- `CHANGELOG.md`
- `CHANGELOG_cn.md`

## Suggested Prompting for Users

If you want the AI to work more reliably under the current repository standards, prompts like these help:

### Architecture question

```text
Please understand this task using the repository's fixed pipeline, file-backed rules, and algorithm boundary before proposing a solution.
```

### Rule question

```text
Please decide which canonical TOML pack this requirement belongs to, then implement it and update tests and docs.
```

### Governance question

```text
Please scan the repository against the current constraints, consolidate legacy residue, and update the related documents.
```

## Common Mistakes

### 1. Treating the skill as user documentation

Do not use `.cursor/skills` as the main user-reading entrypoint.

- `skill` is primarily for the AI
- `docs` are the user-facing explanation layer

### 2. Updating rules without updating governance docs

If a change affects canonical ownership, execution entrypoints, or governance structure, it should not stop at code or TOML changes only.

### 3. Putting new rules into legacy packs

These files are compatibility-only and should not receive new business rules:

- `src/porosdata_processor/rules/term_consistency.toml`
- `src/porosdata_processor/rules/citation_rules.toml`
- `src/porosdata_processor/rules/audit_rules.toml`

### 4. Forcing complex structure problems into declarative rules

Formula-structure repair, parsing, protection, restoration, and structural validation should remain in Python first.

## Related Documents

- `docs/guides/cursor_skill_usage.md`
- `docs/usage_guide.md`
- `docs/rules/rule_governance_sop.md`
- `docs/rules/canonical_rule_pack_matrix.md`
- `ARCHITECTURE_LEDGER.md`
