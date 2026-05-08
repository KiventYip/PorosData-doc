# Troubleshooting

Symptoms map to code paths in the reference `designer` package. Adjust messages if your fork changes logging text.
{: .lead}

## Log levels (selected)

| Level | Message pattern (approx.) | Typical cause |
|-------|----------------------------|---------------|
| error | `Input directory does not exist` | `--input_dir` path missing |
| error | `No content_list.json files found` | No `*_content_list.json` under the tree |
| error | `Error processing document {doc_id}` | Per-document exception inside a run |
| warning | `Schema validation: doc=…` | `SchemaValidator` found blocking issues |
| warning | `tqdm is not installed` | Progress bar dependency missing |
| warning | `Processing interrupted by user` | Ctrl+C |
| exception | `An error occurred…` / `Execution failed` | Uncaught error at pipeline boundary |
| warning | `content_list_path was not provided; skipping multimodal export materialization` | Output dir set without a list path for asset copy |
| warning | `Source image does not exist` / `skipping copy` | Bad `img_path` |
| warning | `Image copy failed` / `Fallback copy also failed` | IO or permission problems |
| error | validate / delivery family | Missing directories, no JSON matches, assertion-style validation failures |

## `validate structured` failures

| Symptom | What to inspect |
|---------|-----------------|
| Missing keys or invalid JSON | Regenerate `content.json` or merge fields manually |
| Joined `content` missing `</s>` or `<poros_doc>` | `TextAggregator` training post-process |
| Empty `pure_text_stream` | Mapper input / empty aggregate |
| `<br>` present | Remove at source or add an explicit normalisation step (not currently in aggregator) |
| `content` / `pure_text_stream` not lists | Writer expects arrays; do not hand-edit to a single JSON string |

## Structured view oddities

| Symptom | Likely cause |
|---------|--------------|
| `sections` empty | No `<poros_section_*>` matched; headings never classified as section opens |
| `pure_text_stream` still shows `poros_*` | Tag outside `_ALL_POROS_TAGS` stripping, or non-standard tag names |
| Broken image index paths | `img_path` not relative to the list file’s parent |
| `asset_copied` false | Missing source image or `safe_copy_image` failure |
| `poros_asset` missing in text | Anchoring engine only replaces ids present in the image registry |
| `link` in `structure.json` points to missing files | Long `fig_id` hashed to `image_{md5}` on disk while `link` still uses `images/{type}_{ref}.jpg` |

## Related

- [Validation and audit](validation-and-audit.md) — which command to rerun  
- [Multimodal](multimodal.md) — filename and path details  
