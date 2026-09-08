# D10-H14 / round22_interior4

This batch extends the fixed-Q spectral-rate profile into the central spectral
box. It remains a finite diagnostic.

## Frozen design

- dimension: `n=12`;
- H10 strongest spectrum contracted toward `1/2` to source margin `0.22`;
- every proposal clipped to spectral margin at least `0.20`;
- four shards, seeds `2026090878` through `2026090881`;
- `5,000` proposals per shard plus one ledgered source row;
- joint spectrum/basis perturbations and an optimized positive spectral-rate
  direction at each fixed-Q center.

The source ratio is `0.2425492210`; its NPZ SHA256 is
`b5972686e06976da1ac5e8dc3dcef2090fdd010e2586520ee69836a25ee684cf`.
All 24 files copied from the compute run were hash-matched locally before its
temporary directory was removed.

## Author gate

All `20,000` proposals and four source rows are accounted for. No stored row
has a positive gap or `rho>=1`. The strongest is shard `0`, index `2996`,
labelled `spectrum_local`:

```text
rho                 = 0.3337720601402677
spectrum margin     = 0.19999999999999996
H'' (80 digit gate) = -45.655925925876573331427550677098464667818539045735...
```

The strongest NPZ SHA256 is
`8c62a7236a613640f0d76f3cedc1899825d63e60a33ca9c49beba4f8754a822b`.
Its exact-decimal-rational endpoint LDL checks certify a positive-definite
direction and strict feasibility with margin `1/2000` on `|t|<=1/200`. Three
high-precision chord midpoint gaps are negative.

The best ratio falls from about `0.5314` at margin `0.10` to about `0.3338` at
margin `0.20`. Together with H10--H13 this gives a broad finite profile: the
near-boundary mechanism remains negative everywhere checked and weakens in the
central box. This is neither a monotonicity proof nor a global upper bound.

A fresh non-author implementation under `audit_nonauthor/` independently
reconstructed the 20,004-row accounting, the 130-digit exact-event gate,
four strict chords, and the rational LDL feasibility certificate.  It returned
`CORRECT` for the frozen computation and retained `SCOUT` for every profile or
global inference.
