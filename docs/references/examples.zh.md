# 使用示例

本页提供可直接起步的最小示例。每个示例都包含可复制命令、输入目录示意、预期输出，以及失败时优先检查的位置。
{: .lead}

## 示例一：单篇论文试跑

适合先验证一篇文献的处理效果，再决定是否扩展到整批数据。

### 适用场景

- 先检查一篇论文的质量整理效果
- 先确认术语、公式和图表引用是否稳定

### 最小命令

```bash
python -m porosdata_processor run \
  --input-dir data/raw \
  --output-dir data/processed \
  --max-workers 1
```

### 输入目录示意

```text
data/
└── raw/
    └── 00001/
        ├── 00001.pdf
        └── ...上游解析文件...
```

### 预期输出

```text
data/
└── processed/
    ├── processing_report.json
    └── 00001/
        └── ...清洗后的中间结果...
```

### 预期产物

- 一份单篇中间结果
- 一份用于快速查看的处理报告

### 失败时先看哪里

- `data/raw` 是否包含完整源数据
- `data/processed` 是否可写
- 处理报告或日志里是否提示缺少源文件

## 示例二：批量处理

适合将多篇论文整理成一批稳定的中间结果。

### 适用场景

- 项目中包含多篇论文
- 团队需要先得到统一的 `processed` 结果，再进入最终交付

### 最小命令

```bash
python -m porosdata_processor run \
  --input-dir data/raw \
  --output-dir data/processed \
  --max-workers 4
```

### 输入目录示意

```text
data/
└── raw/
    ├── 00001/
    ├── 00002/
    └── 00003/
```

### 预期输出

```text
data/
└── processed/
    ├── processing_report.json
    ├── 00001/
    ├── 00002/
    └── 00003/
```

### 预期产物

- 每篇文献对应一份 `processed` 结果
- 一份汇总整批运行情况的处理报告

### 失败时先看哪里

- 各源目录结构是否一致
- 当前机器的并行度是否设置过高
- 处理报告中是否存在跳过项或失败项

## 示例三：构建可复核的交付包

适合接收方既需要可阅读结果，也需要结构化交付结果的场景。

### 适用场景

- 产品、数据和研究团队需要共享同一交付包
- 交付结果既要支持阅读，也要支持抽取和复核

### 最小命令

```bash
python -m porosdata_processor run \
  --input-dir data/raw \
  --output-dir data/processed \
  --max-workers 4
```

```bash
porosdata-designer run all --input_dir data/processed
```

### 输入目录示意

```text
data/
├── raw/
└── processed/
```

### 预期输出

```text
data/
└── structured/
    ├── full_text/
    ├── datamining/
    └── multimodal/
```

### 预期产物

- 可直接阅读的全文结果
- 纯文本流
- 结构化 JSON 结果
- 用于图文对应的多模态索引
- 用于追溯的批处理报告

### 失败时先看哪里

- `processed` 中间结果是否完整稳定
- `structured` 目录是否按预期生成
- 处理报告和校验结果中是否存在未解决的问题

## 相关页面

- [安装指南](../get_started/installation.md)
- [快速开始](../get_started/quickstart.md)
- [端到端工作流](../get_started/end-to-end-workflow.md)
- [Processor](../tools/processor/index.md)
- [Designer](../tools/designer/index.md)

## 快速链接

- [首页](../index.md)
- [快速开始](../get_started/quickstart.md)
{: .tight-list}
