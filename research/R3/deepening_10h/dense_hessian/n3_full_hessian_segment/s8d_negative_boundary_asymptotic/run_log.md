# S8d run log and frozen witness inventory

Date: 2026-09-08. Computation was local, no server/GPU/subagent, with OpenBLAS restricted to one thread. Only this new S8d directory was written. No system dependencies or shared files were modified.

Main command from repository root:

```text
& 'C:/Users/UIO/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe' research/R3/deepening_10h/dense_hessian/n3_full_hessian_segment/s8d_negative_boundary_asymptotic/negative_probe.py
```

One complete execution, exit code 0. Elapsed time 298.532240152359 seconds. The long-running command was polled in short waits while the frozen endpoint/proof documents were written; its source was not changed during execution. Result: PROOF_CANDIDATE_PENDING_REVIEW.

There is no random seed: all parameters, intervals and proposal rules are deterministic. The helper evaluates midpoint Hessians with 90-digit Decimal before converting the matrix to float for inverse-Cholesky proposals. Every proposed preconditioner is rounded to rational entries with denominator cap 4096 and positive diagonal. Acceptance uses exact rational signed interval arithmetic and 24-term rational logarithm enclosures, not floating eigenvalues.

Complete attempt denominator:

- Eight exact event polynomials and all full six-coordinate first/second jets, direct Mobius/signed-determinant cross-checks.
- One full-set singular-jet polynomial check, including zero second F0 derivative for all eight events, and one exact positive diagonal Frobenius Gram check.
- One finite 3x3 endpoint block, all three rational Gershgorin margins positive.
- Three analytic tail widths: h=1/100,1/1000,1/10000. The first fails the lower-model midpoint Cholesky proposal; the latter two pass exact transformed row-margin tests. The widest passing width 1/1000 is used.
- One bridge [1/1000,71/100] in s=t+1. Node cap 4095 and depth cap 14; actual nodes 323, maximum accepted depth 8. There are 162 accepted leaves, 161 rejected internal nodes and 0 failed final leaves. Every accepted and rejected record is retained.
- Ten finite eigenvalue scouts at s=1/10000,1/1000,1/100,1/10,1/5,3/10,2/5,1/2,3/5,71/100. These remain SCOUT; no interpolation or sign extrapolation is used.

Minimum explanatory summaries:

- Endpoint C0 row margins approximately 3.5841579630,4.2480247952,8.3742584400.
- Tail h=1/1000 transformed lower-model row margin approximately 0.20009961668473455.
- Tail h=1/10000 corresponding margin approximately 0.9297282756099975.
- Bridge minimum transformed row margin approximately 0.009384781967274894.
- Bridge minimum exact atom lower bound 11189/2500000000.

These transformed margins are not raw full-Hessian eigenvalue lower bounds. Full rational numerators and denominators, without truncation, are stored in negative_results.json.

Frozen SHA256:

- negative_probe.py: `24912c62694b629f4081a458a6942f895384e51841bcfd6919145914ff9646b1`
- negative_results.json: `7df360071af07b77c1e6ebdac95da5f7ca936a1fffe2b1bac90276cb1e83918d`
- Read-only dependency ../verifications/fresh_s8_audit.py: `2eba997abe32602ac1e8139a9ccaa09999a330d9af735dad136a20fd58149e5a`

The dependency is the previously independent S8 verifier; no S8/S8b/S8c author Hessian module is imported. A future independent reviewer should inspect or independently replace it. The JSON includes elapsed time, so a rerun can change its raw hash without changing any mathematical witness.

No run failed or was abandoned. The failed coarse analytic model and rejected bridge nodes are explicitly retained as method failures, with no conversion into curvature counterexamples. A read-only final summary/hash command completed with exit 0. Skill usage: math-theorem author-proof workflow, with correctness certification left to a different reviewer.
