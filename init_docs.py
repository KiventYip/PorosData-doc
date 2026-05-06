#!/usr/bin/env python3
"""
init_docs.py - Auto-create missing documentation files referenced by the site.

What it does:
- Scans mkdocs.yml nav and all Markdown files for internal links.
- Creates missing English placeholder files under docs/ with sensible templates.
- Helps keep `mkdocs build` warning-free for newly referenced pages.

Usage:
    python init_docs.py              # Scan and create missing files
    python init_docs.py --dry-run    # Preview only; print files that would be created
    python init_docs.py --force      # Recreate placeholders even if files exist
"""

import re
import argparse
from pathlib import Path
from typing import Set, List, Tuple

import yaml


class DocsInitializer:
    """Create missing documentation files referenced by nav or in-page links."""

    def __init__(self, docs_dir: str = "docs", mkdocs_config: str = "mkdocs.yml"):
        self.docs_dir = Path(docs_dir)
        self.mkdocs_config = Path(mkdocs_config)
        self.created_files: Set[Path] = set()

        # Templates use docs-root-relative links (no leading slash, no '../')
        # so generated placeholders work regardless of their depth under docs/.
        self.templates = {
            'en': {
                'default': """# {title}

This page is under development.

## Overview

Content coming soon...

## Quick Links

- [Home](index.md)
- [Quick Start](get_started/quickstart.md)
""",
                'api': """# {title}

This API documentation is under development.

## Classes

## Functions

## Examples

```python
# Example usage will be added here
pass
```

## Quick Links

- [Home](index.md)
- [API Reference](community/api-reference.md)
""",
                'guide': """# {title}

This guide is under development.

## Prerequisites

## Step-by-Step Instructions

## Examples

## Troubleshooting

## Next Steps

## Quick Links

- [Home](index.md)
- [Quick Start](get_started/quickstart.md)
- [Blog](blog/index.md)
"""
            }
        }

    def extract_links_from_mkdocs(self) -> Set[str]:
        """Extract all .md targets from the nav section of mkdocs.yml."""
        links: Set[str] = set()

        if not self.mkdocs_config.exists():
            print(f"[warn] config file {self.mkdocs_config} does not exist")
            return links

        try:
            with open(self.mkdocs_config, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)

            def extract_from_nav(nav_section):
                if isinstance(nav_section, dict):
                    for _, value in nav_section.items():
                        if isinstance(value, str) and value.endswith('.md'):
                            links.add(value)
                        elif isinstance(value, list):
                            for item in value:
                                extract_from_nav(item)
                elif isinstance(nav_section, list):
                    for item in nav_section:
                        extract_from_nav(item)
                elif isinstance(nav_section, str) and nav_section.endswith('.md'):
                    links.add(nav_section)

            if 'nav' in config:
                extract_from_nav(config['nav'])

        except Exception as e:
            print(f"[error] failed to parse mkdocs.yml: {e}")

        return links

    def extract_links_from_markdown(self) -> Set[str]:
        """Extract internal Markdown links across docs/."""
        links: Set[str] = set()
        markdown_pattern = re.compile(r'\[([^\]]+)\]\(([^)]+\.md(?:#.*?)?)\)')

        for md_file in self.docs_dir.rglob("*.md"):
            try:
                with open(md_file, 'r', encoding='utf-8') as f:
                    content = f.read()

                for match in markdown_pattern.finditer(content):
                    link = match.group(2)
                    if link.startswith(('http://', 'https://', '#')):
                        continue
                    link = link.split('#')[0]
                    if link.startswith('../'):
                        current_dir = md_file.parent.relative_to(self.docs_dir)
                        resolved_path = (current_dir / Path(link)).resolve()
                        try:
                            relative_path = resolved_path.relative_to(self.docs_dir)
                            links.add(str(relative_path))
                        except ValueError:
                            pass
                    elif link.startswith('./'):
                        links.add(str((md_file.parent / link[2:]).relative_to(self.docs_dir)))
                    else:
                        links.add(link)

            except Exception as e:
                print(f"[warn] failed to read {md_file}: {e}")

        return links

    def get_missing_files(self) -> List[Tuple[str, str]]:
        """Return a list of (relative_path, language) for files that are missing."""
        missing_files: List[Tuple[str, str]] = []

        config_links = self.extract_links_from_mkdocs()
        markdown_links = self.extract_links_from_markdown()
        all_links = config_links.union(markdown_links)

        for link in all_links:
            en_file = self.docs_dir / link
            if not en_file.exists():
                missing_files.append((link, 'en'))

        return missing_files

    def create_file_template(self, file_path: str, language: str) -> str:
        """Pick a template based on the path and render it with a derived title."""
        path_obj = Path(file_path)
        file_name = path_obj.stem

        if 'api' in file_path.lower():
            template_type = 'api'
        elif 'guide' in file_path.lower():
            template_type = 'guide'
        else:
            template_type = 'default'

        title = file_name.replace('-', ' ').replace('_', ' ').title()

        return self.templates[language][template_type].format(title=title)

    def create_missing_files(self, missing_files: List[Tuple[str, str]],
                             dry_run: bool = False, force: bool = False) -> None:
        """Create placeholder files on disk."""
        for file_path, language in missing_files:
            full_path = self.docs_dir / file_path

            if full_path.exists() and not force:
                continue

            if dry_run:
                print(f"[plan] would create: {file_path} ({language})")
                continue

            try:
                full_path.parent.mkdir(parents=True, exist_ok=True)

                content = self.create_file_template(file_path, language)

                with open(full_path, 'w', encoding='utf-8') as f:
                    f.write(content)

                self.created_files.add(full_path)
                print(f"[ok] created: {file_path}")

            except Exception as e:
                print(f"[error] failed to create {file_path}: {e}")

    def run(self, dry_run: bool = False, force: bool = False) -> None:
        """Scan and create missing files."""
        print("[info] scanning documentation links...")
        missing_files = self.get_missing_files()

        if not missing_files:
            print("[info] no missing files detected")
            return

        print(f"[info] {len(missing_files)} missing file(s) detected")

        self.create_missing_files(missing_files, dry_run=dry_run, force=force)

        if not dry_run and self.created_files:
            print(f"\n[info] created {len(self.created_files)} file(s)")
            print("\nNext steps:")
            print("  - Edit the new files and add real content")
            print("  - Run 'mkdocs serve' to verify rendering")
            print("  - Commit the changes")


def main():
    parser = argparse.ArgumentParser(
        description="Auto-create missing documentation files referenced by mkdocs.yml or in-page links",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python init_docs.py              # Scan and create missing files
  python init_docs.py --dry-run    # Preview only
  python init_docs.py --force      # Force regenerate placeholders
        """
    )

    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Preview mode; print files that would be created without writing them'
    )

    parser.add_argument(
        '--force',
        action='store_true',
        help='Regenerate placeholder content even if the file already exists'
    )

    parser.add_argument(
        '--docs-dir',
        default='docs',
        help='Path to the docs directory (default: docs)'
    )

    parser.add_argument(
        '--config',
        default='mkdocs.yml',
        help='Path to the mkdocs config file (default: mkdocs.yml)'
    )

    args = parser.parse_args()

    initializer = DocsInitializer(args.docs_dir, args.config)
    initializer.run(dry_run=args.dry_run, force=args.force)


if __name__ == "__main__":
    main()
