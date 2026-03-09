#!/usr/bin/env python3
"""
build_clean.py - 干净构建文档，过滤掉已知警告
"""

import subprocess
import sys
import os


def run_command(cmd):
    """运行命令并过滤输出"""
    try:
        # 设置环境变量
        env = os.environ.copy()
        env['PYTHONWARNINGS'] = 'ignore'

        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            env=env
        )

        # 实时过滤输出
        warning_lines = []
        in_warning = False

        while True:
            line = process.stdout.readline()
            if not line:
                break

            # 检测警告开始
            if 'WARNING – MkDocs 2.0 is incompatible with Material for MkDocs' in line:
                in_warning = True
                continue

            # 如果在警告块中，跳过相关行
            if in_warning:
                if line.strip() == '' or line.startswith('│') or 'squidfunk.github.io' in line:
                    continue
                else:
                    # 警告块结束
                    in_warning = False

            # 正常输出
            print(line, end='', flush=True)

        process.wait()
        return process.returncode

    except Exception as e:
        print(f"❌ 运行命令时出错: {e}", file=sys.stderr)
        return 1


def main():
    """主函数"""
    # 获取命令行参数
    args = sys.argv[1:]

    if not args:
        print("用法: python build_clean.py <mkdocs_command>")
        print("例如: python build_clean.py build --quiet")
        print("      python build_clean.py serve")
        return 1

    # 构建完整命令
    cmd = [sys.executable, '-m', 'mkdocs'] + args

    print("🚀 运行命令:", ' '.join(cmd))
    print("📝 过滤 MkDocs 2.0 兼容性警告...\n")

    return run_command(cmd)


if __name__ == "__main__":
    sys.exit(main())