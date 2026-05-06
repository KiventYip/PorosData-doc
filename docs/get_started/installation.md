# Installation

Choose an install path that matches how you intend to use PorosData: a quick check from PyPI, a source checkout for development, or a server-style batch environment.
{: .lead}

**PyPI (recommended for most users)** — install the published package to confirm behaviour and run small experiments:

```bash
pip install porosdata-processor
```

**Source checkout** — use when you need to read or change implementation details, or to test unpublished fixes:

```bash
git clone https://github.com/KiventYip/porosdata-processor.git
cd porosdata-processor
pip install -e .
```

If the repository documents an optional “full” or development extra, install it in the same environment when you run tests or CI locally.

**Environment** — use Python 3.8 or newer, preferably inside a virtual environment with enough disk space for raw, intermediate, and structured outputs. For sustained batch work, Linux on SSD or NVMe is usually more predictable than a laptop disk under heavy I/O.

**Sanity checks** — after install, confirm the package imports and, if you rely on the CLI, that the module entry responds:

```python
import porosdata_processor
print(porosdata_processor.__version__)
```

```bash
python -m porosdata_processor --help
```

**Before the first real run** — line up (1) source documents or parser artefacts, (2) a writable output root, and (3) a small sample you can reprocess until results look stable.

**Next:** [Quick Start](quickstart.md) · [End-to-End Workflow](end-to-end-workflow.md) · [Examples](examples.md) · [Home](../index.md)
