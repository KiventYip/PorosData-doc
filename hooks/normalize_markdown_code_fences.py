"""
Collapse redundant blank lines inside fenced Markdown code blocks at build time.

Authors sometimes leave large gaps inside ```...``` regions, which hurts scanability.
This hook trims leading/trailing empty lines and replaces runs of multiple blank lines
with a single blank line, without altering non-fence Markdown.
"""

from __future__ import annotations

import re

_OPEN_FENCE = re.compile(r"^(\s*)(```+)([^`\n]*)\s*$")
_CLOSE_FENCE = re.compile(r"^\s*(```+)\s*$")


def _normalize_body_lines(raw_lines: list[str]) -> list[str]:
    logical = [ln.rstrip("\r\n") for ln in raw_lines]
    while logical and logical[0].strip() == "":
        logical.pop(0)
    while logical and logical[-1].strip() == "":
        logical.pop()
    out: list[str] = []
    prev_blank = False
    for line in logical:
        blank = line.strip() == ""
        if blank:
            if not prev_blank:
                out.append("")
            prev_blank = True
        else:
            out.append(line)
            prev_blank = False
    return [ln + "\n" for ln in out]


def _normalize_fenced_code(markdown: str) -> str:
    lines = markdown.splitlines(keepends=True)
    i = 0
    chunks: list[str] = []

    while i < len(lines):
        line = lines[i]
        m = _OPEN_FENCE.match(line.rstrip("\r\n"))
        if m is None:
            chunks.append(line)
            i += 1
            continue

        tick_len = len(m.group(2))
        if tick_len > 3:
            chunks.append(line)
            i += 1
            continue

        block_prefix = [line]
        i += 1
        body: list[str] = []
        closed = False
        while i < len(lines):
            cur = lines[i]
            cm = _CLOSE_FENCE.match(cur.rstrip("\r\n"))
            if cm is not None and len(cm.group(1)) >= tick_len:
                normalized_body = _normalize_body_lines(body)
                chunks.extend(block_prefix)
                chunks.extend(normalized_body)
                chunks.append(cur)
                i += 1
                closed = True
                break
            body.append(cur)
            i += 1

        if not closed:
            chunks.extend(block_prefix)
            chunks.extend(body)

    return "".join(chunks)


def on_page_markdown(markdown, page, config, **kwargs):
    return _normalize_fenced_code(markdown)
