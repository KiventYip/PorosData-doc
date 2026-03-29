# 使用指南

[English Version](usage_guide.md)

## 项目定位

PorosData-Processor 用于将 MinerU OCR 输出转换为适合 LLM 使用的科学文本，同时尽量保护公式、引用和结构信息。

## 快速开始

### Python API

```python
from porosdata_processor import TextCleaner

cleaner = TextCleaner()
result = cleaner.clean("The α phase appears in Section IV.")
print(result)
```

### 批量处理

```bash
porosdata-processor \
    --input-dir data/raw \
    --output-dir data/processed \
    --max-workers 4
```

源码仓中的等价入口：

```bash
python examples/run_pipeline.py \
    --input-dir data/raw \
    --output-dir data/processed
```

## 规则工作流命令

### 初始化候选规包

```bash
python -m porosdata_processor bootstrap-candidate \
    --audit-file docs/audit/aiready_data_audit_result.json \
    --issue-type decimal_break
```

该命令会根据审计问题推断目标正式规包，并生成：

- 候选 TOML 规包
- 配套样本 JSON 模板

### 验证候选规则

```bash
python -m porosdata_processor sample-validate \
    --sample-file data/samples/rule_eval_samples.template.json \
    --candidate-pack src/porosdata_processor/rules/candidates/normalize_terms_candidate.toml \
    --report-file docs/rules/reports/normalize_terms_candidate.md
```

### 采纳验证通过的规则

```bash
python -m porosdata_processor promote-rule \
    --candidate-pack src/porosdata_processor/rules/candidates/normalize_terms_candidate.toml
```

`promote-rule` 会按规则 ID 增量合并，并在 `docs/rules/backups/` 下保留备份。

### 审计处理结果

```bash
python -m porosdata_processor audit \
    --processed-dir data/processed \
    --report-file docs/audit/aiready_data_audit_result.json
```

### 执行交付门禁

```bash
python -m porosdata_processor delivery-gate \
    --processed-dir data/processed \
    --report-file docs/audit/delivery_gate_report.md \
    --json-file docs/audit/delivery_gate_result.json
```

PowerShell 快捷入口：

```powershell
scripts/run_delivery_gate.ps1
```

## 处理流程

```text
原始文本
 -> _pre_shield_processing
 -> Shield.protect
 -> Pipeline steps
 -> Shield.restore
 -> _post_shield_processing
 -> LLM-ready text
```

`local_text_compression` 在 Shield 之前执行，因为它需要直接访问原始 `$...$` 数学片段。

## 注意事项

- 质量保障和 token 评估模式会增加运行时间。
- `clean_stream` 适用于更简单的流式场景，不提供完整的 Shield 行为。
- 大批量运行前建议先在样本集上验证配置。
- 服务器部署请参考 `docs/deployment_guide_cn.md`。
