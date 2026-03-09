# PorosData

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PyPI version](https://img.shields.io/pypi/v/PorosData-Processor.svg)](https://pypi.org/project/porosdata-processor/)

PorosData is an AI4S data orchestration framework specifically engineered for materials science and related empirical fields. It provides a full-lifecycle solution—from parsing and refinement to data synthesis—bridging raw scientific literature and AI models, and safeguarding the semantic integrity, fidelity, and end-to-end provenance of scientific data.

## Core Features

- **Data Integrity Guarantee**: Protects the atomic integrity of mathematical formulas, citation systems, and scientific semantics.
- **Synergistic Modular Architecture**: Three core toolkits (Parser, Processor, and Designer) cover the entire scientific data processing workflow.
- **Academic-Oriented Design**: Prioritizes the requirements of academic standards and scientific workflows.

## Academic Atomicity

PorosData treats every piece of data as an indivisible unit of academic value. During the data refinement process, we commit to:

- **Semantic Fidelity**: Ensure mathematical expressions are not distorted and citation chains remain unbroken.
- **Traceability**: Record the academic basis for every cleaning decision.
- **Seamless Extensibility**: Allow new components and plugins to inherit the atomicity contract.

## AI-Ready Data Standards

To ensure data is truly suitable for large models, PorosData strictly adheres to the following AI-Ready data processing requirements:

### 1. Pre-training Requirements: Token Purity and Semantic Common Sense

The goal of pre-training is to let the model learn world knowledge (e.g., laws of physics and chemistry). If the data itself contains errors, the model will suffer from "knowledge poisoning".

- **Token Stream Purity**: The main text should not contain semantic-irrelevant control characters or indices. Such data, unrelated to semantics and grammatical structure, acts as interference noise during training, destroying the model's prediction of context probabilities.
- **Semantic Common Sense Accuracy**: Core terminology must not have systematic misrecognitions. If "X-ray" is recognized as "10-ray", the model will learn incorrect scientific concepts, causing it to fail to understand the logic of ray diffraction in subsequent tasks.
- **Long-text Coherence**: Word breaks caused by improper handling of line breaks (e.g., missing hyphens like "shortrange" for "short-range") increase the entropy of the model's vocabulary and reduce its ability to understand long, complex sentences.

### 2. Data Mining Requirements: Entity Precision and Logical Linking

The goal of data mining is to automatically extract structured knowledge (e.g., alloy composition, transition temperature) from massive documents.

- **Certainty of Values and Units**: Scientific mining is extremely sensitive to numbers. Numbers broken up by OCR (e.g., $1 0 ^ { 5 }$) will cause mining algorithms to fail to recognize the correct order of magnitude, directly ruining automated property extraction tasks.
- **Robustness of Entity Recognition**: Chemical elements (e.g., Ni, Au) must not be misrecognized as LaTeX symbols (e.g., $\Delta$, \Au). Otherwise, when building a knowledge graph, entity linking will fail due to name errors.
- **Anchoring of Multimodal Assets**: Mining work often requires "text-image penetration". AI-Ready requires that "Fig. 1" in the text is not just a few characters, but a hard-link anchor that can directly index to the image asset and its corresponding caption.

!!! note "Case Study"
    Check out the [End-to-End Workflow](get_started/end-to-end-workflow.md) to see the conversion process from PDF papers to AI training datasets.

## PorosData-Parser

🔍 Data Extraction Engine

Intelligently extracts structured scientific data from unstructured literature such as PDF papers and LaTeX source code.

## PorosData-Processor

🧹 Data Cleaning Pipeline

Standardizes, controls quality, and preprocesses data based on the principle of academic atomicity.

## PorosData-Designer

🎯 Data Synthesis Designer

Recombines cleaned data into instruction datasets and experimental design plans suitable for large model training.

## Quick Start

- [Installation Guide](get_started/installation.md)
- [Quick Start](get_started/quickstart.md)
- [Usage Examples](references/examples.md)

## In-Depth Reference

- [Design Philosophy](concepts/design-philosophy.md)
- [Research Review](research/research-review.md)
- [Design Insights](research/design-insights.md)
- [Glossary](concepts/glossary.md)
- [API Reference](references/api-reference.md)

## Project Ecosystem

- [Contributing Guide](community/contributing.md)
- [Roadmap](community/roadmap.md)
- [Changelog](community/changelog.md)
