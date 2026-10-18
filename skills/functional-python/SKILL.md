---
name: functional-python
description: Build Python changes as immutable domain data and explicit union outcomes, with filesystem, network, and presentation effects owned by adapters.
---

# Functional Python

Use frozen, slotted dataclasses for domain values. Make expected failure a returned `Accepted | Rejected` value rather than an exception; reserve exceptions for irrecoverable program or adapter failures. Keep domain functions deterministic and pass dependencies such as clocks, stores, and clients through adapter boundaries.

At a boundary, parse untrusted data once, validate it, and construct trusted values. Do not use `assert` for user-facing validation. Tests should name both an accepted value and a rejected value and should not depend on global time, a network, or filesystem state.
