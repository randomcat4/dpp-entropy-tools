# boundary_full_atom run log

## Scope

- Wrote only:
  `research/R3/deepening_10h/dense_hessian/n3_global_full_hessian/symmetric_path_global/boundary_full_atom/`
- No author files or shared indexes were edited.
- No subagents, no remote computation, no dependency installation.
- `C:\canglan\` was not accessed, searched, traversed, or modified.

## Files

- `asymptotic_probe.py`
- `asymptotic_results.json`
- `analysis.md`
- `verdict.md`
- `run_log.md`

## Command

From `C:\game\gameproject\showa100\math\i05-real-20260908\R3\repo`:

```powershell
$env:OMP_NUM_THREADS='1'
$env:OPENBLAS_NUM_THREADS='1'
$env:MKL_NUM_THREADS='1'
& 'C:\Users\UIO\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' `
  'research\R3\deepening_10h\dense_hessian\n3_global_full_hessian\symmetric_path_global\boundary_full_atom\asymptotic_probe.py'
```

Exit code: `0`.

Output status:

```text
BOUNDARY_SCOUT_NO_NEGATIVE__ASYMPTOTIC_BLOCKER_REFINED
```

## Denominator

- Fixed-`x` profiles: `6` x-values, `11` s-values each.
- Power-rate profiles: `5` powers, `7` x-values each.
- Exponential-rate profiles: `9` beta-values, `8` x-values each.
- Beta refinement: `146` beta values at `x=10^-4`.

The run is intentionally a boundary/asymptotic scout, not a rigorous interval
subdivision.
