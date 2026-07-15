# Contributing to this documentation

This page describes how to contribute to the `PorosData-doc` site: prose, structure, navigation, and examples in this repository only.
{: .lead}

Changes to runtime behaviour or processing code usually belong in another repository; restrict pull requests here to documentation and site configuration.

## What we welcome

Contributions that improve the experience of external readers are especially valuable: clearer wording, fixed or updated internal links, missing examples or reference detail, more consistent structure across English pages, and corrections to navigation or cross-references.

## Contribution workflow

**1. Clone and enter the repository**

```bash
git clone https://github.com/KiventYip/PorosData-doc.git
cd PorosData-doc
```

**2. Use a dedicated branch**

```bash
git checkout -b docs/your-change-name
```

**3. Edit sources under `docs/`**  
Revise Markdown, tighten links between guides and reference material, and keep filenames and paths aligned with `mkdocs.yml`.

**4. Preview locally**  
Before opening a pull request, build or serve the site in your environment and check heading hierarchy, link targets, and whether new pages appear correctly in the nav.

**5. Open a pull request**  
Include a concise summary, the reason for the change, the paths affected, and screenshots if layout or theme behaviour changes.

## Blog posts from third parties

Blog essays are welcome via the same pull-request flow. Keep them in English and follow the Material blog layout used by this site.

1. Add one Markdown file under `docs/blog/posts/` (do **not** register the post in `mkdocs.yml` `nav`; the blog plugin owns post URLs).
2. Include front matter with at least `date.created`, a stable `slug`, `categories`, `tags`, and `authors`. Use `<!-- more -->` where you want the index excerpt to end.
3. If you are a new author, **append** a new id under `authors:` in `docs/blog/.authors.yml` (do not overwrite existing entries). Add an avatar under `docs/assets/images/` if needed, then reference that id in the post’s `authors` list.
4. Link the post from the **Recent posts** list in [`docs/blog/index.md`](../blog/index.md) so readers can find it from the blog landing page.
5. Preview with `mkdocs serve` (or `python build_clean.py serve`) and check the post page: title, excerpt, author card, and category links.

Use existing posts under `docs/blog/posts/` as templates when unsure about fields or tone.

## Style and substance

Write for someone encountering the project without insider context; prefer stable, product-facing language over temporary internal names. Keep section structure predictable so readers and search can rely on headings, and avoid publishing obsolete scripts, private paths, or draft-only material on public pages.

## Good first tasks

Thin reference pages, glossary entries, runnable examples, tighter roadmap and changelog wording, and repair of stale cross-references all tend to merge cleanly and help readers immediately.

## Support

Raise documentation issues or suggestions via the repository issue tracker or the discussion on your pull request.

**Related pages:** [Home](../index.md) · [Roadmap](roadmap.md) · [Changelog](changelog.md)
