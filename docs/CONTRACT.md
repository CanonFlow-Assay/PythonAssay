# PythonAssay v0.1 contract

PythonAssay scans Python files beneath the supplied directory and produces sorted findings. `check` exits `0` when none of its selected fragments are found, `1` when a finding exists, and `2` when source cannot be read. `--json` emits a canonical receipt without timestamps, hostnames, or absolute-path normalization.

The v0.1 rules observe `raise`, selected filesystem/network/console fragments, and `assert` in domain code. This is lexical evidence: comments, aliases, syntax trees, types, imports, and runtime behavior are outside its scope. A pass is not a claim of purity, correctness, security, or complete functional style.
