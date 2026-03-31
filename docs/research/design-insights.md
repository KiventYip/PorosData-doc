---
status: exploratory
author: KiventYip
date: 2024-03-09
hide:
  - toc
---

!!! abstract "Research Note"
    This page belongs to the **PorosData Research & Thinking** series. It records architectural evolution, unfinished algorithmic explorations, and open questions around scientific data processing. It should not be interpreted as a final or stable product commitment.

# Design Insights

**Quick Links:** [Home](../index.md) | [Quick Start](../get_started/quickstart.md)
{: .lead}

---

To ensure that scientific data can truly support model training and scientific data mining, PorosData follows a data-processing standard centered on **semantic stability**, **structural consistency**, and **minability**.

Different downstream scenarios impose different quality requirements. The two most central scenarios are:

- **Pre-training**: learning world knowledge and language structure
- **Automated Data Mining**: extracting structured knowledge from large-scale scientific literature
{: .tight-list}

## Document Placement

This page serves as a **research-level overview and technical-path discussion**. The concrete engineering constraints have been absorbed into the two tool pages in the current documentation structure:
{: .section-intro}

- `Processor`: see [tools/processor/index.md](../tools/processor/index.md), focused on data quality delivery, cleaning standards, and entry conditions for `Designer`
- `Designer`: see [tools/designer/index.md](../tools/designer/index.md), focused on structured views, Poros tag contracts, and data-mining delivery standards

## Functional Design

## 1. Data Cleaning Capability (`PorosData Processor`)

At the pre-training stage, text is consumed as token sequences. The goal is to let the model learn world knowledge and linguistic structure. If raw data contains noise or errors, the model may learn false statistical correlations and fail to understand scientific concepts. Therefore, training-ready data must satisfy three baseline properties before entering pre-training: token purity, terminology accuracy, and structural coherence.

First, the token stream must remain pure. Text converted from PDFs or OCR often contains non-semantic artifacts such as control symbols, page indices, or formatting residue. These fragments do not belong to grammar or meaning, but language models still tokenize them as ordinary input, disturbing contextual probability learning. Such noise must therefore be detected and removed.

Second, scientific terminology must remain semantically accurate. Scientific terms are highly stable semantic units. If parsing introduces systematic corruption, the model learns wrong knowledge. For example, if `X-ray` is misread as `10-ray`, the scientific concept itself is damaged. Domain dictionaries and contextual rules are therefore necessary to protect critical scientific terms from incorrect substitution.

Third, long-text structure must remain coherent. In PDF parsing, broken words and missing hyphens across line breaks are common. For example, `short-range` may be split into `short - range`, or collapsed into `shortrange`. Such damage increases vocabulary uncertainty and breaks stable terminology into meaningless tokens. This cleaning stage restores word continuity and hyphen structure so that the model can learn long and complex scientific sentences more reliably.

## 2. Structured Data Capability (`PorosData Designer`)

Unlike pre-training, the goal of data mining is to extract structured knowledge from scientific literature, such as material composition, experimental conditions, or physical parameters. In this setting, the key requirement is no longer language fluency, but **stable entity recognition**, **accurate numerical expression**, and **alignment between text and multimodal assets**.

First, numerical values and units must remain determinate. Key scientific knowledge is often expressed numerically, such as temperature, pressure, or material properties. During OCR, exponent forms and digit sequences are often broken apart, for example `$10^5$` becoming `$1 0 ^ { 5 }$`. Such corruption prevents automated mining systems from recognizing the correct magnitude, and directly damages downstream extraction. The processing pipeline must therefore restore scientific notation and exponent structures into standardized form.

Second, entity recognition must remain stable. Scientific documents depend heavily on chemical elements and material names such as `Ni`, `Au`, or `Fe3C`. If these are misread into LaTeX-like commands or malformed symbol structures, downstream NER and entity linking fail, and knowledge graph entities cannot be built correctly. The processing pipeline therefore needs rule and dictionary protection for scientific entities.

Third, multimodal assets must be anchorable. Important information in scientific papers often exists not only in the main text, but also in figures, tables, and images. Traditional text parsing often preserves only string mentions like `Fig. 1` or `Table 2`, without building a direct connection to the actual assets. The processing pipeline should convert those mentions into indexable structural anchors, so the textual reference can directly point to the corresponding figure asset and caption. This text-image linkage is foundational for multimodal knowledge mining and scientific document understanding.

## Technical Planning

## Panorama of Technical Paths for Scientific Data Processing

### 1. Regex: the Low-Level Sweeper

| Dimension | Description |
|------|------|
| **Core Logic** | Hard-coded rule matching based on patterns |
| **Typical Cases** | Physical-unit concatenation (`3 m m` -> `3mm`), broken decimals (`0 . 1` -> `0.1`), page-header and page-number noise removal |
| **Advantages** | Extremely fast, deterministic, and nearly free computationally |
| **Limitations** | Cannot resolve ambiguity well, for example whether `Ni-` should be merged or treated as a minus sign |
| **Contribution** | Improves the signal-to-noise ratio and reduces wasted tokens |

### 2. Glossaries and Dictionaries: the Domain Defense Line

| Dimension | Description |
|------|------|
| **Core Logic** | Multi-pattern matching, such as Aho-Corasick, to force fragmented OCR strings into professional terminology |
| **Typical Cases** | Chemical elements (`Z r` -> `Zr`), material abbreviations (`B M G` -> `BMG`), instrument names |
| **Advantages** | Strongly improves entity stability and protects critical scientific data |
| **Limitations** | Expensive to maintain and weak on genuinely new compounds or novel materials outside the dictionary |
| **Data Mining Contribution** | Essential for entity normalization, knowledge graph construction, and attribute extraction |

### 3. OCR Model Selection: Source-Level Suppression

| Dimension | Description |
|------|------|
| **Core Logic** | Shift from character recognition to visual-semantic understanding |
| **Representative Tools** | **Traditional OCR** such as PaddleOCR and Tesseract, which often break formulas and chemistry notation; **vision-formula models** such as Nougat and Marker, which directly predict Markdown or LaTeX sequences from academic PDFs |
| **Advantages** | Better recovery of tables, formulas, and multi-column layouts |
| **Limitations** | Requires more compute and may hallucinate missing segments on irregular layouts |
| **Contribution** | Produces structured text closer to the source and skips a large share of downstream regex cleanup |

### 4. Small-Model Finetuning or Polishing: Semantic Final Correction

| Dimension | Description |
|------|------|
| **Core Logic** | Use 1B-3B scale models such as Qwen or Llama through prompting or supervised finetuning for semantic correction |
| **Typical Cases** | Complex OCR artifacts that are not fixed patterns, such as malformed symbol sequences around chemical terms |
| **Advantages** | Brings semantic commonsense into the loop and can infer likely scientific corrections |
| **Limitations** | Slower, and must be tightly controlled so the original meaning is corrected rather than rewritten |
| **Contribution** | Pushes text quality closer to publication-grade language and improves embedding retrieval quality |

### Comparative Summary

| Approach | Cost | Flexibility | Accuracy | Core Goal |
|------|------|------|------|------|
| Regex | Very low | Low | Very high for known patterns | Remove physical noise such as spacing and formatting artifacts |
| Dictionary attachment | Low | Medium | Near-perfect inside the dictionary scope | Normalize entities such as material names and formulas |
| OCR model selection | Medium to high | High | High for academic PDFs | Restore structural content such as formulas and tables |
| Small-model finetuning | High | Very high | Very high with semantic context | Final semantic-level correction |

## Current Limits

Even under a layered processing strategy, some questions remain unresolved:

- how to repair difficult formulas without over-correcting them
- how to keep terminology dictionaries broad enough without making them too expensive to maintain
- how to preserve stable anchors across different parser outputs
- how to balance throughput, precision, and review cost in large delivery batches

## Further Reading

- [Research Review](research-review.md)
- [Processor](../tools/processor/index.md)
- [Designer](../tools/designer/index.md)

## Current Limits

Even under a layered processing strategy, some questions remain unresolved:

- how to repair difficult formulas without over-correcting them
- how to keep terminology dictionaries broad enough without making them too expensive to maintain
- how to preserve stable anchors across different parser outputs
- how to balance throughput, precision, and review cost in large delivery batches

## Further Reading

- [Research Review](research-review.md)
- [Processor](../tools/processor/index.md)
- [Designer](../tools/designer/index.md)

