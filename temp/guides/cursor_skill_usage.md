# Cursor Skill Usage Guide

## Purpose

This document is for repository users. It explains what the project Cursor skill is for, when to rely on it, and how to phrase requests so the AI works within this repository's established standards.

The corresponding AI skill lives at:

- `.cursor/skills/datapreprocessing-project/SKILL.md`

That skill is primarily for the AI model, not the main user-facing explanation layer.

## When to Use It

Use this guidance when you want the AI to work inside this repository using the current architecture and rule-governance standards. Typical scenarios include:

- understanding the repository before making changes
- adding, adjusting, or migrating a cleaning rule
- deciding whether a change belongs in a TOML rule pack or Python code
- checking whether a change follows the current development constraints
- continuing canonical vs legacy rule-pack consolidation
- asking how the package, governance flow, or delivery gate should be used

## Recommended Prompting Style

You do not need to manually execute the skill file. It works better to include repository context and the desired working mode directly in your prompt.

### 1. Architecture entry

```text
Please understand this repository using its current architecture first, then start modifying it.
```

### 2. Rule-development entry

```text
This is a new cleaning requirement. Please decide which canonical TOML pack it belongs to before implementing it.
```

### 3. Solution-design entry

```text
Please give me an implementation plan using this repository's current development constraints, then execute it.
```

### 4. Governance-scan entry

```text
Please scan this repository against the current project standards and identify what still does not satisfy single-source-of-truth and rule externalization.
```

### 5. Usage-guidance entry

```text
Please explain how this package should be developed, applied, and validated under the current project standards.
```

## Recommended Keywords

Including these terms makes it easier for the AI to enter the correct repository-specific context:

- `datapreprocessing`
- `porosdata_processor`
- `rule pack`
- `TOML`
- `pipeline`
- `audit`
- `delivery gate`
- `canonical`
- `legacy`
- `term consistency`
- `citation`

## What You Should Expect from the AI

When the skill context is applied correctly, the AI should:

1. interpret the problem using this repository's architecture instead of giving generic advice
2. decide whether the change belongs in a canonical pack, a legacy compatibility layer, or a Python algorithm boundary
3. consider tests, samples, changelog updates, and governance-document updates together
4. explain proposals around these dimensions:
   - fixed pipeline
   - file-backed rules
   - algorithms in code
   - single source of truth
   - governance loop

## Related Documents

- `docs/rules/canonical_rule_pack_matrix.md`
- `docs/rules/rule_externalization_plan.md`
- `docs/rules/repository_constraint_scan_20260319_cn.md`
- `ARCHITECTURE_LEDGER.md`
- `docs/guides/project_development_workflow.md`
