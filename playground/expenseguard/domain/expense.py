"""Pure ExpenseGuard decisions; all effects belong to the harness."""
from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class Approved:
    amount: int

@dataclass(frozen=True, slots=True)
class NeedsReview:
    amount: int

@dataclass(frozen=True, slots=True)
class Invalid:
    reason: str

type Decision = Approved | NeedsReview | Invalid

def decide(amount: int, currency: str, memo: str, limit: int) -> Decision:
    if limit <= 0:
        return Invalid("policy")
    if amount <= 0:
        return Invalid("amount")
    if currency != "USD":
        return Invalid("currency")
    if not memo.strip():
        return Invalid("memo")
    if amount > limit:
        return NeedsReview(amount)
    return Approved(amount)
