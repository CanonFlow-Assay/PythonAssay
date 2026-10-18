from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Accepted:
    quantity: int


@dataclass(frozen=True, slots=True)
class Rejected:
    reason: str


def decide(quantity: int) -> Accepted | Rejected:
    if quantity <= 0:
        return Rejected("quantity must be positive")
    return Accepted(quantity)
