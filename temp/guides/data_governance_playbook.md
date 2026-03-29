# Data Governance Playbook

*Last updated: 2026-03-19*

[中文版本](data_governance_playbook_cn.md)

This playbook describes how to use the `porosdata_processor` audit and rule workflow to achieve continuous, data-driven quality improvement. It is designed for human operators who need to understand the process, make judgment calls, and track progress.

## Core Principle

> Quality improvement happens by adding declarative TOML rules — not by modifying Python code.
>
> Every improvement cycle must be traceable: timestamped artifacts, auditable results, and a clear decision trail.

---

## The Data Governance Loop

```
┌───────────────────────────────────────────────────────────────┐
│                                                               │
│  ┌─────────┐    ┌──────────────┐    ┌──────────────────────┐  │
│  │  Audit   │───>│ Identify Gap │───>│ Bootstrap Candidate  │  │
│  └─────────┘    └──────────────┘    └──────────────────────┘  │
│       ^                                        │              │
│       │                                        v              │
│  ┌─────────────┐  ┌────────────┐   ┌──────────────────────┐  │
│  │Delivery Gate│<──│Promote Rule│<──│  Sample Validate     │  │
│  └─────────────┘  └────────────┘   └──────────────────────┘  │
│                                                               │
└───────────────────────────────────────────────────────────────┘
```

Each step produces artifacts that feed into the next. The loop never stops — each delivery triggers a new audit cycle for the next release.

---

## Step-by-Step Workflow

### Step 1: Audit

**Purpose**: Discover quality issues in processed data.

**Command**:
```bash
python run_processor.py audit
```

**What it does**:
- Runs `detect_audit.toml` patterns (OCR residue, quality patterns) against processed data.
- Executes Python-based structural checks (dollar sign balancing, citation metrics, metadata coverage).
- Produces a JSON report at `docs/audit/aiready_data_audit_result.json`.

**Human judgment required**:
- Review flagged issues to determine if they are true positives or false positives.
- Prioritize issues by severity (blocking vs. warning).
- Decide which issues warrant new rules vs. which are acceptable edge cases.

**Output**: Timestamped audit result (`aiready_data_audit_result.json` with ISO timestamp field).

---

### Step 2: Identify Gap

**Purpose**: Classify each audit finding and decide the response.

**Decision matrix**:

| Finding type | Response | Where |
|---|---|---|
| Regex-fixable pattern | Add TOML rule | Canonical rule pack |
| Structural/algorithmic issue | Code fix (with approval) | Python source |
| False positive in detection | Refine audit pattern | `detect_audit.toml` |
| Acceptable edge case | Document and skip | Audit notes |

**Human judgment required**:
- Inspect the context of flagged text to understand what the pattern actually matched.
- Use `scripts/check_hyphen_context.py` or similar ad-hoc scripts to examine matches in detail.
- Determine whether a rule can safely fix the issue without introducing regressions.

---

### Step 3: Bootstrap Candidate

**Purpose**: Create candidate rules for the identified gaps.

**Command**:
```bash
python run_processor.py bootstrap-candidate
```

**What it does**:
- Generates candidate rule entries based on audit findings.
- Candidates are placed in a staging area for review before promotion.

**Rule authoring guidelines**:
- Rule ID format: `{domain}.{target}.{description}` (e.g., `post_shield.unwrap.element_based`).
- Every rule needs: `id`, `priority`, `target`, `pattern`, `replacement`.
- Test the regex pattern against the actual flagged text before proceeding.

---

### Step 4: Sample Validate

**Purpose**: Verify that candidate rules work correctly and do not cause regressions.

**Command**:
```bash
python run_processor.py sample-validate
```

**What it does**:
- Applies candidate rules to sample data.
- Checks for replacement chain conflicts (where one rule's output triggers another rule unintentionally).
- Reports on match counts and any unexpected side effects.

**Human judgment required**:
- Review the validation output for unexpected matches.
- Check that the replacement is semantically correct, not just syntactically valid.
- Verify that the rule does not over-match (too broad) or under-match (too narrow).

---

### Step 5: Promote Rule

**Purpose**: Move validated candidates into the canonical rule pack.

**Command**:
```bash
python run_processor.py promote-rule
```

**What it does**:
- Backs up the current canonical pack with a `YYYYMMDD_HHMMSS` timestamp.
- Merges validated candidates into the canonical pack.
- Updates rule metadata.

**After promotion**:
- Reprocess the affected data with the updated rules.
- Run `python -m pytest tests/unit/ -q` to verify no test regressions.

---

### Step 6: Delivery Gate

**Purpose**: Confirm that processed data meets delivery standards with zero blocking issues.

**Command**:
```bash
python run_processor.py delivery-gate
```

**What it does**:
- Runs `detect_delivery.toml` blocking checks against all processed data.
- Reports pass/fail status per document.
- A single blocking issue fails the entire gate.

**Human judgment required**:
- Review any failures and decide whether to create additional rules or request an exception.
- Sign off on the delivery once the gate passes.

---

## Timestamp and Traceability Requirements

| Artifact | Timestamp format | Location |
|----------|-----------------|----------|
| Audit JSON results | ISO datetime (auto-set) | `docs/audit/` |
| Audit report files | `_YYYYMMDD` in filename | `docs/audit/` |
| Rule backups | `YYYYMMDD_HHMMSS` in filename | `docs/rules/backups/` |
| CHANGELOG entries | Date header per section | `CHANGELOG.md` |
| Architecture decisions | Date in ledger entry | `ARCHITECTURE_LEDGER.md` |

---

## Common Scenarios

### Scenario A: OCR residue found in processed data

1. Run `audit` — see `ocr_pattern` matches.
2. Inspect the context of each match using ad-hoc scripts.
3. Classify: is this a `repair_ocr.toml` or `post_shield.toml` fix?
4. Add a candidate rule to the appropriate pack.
5. `sample-validate` → `promote-rule` → reprocess → `audit` → `delivery-gate`.

### Scenario B: Formula formatting issue

1. Run `audit` — see `formula_hyphen_spacing` or similar quality pattern.
2. Inspect: is the math mode semantically necessary? Or is it wrapping a plain element symbol?
3. If plain element: add an `unwrap` rule to `post_shield.toml`.
4. If semantically necessary formula: mark as false positive, refine the audit pattern if needed.
5. Complete the governance loop.

### Scenario C: New term normalization needed

1. Identify inconsistent terminology in processed output.
2. Add a mapping rule to `normalize_terms.toml`.
3. Validate, promote, reprocess, audit, gate.

---

## Architecture Boundaries

When deciding where a fix belongs, respect these boundaries:

- **TOML rules**: regex-based patterns, text replacement, normalization mappings.
- **Python code**: context-aware logic, multi-step algorithms, stateful transformations.
- **Frozen elements**: pipeline step sequence, Shield mechanism, module hierarchy — do not modify without explicit approval.
- **Extensible elements**: TOML rule files, detection patterns, tests, documentation.

For the detailed architecture freeze boundary, see the project skill reference documentation.
