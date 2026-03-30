# Processor API 概览

本页是当前处理层接口的实用参考入口，重点回答三件事：
{: .lead}

- 我该调用什么
- 我该传什么
- 我会得到什么
{: .tight-list}

## 本页范围

当前仓库文档主要围绕处理层展开。对外最常用的入口可分为四类：

| 范围 | 负责内容 | 常见入口 |
|------|------|------|
| `Processor` | 文本清洗与质量整理 | `TextCleaner`、CLI `run` |
| 批处理 | 将多篇文献整理为 `processed` 结果 | `python -m porosdata_processor run` |
| 复核与验收 | 在交付前检查中间结果 | `audit`、`delivery-gate` 一类命令 |
| `Designer` 交接 | 将稳定的 `processed` 结果转入最终交付 | 作为下游阶段存在，不是本页主要代码接口 |

如果你正在寻找最终结构化交付结果，请在完成处理阶段后继续阅读 `Designer` 文档。

## 典型调用路径

最常见的使用路径是：

```text
原始论文或上游解析结果
-> TextCleaner 或批处理命令
-> processed 中间结果
-> 复核与验收
-> 下游结构化交付
```

## 最常用入口

### `TextCleaner`

当你希望在 Python 代码里清洗单段科研文本时，优先使用 `TextCleaner`。

#### 构造函数

```python
TextCleaner(pipeline=None, clean_options=None)
```

| 参数 | 类型 | 含义 |
|------|------|------|
| `pipeline` | `list | None` | 清洗插件的执行顺序 |
| `clean_options` | `dict | None` | 额外的清洗开关 |

#### 常用方法

##### `clean(text)`

使用当前配置清洗一段文本。

| 项目 | 说明 |
|------|------|
| 输入 | `text: str` |
| 返回 | `str` |
| 适用场景 | 单段文本测试、局部规则验证、嵌入式调用 |

```python
from porosdata_processor import TextCleaner

cleaner = TextCleaner()
result = cleaner.clean("The α phase appears in Fig. 1.")
print(result)
```

##### `clean_file(input_path, output_path, encoding="utf-8")`

清洗单个文件并将结果写入目标路径。

| 参数 | 类型 | 含义 |
|------|------|------|
| `input_path` | `str` | 输入文件路径 |
| `output_path` | `str` | 输出文件路径 |
| `encoding` | `str` | 文件编码，默认 `utf-8` |

| 返回 | 说明 |
|------|------|
| 输出文件 | 在 `output_path` 生成清洗后的文件 |

### 批处理 CLI

当你需要处理一个目录而不是一段文本时，优先使用命令行入口。

#### 典型命令

```bash
python -m porosdata_processor run \
  --input-dir data/raw \
  --output-dir data/processed \
  --max-workers 4
```

#### 输入与输出

| 项目 | 说明 |
|------|------|
| `--input-dir` | 原始数据或上游解析结果所在目录 |
| `--output-dir` | 中间结果输出目录 |
| `--max-workers` | 批处理并行度 |

| 输出 | 说明 |
|------|------|
| 清洗后的内容列表 | 可直接进入下一步的中间结果 |
| 复制后的图片资源 | 供后续复用的图片资产 |
| `processing_report.json` | 批处理摘要与复核依据 |

### 复核与验收命令

当批处理完成后，如果你需要判断结果是否适合交付，可以使用以下命令。

#### 质量复核

```bash
python -m porosdata_processor audit \
  --processed-dir data/processed \
  --report-file docs/audit/aiready_data_audit_result.json
```

#### 交付验收

```bash
python -m porosdata_processor delivery-gate \
  --processed-dir data/processed \
  --report-file docs/audit/delivery_gate_report.md \
  --json-file docs/audit/delivery_gate_result.json
```

这类命令更适合项目交付、整批复核和阶段性质量检查。

## 参数与行为速览

### 常用处理参数

| 选项 | 出现位置 | 含义 |
|------|------|------|
| `pipeline` | `TextCleaner(...)` | 选择或排列清洗插件 |
| `clean_options` | `TextCleaner(...)` | 打开或调整特定清洗行为 |
| `--input-dir` | CLI | 输入数据位置 |
| `--output-dir` | CLI | 中间结果输出位置 |
| `--max-workers` | CLI | 并行 worker 数量 |

### 常见返回结果

| 入口 | 返回或产出 |
|------|------|
| `clean(text)` | 一段清洗后的字符串 |
| `clean_file(...)` | 一个清洗后的文件 |
| `run` | 一组 `processed` 目录结果与批处理报告 |
| `audit` | 一份复核报告 |
| `delivery-gate` | 一份验收报告和结构化结果 |

## 异常与失败信号

Python API 在配置不正确或处理失败时，可能抛出以下两类常见异常：

| 异常 | 含义 | 常见原因 |
|------|------|------|
| `ProcessingError` | 处理失败 | 输入异常、特殊文本情况或运行失败 |
| `ConfigurationError` | 配置无效 | 参数结构错误或配置值不支持 |

```python
try:
    cleaner = TextCleaner()
    result = cleaner.clean(text)
except ProcessingError as e:
    print(f"处理失败: {e}")
except ConfigurationError as e:
    print(f"配置错误: {e}")
```

对于批处理任务，更多失败信号通常出现在日志、处理报告和交付验收结果中，而不是直接体现在单个 Python 异常里。

## 常见插件示例

常见插件名称包括：

- `citation_rules`
- `greek_to_latex`
- `normalize_whitespace`
- `latex_math_spaces`
{: .tight-list}

## 什么时候用哪个入口

| 如果你要做的是... | 推荐入口 |
|------|------|
| 在代码里清洗一段文本 | `TextCleaner.clean()` |
| 本地清洗一个文件 | `TextCleaner.clean_file()` |
| 处理一批源文件 | CLI `run` |
| 在交付前复核中间结果 | CLI `audit` |
| 判断是否满足交付条件 | CLI `delivery-gate` |

## 相关页面

- [快速开始](../get_started/quickstart.md)
- [使用示例](examples.md)
- [Processor](../tools/processor/index.md)
- [Designer](../tools/designer/index.md)