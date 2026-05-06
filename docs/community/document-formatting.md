# Document Formatting Guide

This guide standardizes body presentation without changing the existing documentation structure.

## Page Opening

- Start each page with one short lead paragraph after the H1 or the introductory H2 block.
- Keep the lead paragraph to 1 to 3 sentences that answer what the page covers and why it matters.
- Apply the `lead` utility class to that paragraph.

```md
PorosData organizes scientific document processing into a delivery-ready workflow.
{: .lead}
```

## Section Rhythm

- Start each major section with one short bridge sentence before a list, table, or diagram.
- Apply the `section-intro` utility class when the sentence is there only to guide reading rhythm.
- Keep each paragraph focused on one idea.

```md
These links are the fastest way to understand the workflow.
{: .section-intro}
```

## Emphasis Rules

- Use bold for principles, key judgments, or named concepts.
- Use inline code for package names, fields, directories, commands, and file formats.
- Do not bold full sentences or entire list items.

## Lists And Tables

- Prefer one idea per list item.
- Use `tight-list` for short navigation lists or compact capability summaries.
- Keep tables scan-friendly: short labels on the left, explanations on the right.

```md
- [Quick Start](docs/get_started/quickstart.md)
- [Examples](docs/get_started/examples.md)
{: .tight-list}
```

## Admonitions

- Use `tip` for recommended reading paths or starting points.
- Use `note` for scope boundaries and terminology.
- Use `warning` only for limitations, risks, or easy-to-misread behavior.
- Avoid stacking multiple admonitions in one short page section.
