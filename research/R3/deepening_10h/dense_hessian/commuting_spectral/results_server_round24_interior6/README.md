# D10-H16 / round24_interior6

This batch extends the fixed-Q spectral-rate profile to a spectrum margin of
at least `0.40`, close to the central scalar kernel. It remains a finite
diagnostic.

## Frozen design

- dimension: `n=12`;
- H10 strongest spectrum contracted toward `1/2` to source margin `0.42`;
- every proposal clipped to spectral margin at least `0.40`;
- four shards, seeds `2026090886` through `2026090889`;
- `5,000` proposals per shard plus one ledgered source row;
- joint spectrum/basis perturbations and an optimized positive spectral-rate
  direction at every fixed-Q center.

The source ratio is `0.02049146815`; its NPZ SHA256 is
`52a0f584d37a7f8166a72a870ad0b0f9ce4156e2d5cfdac5b8d2aa24f5986e25`.
All 24 files copied from the compute run were hash-matched locally before its
temporary directory was removed.

## Author gate

All `20,000` proposals and four source rows are accounted for. No stored row
has a positive gap or `rho>=1`. The strongest is shard `1`, index `4686`,
labelled `three_basis_rotations`:

```text
rho                 = 0.03861710868283657
spectrum margin     = 0.40
H'' (80 digit gate) = -41.5919048131766515475529903141596666244228199640...
```

The strongest NPZ SHA256 is
`d89602bb84c3ba67acb152fab383f398af2248c0cfe27147226c09d71ed3889b`.
Its exact-decimal-rational endpoint LDL checks certify a positive-definite
direction and strict feasibility with margin `1/2000` on `|t|<=1/200`.
Three high-precision chord midpoint gaps are negative.

The best ratio falls from about `0.1522` at margin `0.30` to about `0.03862`
at margin `0.40`. Together with H10--H15 this completes a finite profile from
the near-boundary region into the central spectral box. It proves neither
monotonicity nor a global upper bound.

The fresh non-author audit under `audit_nonauthor/` independently checked all
20,004 ledger rows and rebuilt the strongest case at 160-digit precision.  It
obtained

```text
rho = 0.0386171086828367035336126216976...
H'' = -41.5919048131766516073319767526...
```

Three actual chords were negative, and exact-rational LDL certificates proved
the PSD direction and the requested endpoint margins.  The audited status is
still `SCOUT`: the finite run is internally consistent, but it is neither seed
regeneration nor a theorem about the whole spectral box.
