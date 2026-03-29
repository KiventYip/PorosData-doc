# Design Philosophy

The core idea behind PorosData is simple: scientific literature is not ordinary text. It carries terms, units, formulas, figures, and contextual relations that must survive processing if the result is meant to stay useful.
{: .lead}

The value of the system is not in rewriting papers into simpler language. It is in making them more stable, more structured, and easier to use downstream without losing scientific meaning.

## Pillar One: Academic Atomicity

PorosData treats each piece of scientific content as a unit that should not be broken apart carelessly. Processing should preserve meaning, physical constraints, and contextual relations as much as possible.

### Character Level

Formulas, chemical expressions, and special symbols should not be structurally damaged by processing steps.

### Relation Level

Numbers, units, experimental conditions, and conclusions should remain connected during cleaning and reorganization.

### Structure Level

Section hierarchy, figure references, and key context should remain traceable and understandable in the final outputs.

## Pillar Two: Knowledge-Constrained Processing

PorosData does not treat scientific content as plain strings alone. It applies domain-aware constraints when normalizing and organizing data.

### Rules Should Serve Meaning

Term normalization, unit consistency, citation cleanup, and chemical-expression protection are used to keep outputs closer to the intended scientific meaning, not just to make formatting look cleaner.

### Experience Should Become Reusable

Domain experience should be turned into reusable processing strategies so batch workflows can follow a more stable standard.

## Pillar Three: Layered Delivery

PorosData uses a layered delivery chain instead of trying to solve every problem in one step.

### Parser

Keep as much usable content and as many source assets as possible from the original literature.

### Processor

Resolve quality issues first so text, captions, and key fields become stable enough for further use.

### Designer

Then organize those stable inputs into full-text, structured, and multimodal outputs for final delivery.

## Vision

PorosData aims to provide a practical delivery chain for scientific literature, so papers can move more smoothly into training, extraction, retrieval, and review workflows while preserving the rigor expected in research communication.