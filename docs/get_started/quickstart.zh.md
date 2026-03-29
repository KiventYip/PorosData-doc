# 快速开始

## 安装 PorosData

从 PyPI 安装 (推荐):
{: .section-intro}

```bash
pip install porosdata-processor
```

从源码安装:

```bash
git clone https://github.com/KiventYip/porosdata-processor.git
cd porosdata-processor
pip install -e .
```

验证安装:

```python
import porosdata_processor
print(f"Version: {porosdata_processor.__version__}")
```

## 清洗文本

使用 `TextCleaner` 标准化科学文本，同时保留数学公式的完整性：
{: .section-intro}

```python
from porosdata_processor import TextCleaner

# 初始化默认设置的清洗器
cleaner = TextCleaner()

# 处理文本
raw_text = "The energy equation is $E = mc^2$, involving α particles and β rays."
cleaned_text = cleaner.clean(raw_text)

print(cleaned_text)
# 输出: "The energy equation is $E = mc^2$, involving \alpha particles and \beta rays."
```

## 自定义流水线

配置带有特定插件的清洗器：
{: .section-intro}

```python
# 创建带有特定插件的清洗器
cleaner = TextCleaner(pipeline=[
    "citation_rules",      # 标准化引用
    "greek_to_latex",      # 转换希腊字母
    "normalize_whitespace" # 清理间距
])

text = "See reference 【1】 for α particle data."
result = cleaner.clean(text)
# 输出: "See reference [1] for \alpha particle data."
```

## 高级选项

启用高级 LaTeX 公式清洗功能：
{: .section-intro}

```python
# 启用高级 LaTeX 公式清洗
cleaner = TextCleaner(clean_options={
    "clean_latex_math_spaces": True  # 移除公式内的额外空格
})

text = "Formula: $\\mathbf { X } + \\frac { a }{ b }$"
result = cleaner.clean(text)
# 输出: "Formula: $\\mathbf{X} + \\frac{a}{b}$"
```

## 处理文件

### 处理单个文件

```python
# 清洗 Markdown 文件
cleaner.clean_file(
    input_path="document.md",
    output_path="clean_document.md",
    encoding="utf-8"
)
```

### 批量处理

```python
from processing.batch_processor import BatchProcessor

processor = BatchProcessor()
processor.process_text_data(
    input_dir="data/raw",
    output_dir="data/cleaned"
)
```

## 配置

### 处理配置

创建 `config/processing_config.yaml`：
{: .section-intro}

```yaml
cleaning:
  convert_greek: true
  apply_rules: true
  apply_patterns: true
  normalize_whitespace: true
  remove_extra_spaces: true

processing:
  concurrency: 0  # 0 表示顺序处理
  verbose: true
```

### Token 配置

对于高级分词设置，创建 `config/token_config.yaml`：
{: .section-intro}

```yaml
model_type: "llama"  # 或 "gpt", "custom"

tokens:
  llama:
    bos: "<s>"
    eos: "</s>"
    inst_start: "[INST]"
    inst_end: "[/INST]"

splitting:
  max_chunk_tokens: 512
  split_by_paragraph: true
  preserve_paragraphs: true
  overlap_tokens: 50
```

## 下一步

- 查看 [API 参考](../references/api-reference.md) 了解详细的方法文档
- 查看 [示例](../references/examples.md) 了解实际使用案例
- 了解 [插件开发](../community/contributing.md) 来扩展功能
{: .tight-list}