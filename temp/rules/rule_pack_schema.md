# Rule Pack Schema

## Purpose

This document defines the normalized declarative rule-pack model for `porosdata_processor`.

The goal is to keep rule content in TOML while keeping execution order, safety boundaries, and audit traceability explicit.

## Rule-Pack Shape

Every new rule pack should use:

```toml
schema = "rule-pack.v1"
version = 1
description = "..."

[defaults]
enabled = true
kind = "normalize"
phase = "in_pipeline"
scope = "text"
target = "term_consistency_mapping"
risk_level = "medium"
owner = "processor"
source_audit = "docs/audit/..."

[[rules]]
id = "term.short-range"
priority = "P1"
pattern = '\bshortrange\b(?!\w)'
replacement = 'short-range'
replacement_mode = "literal"
```

## Required Fields

### Pack level

- `schema`: must be `rule-pack.v1`
- `version`: integer pack version
- `description`: short pack purpose

### Rule level

- `id`: globally unique stable rule identifier
- `priority`: `P0` / `P1` / `P2`
- `pattern`: regex pattern

## Recommended Rule Metadata

- `enabled`: default `true`
- `kind`: `detect` / `normalize` / `repair`
- `scope`: `text` / `metadata` / `formula_safe` / `audit_only`
- `phase`: `pre_shield` / `in_pipeline` / `post_shield` / `audit`
- `target`: concrete execution target such as `scientific_ocr_repair`
- `replacement`
- `replacement_mode`: `literal` / `expand`
- `flags`: regex flags list
- `risk_level`: `low` / `medium` / `high`
- `owner`: maintainer
- `source_audit`: source report or issue
- `notes`: optional rationale
- `examples`: optional before/after examples

## Execution Rules

- `pre_shield`: only deterministic low-risk cleanup, no formula-structure rewrites
- `in_pipeline`: standard normalize/repair rules inside Shield protection
- `post_shield`: only restored-text cleanup and low-risk finishing passes
- `audit`: detect-only or delivery-gate rules used by audit scripts and validation

## Scope Rules

- `text`: general prose body
- `metadata`: caption, footnote, and delivery metadata fields
- `formula_safe`: allowed to run near math content but must remain regex-safe
- `audit_only`: never mutates text, only reports findings

## Compatibility Policy

Legacy packs such as:

- `term-consistency.v1`
- `citation-rules.v1`
- `audit-rules.v1`

are still loadable through the normalization layer, but new packs should be authored only as `rule-pack.v1`.
