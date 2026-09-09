# Round 2 Rate Certificate

Status: `NEGATIVE_PAIR_GAP` for the fixed non-even mixed-direction baseline `S1-R2-B1`.

This directory contains the rate subtask for round two.  It adapts the round-one exact Bareiss/interval and variational residual method to three distinct symbols:

```text
f_- = f_{-tau},   f_0,   f_+ = f_tau.
```

No endpoint equality, reflection, or conjugation shortcut is used.

The strict certificate already separates at past length `n=4`, so no `n=8` expansion was run.  The certified entropy-rate gap is:

```text
-3.0348902924818035e-05
<= (h(f_-)+h(f_+))/2 - h(f_0)
<= -7.3460456800473595e-06.
```

Thus this fixed round-two baseline is excluded as a positive counterexample to scalar entropy-rate concavity.  This is one fixed-pair result, not a family theorem and not a solution of the Lyons--Steif conjecture.

Main files:

- `candidate.json`: copied fixed object for the rate certificate.
- `scripts/r2_variational_boundary.py`: six extreme-past variational boundary enclosures.
- `scripts/r2_rate_certificate.py`: exact determinant and interval-log three-symbol rate certificate.
- `artifacts/r2_boundary_M64.json`: six boundary kernels, one thread, M=64.
- `artifacts/r2_rate_n4.json`: exact/interval rate certificate at past length 4.
- `proof_or_certificate.md`: proof chain and limitations.
- `run_log.md`: commands, versions, hashes, PID, exit status and coverage.
