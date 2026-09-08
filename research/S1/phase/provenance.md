# Provenance and actual execution

Author: the main S1 route's phase sub-instance. It authored the candidate, the single-edge and symmetry proofs, and both scripts. No child agents were started. Review of the mathematical proofs is delegated to the main route; no self-certification is claimed.

Read-only source baseline: `fa504ec74e16843fafc395880d7ba99b4c1d2129`, equal in this child's local and server checkouts. Own branch: `research/S1-phase-20260909`. The main frozen theorem was read from the route-owned `research/S1/frozen_theorem_v1.md` without edits. Private connection details and handoffs are not included in these artifacts.

Only the original Lyons–Steif paper, Conjecture 9.2 and necessary Section 6 passages were read as mathematical sources. No current-state or novelty conclusion is claimed from that restricted reading.

The public reproducible commands, from this child's repository root, were:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 /opt/venv/bin/python research/S1/phase/phase_probe.py --output research/S1/phase/phase_probe_results.json
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 /opt/venv/bin/python research/S1/phase/phase_probe.py --output research/S1/phase/phase_probe_recheck.json
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 /opt/venv/bin/python research/S1/phase/sparse_probe.py --output research/S1/phase/sparse_probe_results.json
```

Standard output and errors were redirected to the correspondingly named `.log` files. Each process limits address space to 4294967296 bytes. No GPU or system installation was used. The environment was Python 3.12.3, NumPy 2.1.2, SciPy 1.14.1. Both scripts set BLAS/OpenMP thread variables to 1 before importing NumPy.

Executed source SHA256 values:

- `phase_probe.py`: `95510f8af862bb71b029ce51a3c5013d18252077e1b3dbff2a78c41971a60228`.
- `sparse_probe.py`: `58fa4fef2e5c9bc81741d7f4034b76b3902fd7509e3a9b9d6dea9c063b845fd6`.

The first process was PID 158039, completed status 0, elapsed 0.15009 seconds, peak RSS 34876 KiB. Its surrounding shell's extra exit-code echo was misquoted, so the exact same batch was repeated with a clean standalone invocation. The repeated process was PID 158507, clean exit 0, elapsed 0.15135 seconds, peak RSS 35924 KiB; its metadata are retained in the recheck log/result. The repetition does not increase the declared parameter denominator. The first script's inline comment describes four sign patterns as 'genuinely different'; this means different parameter tuples, not gauge inequivalence. The report explicitly records the symmetry repetitions.

The second distinct unit was PID 158610, completed status 0, elapsed 0.58176 seconds, peak RSS 33864 KiB. There was no failed numerical computation, no resumed partial result and no hidden unreported candidate. Before launching, process metadata and installed dependencies were inspected read-only; other processes were not touched.

Unique completed coverage: first unit 24 Hessians and 30 entropy distributions (8 center points plus 1 fixed chord); second unit 30 Hessians (10 center points). The first-unit exact same coverage was repeated once as a process-status check. Seed is recorded as 0, with no randomness actually used. Result files contain the exact arrays and all per-window normalization and derivative checks.
