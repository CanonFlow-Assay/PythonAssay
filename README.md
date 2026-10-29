# PythonAssay

PythonAssay is a deterministic checker for a small functional Python profile. Its pure scanner reports selected lexical hazards, while the included order core demonstrates immutable data, an `Accepted | Rejected` outcome, and a fold-like total.

The repository requires [Python `3.14.7`](https://www.python.org/doc/versions/), the current stable Python release at its creation. It has no runtime dependencies and does not send source or telemetry anywhere.

```sh
python -m unittest discover -s tests -v
PYTHONPATH=src python -m python_assay.cli check examples/clean/src/domain --json
PYTHONPATH=src python -m python_assay.cli check examples/violations/src/domain
```

Read [the v0.1 contract](docs/CONTRACT.md) before using a clean result as evidence. The authoring guide is [functional-python](skills/functional-python/SKILL.md).

Licensed under Apache-2.0.

## ExpenseGuard playground

The [native ExpenseGuard playground](playground/README.md) adds requirements,
real baseline/expanded acceptance execution, isolated mutation controls, bounded
offline investigation advice and source/log freshness checks. Run:

```sh
python3 playground/run.py --output artifacts/playground/first-run
```

This experiment is separate from checker authority. Exact runtime pin gaps remain
Inconclusive even when the experiment completes; survivors remain visible.
