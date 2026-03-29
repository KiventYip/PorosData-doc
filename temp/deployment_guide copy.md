# PorosData-Designer deployment guide

- doc_type: deployment_guide
- status: active
- updated_at: 2026-03-18 10:15:00

本文档只说明部署、后台运行、日志与环境准备。命令口径与 `docs/usage_guide.md` 保持一致，不再单独定义另一套入口体系。

## 前置条件

- Linux 服务器，建议 Ubuntu 20.04+ 或同级发行版
- Python `>=3.8`，建议 `3.10+`
- 首次安装依赖时可联网

检查 Python：

```bash
python3 --version
```

## 上传仓库

推荐直接克隆仓库：

```bash
git clone <your-repo-url>
cd datadesigning
```

如果手动上传，至少保留这些目录：

```text
datadesigning/
├── pyproject.toml
├── src/
├── examples/
├── docs/
├── scripts/
└── data/
```

以下目录可以不传：

- `logs/`
- `data/structured/`
- `.git/`
- `__pycache__/`

## 安装

```bash
cd /home/user/datadesigning
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -e .
python -c "import porosdata_designer; print('install ok')"
python -m porosdata_designer --help
```

## 输入数据要求

输入目录下需要能递归找到 `*_content_list.json` 文件；图片资源应与对应内容列表一起保留。输入目录既可以是仓库内的 `data/raw`、`data/processed`，也可以是服务器上的任意绝对路径。

## 运行命令

正式入口优先使用包级 CLI。

全流程：

```bash
porosdata-designer run all --input_dir /home/user/my_input_data
```

模块态等价命令：

```bash
python -m porosdata_designer run all --input_dir /home/user/my_input_data
```

源码态仓库包装入口：

```bash
python examples/run_pipeline.py --input_dir /home/user/my_input_data
```

仅全文本结构化：

```bash
porosdata-designer run text --input_dir /home/user/my_input_data
```

仅多模态提取：

```bash
porosdata-designer run multimodal --input_dir /home/user/my_input_data
```

## 自定义输出与日志目录

```bash
porosdata-designer run all \
  --input_dir /home/user/my_input_data \
  --output_dir /data/results/structured \
  --log_dir /data/results/logs
```

## 后台运行

使用 `nohup`：

```bash
nohup porosdata-designer run all \
  --input_dir /home/user/my_input_data \
  --output_dir /data/results/structured \
  --log_dir /data/results/logs \
  > /data/results/run.out 2>&1 &
```

使用 `screen`：

```bash
screen -S designer
cd /home/user/datadesigning
source venv/bin/activate
porosdata-designer run all \
  --input_dir /home/user/my_input_data \
  --output_dir /data/results/structured \
  --log_dir /data/results/logs
```

## 输出结构

```text
data/structured/
├── full_text/
│   └── <doc_id>/
│       ├── <doc_id>_structured.json
│       └── <doc_id>_structured.txt
├── datamining/
│   └── <doc_id>/
│       └── <doc_id>_datamining.json
└── multimodal/
    └── <doc_id>/
        ├── <doc_id>_index.json
        ├── assets/
        └── fig_*.md
```

## 日志

默认日志写入 `logs/`，常见文件名包括：

```text
run_all_YYYY-MM-DD.log
run_text_standardization_YYYY-MM-DD.log
run_multimodal_extraction_YYYY-MM-DD.log
validate_structured_output_YYYY-MM-DD.log
validate_multimodal_output_YYYY-MM-DD.log
final_acceptance_validation_YYYY-MM-DD.log
```

查看日志：

```bash
tail -50 /data/results/logs/run_all_YYYY-MM-DD.log
tail -f /data/results/logs/run_all_YYYY-MM-DD.log
```

## 部署后校验

```bash
porosdata-designer audit structured
porosdata-designer validate structured
porosdata-designer validate multimodal
porosdata-designer validate acceptance
pytest tests -v
```

## 常见问题

`ModuleNotFoundError: No module named 'porosdata_designer'`

- 确认已激活虚拟环境
- 确认执行过 `pip install -e .`
- 确认当前目录是仓库根目录，或使用已安装的 `porosdata-designer`

`No content_list.json files found`

- 检查 `--input_dir`
- 检查输入目录是否真的包含 `*_content_list.json`
- 检查数据是否解压完整

SSH 断开后任务中止

- 使用 `nohup`、`screen` 或 `tmux`
- 确认日志目录和输出目录有写权限
