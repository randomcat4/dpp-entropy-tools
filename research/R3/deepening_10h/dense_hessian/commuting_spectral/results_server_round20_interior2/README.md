# D10-H12 / round20_interior2

This batch moves the H10 fixed-eigenvector spectral-rate mechanism farther
into the strict spectral interior. It is a finite diagnostic, not a global
concavity result.

## Frozen design

- dimension: `n=12`;
- source: the H10 strongest spectrum contracted toward `1/2` to margin `0.06`;
- enforced proposal floor: `min(lambda_i,1-lambda_i) >= 0.05`;
- four shards, seeds `2026090870` through `2026090873`;
- `5,000` proposals per shard plus one explicitly ledgered source row;
- joint spectrum/basis perturbations, with a one-sign positive spectral-rate
  direction optimized at each fixed-Q center.

The source ratio is `0.5316300785`. Its NPZ SHA256 is
`34a8a9345c094c34aac0c4c48a5033a58457174de3d283868f81dba1c584fa75`.
All files copied from the compute run were hash-matched before the temporary
compute directory was removed.

## Author gate

All `20,000` proposal rows and four source rows are present. Every stored
status is `NO_HIT`; every chord gap is negative. The strongest row is shard
`1`, index `2701`, labelled `one_basis_rotation`:

```text
rho                 = 0.5729410207438331
spectrum margin     = 0.05
H'' (80 digit gate) = -64.360076939131812434868479851119151051656349935581...
```

The strongest NPZ SHA256 is
`1b24617db8d44973a55d4128b0763260a428b4d8227e1acaea4378750d9db439`.
Its exact-decimal-rational endpoint LDL checks certify a positive-definite
direction and strict feasibility with margin `1/2000` on `|t|<=1/200`. Three
high-precision chord midpoint gaps are negative.

H12 is below the current H10/H11 ratios (`0.5746069` and `0.5745947`) but still
reaches about `0.57294` with every proposal kept at least `0.05` from either
spectral endpoint. This establishes neither monotonicity in the margin nor a
global optimum. It does show that the observed high-ratio mechanism persists
well inside the feasible spectral box, while remaining far below the positive
curvature threshold `rho>1`.

Independent non-author reconstruction under `verifications/` gives `CORRECT`
for the frozen accounting and strongest gate. It independently rebuilds the
4,096 events at 120 digits, all three chords, and the Fraction LDL certificate
without importing the author modules. Full seed regeneration and reconstruction
of every proposal matrix remain `INCOMPLETE`, so the global status is `SCOUT`.
