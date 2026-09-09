# Verification

Independent nonauthor review: not yet performed.  This file is the author
self-check and server execution record for the mechanism child.

## Server execution

All successful mathematical runs were executed on the authorized server in
this child directory with

    OMP_NUM_THREADS=1
    OPENBLAS_NUM_THREADS=1
    MKL_NUM_THREADS=1
    NUMEXPR_NUM_THREADS=1

No GPU, package installation, system dependency change, or parent checkout
write was used.

Version probe:

    PID 163138
    /opt/venv/bin/python
    Python 3.12.3
    NumPy 2.1.2
    SciPy 1.14.1
    mpmath 1.3.0

Successful final runs:

    PID 164712  scripts/mechanism_probe.py
    PID 164711  scripts/sparse_rational_certificate.py

Earlier implementation failures:

    mechanism_probe.py first run: Fraction-to-mpmath sign conversion error.
    sparse_phase_certificate.py: square-root interval dependency made whole
      bracket event/solve intervals too wide.
    sparse_rational_certificate.py with 24 and 36 certification bisections:
      same-root interval bracket too wide for the determinant/solve bounds.
    sparse_rational_certificate.py with 60 certification bisections: passed.

These failures did not produce mathematical counterexamples.

## Certificate checks passed

For the epsilon=10^-8 rational sparse family, the certificate records:

- exact endpoint sign enclosures for `beta sqrt(Z)`;
- whole-bracket positive atom lower bound;
- whole-bracket positive leading minors for N;
- whole-bracket positive det(N);
- interval Gaussian solve pivots excluding zero;
- interval residuals containing zero;
- whole-bracket `det(N)alpha` upper bound below 1.

The root certificate status is

    CERTIFIED_RATIONAL_SPARSE_ROOT_DALPHA_LT_ONE.

No Lean or formal proof checker was run.
