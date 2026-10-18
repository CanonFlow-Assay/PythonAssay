"""A functional order core: immutable values and explicit validation outcomes."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TypeAlias


@dataclass(frozen=True, slots=True)
class DraftLine:
    sku: str
    quantity: int
    unit_price_cents: int


@dataclass(frozen=True, slots=True)
class Order:
    identifier: str
    lines: tuple[DraftLine, ...]


@dataclass(frozen=True, slots=True)
class Accepted:
    order: Order


@dataclass(frozen=True, slots=True)
class Rejected:
    reason: str


OrderDecision: TypeAlias = Accepted | Rejected


def create_order(identifier: str, lines: tuple[DraftLine, ...]) -> OrderDecision:
    if not identifier.strip():
        return Rejected("order identifier is required")
    if not lines:
        return Rejected("an order needs at least one line")
    if any(not line.sku.strip() for line in lines):
        return Rejected("each line needs a SKU")
    if any(line.quantity <= 0 for line in lines):
        return Rejected("quantity must be positive")
    if any(line.unit_price_cents < 0 for line in lines):
        return Rejected("unit price cannot be negative")
    return Accepted(Order(identifier=identifier, lines=lines))


def total_cents(order: Order) -> int:
    return sum(line.quantity * line.unit_price_cents for line in order.lines)
