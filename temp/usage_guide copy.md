# usage guide

- doc_type: usage_guide
- status: active
- updated_at: 2026-03-18 10:15:00

## command policy

The repository uses a three-layer entry model:

- Official installed entry: `porosdata-designer`
- Official module entry: `python -m porosdata_designer`
- Repository source wrapper: `python examples/run_pipeline.py`

Legacy files under `examples/` and `scripts/` are compatibility wrappers only. They remain runnable during the transition period, but they are not the primary documented interface.

## install

```bash
pip install -e ".[dev]"
```

## run the full pipeline

Installed mode:

```bash
porosdata-designer run all --input_dir data/processed
```

Module mode:

```bash
python -m porosdata_designer run all --input_dir data/processed
```

Repository source mode:

```bash
python examples/run_pipeline.py --input_dir data/processed
```

## run individual stages

```bash
porosdata-designer run text --input_dir data/processed
porosdata-designer run multimodal --input_dir data/raw
```

Equivalent module commands:

```bash
python -m porosdata_designer run text --input_dir data/processed
python -m porosdata_designer run multimodal --input_dir data/raw
```

## audit and validate outputs

```bash
porosdata-designer audit structured
porosdata-designer validate structured
porosdata-designer validate multimodal
porosdata-designer validate acceptance
```

## test

```bash
pytest tests -v
```

## compatibility note

Legacy wrappers under `examples/` and `scripts/` still forward to the same package services during the transition period, but this guide does not list them as supported primary commands.
