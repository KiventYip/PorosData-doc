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

## Style and substance

Write for someone encountering the project without insider context; prefer stable, product-facing language over temporary internal names. Keep section structure predictable so readers and search can rely on headings, and avoid publishing obsolete scripts, private paths, or draft-only material on public pages.

## Good first tasks

Thin reference pages, glossary entries, runnable examples, tighter roadmap and changelog wording, and repair of stale cross-references all tend to merge cleanly and help readers immediately.

## Support

Raise documentation issues or suggestions via the repository issue tracker or the discussion on your pull request.

**Related pages:** [Home](../index.md) · [Roadmap](roadmap.md) · [Changelog](changelog.md)
