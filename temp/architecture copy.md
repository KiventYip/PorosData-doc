# architecture

- doc_type: architecture
- status: active
- updated_at: 2026-03-18 10:15:00

## repository layout

- `data/raw`: 上游原始 MinerU 产物。
- `data/processed`: 下游可复用的中间处理数据。
- `data/structured`: Designer 最终交付的结构化产物。
- `examples/`: 仓库源码态包装入口与兼容入口。
- `scripts/`: 审计、验证、验收的兼容包装。
- `src/porosdata_designer/cli.py`: 正式 CLI 分发层。
- `src/porosdata_designer/runtime/pipelines.py`: 运行编排层，承载 `run all/text/multimodal`。
- `src/porosdata_designer/runtime/commands.py`: 审计与校验命令服务层。
- `src/porosdata_designer/reorganizers`: 文本重组与结构识别。
- `src/porosdata_designer/validators`: schema 与 LaTeX 校验。
- `src/porosdata_designer/mappers`: 资产锚定与数据挖掘映射。
- `tests/unit`, `tests/integration`, `tests/fixtures`: 顶层测试体系。

## entry model

The repository now uses three entry layers:

1. Official CLI layer:
   `porosdata-designer` and `python -m porosdata_designer`
2. Repository wrapper layer:
   `examples/run_pipeline.py`
3. Internal implementation layer:
   `src/porosdata_designer/runtime/pipelines.py` and `src/porosdata_designer/runtime/commands.py`

This keeps installed mode, module mode, and repository mode aligned while moving real orchestration out of `examples/` and `scripts/`.

## pipeline flow

1. `data/raw` 提供原始内容列表与图片资源。
2. `data/processed` 提供可供 Designer 复用的标准化中间输入。
3. CLI 把运行请求分发到包内编排层，生成 `data/structured/full_text`、`data/structured/datamining`、`data/structured/multimodal`。
4. CLI 再调用包内校验服务，对结构化结果执行审计、验证与验收。