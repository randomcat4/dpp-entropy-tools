# Reproducibility record

Date: 2026-09-08. Single bounded analytic unit. No random seed is used.
Author role: independent analytic route, no child instances.
Baseline: e6462caa8f9ec0c9033be376c3c39343a0175e32.
Frozen standard-mode statement supplied by owner and read before completing
the proof. Frozen original premises were not modified.

All computation used one CPU process and OMP_NUM_THREADS=1,
OPENBLAS_NUM_THREADS=1, MKL_NUM_THREADS=1. No GPU or global installation.
The interpreter was Python 3.12.3 in an isolated route-owned virtual
environment; SymPy 1.14.0 and mpmath 1.3.0 were installed in that environment.
The jobs are small exact symbolic computations, far below the 8 GiB cap.
Connection details are deliberately omitted.

Initial local `python` launcher was unavailable (exit 1); the bundled local
Python lacked SymPy (exit 1). A route-private remote virtual environment was
then used. The remote default Python also lacked SymPy (exit 1). No job was
restarted while an earlier copy was active. The route directory and process
list were checked before its initial setup.

Recorded completed jobs:

| Script | PID | Seed | Exit | Outcome |
| --- | ---: | --- | ---: | --- |
| derive.py | 144734 | none | 0 | exact trivial/standard derivative expressions |
| half.py | 144803 | none | 0 | exact derivatives of M and Lg |
| verify.py | 145303 | none | 0 | 24 exact identities PASS |

Replay from this directory using an environment with SymPy 1.14.0:

    OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 python verify.py

Observed verification output (the command field is portable rather than a
private interpreter path):

    {"pid":145303,"command":"python verify.py","seed":null,"python":"3.12.3","sympy":"1.14.0"}
    {"status":"PASS","exact_identity_checks":24,"exit_code":0}

The computer algebra checks probability formulas, normalization, each
cardinality's arbitrary-direction Fisher numerator decomposition, the entire
logarithmic Hessian decomposition, half-filled probability factorizations,
the rational derivative identities, the 2 by 2 determinant, and r=0.
The positivity argument is the displayed real-variable proof, not numerical
sampling or an automatic sign solver.

Not performed: Lean, interval certification, a finite-chord search,
independent verification, or a new literature/novelty audit. The baseline's
public prior-art and hazards files were read. No sibling probe draft was read.
