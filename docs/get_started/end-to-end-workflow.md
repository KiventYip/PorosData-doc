# PorosData Workflow: From 500 PDFs to Structured Training and Mining Views

This guide demonstrates how to use PorosData to process unstructured academic papers in the high-entropy alloy (HEA) domain and convert them into structured outputs that can be directly consumed by training and data-mining pipelines.

## Stage 1: Parsing (Parser)

Use `DocumentParser` to extract processable content from PDF papers while preserving formulas and citation structure.

```python
from porosdata.parser import DocumentParser

# Initialize a domain-specific parser with academic atomicity protection
parser = DocumentParser(
    domain='materials_science',
    preserve_semantics=True,
    extract_references=True
)

# Batch-process PDF papers
pdf_files = [f"HEA_paper_{i}.pdf" for i in range(1, 501)]
parsed_results = parser.parse_batch(pdf_files)
```

**Example parser output:**

```json
{
  "document_id": "HEA_paper_123",
  "alloy_composition": {
    "formula": "FeCoNiCrMn",
    "standardized_notation": "Fe₂₀Co₂₀Ni₂₀Cr₂₀Mn₂₀"
  },
  "mechanical_properties": {
    "hardness": {"value": 485, "unit": "HV", "temperature": 298}
  }
}
```

## Stage 2: Cleaning and Quality Delivery (Processor)

Before any structuring step, `Processor` removes OCR noise, protects scientific terms and formula boundaries, and delivers text that is AI-Ready and Data Mining Ready.

```python
from porosdata.processor.domains import MaterialScienceProcessor

# Initialize the processor and run quality cleaning
processor = MaterialScienceProcessor(
    domain_knowledge_base='hea_research',
    atomicity_preservation=True
)

quality_ready_data = processor.process_material_properties(
    parsed_results,
    strict_mode=True
)

# Validate quality and contextual consistency
validator = processor.get_validator('mechanical_properties')
validation = validator.validate_range(
    hardness_value=485,
    material_type='high_entropy_alloy',
    temperature=298
)
```

## Stage 3: Structured Expression (Designer)

`Designer` turns quality-ready text into tagged training views, plain-text views, and `datamining` outputs that can be consumed by retrieval and extraction systems.

```python
from porosdata.designer import StructuredDocumentDesigner

# Initialize the designer
designer = StructuredDocumentDesigner(
    section_policy='stable-coarse-types',
    export_views=['full_text', 'datamining']
)

# Export structure-aware training views and data-mining views
structured_outputs = designer.export_views(
    quality_ready_data,
    doc_id='HEA_paper_123'
)
```

**Example structured outputs:**

```json
{
  "full_text": {
    "doc_id": "HEA_paper_123",
    "content": [
      "<poros_doc>",
      "<poros_section_abstract>...</poros_section_abstract>",
      "<poros_section_results>...</poros_section_results>",
      "</s>"
    ],
    "pure_text_stream": [
      "FeCoNiCrMn alloy shows ...",
      "The hardness at room temperature is 485 HV.",
      "</s>"
    ]
  },
  "datamining": {
    "doc_id": "HEA_paper_123",
    "title": "Mechanical properties of FeCoNiCrMn alloy",
    "sections": [
      {
        "section_type": "results",
        "paragraphs": [
          "The hardness at room temperature is 485 HV."
        ]
      }
    ],
    "formulas": [],
    "chemical_formulas": ["FeCoNiCrMn"],
    "asset_refs": []
  }
}
```

## Workflow Outcome

- **Transformation**: 500 PDFs -> structured views for training and mining
- **Processing Time**: ~4 hours using `parser.parse_batch` and parallel processing
- **Quality Guarantee**: preserves LaTeX formulas, citation chains, physical units, and section structure