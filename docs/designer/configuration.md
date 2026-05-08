# Configuration

Designer behaviour is driven mainly by **Python constants and dicts** in `designer/runtime/config.py`. There is **no** separate business YAML/TOML file in the reference package.
{: .lead}

## Notable defaults

| Name | Kind | Default / shape | Role |
|------|------|-----------------|------|
| `DEFAULT_DESIGNED_OUTPUT_DIR_NAME` | `str` | `"Designed Database"` | Last segment of the default output root under `data/` |
| `TAG_PREFIX` | `str` | `"poros_"` | Prefix for all custom tags |
| `TRAINING_CONFIG` | `dict` | `append_eos` true, `eos_token` `"</s>"`, whitespace and EOS normalisation flags | Final text shaping for training-oriented exports |
| `DEFAULT_SEPARATOR_CONFIG` | `dict` | Abstract / keywords / main-text separator strings | Reserved / documentation-oriented; not all paths read it |
| `DEFAULT_CLASSIFIER_CONFIG` | `dict` | Thresholds and labels for `ParagraphClassifier` | Merged with runtime overrides |
| `DEFAULT_FILTER_CONFIG` | `dict` | Includes `include_images` default `False` for `ContentFilter` | Block filtering before aggregation |
| Misc. sets | constants | `NON_CHEMICAL_ABBREVIATIONS`, article-info heuristics, physical-quantity subscripts, context keywords | Chemistry detection and noise control |

## Multimodal class defaults

`MultimodalInterleaver` accepts **`asset_io_workers`** (defaults to a small cap based on CPU count) and **`assets_subdir`** (defaults to `"images"`). These are **constructor parameters only**; the published CLI does not expose them.

## Paths recap

| Concern | Default |
|---------|---------|
| Output root | `get_project_root() / "data" / DEFAULT_DESIGNED_OUTPUT_DIR_NAME` when `--output_dir` / `--root_dir` omitted |
| Logs | `get_project_root() / "logs"` when `--log_dir` omitted |

## Related

- [CLI reference](cli-reference.md) — flags that override paths  
- [Python API](python-api.md) — how to pass configs into classes  
