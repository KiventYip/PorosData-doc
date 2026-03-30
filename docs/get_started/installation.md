# Installation

Install PorosData in the way that best fits your workflow: quick local evaluation, source-based development, or long-running server execution.
{: .lead}

## Recommended Method

For most users, start with the published package:

```bash
pip install porosdata-processor
```

This is the fastest way to verify the basic text-processing capability and run small local tests.

## Install from Source

If you need to inspect the codebase, adjust processing behavior, or test local changes, install from source:

```bash
git clone https://github.com/KiventYip/porosdata-processor.git
cd porosdata-processor
pip install -e .
```

For development environments, you can install the extended dependency set if it is available in the repository configuration.

## Environment Notes

Before installation, make sure the environment meets these basic requirements:

- Python `3.8+`
- a writable local environment or virtual environment
- enough disk space for raw, processed, and structured outputs

For larger batch projects, Linux plus SSD or NVMe storage is recommended.

## Verify the Installation

After installation, confirm that the package is available:

```python
import porosdata_processor
print(porosdata_processor.__version__)
```

If you plan to run batch jobs, also verify the command-line entry:

```bash
python -m porosdata_processor --help
```

## What to Prepare Next

After installation, prepare three things before your first run:

1. raw source documents or upstream parser results
2. a target output location for processed results
3. a small validation sample before launching a full batch

## Recommended Next Steps

- Continue with [Quick Start](quickstart.md)
- Review the [End-to-End Workflow](end-to-end-workflow.md)
- See [Examples](../references/examples.md) for common usage patterns

## Quick Links

- [Home](../index.md)
- [Quick Start](../get_started/quickstart.md)
{: .tight-list}
