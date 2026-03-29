# Documentation Language Policy

[中文版本](documentation_language_policy_cn.md)

## Goal

All maintained project documentation should exist in two editions:

- English primary document
- Chinese companion document

## Naming Rule

- The English document keeps the canonical filename.
- The Chinese companion uses the same filename with `_cn` or `_CN` before `.md`.
- English is the canonical reference target for cross-links unless a Chinese-only reading flow is explicitly needed.

## Scope

This policy applies to maintained repository documentation, including:

- root-level project documents
- `docs/` user guides, architecture notes, and governance documents
- `scripts/` audit reports and operator-facing Markdown notes

## Historical Documents

Historical audit archives may still contain older wording or older repository paths. They should be kept for traceability, but when updated they should follow the bilingual naming rule.

## Maintenance Rule

When adding or updating a maintained document:

1. Update the English primary document first.
2. Create or update the Chinese companion with the `_cn` or `_CN` suffix.
3. Add cross-links between the two editions when practical.
