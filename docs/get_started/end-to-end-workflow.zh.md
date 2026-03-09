# PorosData 工作流：从 500 篇 PDF 到 5000 条微调指令

本指南演示如何使用 PorosData 框架处理高熵合金（HEA）领域的非结构化学术论文，生成用于 LLM 微调的高质量指令数据集。

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

## 阶段 2：清洗与质量控制 (Processor)

应用领域知识验证数据合理性，检测异常并整合跨文献数据。

```python
from porosdata.processor.domains import MaterialScienceProcessor

# 初始化处理器并执行清洗
processor = MaterialScienceProcessor(
    domain_knowledge_base='hea_research',
    atomicity_preservation=True
)

cleaned_data = processor.process_material_properties(
    parsed_results,
    strict_mode=True
)

# 验证数据（如：检查硬度值是否在合理范围内）
validator = processor.get_validator('mechanical_properties')
validation = validator.validate_range(
    hardness_value=485,
    material_type='high_entropy_alloy',
    temperature=298
)
```

## 阶段 3：指令生成 (Designer)

将清洗后的数据转化为包含完整科学推理链的指令对。

```python
from porosdata.designer.specialized import AlloyDesignDesigner

# 初始化设计器
designer = AlloyDesignDesigner(
    physics_model='thermodynamics_mechanics',
    reasoning_depth=3
)

# 生成 5000 条推理增强的指令数据集
instruction_dataset = designer.generate_instruction_dataset(
    cleaned_data,
    task_type='alloy_performance_prediction',
    num_samples=5000,
    reasoning_template='scientific_method'
)
```

**生成的指令对结构：**

```json
{
  "instruction": "基于热力学和力学原理，预测FeCoNiCrMn高熵合金在室温下的硬度范围。",
  "input": {
    "alloy_composition": "Fe₂₀Co₂₀Ni₂₀Cr₂₀Mn₂₀ (at.%)",
    "processing_conditions": {"sintering_temperature": "1100°C"}
  },
  "output": {
    "prediction": "450-550 HV",
    "scientific_reasoning": [
      "热力学分析: FeCoNiCrMn具有较低的混合熵(>1.61R)，形成单相FCC结构",
      "力学原理: FCC结构的高对称性导致较低的硬度"
    ]
  }
}
```

## 工作流结果

- **数据转换**: 500 篇 PDF -> 5000 条指令对
- **处理时间**: ~4 小时 (使用 `parser.parse_batch` 和并行处理)
- **质量保证**: 保留 LaTeX 公式、引用链和物理量纲的一致性
