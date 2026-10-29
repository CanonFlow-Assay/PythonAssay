"""The filesystem-owning shell for PythonAssay."""

from __future__ import annotations

import argparse
import os
from pathlib import Path
import stat
import sys

from .scanner import Finding, inspect_source, render_receipt

MAX_FILES = 10_000
MAX_DEPTH = 64
MAX_FILE_BYTES = 4 * 1024 * 1024
MAX_TOTAL_BYTES = 64 * 1024 * 1024


def source_files(root: Path) -> tuple[list[Path], tuple[str, ...]]:
    """Enumerate a bounded regular-file scope without following links."""
    absolute = root.absolute()
    if any(path.is_symlink() for path in (absolute, *absolute.parents)):
        return [], ("Source root or an ancestor is a symbolic link.",)
    if not root.is_dir():
        return [], ("Source directory is missing or unreadable.",)
    files: list[Path] = []
    errors: list[str] = []
    for directory, directories, names in os.walk(root, followlinks=False,
            onerror=lambda _: errors.append("A source directory could not be enumerated.")):
        current = Path(directory)
        if len(current.relative_to(root).parts) > MAX_DEPTH:
            return [], ("Source directory depth exceeds the supported limit.",)
        file_names = set(names)
        for name in sorted(directories + names):
            path = current / name
            if path.is_symlink():
                return [], ("Symbolic links make the declared source scope incomplete.",)
            if name in file_names and path.suffix == ".py":
                try:
                    if not stat.S_ISREG(path.stat().st_mode):
                        return [], ("Source inputs must be regular files.",)
                except OSError:
                    return [], ("Source metadata could not be read.",)
                files.append(path)
                if len(files) > MAX_FILES:
                    return [], ("Source file count exceeds the supported limit.",)
    return sorted(files), tuple(sorted(set(errors)))


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
    findings: list[Finding] = []
    files, gaps = source_files(root)
    scanned = 0
    total_bytes = 0
    for path in files:
        try:
            with path.open("rb") as stream:
                data = stream.read(MAX_FILE_BYTES + 1)
            total_bytes += len(data)
            if len(data) > MAX_FILE_BYTES or total_bytes > MAX_TOTAL_BYTES:
                gaps += ("Source bytes exceed the supported scope limit.",)
                break
            findings.extend(inspect_source(path, data.decode("utf-8")))
            scanned += 1
        except (OSError, UnicodeError):
            gaps += ("Source could not be read as UTF-8.",)
    if not scanned and not gaps:
        gaps = ("No supported source files were scanned.",)

    stable_findings = tuple(sorted(findings))
    if parsed.json_output:
        print(render_receipt(root, scanned, stable_findings, gaps))
    elif stable_findings:
        for finding in stable_findings:
            print(f"{finding.path}:{finding.line}:{finding.column} {finding.rule_id} {finding.message}")
    elif gaps:
        print("Inconclusive: " + "; ".join(sorted(set(gaps))))
    else:
        print(f"Pass: {scanned} Python files scanned.")
    return 1 if stable_findings else 2 if gaps else 0


if __name__ == "__main__":
    raise SystemExit(main())
