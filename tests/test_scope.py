import contextlib
import io
import json
from pathlib import Path
import tempfile
import unittest

from python_assay.cli import main
from python_assay.scanner import inspect_source, render_receipt


class ScopeTests(unittest.TestCase):
    def invoke(self, root):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            code = main(["check", str(root), "--json"])
        return code, json.loads(output.getvalue())

    def test_empty_and_missing_scope_never_pass(self):
        with tempfile.TemporaryDirectory() as temporary:
            for root in (Path(temporary), Path(temporary) / "missing"):
                code, receipt = self.invoke(root)
                self.assertEqual((code, receipt["verdict"]), (2, "Inconclusive"))
                self.assertTrue(receipt["missingEvidence"])

    def test_linked_root_file_and_directory_are_incomplete(self):
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            source = base / "source"; source.mkdir()
            outside = base / "outside"; outside.mkdir()
            (outside / "clean.py").write_text("value = 1\n")
            for name, target in (("file.py", outside / "clean.py"), ("directory", outside)):
                link = source / name
                link.symlink_to(target)
                self.assertEqual(self.invoke(source)[1]["verdict"], "Inconclusive")
                link.unlink()
            link = base / "root-link"; link.symlink_to(outside)
            self.assertEqual(self.invoke(link)[0], 2)

    def test_bad_utf8_and_oversized_sources_never_pass(self):
        with tempfile.TemporaryDirectory() as temporary:
            source = Path(temporary) / "source.py"
            source.write_bytes(b"\xff")
            self.assertEqual(self.invoke(source.parent)[0], 2)
            with source.open("wb") as stream:
                stream.truncate(4 * 1024 * 1024 + 1)
            self.assertEqual(self.invoke(source.parent)[0], 2)

    def test_known_findings_remain_fail_when_other_evidence_is_missing(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "bad.py").write_text("raise ValueError()\n")
            (root / "unreadable.py").write_bytes(b"\xff")
            code, receipt = self.invoke(root)
            self.assertEqual((code, receipt["verdict"]), (1, "Fail"))
            self.assertTrue(receipt["findings"])
            self.assertTrue(receipt["missingEvidence"])

    def test_nonempty_clean_and_violating_scopes_keep_old_exit_meanings(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary); source = root / "domain.py"
            source.write_text("value = 1\n")
            self.assertEqual(self.invoke(root)[0], 0)
            source.write_text("raise ValueError()\n")
            self.assertEqual(self.invoke(root)[0], 1)

    def test_pure_receipt_cannot_grant_pass_for_zero_observed_files(self):
        self.assertEqual(json.loads(render_receipt("empty", 0, ()))["verdict"], "Inconclusive")
        findings = inspect_source("known.py", "raise ValueError()")
        self.assertEqual(json.loads(render_receipt("partial", 0, findings))["verdict"], "Fail")
