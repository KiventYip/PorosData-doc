# PorosData-Parser 工具调用

## 快速开始

### 安装依赖

```bash
pip install porosdata-parser
```

### 基本使用

```python
from porosdata.parser import DocumentParser

# 初始化解析器
parser = DocumentParser()

# 解析PDF文档
result = parser.parse_file("research_paper.pdf")
print(result.metadata)
print(result.content)
```

## API 参考

### DocumentParser 类

#### 初始化参数

```python
DocumentParser(
    language='auto',      # 文档语言：'auto', 'en', 'zh'
    extract_formulas=True, # 是否提取数学公式
    preserve_citations=True, # 是否保留引用信息
    output_format='json'   # 输出格式：'json', 'xml', 'dict'
)
```

#### 主要方法

##### parse_file(file_path, **options)

解析单个文件

**参数:**
- `file_path` (str): 文件路径
- `**options`: 额外的解析选项

**返回值:**
- `ParseResult` 对象，包含解析后的结构化数据

##### parse_batch(file_paths, **options)

批量解析多个文件

**参数:**
- `file_paths` (list): 文件路径列表
- `**options`: 批处理选项

**返回值:**
- `BatchParseResult` 对象

##### extract_formulas(content)

专门提取数学公式

**参数:**
- `content` (str): 文本内容

**返回值:**
- 公式列表，每个公式包含 LaTeX 表示和位置信息

## 高级用法

### 自定义解析配置

```python
from porosdata.parser import ParserConfig

config = ParserConfig(
    # 数学公式识别
    formula_recognition={
        'enable_latex': True,
        'enable_mathml': True,
        'confidence_threshold': 0.8
    },

    # 表格提取
    table_extraction={
        'merge_cells': True,
        'header_detection': True
    },

    # 引用处理
    citation_handling={
        'extract_bibliography': True,
        'link_citations': True
    }
)

parser = DocumentParser(config=config)
```

### 插件扩展

```python
from porosdata.parser.plugins import CustomParserPlugin

class MaterialSciencePlugin(CustomParserPlugin):
    def parse_material_data(self, content):
        # 自定义材料科学数据解析逻辑
        pass

# 注册插件
parser.register_plugin(MaterialSciencePlugin())
```

### 错误处理

```python
try:
    result = parser.parse_file("problematic_file.pdf")
except ParseError as e:
    print(f"解析错误: {e}")
    # 处理错误情况
except ValidationError as e:
    print(f"验证错误: {e}")
    # 处理验证失败
```

## 性能优化

### 大文件处理

```python
# 分块处理大文件
parser.parse_large_file(
    "large_document.pdf",
    chunk_size=1024*1024,  # 1MB 分块
    parallel=True          # 并行处理
)
```

### 内存管理

```python
# 流式处理，避免加载整个文件到内存
with parser.stream_parse("huge_file.pdf") as stream:
    for chunk in stream:
        process_chunk(chunk)
```

## 输出格式

### JSON 格式

```json
{
  "metadata": {
    "title": "研究论文标题",
    "authors": ["作者1", "作者2"],
    "language": "zh",
    "page_count": 15
  },
  "content": {
    "abstract": "摘要内容...",
    "sections": [
      {
        "title": "引言",
        "content": "引言内容...",
        "formulas": ["$E = mc^2$"],
        "citations": ["[1]", "[2]"]
      }
    ],
    "bibliography": [
      {
        "key": "[1]",
        "text": "引用条目..."
      }
    ]
  }
}
```

### 自定义输出处理器

```python
from porosdata.parser.output import CustomOutputHandler

class DatabaseOutputHandler(CustomOutputHandler):
    def save_result(self, result):
        # 保存到数据库的逻辑
        pass

parser.set_output_handler(DatabaseOutputHandler())
```