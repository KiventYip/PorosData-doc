# PorosData Documentation

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Documentation Status](https://readthedocs.org/projects/porosdata-doc/badge/?version=latest)](https://porosdata-doc.readthedocs.io/en/latest/)

**PorosData** is a comprehensive scientific data processing suite for AI for Science applications. Our ecosystem includes:

- **PorosData-Parser**: High-quality parsing for PDF, HTML, and scientific documents
- **PorosData-Processor**: Intelligent text cleaning with LaTeX protection and academic standardization
- **PorosData-Designer**: Data annotation, fine-tuning, and training data generation

## 📖 Documentation

Complete documentation is available at: [https://porosdata-doc.readthedocs.io/en/latest/](https://porosdata-doc.readthedocs.io/en/latest/)

## 🚀 Quick Start

Please refer to the [Installation Guide](docs/installation.md) and [Quick Start](docs/quickstart.md).

## 🏗️ Documentation Repository Structure

This guide explains the MkDocs-based documentation repository architecture, helping contributors understand file responsibilities and modification workflows.

### 🗺️ File System Mapping

| Path | Responsibility | Key Files |
|------|----------------|-----------|
| `docs/` | **Content Root** - All documentation source files | `*.md`, `*.zh.md`, `index.md` |
| `docs/assets/` | **Assets Layer** - CSS, JS, images, and custom resources | `custom.css`, `mathjax.js`, logos |
| `mkdocs.yml` | **Configuration Engine** - Controls themes, extensions, navigation, and i18n | MkDocs settings, material config |
| `site/` | **Output Layer** - Generated HTML (auto-created, don't edit) | `html/` output |

### ✍️ Developer Modification Guide

#### **Scenario A: Adding New Documentation**
- **Create**: New `.md` file in appropriate directory (e.g., `docs/tools/parser/index.md`)
- **Register**: Add to `mkdocs.yml` under the `nav` section
- **Build**: Run `python build_clean.py serve` to verify navigation and preview locally

#### **Scenario B: Modifying Theme Styling**
- **Edit**: `docs/assets/stylesheets/custom.css` for color, font, and layout changes
- **Register**: Ensure `custom.css` is listed in `mkdocs.yml` `extra_css` array
- **Apply**: Changes take effect immediately via live reload

#### **Scenario C: Multi-language Support (i18n)**
- **Create Translation**: For `file.md`, create a sibling file `file.zh.md`
- **Link Rule**: All internal links in BOTH `.md` and `.zh.md` MUST point to the base `.md` format. The i18n plugin handles the routing automatically.

### 🔧 Quick Workflow Reference

1. **Content Changes**: Edit `.md` files → live reload handles it → commit
2. **Style Changes**: Edit `custom.css` → live reload handles it → commit
3. **Structure Changes**: Edit `mkdocs.yml` → restart server if necessary → commit

**Pro Tip**: Always run `python build_clean.py serve` locally before committing to catch formatting errors early!

## 🤝 Contributing

We welcome contributions! Please read our [Contributing Guide](docs/community/contributing.md).

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.