# N3 round 2 inequality unit

Status: `INCOMPLETE`.

This round attacks the frozen beta-zero slice

```text
beta(K)=0 => det(N) alpha(K) <= 1.
```

The new artifact is
[`rayleigh_beta_zero_obstruction.md`](rayleigh_beta_zero_obstruction.md).
It proves the exact Rayleigh-square jet identities for real three-point
kernels under affine `K+tD`, records the beta-zero optimiser equations, and
isolates the obstruction: first- and second-order square constraints alone do
not force beta away from zero.  The missing ingredient is a DPP-specific
alignment or sign consequence of the full `H=F_pair+det(N)G` stationarity
system.

The short status and failure ledger is in [`verdict.md`](verdict.md).

This does not use the old Qk closure, the failed F_pair full-direction
condition, a `Lambda=0` shortcut, or a near-zero beta tolerance.

Command records are in [`command_log.md`](command_log.md).
