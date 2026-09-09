# Round-two execution ledger

All main and falsification mathematical server jobs used the existing
/opt/venv/bin/python, Python 3.12.3, NumPy 2.1.2, SciPy 1.14.1,
mpmath 1.3.0 and SymPy 1.13.3. OPENBLAS_NUM_THREADS, OMP_NUM_THREADS,
MKL_NUM_THREADS and NUMEXPR_NUM_THREADS were each 1. No GPU, global
installation, unrelated job termination or resource expansion occurred.
The initial limit was two simultaneous one-thread compute jobs; the route
ceiling remained eight CPU threads and 32 GiB. Existing resource use was
checked before execution. Private connection details are excluded here.

| Author execution | PID | Actual denominator | Status |
|---|---:|---|---|
| main/beta_probe.py | 160670 | 15 attempted centers, 14 feasible evaluations, 1 rejected | exit 0 |
| main/weak_edge_probe.py | 160749 | 12 fixed exact-input centers | exit 0 |
| main/lambda_tangent_certificate.py | 161284 | 1 exact rational center and direction | exit 0 |
| falsification/beta_affine_probe.py | 160926 | 12 segments times 9 parameters =108 evaluations | exit 0 |
| falsification/beta_root_certificate.py | 161034 | 42 bisection selectors +5 interval evaluations | exit 0 |
| inequality locked-odds formula sanity check, local | 40996 | 20 random kernels, seed 20260909 | exit 0 |
| falsification/locked_probe.py | 161752 | 4 existing kernels, 8 starts, 196 objective calls | exit 0 |
| falsification/locked_certificate.py | 161832 | 1 exact rational center/direction | exit 0 |

The first locked-probe launch failed before any optimizer call because the
library determinant routine mishandled a singular two-by-two cofactor.
The exact two-by-two polynomial replaced that routine, with the failed
source and missing short-lived PID disclosed in `falsification/locked_run_log.md`.
This is a runtime failure, not a rejected mathematical counterexample.

Main probe decimal precisions were 100 and 120 respectively; they are
diagnostics, not interval certificates. Their inputs are deterministic and
have no random seed. The main tangent certificate uses exact Fraction
arithmetic with the inherited rigorous log series. The root certificate
uses 160 decimal digits only for bracket selection, then 240-bit outward
dyadic intervals and 80-term rigorously bounded log series for proof.
The local inequality sanity check used Python 3.12.14 and NumPy 2.3.5.

Script-relative commands, source hashes, timings and JSON inputs/outputs
are stored beside each script. Counts are execution counts and may include
repeated kernels across units; they are not counts of distinct kernels or
independent theorem tests. A whole-interval enclosure counts as one interval
call and proves coverage by interval inclusion, not by sampling infinitely
many points. Child `run_log.md`/`command_log.md` files preserve finer details.

The final locked-bound test and independent reviewer runs are separately
logged by their owners. The final checkpoint records their frozen commits,
remaining live jobs and transport verification.

Final integration checks passed: six groups of proof/certificate files
match their original frozen Git objects exactly; the mathematical-run
structure validator reported no errors or warnings. Its one proof index
and one verification index are indexing conventions, not counts of
independent proofs or reviewers. The validator checks structure only.
All child mathematical jobs are complete, and no background continuation
is scheduled. Reviewed run failures remain in the final reviewer ledger.
