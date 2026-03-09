#!/usr/bin/env python3
"""
mkdocs_wrapper.py - MkDocs 包装器，过滤掉 MkDocs 2.0 兼容性警告

使用方法：
    python mkdocs_wrapper.py build
    python mkdocs_wrapper.py serve
    python mkdocs_wrapper.py --help
"""

import subprocess
import sys
import os


def run_mkdocs(args):
    """运行 MkDocs 并过滤警告"""
    try:
        # 设置 PYTHONWARNINGS 环境变量来抑制警告
        env = os.environ.copy()
        env['PYTHONWARNINGS'] = 'ignore'

        # 运行 mkdocs 命令
        result = subprocess.run(
            [sys.executable, '-m', 'mkdocs'] + args,
            capture_output=True,
            text=True,
            env=env
        )

        # 过滤掉 MkDocs 2.0 警告
        lines = result.stdout.split('\n')
        filtered_lines = []

        skip_warning = False
        for line in lines:
            # 检测警告开始
            if 'WARNING – MkDocs 2.0 is incompatible with Material for MkDocs' in line:
                skip_warning = True
                continue

            # 跳过警告块
            if skip_warning:
                if line.strip() == '' or line.startswith('│'):
                    continue
                else:
                    skip_warning = False

            filtered_lines.append(line)

        # 输出过滤后的结果
        print('\n'.join(filtered_lines))

        # 如果有 stderr，也过滤一下
        if result.stderr:
            stderr_lines = result.stderr.split('\n')
            filtered_stderr = []
            skip_warning = False

            for line in stderr_lines:
                if 'WARNING – MkDocs 2.0 is incompatible with Material for MkDocs' in line:
                    skip_warning = True
                    continue

                if skip_warning:
                    if line.strip() == '' or line.startswith('│'):
                        continue
                    else:
                        skip_warning = False

                filtered_stderr.append(line)

            if filtered_stderr:
                print('\n'.join(filtered_stderr), file=sys.stderr)

        return result.returncode

    except Exception as e:
        print(f"❌ 运行 MkDocs 时出错: {e}", file=sys.stderr)
        return 1


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法: python mkdocs_wrapper.py <command> [args...]")
        print("例如: python mkdocs_wrapper.py build --quiet")
        return 1

    # 移除脚本名，传递其余参数给 mkdocs
    args = sys.argv[1:]
    return run_mkdocs(args)


if __name__ == "__main__":
    sys.exit(main())