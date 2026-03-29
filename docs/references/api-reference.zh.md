# API 参考

## 核心类

### TextCleaner

文本清洗操作的核心类。

#### 构造函数

```python
TextCleaner(pipeline=None, clean_options=None)
```

**参数：**
- `pipeline` (list, 可选): 要应用的清洗插件列表
- `clean_options` (dict, 可选): 额外的清洗选项
{: .tight-list}

#### 方法

##### clean(text)

使用配置的流水线清洗输入文本。

**参数：**
- `text` (str): 要清洗的输入文本
{: .tight-list}

**返回值：**
- `str`: 清洗后的文本
{: .tight-list}

**示例：**
```python
cleaner = TextCleaner()
result = cleaner.clean("包含 $公式$ 的原始文本")
```

##### clean_file(input_path, output_path, encoding='utf-8')

清洗文件并保存结果。

**参数：**
- `input_path` (str): 输入文件路径
- `output_path` (str): 输出文件路径
- `encoding` (str): 文件编码 (默认: 'utf-8')
{: .tight-list}

## 插件

### 可用的插件

- `citation_rules`: 标准化引用格式
- `greek_to_latex`: 将希腊字母转换为 LaTeX
- `normalize_whitespace`: 清理间距问题
- `latex_math_spaces`: 移除数学公式中的额外空格
{: .tight-list}

### 自定义插件

创建自定义插件：
{: .section-intro}

```python
from porosdata_processor.plugins.base import BasePlugin

class MyPlugin(BasePlugin):
    def process(self, text):
        # 你的处理逻辑
        return processed_text
```

## 异常

### ProcessingError

文本处理失败时抛出。
{: .section-intro}

```python
try:
    result = cleaner.clean(text)
except ProcessingError as e:
    print(f"处理失败: {e}")
```

### ConfigurationError

配置无效时抛出。
{: .section-intro}

```python
try:
    cleaner = TextCleaner(invalid_config)
except ConfigurationError as e:
    print(f"配置错误: {e}")
```