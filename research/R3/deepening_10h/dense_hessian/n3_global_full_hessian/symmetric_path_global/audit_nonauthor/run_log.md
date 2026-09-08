# D10-U10e audit run log

STATUS: INCOMPLETE

## Scope

- Correct audit output directory:
  `research/R3/deepening_10h/dense_hessian/n3_global_full_hessian/symmetric_path_global/audit_nonauthor/`.
- Target author directories:
  `symmetric_path_global/` and `symmetric_path_global/boundary_full_atom/`.
- Dependency read:
  `symmetric_path_subfamily/audit_nonauthor/verdict.md` and U10d author
  materials, as prior audited input.
- No author files, shared indexes, or previous audit directories were edited.
- No subagents were spawned.
- `C:\canglan\` was not accessed, searched, traversed, or modified.

## Path correction

Before the route correction arrived, I had created an unrun draft script under
the originally requested U10d-side path:

```text
symmetric_path_subfamily/audit_general_path_nonauthor/
```

After the correction, I verified source and destination absolute paths and
moved that newly-created draft directory to the correct U10e-side path:

```text
symmetric_path_global/audit_nonauthor/
```

The mistaken U10d-side audit directory no longer exists.  I did not touch
`symmetric_path_subfamily/sanity.json`.

## Commands and execution

From workspace root `C:\game\gameproject\showa100`:

1. Read `math-theorem` skill instructions and `repo/AGENTS.md`.
2. Listed targeted files under
   `research/R3/deepening_10h/dense_hessian/n3_global_full_hessian/`.
3. Read U10d, U10e, and `boundary_full_atom` author/audit materials.
4. Wrote `audit.py`.
5. First run failed in the exponential boundary branch because evaluating
   `c=1-s` directly rounds to `1` when `s=exp(-beta/x)` is far below the
   Decimal working precision.  This was an audit-script issue and it confirmed
   why the boundary calculation must use the `s`-stable atom formulas.
6. Patched `audit.py` so `sigma_stable_xs` computes boundary atoms and `jF`
   directly in `s`.
7. Second run produced one false failed Boolean because the fixed-`x`, `s=0`
   atom check again used a square-root route.  Patched it to use the exact
   boundary atom limits.
8. Final run:

   ```powershell
   $env:OMP_NUM_THREADS='1'
   $env:OPENBLAS_NUM_THREADS='1'
   $env:MKL_NUM_THREADS='1'
   & 'C:\Users\UIO\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' 'math\i05-real-20260908\R3\repo\research\R3\deepening_10h\dense_hessian\n3_global_full_hessian\symmetric_path_global\audit_nonauthor\audit.py'
   ```

   Output:

   ```json
   {
     "overall": "AUDIT_PASS_WITH_OPEN_GLOBAL_INEQUALITY",
     "out": "C:\\game\\gameproject\\showa100\\math\\i05-real-20260908\\R3\\repo\\research\\R3\\deepening_10h\\dense_hessian\\n3_global_full_hessian\\symmetric_path_global\\audit_nonauthor\\audit_results.json"
   }
   ```

## Produced files

- `audit.py`
- `audit_results.json`
- `verdict.md`
- `run_log.md`

## Summary of final script checks

All Boolean checks in `audit_results.json` are true:

- exact atoms match Möbius events on independent rational samples;
- `B_even` formula matches exact-event Hessian jets to residual at most
  `1.2e-166`;
- reflection even/odd cross block is zero to residual at most `2e-168`;
- reflection odd block sample pivots are positive;
- full-atom `jF` derivatives match exact Möbius jets exactly;
- Schur determinant relation for `sigma` holds on samples;
- rectangular-domain samples have positive atoms;
- fixed-`x`, `s=0` boundary has only `F=0`;
- Sherman--Morrison stable formula matches direct sigma on moderate boundary
  samples;
- independent power/exponential boundary samples are positive;
- exposed sigma fields in author `profile.json` and `asymptotic_results.json`
  contain no nonpositive value.

The final mathematical status remains INCOMPLETE because none of these checks
proves the full continuum inequality `sigma(x,c)>0`.
