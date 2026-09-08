# D10-U10i run log

Date: 2026-09-08. Only the new boundary_exponential_limit directory was
modified. No commits, shared-index edits, remote computation, dependency
installation, GPU use, or child agents.

Replay from this directory, using standard Python 3.11+:

```text
python sanity.py
```

Execution history:

1. An initial read requested a nonexistent proof_or_blocker.md in the older
   boundary unit; that read command exited 1. The actual analysis.md was
   then located by the scoped inventory and fully read. No files changed.
2. The first independent script run exited 1 before completing a gate:
   its generic determinant base returned Fraction(1), causing a TypeError
   when the same routine was used on Decimal matrices. The one-line repair
   changed the empty determinant value to the scalar integer 1, valid in
   both arithmetic domains. No mathematical formula or sample changed.
3. The repaired run exited 0: 3/3 rational Möbius gates and 28/28 exponential
   points passed.
4. A final clean replay after adding explicit failure history to the JSON
   also exited 0 with the same results. Per-case failures are zero; the
   initial runtime failure is not hidden by that statistic.

Arithmetic: Fraction for independent small-dimensional event jets and LDL;
Decimal at 180 digits for logarithms and the stable positive-matrix inverse.
The local Decimal exponent range is enlarged to retain exp(-beta/x) without
underflow. No process-wide dependency or system environment was modified.
The input profile is not imported or used as a cached answer.

Frozen hashes:

| File | SHA256 |
| --- | --- |
| frozen_problem.md | 2f86c0f1859050d78c50e7b33a2addb1d60473fd24722089b4f4549d8ee35ad0 |
| proof_candidate.md | 52106879f3f522828fbdc834e6c15ba7d12f4f74242ab3a8bd306a4211ea54c4 |
| sanity.py | a18da3c948a4fa15ca0b0bb3d2d8c7bddb885d1e4bd32c6fe6869df0101e8d3e |
| sanity.json | e9acbefb654f6b3442f4ab797580beff269c9ad64726d2ddacd4c61650146b5b |

New limit/compact-wedge conclusions are author proof candidates awaiting a
fresh non-author audit. Finite computations are SCOUT. The full original
path domain and noncompact beta(x) regimes remain INCOMPLETE.
