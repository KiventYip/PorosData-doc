# Multimodal extraction

How figure rows are built, copied, and named. Read this section before you assume `structure.json` **`link`** fields always match bytes on disk.
{: .lead}

## Filename stabilisation

`_build_filename_base(fig_id)`:

- If `len(str(fig_id)) <= 3`, files use the prefix `fig_{fig_id}` (for example `fig_1.jpg`).  
- Otherwise the base becomes `image_{md5[:8]}` where **MD5** is taken over the UTF-8 bytes of the string `fig_id` (not SHA-256).

Extension and directory layout still follow the interleaver / writer defaults (`images/` subfolder unless overridden in code).

## Where source images resolve

During materialisation, **`content_list_path.parent`** is the root for **relative** `img_path` values from the list JSON. There is **no** automatic switch between **Raw Database** and **Processed Database** trees—the paths stored upstream decide which tree is read. If copies fail, check that `img_path` is correct relative to the list file that Designer loaded.

## Mentions and captions

1. **Registry** — scans text for figure-reference patterns, collects candidate mention blocks, and binds list entries that carry captions or inferred `fig_id`.  
2. **Per-item context** — chooses a caption from image metadata or neighbouring blocks; gathers sentence-level **mentions** with a compiled regex over registered blocks.  
3. **Materialisation** — copies bytes into `{output_dir}/images/` and updates `image_path`, `markdown_file`, and `asset_copied`.

## `asset_refs.link` vs multimodal filenames

`structure.json` always injects:

`link = "images/{type}_{ref}.jpg"`

using the **table/figure reference token** from anchoring. The multimodal writer may instead emit **`image_{hash}.jpg`** for long `fig_id` values. In edge cases the **JSON link and the real filename can diverge**; downstream code should prefer the multimodal index and disk listing as the source of truth for bytes, and treat `structure.json` links as a **convention** tied to short, sanitised ids.

## Related

- [Output artefacts](output-artifacts.md) — index JSON fields  
- [Troubleshooting](troubleshooting.md) — missing images and `asset_copied: false`  
