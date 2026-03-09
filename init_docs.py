#!/usr/bin/env python3
"""
init_docs.py - 自动化文档初始化和死链修复脚本

功能特性：
- 扫描 mkdocs.yml 和所有 Markdown 文件中的链接
- 自动创建缺失的文档文件 (英文和中文版本)
- 生成基础模板，包含适当的标题和导航占位符
- 零警告构建保证，确保本地预览和 CI/CD 流水线畅通

使用方法：
    python init_docs.py              # 扫描并修复所有死链
    python init_docs.py --dry-run    # 预览模式，只显示将要创建的文件
    python init_docs.py --force      # 强制重新生成所有占位文件

作者：PorosData 文档架构师
"""

import os
import re
import yaml
import argparse
from pathlib import Path
from typing import Set, Dict, List, Tuple
from urllib.parse import urlparse


class DocsInitializer:
    """文档初始化器 - 自动创建缺失的文档文件"""

    def __init__(self, docs_dir: str = "docs", mkdocs_config: str = "mkdocs.yml"):
        self.docs_dir = Path(docs_dir)
        self.mkdocs_config = Path(mkdocs_config)
        self.created_files: Set[Path] = set()

        # 基础模板
        self.templates = {
            'en': {
                'default': """# {title}

This page is under development.

## Overview

Content coming soon...

## Quick Links

- [Home](../index.md)
- [Quick Start](../quickstart.md)
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

- [Home](../index.md)
- [API Reference](../api-reference.md)
""",
                'guide': """# {title}

This guide is under development.

## Prerequisites

## Step-by-Step Instructions

## Examples

## Troubleshooting

## Next Steps

## Quick Links

- [Home](../index.md)
- [Guides](../guides/)
"""
            },
            'zh': {
                'default': """# {title}

此页面正在开发中。

## 概述

内容即将发布...

## 快速链接

- [首页](../index.md)
- [快速开始](../quickstart.md)
""",
                'api': """# {title}

此 API 文档正在开发中。

## 类

## 函数

## 示例

```python
# 示例代码将在这里添加
pass
```

## 快速链接

- [首页](../index.md)
- [API 参考](../api-reference.md)
""",
                'guide': """# {title}

此指南正在开发中。

## 前置要求

## 逐步说明

## 示例

## 故障排除

## 下一步

## 快速链接

- [首页](../index.md)
- [指南](../guides/)
"""
            }
        }

    def extract_links_from_mkdocs(self) -> Set[str]:
        """从 mkdocs.yml 中提取所有导航链接"""
        links = set()

        if not self.mkdocs_config.exists():
            print(f"⚠️  配置文件 {self.mkdocs_config} 不存在")
            return links

        try:
            with open(self.mkdocs_config, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)

            def extract_from_nav(nav_section):
                """递归提取导航中的链接"""
                if isinstance(nav_section, dict):
                    for key, value in nav_section.items():
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
            print(f"❌ 解析 mkdocs.yml 时出错: {e}")

        return links

    def extract_links_from_markdown(self) -> Set[str]:
        """从所有 Markdown 文件中提取内部链接"""
        links = set()
        markdown_pattern = re.compile(r'\[([^\]]+)\]\(([^)]+\.md(?:#.*?)?)\)')

        for md_file in self.docs_dir.rglob("*.md"):
            try:
                with open(md_file, 'r', encoding='utf-8') as f:
                    content = f.read()

                # 查找所有 Markdown 链接
                for match in markdown_pattern.finditer(content):
                    link = match.group(2)
                    # 只处理相对链接，不包含 http/https
                    if not link.startswith(('http://', 'https://', '#')):
                        # 移除锚点部分
                        link = link.split('#')[0]
                        # 转换为相对于 docs/ 的路径
                        if link.startswith('../'):
                            # 处理上级目录引用
                            current_dir = md_file.parent.relative_to(self.docs_dir)
                            resolved_path = (current_dir / Path(link)).resolve()
                            try:
                                relative_path = resolved_path.relative_to(self.docs_dir)
                                links.add(str(relative_path))
                            except ValueError:
                                pass  # 超出 docs/ 目录的链接忽略
                        elif link.startswith('./'):
                            links.add(str((md_file.parent / link[2:]).relative_to(self.docs_dir)))
                        else:
                            links.add(link)

            except Exception as e:
                print(f"⚠️  读取文件 {md_file} 时出错: {e}")

        return links

    def get_missing_files(self) -> List[Tuple[str, str]]:
        """获取所有缺失的文件列表 (文件路径, 语言)"""
        missing_files = []

        # 从配置和文档中提取所有链接
        config_links = self.extract_links_from_mkdocs()
        markdown_links = self.extract_links_from_markdown()
        all_links = config_links.union(markdown_links)

        for link in all_links:
            # 检查英文版本
            en_file = self.docs_dir / link
            if not en_file.exists():
                missing_files.append((link, 'en'))

            # 检查中文版本 (对于非中文文件)
            if not link.endswith('.zh.md'):
                zh_link = link.replace('.md', '.zh.md')
                zh_file = self.docs_dir / zh_link
                if not zh_file.exists():
                    missing_files.append((zh_link, 'zh'))

        return missing_files

    def create_file_template(self, file_path: str, language: str) -> str:
        """根据文件路径和语言生成合适的模板"""
        path_obj = Path(file_path)
        file_name = path_obj.stem

        # 根据路径判断文件类型
        if 'api' in file_path.lower():
            template_type = 'api'
        elif 'guide' in file_path.lower():
            template_type = 'guide'
        else:
            template_type = 'default'

        # 生成标题
        title = file_name.replace('-', ' ').replace('_', ' ').title()

        return self.templates[language][template_type].format(title=title)

    def create_missing_files(self, missing_files: List[Tuple[str, str]], dry_run: bool = False, force: bool = False) -> None:
        """创建缺失的文件"""
        for file_path, language in missing_files:
            full_path = self.docs_dir / file_path

            if full_path.exists() and not force:
                continue

            if dry_run:
                print(f"📄 将创建: {file_path} ({language})")
                continue

            try:
                # 确保目录存在
                full_path.parent.mkdir(parents=True, exist_ok=True)

                # 生成内容
                content = self.create_file_template(file_path, language)

                # 写入文件
                with open(full_path, 'w', encoding='utf-8') as f:
                    f.write(content)

                self.created_files.add(full_path)
                print(f"✅ 已创建: {file_path}")

            except Exception as e:
                print(f"❌ 创建文件 {file_path} 时出错: {e}")

    def run(self, dry_run: bool = False, force: bool = False) -> None:
        """运行文档初始化"""
        print("🔍 扫描文档链接...")
        missing_files = self.get_missing_files()

        if not missing_files:
            print("🎉 没有发现缺失的文件！")
            return

        print(f"📋 发现 {len(missing_files)} 个缺失文件")

        self.create_missing_files(missing_files, dry_run=dry_run, force=force)

        if not dry_run and self.created_files:
            print(f"\n🎯 成功创建 {len(self.created_files)} 个文件")
            print("\n💡 提示:")
            print("   - 编辑新创建的文件，添加具体内容")
            print("   - 运行 'mkdocs serve' 验证文档构建")
            print("   - 提交更改到版本控制")


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="自动化文档初始化和死链修复脚本",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  python init_docs.py              # 扫描并修复所有死链
  python init_docs.py --dry-run    # 预览模式
  python init_docs.py --force      # 强制重新生成
        """
    )

    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='预览模式，只显示将要创建的文件，不实际创建'
    )

    parser.add_argument(
        '--force',
        action='store_true',
        help='强制重新生成所有占位文件，即使文件已存在'
    )

    parser.add_argument(
        '--docs-dir',
        default='docs',
        help='文档目录路径 (默认: docs)'
    )

    parser.add_argument(
        '--config',
        default='mkdocs.yml',
        help='MkDocs 配置文件路径 (默认: mkdocs.yml)'
    )

    args = parser.parse_args()

    # 初始化
    initializer = DocsInitializer(args.docs_dir, args.config)

    # 执行
    initializer.run(dry_run=args.dry_run, force=args.force)


if __name__ == "__main__":
    main()