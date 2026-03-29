# 部署指南

[English Version](deployment_guide.md)

## 环境要求

- Python 3.8+
- 建议内存 8 GB 及以上
- 建议使用多核 CPU 以支持并行批处理

## 需要复制的内容

优先直接复制仓库根目录。运行时关键内容包括：

- `src/porosdata_processor/`
- `run_processor.py`
- `examples/run_pipeline.py`
- `pyproject.toml`
- `scripts/`
- 按需携带 `data/`

通常可排除：

- `tests/`
- `.pytest_cache/`
- `__pycache__/`
- `.git/`

## 安装步骤

```bash
git clone <repo-url> /opt/datapreprocessing
cd /opt/datapreprocessing
python3 -m venv venv
source venv/bin/activate
pip install .
```

调试阶段可使用可编辑安装：

```bash
pip install -e .
```

## 基本运行

正式入口优先使用：

- `porosdata-processor`
- `python -m porosdata_processor`

示例：

```bash
python -m porosdata_processor run \
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

## 日志与输出

默认输出：

- 处理结果目录：`data/processed`
- 处理报告：`data/processed/processing_report.json`

默认日志：

- `logs/processor.log`

自定义日志目录：

```bash
export POROS_LOGS_PATH=/var/log/porosdata
```

## 推荐操作

### 审计处理结果

```bash
python -m porosdata_processor audit \
    --processed-dir data/processed \
    --report-file docs/audit/aiready_data_audit_result.json
```

### 交付前执行门禁

```bash
python -m porosdata_processor delivery-gate \
    --processed-dir data/processed \
    --report-file docs/audit/delivery_gate_report.md \
    --json-file docs/audit/delivery_gate_result.json
```

## 后台运行

### `nohup`

```bash
nohup python -m porosdata_processor run \
    --input-dir /data/mineru_raw \
    --output-dir /data/cleaned \
    --max-workers 8 \
    > nohup_output.log 2>&1 &
```

### `screen` / `tmux`

建议在受管终端会话中运行同样的命令，以便处理中长时间任务。

### `systemd`

如需稳定的生产环境运行与失败自动重启，可封装为 `systemd` 服务。

## 常见问题

- 如果 `transformers` 相关评估失败，可移除 `--enable-evaluation` 或补装依赖。
- 如果内存占用偏高，请降低 `--max-workers`。
- 如果批处理被中断，重新执行相同命令即可；除非显式使用 `--force-reprocess`，否则增量机制会跳过未变化输出。
