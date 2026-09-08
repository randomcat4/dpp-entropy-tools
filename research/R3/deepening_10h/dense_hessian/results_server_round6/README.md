# Round 6 isolated CPU scout

This directory is the complete copied output of one bounded single-CPU run of
`dense_hessian.py` in an isolated compute environment.  No connection details
are recorded in the repository.

- seed: `2026090815`
- dimensions: `n=12,13`
- centers per dimension: `80`
- total centers: `160`
- exact events per center: `2^n`
- threads: `1`
- status: `SCOUT_COMPLETE`
- positive curvature candidates: `0`
- best total Hessian eigenvalue: `-0.00032050281426960933`
- best mechanism ratio: `0.5261099452386901`

All seven copied files were SHA-256 compared with the source outputs before the
temporary compute directory was removed.  The frozen best-mechanism NPZ hash is
`e614dff920277e60929a6f8e1cfb37bd19d7c8d30a6a61a9488c424a8eb7ff3f`.

The 160-row ledger remains float64 scout evidence.  The strongest frozen point,
including its exact-event semantics, high-precision curvature, PSD direction,
strict chord feasibility, and commuting-direction reduction, was independently
checked in `../server_round6_analysis/` and again in
`../server_round6_analysis/verifications/`.
