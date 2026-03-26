# Design Philosophy

PorosData addresses a core AI for Science challenge: how to transform fragmented scientific literature into high-quality AI assets without sacrificing scientific rigor.

## Pillar One: Academic Atomicity

In general NLP, data is often treated as a collection of symbols. In empirical science, data is the smallest unit of academic discourse. PorosData follows the principle of **Academic Atomicity**: every scientific datum carries indivisible scholarly value, and its semantics, physical constraints, and logical relations must remain intact during processing.

### Character-Level Atomicity

The parser protects scientific formulas such as $Li_7La_3Zr_2O_{12}$ and LaTeX symbols, preventing operations that would split characters or introduce semantic ambiguity.

### Relational Atomicity

The processor prevents physical values from being detached from their units, and prevents experimental conditions from drifting away from results. Cleaning must preserve logical consistency among quantities, units, and context.

### Structural Atomicity

The designer must preserve section hierarchy, formula boundaries, chemical semantics, multimodal anchors, and context ownership during structured reconstruction, so that training views and data-mining views remain computationally meaningful.

## Pillar Two: Knowledge-Driven Processing

PorosData relies on domain knowledge rather than generic statistical preprocessing alone.

### Physical Constraints

Thermodynamic rules, dimensional consistency, and other scientific constraints are used to validate whether data remains physically meaningful.

### Expert Knowledge Integration

Expert intuition, such as how non-standard chemical formulas should be normalized, is translated into computable rules so the toolchain gains domain-specific scientific commonsense.

## Pillar Three: Full-Lifecycle Pipeline

PorosData forms a three-part closed loop that spans the end-to-end path from literature to usable AI assets.

### Perception (Parser)

The parser performs non-destructive extraction, rescuing buried knowledge from heterogeneous documents while preserving original academic value.

### Refinement (Processor)

The processor removes noise and raises input quality under the constraints of academic atomicity.

### Structured Expression (Designer)

The designer reconstructs high-quality text into tagged training views, plain-text views, data-mining views, and multimodal indexes, so the same knowledge can be consumed both by models and by structured downstream systems.

## Vision

PorosData aims to build a rigorous bridge between literature and models, preserving academic seriousness while turning accumulated scientific experience into durable digital assets for the AI era.