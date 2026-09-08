# D10-U10h audit log

STATUS: INCOMPLETE_GLOBAL

## Scope

- Target:
  `research/R3/deepening_10h/dense_hessian/n3_global_full_hessian/exchangeable_triangle_global_attempt/`.
- Wrote only:
  `exchangeable_triangle_global_attempt/audit_nonauthor/`.
- Did not modify author files, shared indexes, or prior audit files.
- Did not import author `sanity.py` or cached code.
- Did not spawn subagents.
- Did not access, search, traverse, or modify `C:\canglan\`.

## Commands

From workspace root `C:\game\gameproject\showa100`:

1. Read `math-theorem` skill instructions and `repo/AGENTS.md`.
2. Listed the target directory with `rg --files`.
3. Read U10h author files:
   `frozen_problem.md`, `proof_or_blocker.md`, `verdict.md`, `run_log.md`,
   `sanity.py`, and `sanity.json`.
4. Read U10f dependency/audit files:
   `exchangeable_triangle_subfamily/fresh_audit.md` and `verdict.md`.
5. Created `audit_nonauthor/`.
6. Wrote `audit.py`.
7. Ran:

   ```powershell
   $env:OMP_NUM_THREADS='1'
   $env:OPENBLAS_NUM_THREADS='1'
   $env:MKL_NUM_THREADS='1'
   & 'C:\Users\UIO\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' 'math\i05-real-20260908\R3\repo\research\R3\deepening_10h\dense_hessian\n3_global_full_hessian\exchangeable_triangle_global_attempt\audit_nonauthor\audit.py'
   ```

   Output:

   ```json
   {
     "overall": "AUDIT_PASS_WITH_GLOBAL_OPEN",
     "out": "C:\\game\\gameproject\\showa100\\math\\i05-real-20260908\\R3\\repo\\research\\R3\\deepening_10h\\dense_hessian\\n3_global_full_hessian\\exchangeable_triangle_global_attempt\\audit_nonauthor\\results.json"
   }
   ```

## Produced files

- `audit.py`: independent polynomial/Decimal checker.
- `results.json`: full machine-readable audit output.
- `verdict.md`: layered mathematical verdict.
- `log.md`: this run log.

## Main checks

The final script checks all returned true:

- exchangeable layer atom mass identity;
- three cleared-denominator Fisher rank-one identities;
- explicit failure of the missing-factor-two Fisher variant;
- all log-acceleration coefficient identities, including the correct
  `n_beta`/`n_alpha` placement;
- Decimal direct-vs-formula Hessian checks;
- positive normalized edge-limit samples for all four boundary edges;
- exact alpha/beta swap asymmetry witness;
- strict failure of the `C_ab>=0` shortcut near `beta->0`;
- author sanity denominator consistency: `86/86`, no failures and no positive
  curvature candidates.

## Limitation

This audit certifies the scoped reductions and boundary-strip candidate logic.
It does not prove the global determinant inequality over the whole strict
square, does not cover joint corners, and does not convert finite sanity data
into an interval certificate.
