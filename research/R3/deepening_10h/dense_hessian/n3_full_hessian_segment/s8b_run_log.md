# D10-S8b run log

AUTHOR STATUS: PROOF_CANDIDATE_PENDING_FRESH_REVIEW.

No server was used.  No GPU was used.  No system dependencies were installed.
No randomness is used in the rigorous certificate, except that floating-point
Cholesky is used deterministically to propose rational preconditioners; the
proof checks only the rationalized matrices.

I did not modify the original S8 certificate files.  New files added:

- `s8b_preconditioned_expansion.py`
- `s8b_preconditioned_certificate.json`
- `s8b_expansion.md`
- `s8b_run_log.md`
- `s8b_verdict.md`

## Main final run

From the repository root:

```powershell
$env:OMP_NUM_THREADS='1'; $env:OPENBLAS_NUM_THREADS='1'; $env:MKL_NUM_THREADS='1'; $env:NUMEXPR_NUM_THREADS='1'; & 'C:\Users\UIO\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' 'research\R3\deepening_10h\dense_hessian\n3_full_hessian_segment\s8b_preconditioned_expansion.py'
```

Exit code: `0`.

Output summary:

```json
{
  "status": "PROOF_CANDIDATE_PENDING_FRESH_REVIEW",
  "largest_certified_radius": "29/100",
  "largest_certified_interval": ["-29/100", "29/100"],
  "largest_certified_min_margin_decimal": "0.0004096514363704310530437057056",
  "largest_certified_min_atom_lower": "15168331/7680000000"
}
```

The complete certificate JSON is `s8b_preconditioned_certificate.json`.

## Preliminary runs and blockers

Before the final scripted run:

- `49/200` was certified individually at depth `10`, using 34 leaves.
- `1/4` was certified individually at depth `10`, using 34 leaves.
- `7/25` was certified individually at depth `10`, using 49 leaves.
- `29/100` was certified individually at depth `11`, using 68 leaves in that
  preliminary run; the final script certified it with 67 leaves after the code
  was made to store rational preconditioners.
- A batch run including `299/1000` was interrupted because the near-endpoint
  case dominated runtime.
- A later individual `299/1000` attempt with `log_terms=20`, `max_depth=12`,
  and denominators `[64,256,1024]` produced no result after roughly 150 seconds
  and was interrupted.  This is recorded as `TIMEOUT_INTERRUPTED`.

## Float scouts

Float grids are not proof.  They were used only to check whether failed or
timed-out radii showed obvious positive curvature directions.

For `29/100`, a 401-point grid had worst sampled
`lambda_min(B)≈0.7138672670`.

For `299/1000`, a 401-point grid had worst sampled
`lambda_min(B)≈0.7135744966`.

Both are consistent with continued negativity, but only `29/100` has a rigorous
continuous certificate in this work unit.
