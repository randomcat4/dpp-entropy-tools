# Run Log

Working directory:

    runs/C1/children/mechanism

Remote execution directory:

    /root/i05-seven-fronts-20260909/C1/mechanism

Private connection details are excluded.

## Environment

The server version probe was run with one-thread environment variables.

    PID 163138
    Python 3.12.3
    NumPy 2.1.2
    SciPy 1.14.1
    mpmath 1.3.0
    Platform Linux-6.8.0-79-generic-x86_64-with-glibc2.39

## Successful commands

Calibration and bounded mechanism table:

    PYTHONPATH=scripts OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 /opt/venv/bin/python scripts/mechanism_probe.py --output outputs/mechanism_probe.json --dps 180 --steps 70
    PID 164712
    exit 0

Rational sparse beta-root interval certificate:

    PYTHONPATH=scripts OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 /opt/venv/bin/python scripts/sparse_rational_certificate.py --output outputs/sparse_rational_certificate.json --table-exps 6,8,12 --table-steps 80 --cert-exp 8 --cert-steps 60
    PID 164711
    exit 0

## Failed implementation attempts

The first `mechanism_probe.py` server run exited 1 because mpmath could not
construct an mpf directly from a Fraction sign.  The script was patched to use
integer signs.

The first `sparse_phase_certificate.py` interval attempt used square-root
intervals for the non-rational finite-epsilon sparse variant.  Whole-bracket
rank-one cancellations made the event or solve intervals too wide, and the run
exited before a certificate.

The rational sparse script initially failed at 24 and 36 certification
bisections because the whole-root bracket was still too wide for the naive
interval solve.  The same root bracket with 60 bisections passed.
