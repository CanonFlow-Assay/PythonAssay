"""The filesystem-owning shell for PythonAssay."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

from .scanner import Finding, inspect_source, render_receipt


def parser() -> argparse.ArgumentParser:
    command_parser = argparse.ArgumentParser(prog="python-assay")
    subcommands = command_parser.add_subparsers(dest="command", required=True)
    check = subcommands.add_parser("check", help="scan Python source below a directory")
    check.add_argument("directory", type=Path)
    check.add_argument("--json", action="store_true", dest="json_output")
    return command_parser


def main(arguments: list[str] | None = None) -> int:
    parsed = parser().parse_args(arguments)
    root: Path = parsed.directory
    if not root.is_dir():
        print(f"python-assay: not a directory: {root}", file=sys.stderr)
        return 2

    findings: list[Finding] = []
    files = sorted(path for path in root.rglob("*.py") if path.is_file())
    for path in files:
        try:
            findings.extend(inspect_source(path, path.read_text(encoding="utf-8")))
        except OSError as error:
            print(f"python-assay: cannot read {path}: {error}", file=sys.stderr)
            return 2

    stable_findings = tuple(sorted(findings))
    if parsed.json_output:
        print(render_receipt(root, len(files), stable_findings))
    elif stable_findings:
        for finding in stable_findings:
            print(f"{finding.path}:{finding.line}:{finding.column} {finding.rule_id} {finding.message}")
    else:
        print(f"Pass: {len(files)} Python files scanned.")
    return 0 if not stable_findings else 1


if __name__ == "__main__":
    raise SystemExit(main())
