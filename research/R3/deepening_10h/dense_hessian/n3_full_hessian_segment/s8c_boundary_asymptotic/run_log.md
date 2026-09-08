# D10-S8c run log

Scope: only this new directory was written. Date: 2026-09-08. All commands ran from the repository root. No remote computation, subprocess agents, or system dependency changes were used.

Command (Python runtime selected explicitly):

```text
& 'C:/Users/UIO/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe' research/R3/deepening_10h/dense_hessian/n3_full_hessian_segment/s8c_boundary_asymptotic/boundary_probe.py
```

No random seed is needed: the family, basis, h attempts and bisection interval are fixed. The only floating-point operation is proposal of a rational inverse-Cholesky preconditioner. Exact acceptance uses rational bounds. OpenBLAS threads are fixed to one. Log series length is 24; preconditioner denominator cap is 4096; all resulting rational endpoints and margins retain their full denominators in JSON. Bridge depth cap is 10 and node cap 2047; actual processed nodes 11.

Execution history:

1. Initial asymptotic/tail script: exit 0; h=1/100 failed, h=1/1000 and h=1/10000 passed; finite boundary block passed.
2. First bridge extension: exit 1 on a nonpositive Horner atom lower bound at the coarse bridge root. This was interval overestimation, not an invalid actual atom or a curvature counterexample. No replacement JSON was written by that failed execution.
3. Bridge revised to retain that rejected node and subdivide: exit 0; 6 accepted leaves, 5 rejected internal nodes, 0 failed final leaves.
4. Final run added full tail matrices and exact jet/basis checks: exit 0, elapsed 5.51375126838684 seconds. It retained all three h attempts and bridge rejection records.
5. A read-only JSON summary command initially exited 1 due to Python's default 4300-digit integer parsing limit. Repeating with sys.set_int_max_str_digits(0) exited 0; the probe already sets this, and no result changed.

Frozen source SHA256:

boundary_probe.py: fcdba3f63661f4f20143f9267b652635c8571f291e7c5f88cc508577849a545a

boundary_probe_results.json: 2c257777b29d33b38c1ae5de9c2e0aba775bf43e13ab5038dfbf41c361ee45da

Read-only dependency ../verifications/fresh_s8_audit.py: 2eba997abe32602ac1e8139a9ccaa09999a330d9af735dad136a20fd58149e5a

The JSON includes elapsed time, so an exact rerun normally changes its file hash even when all mathematical witnesses are identical. Compare witness fields and source/dependency hashes, not only the serialized output hash.

Minimum margins (approximate summaries, not proof inputs): C0 0.9885840928424285; h=1/1000 transformed Schur lower-model 0.6499154101790116; bridge leaves 0.20663148368552395. The h=1/100 transformed lower-model minimum is negative, about -4.18852725571, and h=1/10000 is positive, about 0.96004204428. These are margins after the recorded congruences, not eigenvalue bounds for the raw Hessian.
