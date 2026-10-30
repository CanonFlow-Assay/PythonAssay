"""Pure, deterministic observations for the Python functional profile.

The rules intentionally operate on text. They do not claim AST, type, or runtime
truth, and are kept pure so their behavior is directly testable.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
import json
from pathlib import Path
from typing import Final


@dataclass(frozen=True, slots=True)
class Rule:
    identifier: str
    message: str
    forbidden_fragments: tuple[str, ...]


@dataclass(frozen=True, order=True, slots=True)
class Finding:
    path: str
    line: int
    column: int
    rule_id: str
    message: str


RULES: Final[tuple[Rule, ...]] = (
    Rule(
        "PYA-F001",
        "Expected domain failures are values, not raised control flow.",
        ("raise ",),
    ),
    Rule(
        "PYA-F002",
        "Domain code does not perform named filesystem, network, or console effects.",
        ("open(", "requests.", "httpx.", "urllib.", "print("),
    ),
    Rule(
        "PYA-F003",
        "Domain code does not use assertion as input validation.",
        ("assert ",),
    ),
)


def inspect_source(path: str | Path, source: str) -> tuple[Finding, ...]:
    """Return sorted observations for one source string without touching disk."""
    rendered_path = str(path)
    findings: list[Finding] = []
    for line_number, line in enumerate(source.splitlines(), start=1):
        for rule in RULES:
            match = next((line.find(fragment) for fragment in rule.forbidden_fragments if fragment in line), -1)
            if match >= 0:
                findings.append(
                    Finding(
                        path=rendered_path,
                        line=line_number,
                        column=match + 1,
                        rule_id=rule.identifier,
                        message=rule.message,
                    )
                )
    return tuple(sorted(findings))


def render_receipt(root: str | Path, scanned_files: int, findings: tuple[Finding, ...],
                   missing_evidence: tuple[str, ...] = ()) -> str:
    """Render canonical JSON suitable for a checked-in evidence comparison."""
    gaps = tuple(sorted(set(missing_evidence)))
    if scanned_files <= 0 and not gaps:
        gaps = ("No supported source files were scanned.",)
    document = {
        "findings": [asdict(finding) for finding in findings],
        "root": str(root),
        "scannedFiles": scanned_files,
        "schemaVersion": "python-assay/v0.1",
        "verdict": "Fail" if findings else "Inconclusive" if gaps else "Pass",
    }
    if gaps:
        document["missingEvidence"] = list(gaps)
    return json.dumps(document, ensure_ascii=False, separators=(",", ":"), sort_keys=True)
