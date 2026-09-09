# Verification and execution

Author self-check: completed. Independent reviewer: not yet performed.

`preflight.json` records exact rational inclusion--exclusion versus polynomial probability equality, exact polynomial normalization, exact isometry and sum q checks, and independent floating-point gradients and Hessians. Max absolute errors for probability, gradient, Hessian are respectively 4.03e-16, 2.92e-16, 5.00e-16. A direct symmetric finite difference at h=1e-4 has probability first-derivative error 1.59e-9 and second-derivative error 6.25e-8. Jet normalization errors are below 2.3e-16. These tolerances passed before the center loop.

For the exact fixtures all 26 center and endpoint probabilities are positive rational numbers, all 18 required Sylvester determinants are positive rational numbers, and interval total curvature and finite chord are strictly negative. Each layer's cost, acceleration, and total is retained. Rationalization changed the noncommuting representative's curvature from about -4.04252924546 to -4.04252934872; the exact input, rather than the float, determines the certificate.

Dependencies: Python 3.12.3, numpy 2.5.3, scipy 1.18.1, sympy 1.14.0, mpmath 1.3.0. Calculation ran on the authorized server, one thread each for OPENBLAS, OMP, and MKL, no GPU. `results.json` records PID, dependency versions, thread variables and SHA-256 of the exact script. `command.txt`, `run.log`, and `exit_status.txt` retain the final invocation and successful exit status 0.

Version history: search.py v1.0 completed all computations and output, but the remote shell wrapper's status-recording suffix had an escaping error and the wrapper exited 1. The original results are retained in `results_v1.json`. Version 1.1 changed only representative selection to require noncommutation and saved candidate rows before asserting negativity. Its correctly quoted `run.sh` reran the identical bounded set, not an expanded search, and exited 0. The scalar v1 interval fixture remains retained under its original name.

To reproduce in an isolated directory, install the five listed dependencies in a Python 3.12 environment, set OPENBLAS_NUM_THREADS=OMP_NUM_THREADS=MKL_NUM_THREADS=1, then run `python search.py`. Alternatively the supplied `run.sh` assumes a virtual environment in the parent folder. No access details or machine credentials are needed. Output JSON includes every sampled matrix and direction, not only the best cases.

Known limits: general eigenvalue signs outside these centers are not certified; floating Hessian definiteness at the centers was not itself interval certified; no independent reviewer has run this unit yet; mpmath interval output is not a formally verified theorem prover. All quantitative sign claims in the final exact fixtures use their explicit rational inputs.
