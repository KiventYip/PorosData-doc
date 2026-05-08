# Python API

Public surface of the **`designer`** package for library use and tests. Import names refer to the modules shipped under `src/designer/` in the reference repository.
{: .lead}

## Convenience function

| Function | Signature (conceptual) | Returns |
|----------|-------------------------|---------|
| `aggregate_text` | `(content_list: list[dict]) -> str` | Poros-tagged aggregate string **without** the full standardiser write path |

Use the classes below when you need filtering, classification, anchoring, validation, or disk output.

## Core types (selected)

| Class | Construction | Notable methods |
|-------|--------------|-----------------|
| `ContentFilter` | `ContentFilter(config: dict \| None)` | `filter_text_blocks(content_list) -> list[dict]` |
| `ParagraphClassifier` | `ParagraphClassifier(config: dict \| None)` | `classify(text, index, total, page_idx=0, block=None) -> ParagraphType` |
| `TokenMarker` | `TokenMarker(token_config: dict \| None)` | `wrap(text, para_type) -> str` |
| `TextAggregator` | `TextAggregator(content_filter_config: dict \| None)` | `aggregate(content_list) -> str`, `get_output_schema() -> dict[str, str]` |
| `MultimodalInterleaver` | `MultimodalInterleaver(asset_io_workers=None, assets_subdir=None)` | `interleave(...) -> list[dict]`, `get_output_schema()`, `demonstrate_precision_matching(...)` |
| `ContentListAdapter` | — | `load`, `get_image_caption_texts`, `get_image_footnote_texts`, `save` |
| `SchemaValidator` | — | `validate(text) -> SchemaValidationResult` |
| `LaTeXValidator` | — | `validate_text(text) -> LaTeXValidationResult`, `should_mark_low_quality(result) -> bool` |
| `AssetAnchoringEngine` | — | `build_asset_registry(...) -> dict[str, str]`, `anchor_text(text, registry, replace_fig=True, replace_table=True) -> tuple[str, list[dict]]` |
| `DataMiningMapper` | — | `map(structured_text, metadata=None) -> DataMiningView` (`pure_text_stream`, `structured_json`, `metadata`) |
| `PluginRegistry` | — | Plugin discovery (`plugin_system.py`) |

`PorosTextStandardizer` orchestrates list loading, filtering, aggregation, optional **`AssetAnchoringEngine`**, `SchemaValidator`, `DataMiningMapper`, and writers. The CLI does **not** expose every constructor flag (for example toggling asset anchoring); set those in Python when you embed the pipeline.

## CLI entry

| Symbol | Role |
|--------|------|
| `designer.cli.main(argv=None) -> int` | Same logic as the console script |

## Related

- [Configuration](configuration.md) — defaults you can override in constructors  
- [CLI reference](cli-reference.md) — production command surface  
