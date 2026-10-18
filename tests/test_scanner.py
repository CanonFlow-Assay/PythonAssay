from __future__ import annotations

import json
import unittest

from python_assay.domain import Accepted, DraftLine, Rejected, create_order, total_cents
from python_assay.scanner import inspect_source, render_receipt


class ScannerTests(unittest.TestCase):
    def test_pure_discriminated_outcome_is_clean(self) -> None:
        source = "def decide(quantity: int) -> Accepted | Rejected:\n    return Accepted(quantity)"
        self.assertEqual(inspect_source("domain/order.py", source), ())

    def test_selected_hazards_have_stable_locations(self) -> None:
        source = "raise ValueError('bad')\nprint('effect')\nassert quantity > 0"
        findings = inspect_source("domain/order.py", source)
        self.assertEqual([finding.rule_id for finding in findings], ["PYA-F001", "PYA-F002", "PYA-F003"])
        self.assertEqual([finding.line for finding in findings], [1, 2, 3])

    def test_receipt_is_canonical_json(self) -> None:
        findings = inspect_source("domain/order.py", "print('effect')")
        first = render_receipt("examples/clean", 1, findings)
        self.assertEqual(first, render_receipt("examples/clean", 1, findings))
        self.assertEqual(json.loads(first)["verdict"], "Fail")


class DomainTests(unittest.TestCase):
    def test_valid_order_calculates_total_without_mutation(self) -> None:
        outcome = create_order("order-42", (DraftLine("book", 2, 1250),))
        self.assertIsInstance(outcome, Accepted)
        if isinstance(outcome, Accepted):
            self.assertEqual(total_cents(outcome.order), 2500)

    def test_invalid_order_returns_a_rejection_value(self) -> None:
        outcome = create_order("", ())
        self.assertEqual(outcome, Rejected("order identifier is required"))
