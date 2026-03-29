# Roadmap

This page explains the PorosData roadmap from an external delivery perspective. It focuses on two questions:
{: .lead}

- what the product can already deliver today
- how the final delivery package will be expanded over time
{: .tight-list}

## Product Framework

PorosData is organized around one continuous delivery chain:
{: .section-intro}

| Module | Current Role | Main Output |
|------|------|------|
| `Parser` | receives raw papers and upstream parser results | reusable text blocks, image assets, and basic metadata |
| `Processor` | prepares content quality | cleaned intermediate outputs, processing reports, stable inputs |
| `Designer` | builds delivery-ready structure | full-text outputs, structured JSON, multimodal indexes |

These layers are designed to work together as one delivery system: preserve the source package, stabilize content quality, and then organize the final outputs.

## Final Delivery Package

The target delivery package includes:
{: .section-intro}

- a result directory organized by document ID
- plain-text outputs for training preparation
- structured outputs for extraction, retrieval, and storage
- multimodal indexes that keep text and image references connected
- reports that support review and traceability
{: .tight-list}

## Delivery Timeline

### Phase 1: Current Deliverables

The current stage focuses on making the full pipeline operational for batch use:
{: .section-intro}

- end-to-end processing from raw literature to final delivery directories
- three core output groups: full-text, structured results, and multimodal indexes
- a standard `raw -> processed -> structured` directory model
- baseline audit, validation, and batch reporting support
- an early delivery loop of process -> review -> correction -> rerun
{: .tight-list}

### Phase 2: Near-Term Improvements

The near-term goal is to make outputs more stable and easier to adopt in production projects:
{: .section-intro}

- further unify terms, units, citations, and section organization
- improve stability for long documents, complex formulas, and larger batch jobs
- expand deployment guides, usage guides, and result interpretation documents for external users
- strengthen figure-text linking and review workflows
- gradually formalize suspicious-pattern feedback and rule updates
{: .tight-list}

### Phase 3: Final Product Shape

The final goal is a more complete scientific document delivery product:
{: .section-intro}

- clearer standards for batch delivery and result acceptance
- one consistent delivery model across full-text, structured, and multimodal outputs
- stable reuse of outputs for training, extraction, retrieval, and storage
- better project-level tracking, review, and iterative improvement
{: .tight-list}

## Who This Roadmap Serves

This roadmap is mainly intended for:
{: .section-intro}

- project teams preparing scientific literature datasets
- engineering teams building training corpora
- application teams working on structured extraction and semantic retrieval
- product or data teams that need reviewable delivery outputs
{: .tight-list}

## Quick Links

If you want to continue from the roadmap into concrete usage material, start with these pages.
{: .section-intro}

- [Home](../index.md)
- [Quick Start](../get_started/quickstart.md)
- [End-to-End Workflow](../get_started/end-to-end-workflow.md)
{: .tight-list}
