#!/usr/bin/env python3
"""
fix_links.py - 修复自动生成文档文件中的链接问题

问题：init_docs.py 生成的文件使用了 '../' 相对链接，但这些文件实际在 docs/ 根目录中
解决：移除不必要的 '../' 前缀，使链接指向正确的文件
"""

import os
import re
from pathlib import Path


def fix_links_in_file(file_path):
    """修复单个文件中的链接"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 修复相对链接
        # 将 '../index.md' 替换为 'index.md'
        # 将 '../quickstart.md' 替换为 'quickstart.md'
        # 将 '../index.zh.md' 替换为 'index.zh.md'
        # 将 '../quickstart.zh.md' 替换为 'quickstart.zh.md'
        original_content = content

        content = re.sub(r'\.\./index\.md', 'index.md', content)
        content = re.sub(r'\.\./quickstart\.md', 'quickstart.md', content)
        content = re.sub(r'\.\./index\.zh\.md', 'index.zh.md', content)
        content = re.sub(r'\.\./quickstart\.zh\.md', 'quickstart.zh.md', content)

        # 如果内容有变化，写入文件
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True

    except Exception as e:
        print(f"❌ 处理文件 {file_path} 时出错: {e}")

    return False


def main():
    """主函数"""
    docs_dir = Path('docs')
    fixed_count = 0

    if not docs_dir.exists():
        print("❌ docs/ 目录不存在")
        return

    # 扫描所有 .md 文件
    for md_file in docs_dir.rglob('*.md'):
        if fix_links_in_file(md_file):
            print(f"✅ 修复了: {md_file}")
            fixed_count += 1

    if fixed_count > 0:
        print(f"\n🎯 成功修复 {fixed_count} 个文件的链接")
    else:
        print("ℹ️  没有发现需要修复的链接")


if __name__ == "__main__":
    main()