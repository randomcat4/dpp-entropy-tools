# D10-H13 / round21_interior3

This batch profiles the H10 fixed-eigenvector spectral-rate mechanism even
farther inside the strict spectral box. It is finite evidence only.

## Frozen design

- dimension: `n=12`;
- H10 strongest spectrum contracted toward `1/2` to source margin `0.12`;
- every proposal clipped to spectral margin at least `0.10`;
- four shards, seeds `2026090874` through `2026090877`;
- `5,000` proposals per shard plus one ledgered source row;
- joint spectrum/basis perturbations with an optimized positive spectral-rate
  direction at each fixed-Q center.

The source ratio is `0.4245408770`; its NPZ SHA256 is
`8c842a895aef3cec017b3148a404bd6195e78d3f64ebb77d383f7f9003ddbd3d`.
All compute-run files were hash-matched locally before the temporary compute
directory was removed.

## Author gate

All `20,000` proposals and four source rows are present. No stored row has a
positive gap or `rho>=1`. The strongest is shard `0`, index `70`, labelled
`three_basis_rotations`:

```text
rho                 = 0.5313886643536545
spectrum margin     = 0.09999999999999998
H'' (80 digit gate) = -56.144732535786444305780922949895553117522625994742...
```

The strongest NPZ SHA256 is
`7d7cc5ffb5898025f420b50e4223c69c14c0393783171cdcbdd21c2554d5c82e`.
Its exact-decimal-rational endpoint LDL checks certify a positive-definite
direction and strict feasibility with margin `1/2000` throughout
`|t|<=1/200`. Three high-precision chord midpoint gaps are negative.

Across the frozen H10--H13 best points, increasing the observed spectral
margin from roughly `0.015` through `0.0217`, `0.05`, and `0.10` accompanies
ratios `0.574607`, `0.574595`, `0.572941`, and `0.531389`. This is a useful
finite profile: the mechanism survives at margin `0.10` but is visibly weaker
there. It is not a monotonicity theorem or a boundary asymptotic, and the
positive-curvature threshold remains `rho>1`.

Independent non-author reconstruction under `verifications/` gives `CORRECT`
for the frozen accounting and strongest gate. It independently rebuilds all
4,096 event jets at 120 digits, checks three chords and proves the Fraction LDL
certificate without importing the author modules. Full seed regeneration and
reconstruction of all proposal matrices remain `INCOMPLETE`; the profile is
therefore still `SCOUT` globally.
