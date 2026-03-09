# 快速开始指南

本指南将帮助您快速上手 PorosData 的核心功能。

## 环境准备

### 系统要求

- Python 3.8+
- pip (Python 包管理器)

### 安装验证

```bash
python --version
pip --version
```

## 核心工作流

### 1. 数据解析 (Parser)

```python
from porosdata_parser import PDFParser

parser = PDFParser()
data = parser.parse("research_paper.pdf")
print(f"提取到 {len(data)} 个数据点")
```

### 2. 数据清洗 (Processor)

```python
from porosdata_processor import DataProcessor

processor = DataProcessor()
clean_data = processor.process(data)
print(f"清洗后剩余 {len(clean_data)} 个有效数据点")
```

### 3. 数据合成 (Designer)

```python
from porosdata_designer import DataDesigner

designer = DataDesigner()
training_data = designer.generate_training_data(clean_data)
print(f"生成了 {len(training_data)} 个训练样本")
```

## 常见问题

### Q: 解析 PDF 时出现编码错误？

A: 确保 PDF 文件使用 UTF-8 编码，或在解析时指定编码：

```python
parser = PDFParser(encoding='utf-8')
```

### Q: 如何处理大型数据集？

A: 使用批处理模式提高效率：

```python
processor = DataProcessor(batch_size=1000)
results = processor.process_large_dataset("large_dataset.json")
```