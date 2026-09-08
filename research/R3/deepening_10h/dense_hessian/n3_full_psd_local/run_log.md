# D10-S5 run log

Status: **CORRECT_AFTER_FRESH_REVIEW_AND_REVISION_RECHECK** for the full
Hessian certificate and saved-point calculations; finite optimization is
`SCOUT`.

Date: 2026-09-08.  No server, no GPU, no system dependency changes.  Work was
restricted to `research/R3/deepening_10h/dense_hessian/n3_full_psd_local/`.

Command run from the repository root:

```text
C:\Users\UIO\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe research\R3\deepening_10h\dense_hessian\n3_full_psd_local\full_psd_hessian.py
```

Exit code: `0`.

Parameters:

- base point: M7 equation (19) \(K_*\);
- coordinate order: `(11,22,33,12,13,23)`;
- exact atoms: direct inclusion-determinant Möbius inversion;
- decimal precision for displayed Hessian: `100`;
- rational log interval terms: `35`;
- PSD attack seed: `20260908`;
- projected PSD starts: `400`;
- projected steps per start: `300`;
- rank-one random samples: `4000`;
- rationalized best denominator cap: `2000`.

Output summary:

```text
status: PROOF_CANDIDATE_PENDING_FRESH_REVIEW
min_base_atom: 87/1250
gershgorin_min_margin_for_minus_H_decimal:
  1.720007550503861348812899348944947380976567770641073893515221526303979875349498451260476673015553797
unconstrained_max_eigenvalue_float: -2.4526751952000114
commuting_D_star_H2:
  -2.264361218158924839989580424355442546407060002577797282171348263943548119836356161409467927238870972
psd_scout_best_value: -2.285098038212576
psd_scout_best_rank: 1
rank1_best_value: -2.285098038212576
rationalized_best_H2_per_frob2:
  -2.285108948085504855207731325829938649580764389068453907498998503050313106539582651065288520740641309
```

JSON ledger:

- `hessian_scout.json`

The JSON stores the base atoms, Decimal Hessian matrix, exact rational
Gershgorin interval certificate, unconstrained eigenvalue scout, PSD projected
search log, rationalized best PSD direction, principal-minor PSD margins, and
a small strict-feasibility Gershgorin probe at step \(1/1000\).

No positive PSD direction was found.  More importantly, the interval
Gershgorin certificate proves there is no positive direction in all of
\(\mathrm{Sym}(3)\) at \(K_*\).

The first non-author audit found that the projected-search update inserted the
off-diagonal coordinate gradient directly into a symmetric matrix, rather
than dividing those three entries by two for the Frobenius metric.  The source
was corrected and the full `4000 + 400x300` finite scout was replayed.  The
best value and saved JSON were unchanged because the retained best came from
the separate rank-one scan.  The revised source SHA-256 is
`92697514aeaa7c40c5ed8bd21137635f7aa5033698b7a0e7793b6c8b9df38166`;
the same reviewer verified the fix and replay in `verifications/`.
