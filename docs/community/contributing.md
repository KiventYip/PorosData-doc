# Contributing to PorosData Documentation

This page explains how to contribute to the `PorosData-doc` documentation site.
{: .lead}

If you want to improve runtime code or processing behavior, you may need to contribute to a separate code repository. This page is specifically for documentation work in this repository.

## What You Can Contribute

External contributors are welcome to help with:

- wording and clarity improvements
- broken links or navigation issues
- missing examples or reference details
- bilingual consistency between English and Chinese pages
- structure and readability fixes for external readers

## Minimal Documentation Workflow

### 1. Clone the Documentation Repository

```bash
git clone https://github.com/KiventYip/PorosData-doc.git
cd PorosData-doc
```

### 2. Create a Branch

```bash
git checkout -b docs/your-change-name
```

### 3. Edit the Documentation

Typical changes include:

- revising `.md` files under `docs/`
- improving wording in both English and Chinese pages
- updating links among guide, reference, and research pages

### 4. Preview Before You Submit

If your local environment is ready, use a local preview workflow for this documentation site before opening a pull request.

At minimum, check:

- page structure
- heading order
- link targets
- English and Chinese page alignment

### 5. Submit a Pull Request

Your pull request should include:

- a short summary of what changed
- why the change is needed
- the pages affected
- screenshots when layout or rendering is involved

## Writing Expectations

Documentation contributions should follow these expectations:

- write for external readers first
- prefer product-facing explanations over internal shorthand
- keep English and Chinese page structures aligned when both exist
- avoid exposing outdated internal paths, scripts, or temporary materials in public pages

## Suggested Contribution Areas

If you are looking for a good first contribution, these areas usually provide clear value:

- filling thin reference pages
- improving glossary entries
- adding runnable examples
- tightening roadmap and changelog wording
- fixing bilingual mismatches

## Need Help

For documentation issues or suggestions, use the repository issue tracker or pull request discussion in the documentation repository.

## Related Reading

- [Home](../index.md)
- [Roadmap](roadmap.md)
- [Changelog](changelog.md)