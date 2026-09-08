# D10-H15 / round23_interior5

This batch extends the fixed-Q spectral-rate profile to a spectrum margin of
at least `0.30`. It is a finite diagnostic, not a theorem.

## Frozen design

- dimension: `n=12`;
- H10 strongest spectrum contracted toward `1/2` to source margin `0.32`;
- every proposal clipped to spectral margin at least `0.30`;
- four shards, seeds `2026090882` through `2026090885`;
- `5,000` proposals per shard plus one ledgered source row;
- joint spectrum/basis perturbations and an optimized positive spectral-rate
  direction at every fixed-Q center.

The source ratio is `0.1026394416`; its NPZ SHA256 is
`57f08bf9d9abffe23d98d5dbbdd6e3d22026b402f5a7848a4469b70a8b0efcd7`.
All 24 files copied from the compute run were hash-matched locally before its
temporary directory was removed.

## Author gate

All `20,000` proposals and four source rows are accounted for. No stored row
has a positive gap or `rho>=1`. The strongest is shard `3`, index `2902`,
labelled `three_basis_rotations`:

```text
rho                 = 0.15219460446316677
spectrum margin     = 0.30
H'' (80 digit gate) = -44.2031294195358884524964736375954506654559481984...
```

The strongest NPZ SHA256 is
`fe3dff3b540eb110677268005b5b919b0b0ea89d30f5c4e65baca528ed1a4ff9`.
Its exact-decimal-rational endpoint LDL checks certify a positive-definite
direction and strict feasibility with margin `1/2000` on `|t|<=1/200`.
Three high-precision chord midpoint gaps are negative.

The best ratio falls from about `0.3338` at margin `0.20` to about `0.1522` at
margin `0.30`. Together with H10--H14 this extends the finite attenuation
profile across the central spectral box. It proves neither monotonicity nor a
global upper bound.

A fresh non-author implementation under `audit_nonauthor/` reconstructed the
20,004-row accounting, 130-digit exact-event gate, three strict chords, and
rational LDL feasibility certificate. It returned `SCOUT_CORRECT`: the frozen
batch is correct, while all profile and global interpretations remain SCOUT.
