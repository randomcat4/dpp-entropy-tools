# Reliable replay result

The same fixed rank-two script and JSON input were replayed once after the
original process-record failure. All mathematical phases passed again.
`execution.txt` contains a directly observed process exit, and stdout records
the arithmetic PID. The transport exit also agrees. Stderr is retained.

The original unit's polluted PID/exit files and inferred success marker remain
historical records. Their inferred zero must not be presented as a directly
captured exit. This replay supplies the missing operational evidence without
changing the input or mathematical check.

Reproduce from this directory with `bash run.sh`, using a Python environment
with the library versions printed in stdout. Set PYTHON to select that
environment. The runner uses one arithmetic thread, an 8 GiB virtual-memory
limit and a 600-second timeout.

Exact identities and rational event signs are the checked evidence.
High-precision curvature values are diagnostics and do not prove universal
concavity. The fixture's KL compression is supported analytically by exact
likelihood constancy on each fiber; a floating equality check alone would not
be an exact logarithmic identity certificate.
