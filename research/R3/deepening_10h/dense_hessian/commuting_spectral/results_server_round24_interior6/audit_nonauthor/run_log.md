# D10-H16 audit run log

STATUS: SCOUT

## Scope and rules followed

- Audit target:
  `research/R3/deepening_10h/dense_hessian/commuting_spectral/results_server_round24_interior6/`.
- Write target:
  `research/R3/deepening_10h/dense_hessian/commuting_spectral/results_server_round24_interior6/audit_nonauthor/`.
- I did not import the author's `recheck`, `search`, or `gate` code.
- I did not regenerate all seeds or all proposal matrices.
- I did not access or traverse `C:\canglan\`.
- I did not spawn subagents.

## Commands run

From workspace root `C:\game\gameproject\showa100`:

1. Read the math-theorem skill and repository `AGENTS.md`.
2. Listed files only under the H16 target directory.
3. Read the H16 `README.md`, manifests, ledgers, best-case JSON/NPZ metadata,
   log tails, and author high-precision JSON as frozen inputs.
4. Created the audit directory.
5. Wrote `audit.py`.
6. Ran:

   ```powershell
   $env:OMP_NUM_THREADS='1'
   $env:OPENBLAS_NUM_THREADS='1'
   $env:MKL_NUM_THREADS='1'
   & 'C:\Users\UIO\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' 'math\i05-real-20260908\R3\repo\research\R3\deepening_10h\dense_hessian\commuting_spectral\results_server_round24_interior6\audit_nonauthor\audit.py'
   ```

   Output:

   ```json
   {
     "overall": "FINITE_SCOUT_CORRECT",
     "out": "C:\\game\\gameproject\\showa100\\math\\i05-real-20260908\\R3\\repo\\research\\R3\\deepening_10h\\dense_hessian\\commuting_spectral\\results_server_round24_interior6\\audit_nonauthor\\audit_results.json"
   }
   ```

## Produced files

- `audit.py`: independent artifact/entropy/certificate checker.
- `audit_results.json`: full machine-readable results and frozen SHA-256 input
  hash table.
- `verdict.md`: human-readable audit verdict and limitations.
- `run_log.md`: this execution log.

## Result summary

The independent script returned `FINITE_SCOUT_CORRECT`:

- 4 ledgers × 5001 data rows = 20004 rows.
- 20000 proposal rows and 4 source rows.
- 0 positive chord gaps.
- 0 rows with `rho>=1`.
- 0 non-`NO_HIT` rows.
- Strongest row confirmed: shard 1, index 4686, rho
  `0.03861710868283657`.
- 160-digit exact-event/Möbius recomputation of the strongest row gave
  `H''=-41.59190481317665160733197675263453681913860483290264103` and
  `rho=0.03861710868283670353361262169764189212251840786667063928`.
- Three actual midpoint chords at `h=1/100`, `1/1000`, and `1/10000` were
  negative.
- Exact rational no-pivot LDL checks certified `D>0` and strict feasibility at
  `t=±1/200` with the requested `1/2000` margin.

The H10-H16 profile is recorded in `audit_results.json` and summarized in
`verdict.md`; it is finite SCOUT evidence only.
