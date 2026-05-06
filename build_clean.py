#!/usr/bin/env python3
"""
build_clean.py - Run mkdocs commands while filtering known noisy warnings.

Currently filters the multi-line "MkDocs 2.0 is incompatible with Material for
MkDocs" warning block, which is non-actionable on the pinned 1.x stack.
"""

import subprocess
import sys
import os


def run_command(cmd):
    """Run a command and stream its output, suppressing the MkDocs 2.0 warning block."""
    try:
        env = os.environ.copy()
        env['PYTHONWARNINGS'] = 'ignore'

        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            env=env,
        )

        in_warning = False

        while True:
            line = process.stdout.readline()
            if not line:
                break

            stripped = line.strip()
            if not in_warning and (
                ('WARNING' in line and 'MkDocs 2.0' in line)
                or 'MkDocs 2.0 introduces backward-incompatible' in line
                or (stripped.startswith('│') and 'MkDocs 2.0' in line)
                or stripped == '│'
            ):
                in_warning = True
                continue

            if in_warning:
                if stripped in ('', '│') or stripped.startswith('│'):
                    continue
                if (
                    'MkDocs 2.0' in line
                    or '×' in line
                    or 'squidfunk.github.io' in line
                    or 'Our full analysis' in line
                ):
                    continue
                in_warning = False

            print(line, end='', flush=True)

        process.wait()
        return process.returncode

    except Exception as e:
        print(f"[error] failed to run command: {e}", file=sys.stderr)
        return 1


def main():
    args = sys.argv[1:]

    if not args:
        print("Usage: python build_clean.py <mkdocs_command> [args...]")
        print("Examples:")
        print("  python build_clean.py build --quiet")
        print("  python build_clean.py serve")
        return 1

    cmd = [sys.executable, '-m', 'mkdocs'] + args

    print("[info] running:", ' '.join(cmd))
    print("[info] filtering MkDocs 2.0 compatibility warnings\n")

    return run_command(cmd)


if __name__ == "__main__":
    sys.exit(main())
