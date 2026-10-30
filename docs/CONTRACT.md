# PythonAssay v0.1 contract

PythonAssay scans Python files beneath the supplied directory and produces sorted findings. `check` exits `0` when none of its selected fragments are found, `1` when a finding exists, and `2` when source cannot be read. `--json` emits a canonical receipt without timestamps, hostnames, or absolute-path normalization.

The v0.1 rules observe `raise`, selected filesystem/network/console fragments, and `assert` in domain code. This is lexical evidence: comments, aliases, syntax trees, types, imports, and runtime behavior are outside its scope. A pass is not a claim of purity, correctness, security, or complete functional style.

## Scope-completeness increment (29 October 2026)

A missing or empty supported-source scope returns Inconclusive (exit 2). The shell refuses symbolic-link roots/ancestors and entries, nonregular source files, traversal/enumeration failures, malformed UTF-8 and unsupported size/depth/count limits. Limits are 10,000 source files, 64 directory levels, 4 MiB per file and 64 MiB total. A known lexical finding remains Fail (exit 1) even when another input is incomplete. JSON retains findings and adds `missingEvidence` when needed. Existing nonempty complete Pass/Fail receipts retain their schema and rule meanings.

The pure receipt renderer also refuses to grant Pass for zero observed files. The shell assumes a trusted local, quiescent filesystem; it is not a hostile-host sandbox or semantic compiler. Existing lexical false positives, aliases/macros/comments and runtime limitations remain.
