# PorosData Documentation

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Documentation Status](https://readthedocs.org/projects/porosdata-doc/badge/?version=latest)](https://porosdata-doc.readthedocs.io/en/latest/)

**PorosData** is a scientific data-processing stack aimed at AI-for-science workflows. The ecosystem currently centres on:

- **PorosData-Parser** — parsing for PDF, HTML, and scientific documents  
- **PorosData-Processor** — text cleaning with LaTeX-aware handling and academic normalisation  
- **PorosData-Designer** — annotation, fine-tuning support, and training-data preparation  

The published manual lives at [porosdata-doc.readthedocs.io](https://porosdata-doc.readthedocs.io/en/latest/).

## Local setup and preview

Read the [Installation Guide](docs/get_started/installation.md) and [Quick Start](docs/get_started/quickstart.md) for content-oriented onboarding.

Install **all** dependencies from the repository root into the **same** Python environment you use for `mkdocs serve` or `mkdocs build`; a split environment commonly surfaces errors such as a missing `rss` plugin.

```bash
pip install -r requirements.txt
```

## Repository layout

| Path | Role |
|------|------|
| `docs/` | Authoritative Markdown sources (`*.md`) |
| `docs/assets/` | Styles, scripts, images (e.g. `custom.css`, `mathjax.js`, branding) |
| `mkdocs.yml` | Theme, plugins, and navigation (English-only; Material blog + hooks) |
| `site/` | Generated output (do not edit by hand) |

**Adding a page:** create the `.md` file under `docs/`, register it in the `nav` section of `mkdocs.yml`, then run `python build_clean.py serve` (or `mkdocs serve`) to confirm navigation and rendering.

**Adjusting appearance:** edit `docs/assets/stylesheets/custom.css` and ensure that file remains listed under `extra_css` in `mkdocs.yml`.

**Day-to-day workflow:** content changes reload with the dev server; structural edits to `mkdocs.yml` may require a restart. Running `python build_clean.py serve` before you commit helps catch formatting and plugin issues early.

## Contributing and licence

Contributions are welcome; see [docs/community/contributing.md](docs/community/contributing.md). This project is released under the MIT Licence — refer to [LICENSE](LICENSE) for the full text.
