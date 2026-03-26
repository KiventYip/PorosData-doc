# PorosData 工作流：从 500 篇 PDF 到结构化训练/挖掘视图

本指南演示如何使用 PorosData 框架处理高熵合金（HEA）领域的非结构化学术论文，并将其转换为可供训练和数据挖掘直接消费的结构化视图。

## 阶段 1：解析 (Parser)

使用 `DocumentParser` 从 PDF 中提取结构化数据，并保护数学公式和引用的完整性。

```python
from porosdata.parser import DocumentParser

# 初始化领域专用解析器，启用学术原子性保护
parser = DocumentParser(
    domain='materials_science',
    preserve_semantics=True,
    extract_references=True
)

# 批量处理 PDF 论文
pdf_files = [f"HEA_paper_{i}.pdf" for i in range(1, 501)]
parsed_results = parser.parse_batch(pdf_files)
```

**解析结果结构示例：**

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

## 阶段 2：清洗与质量交付 (Processor)

在进入结构化阶段之前，`Processor` 负责清理 OCR 噪音、保护术语与公式结构，并交付 AI-Ready / Data Mining Ready 的高质量文本。

```python
from porosdata.processor.domains import MaterialScienceProcessor

# 初始化处理器并执行质量清洗
processor = MaterialScienceProcessor(
    domain_knowledge_base='hea_research',
    atomicity_preservation=True
)

quality_ready_data = processor.process_material_properties(
    parsed_results,
    strict_mode=True
)

# 验证数据质量与上下文一致性
validator = processor.get_validator('mechanical_properties')
validation = validator.validate_range(
    hardness_value=485,
    material_type='high_entropy_alloy',
    temperature=298
)
```

## 阶段 3：结构化表达 (Designer)

`Designer` 在高质量文本基础上生成带 Poros 标签的训练视图、纯文本视图，以及面向抽取和检索的 `datamining` 结构化结果。

```python
from porosdata.designer import StructuredDocumentDesigner

# 初始化设计器
designer = StructuredDocumentDesigner(
    section_policy='stable-coarse-types',
    export_views=['full_text', 'datamining']
)

# 导出结构感知训练视图与数据挖掘视图
structured_outputs = designer.export_views(
    quality_ready_data,
    doc_id='HEA_paper_123'
)
```

**结构化产物示例：**

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

## 工作流结果

- **数据转换**: 500 篇 PDF -> 可训练与可挖掘的结构化视图
- **处理时间**: ~4 小时 (使用 `parser.parse_batch` 和并行处理)
- **质量保证**: 保留 LaTeX 公式、引用链、物理量纲与章节结构的一致性
