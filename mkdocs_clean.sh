#!/bin/bash
# mkdocs_clean.sh - 干净运行 MkDocs，过滤掉已知警告

# 设置环境变量抑制警告
export PYTHONWARNINGS=ignore

# 运行 MkDocs 命令，过滤掉 MkDocs 2.0 警告
"$@" 2>&1 | grep -v "WARNING – MkDocs 2.0 is incompatible with Material for MkDocs" | \
             grep -v "^│" | \
             grep -v "^│$" | \
             grep -v "https://squidfunk.github.io/mkdocs-material/blog/2026/02/18/mkdocs-2.0/" | \
             cat