# D10-U10i audit log

STATUS: SCOPED_CORRECT_GLOBAL_INCOMPLETE

## Scope

- Target:
  `research/R3/deepening_10h/dense_hessian/n3_global_full_hessian/symmetric_path_global/boundary_exponential_limit/`.
- Wrote only:
  `boundary_exponential_limit/audit_nonauthor/`.
- Did not modify author files, shared indexes, or previous audit files.
- Did not import author code or cache.
- Did not spawn subagents.
- Did not access, search, traverse, or modify `C:\canglan\`.

## Commands

From workspace root `C:\game\gameproject\showa100`:

1. Read `math-theorem` skill instructions and `repo/AGENTS.md`.
2. Listed files in the target `boundary_exponential_limit` directory.
3. Read author files:
   `frozen_problem.md`, `proof_candidate.md`, `verdict.md`, `run_log.md`,
   `sanity.py`, and `sanity.json`.
4. Created `audit_nonauthor/`.
5. Wrote `audit.py`.
6. Ran:

   ```powershell
   $env:OMP_NUM_THREADS='1'
   $env:OPENBLAS_NUM_THREADS='1'
   $env:MKL_NUM_THREADS='1'
   & 'C:\Users\UIO\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' 'math\i05-real-20260908\R3\repo\research\R3\deepening_10h\dense_hessian\n3_global_full_hessian\symmetric_path_global\boundary_exponential_limit\audit_nonauthor\audit.py'
   ```

   Output:

   ```json
   {
     "overall": "SCOPED_CORRECT_GLOBAL_INCOMPLETE",
     "out": "C:\\game\\gameproject\\showa100\\math\\i05-real-20260908\\R3\\repo\\research\\R3\\deepening_10h\\dense_hessian\\n3_global_full_hessian\\symmetric_path_global\\boundary_exponential_limit\\audit_nonauthor\\results.json"
   }
   ```

## Produced files

- `audit.py`
- `results.json`
- `verdict.md`
- `log.md`

## Script denominator

The independent script evaluates:

- closed `phi(beta)`, its derivative polynomial, lower bound, and
  `beta_star`;
- `10` finite exponential samples: beta values
  `0.58`, `beta_star`, `0.3`, `1`, `3` at `x=1e-4` and `x=1e-6`;
- author sanity summary and the old finite `beta=0.58,x=1e-4` row.

All Boolean checks in `results.json` pass:

- stationary polynomial vanishes at `beta_star`;
- `phi_min > 8(log2+2)`;
- all sampled sigmas are positive and strict kernels;
- trial constraints are small;
- trial energy is not below constrained sigma;
- the finite `26.581...` value is distinguished from the limiting
  `26.603760...` minimum.

## Limitation

This is a scoped proof audit, not a long search.  It certifies no noncompact
beta regime and no full-domain theorem.
