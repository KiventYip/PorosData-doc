---
description: >-
  Release highlights, design notes, and engineering updates from the documentation project.
---

# Blog

Short, dated notes sit here when a new handbook chapter would be heavy-handed: release context, design trade-offs, and engineering notes. The site is English-only; each post is one Markdown file under `docs/blog/posts/`.

Start procedures in [Quick Start](../get_started/quickstart.md); vocabulary and principles in [Design Philosophy](../community/design-philosophy.md). Longer narrative—e.g. [Research Review](posts/2026-05-06-research-review.md) and [Design Insights](posts/2026-05-06-design-insights.md)—lives in posts, not in the manuals.

The [Changelog](../community/changelog.md) lists factual documentation moves and milestones. The blog can explain *why* something changed without copying every changelog line.

RSS is emitted when the build runs with **`CI=true`** (as in publishing). A plain `mkdocs serve` often skips the RSS plugin; that is normal locally.

**See also:** [Changelog](../community/changelog.md) · [Contributing](../community/contributing.md)

## Recent posts

- [Research Review](posts/2026-05-06-research-review.md)
- [Design Insights](posts/2026-05-06-design-insights.md)
- [Mapping the pipeline to the docs](posts/2026-04-18-pipeline-docs-overview.md)
