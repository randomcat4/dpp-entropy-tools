# D10-H16 / round24_interior6 fresh non-author audit verdict

STATUS: SCOUT

Audit verdict: within the finite frozen artifacts, I found no accounting gap, no
strongest-case reconstruction gap, and no sign/certificate gap.  This is only a
finite SCOUT audit of the recorded run; it is not a theorem, does not regenerate
all seeds, and does not certify any monotone or global claim.

## Frozen inputs

The machine-readable hash table is in `audit_results.json`.  Key hashes checked:

- `README.md`: `a0f0855cffbf0126102f1e38b7c814d48f0096e813a746cc9fe8d730e72a1e8f`
- `spectral_basis_refine.py`: `28ae523c10184dc1effe2f857adbdad4156683292f2ad7da2d281e2af6ad7268`
- `recheck_best_interior6.json`: `15b700df9925846aa284b209a8b281fe1d00c98850fd86cf345d389173d4acd3`
- `results_1/best_case.npz`: `d89602bb84c3ba67acb152fab383f398af2248c0cfe27147226c09d71ed3889b`
- `results_1/candidate_ledger.csv`: `004ecb52626f3ad7d9f79d75e9f1b6f1ddd2e445757090b2f92737460c762480`

## Ledger/accounting checks

- Four shards are present, each with 5001 data rows: one `source_base` row plus
  5000 proposal rows.
- Total ledger data rows: 20004; total proposal rows: 20000; total source rows:
  4.
- All four manifests report `proposal_count=5000`,
  `ledger_rows_including_source=5001`, `margin_floor=0.4`,
  `positive_count=0`, and `exit_code=0`.
- Ledger scan found 0 positive chord gaps, 0 rows with `rho>=1`, and 0 rows with
  status different from `NO_HIT`.
- Minimum proposal spectral margin is `0.4` under the parsed decimal ledger
  values.

The strongest row is confirmed as shard 1, index 4686, label
`three_basis_rotations`, with ledger `rho_psd=0.03861710868283657`,
`chord_gap=-0.0020797162960004556`, and spectrum margin `0.4`.

## Strongest NPZ reconstruction

From `results_1/best_case.npz`, using only the stored arrays:

- `n=12`.
- `Q^T Q-I` Frobenius residual: `5.639452462080262e-15`.
- `K - Q diag(lambda) Q^T` Frobenius residual:
  `7.978494172206101e-17`.
- `D - Q diag(rate) Q^T` Frobenius residual:
  `1.2789110221541029e-16`.
- Commutator Frobenius residual: `5.73326764908097e-16`.
- Spectrum range is `[0.4, 0.6]`; rate range is
  `[0.8495201078355317, 1.0]`.

Thus the stored strongest candidate is consistent with a legal fixed-Q
PSD spectral-rate K-affine line, up to ordinary floating storage residuals.

## Independent exact-event / Möbius recomputation

Using 160-digit `Decimal`, principal-minor inclusion probabilities, and
Möbius inversion over all 4096 atoms:

- minimum atom: approximately `0.00017372018111775689163770261296544629`;
- `sum p - 1 = -7e-160`;
- `sum p' = 2.7571e-158`;
- `sum p'' = 7.40e-159`;
- maximum inclusion recovery residual: `1.9e-159`;
- Fisher term: `43.26258058970944276337967893340491842385283787740586276`;
- acceleration term: `1.67067577653279115604770218077038160471423304450322173`;
- `H'' = -41.59190481317665160733197675263453681913860483290264103`;
- `rho = 0.03861710868283670353361262169764189212251840786667063928`.

This independently confirms the reported strongest point is safely negative
and has `rho<1`.

## Chord checks

For the same binary-float-frozen `K,D` converted to exact rationals and evaluated
through exact-event/Möbius entropy:

- `h=1/100`: midpoint gap
  `-0.00207971629600055144567100000502045043034082585394644308`.
- `h=1/1000`: midpoint gap
  `-0.0000207959645104334192346969924653263392512078629875845192`.
- `h=1/10000`: midpoint gap
  `-2.0795952527626607862343878622845218240088133648212565e-7`.

All three actual chords are negative, and the scaled values converge toward
approximately half of the recomputed `H''`, as expected.

## Fraction LDL feasibility certificates

Using exact rational matrices obtained from the stored binary floats:

- `D` has positive no-pivot LDL pivots; minimum pivot float
  `0.894309692417035`.
- At `t=+1/200`, both `K+tD-(1/2000)I` and
  `I-(K+tD)-(1/2000)I` have positive LDL pivots.  Minimum pivot floats:
  `0.46249329455690025` and `0.4462967833276879`.
- At `t=-1/200`, both `K+tD-(1/2000)I` and
  `I-(K+tD)-(1/2000)I` have positive LDL pivots.  Minimum pivot floats:
  `0.45310475344618095` and `0.4554867472186564`.

So the audited strongest line has exact rational PSD direction and strict
feasible endpoints with at least the requested `1/2000` certificate margin.

## H10-H16 finite profile

The profile scan over frozen round directories gives the following best
recorded finite-run rho values:

| label | margin floor | best rho | best shard/index |
|---|---:|---:|---|
| H10 | 0.002 | 0.5746069386526107 | shard 2 / index 4877 |
| H11 | 0.02 | 0.5745947308664667 | shard 0 / index 4853 |
| H12 | 0.05 | 0.5729410207438331 | shard 1 / index 2701 |
| H13 | 0.1 | 0.5313886643536545 | shard 0 / index 70 |
| H14 | 0.2 | 0.3337720601402677 | shard 0 / index 2996 |
| H15 | 0.3 | 0.15219460446316677 | shard 3 / index 2902 |
| H16 | 0.4 | 0.03861710868283657 | shard 1 / index 4686 |

This supports only the finite descriptive statement that the recorded best rho
falls sharply by the margin-0.40 round while remaining nonzero.  It does not
prove monotonicity, absence of missed candidates, or any global curvature law.

## Remaining limitations

- I did not regenerate all proposal seeds or reconstruct every proposal matrix
  from RNG state.
- I did not use or audit the author wrapper as a proof dependency; it is only
  hashed as a frozen artifact.
- All statements above are about the frozen finite run and the independently
  recomputed strongest case.
