# D10-U10d audit run log

## Scope and restrictions

- Role: fresh non-author verifier for `symmetric_path_subfamily`.
- Write scope: only `research/R3/deepening_10h/dense_hessian/n3_global_full_hessian/symmetric_path_subfamily/audit_nonauthor/`.
- No subagents, no remote computation, no dependency installation, no commit.
- `C:\canglan\` was not accessed, searched, traversed, or modified.
- The author's `sanity.py` was not imported or executed.

## Files read

- `repo/AGENTS.md`
- `symmetric_path_subfamily/frozen_problem.md`
- `symmetric_path_subfamily/proof_or_blocker.md`
- `symmetric_path_subfamily/derivation.md`
- `symmetric_path_subfamily/verdict.md`
- `symmetric_path_subfamily/run_log.md`
- `symmetric_path_subfamily/sanity.json` for frozen author denominator/hash
  context only, not as a proof source.

## Files written

- `audit.py`
- `audit_results.json`
- `verdict.md`
- `run_log.md`

## Commands

From `C:\game\gameproject\showa100\math\i05-real-20260908\R3\repo`:

```powershell
$env:OMP_NUM_THREADS='1'
$env:OPENBLAS_NUM_THREADS='1'
$env:MKL_NUM_THREADS='1'
& 'C:\Users\UIO\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' `
  'research\R3\deepening_10h\dense_hessian\n3_global_full_hessian\symmetric_path_subfamily\audit_nonauthor\audit.py'
```

Exit code: `0`.

Script status: `PASS_CENTERED_THEOREM_AND_SCOPE_AUDIT`.

## Independent denominator

Atom formula and strict feasibility checks used four rational centers:

- `(x,a)=(2/5,1/9)`
- `(x,a)=(1/3,1/7)`
- `(x,a)=(3/5,-1/8)`
- `(x,a)=(1/2,3/20)`

General even-block derivative and equation (9) checks used three rational
centers/directions:

- `(2/5,1/9)` with `(d,e,h,k)=(3/7,-2/5,1/6,5/11)`
- `(1/3,1/7)` with `(d,e,h,k)=(-1/4,5/8,-2/9,1/3)`
- `(3/5,-1/8)` with `(d,e,h,k)=(2/9,1/5,3/10,-4/7)`

Centered full-Hessian/block/Schur checks used four centered values:

- `a=1/12`
- `a=3/20`
- `a=5/16`
- `a=7/20`

Core q-form checks used three further rational core directions.  These are
finite arithmetic integrity checks only; the theorem-level positivity uses
the symbolic Schur identity and analytic inequalities.

## Notes

An initial draft of `audit.py` had an output-path bug and wrote one temporary
`audit_results.json` under the sibling path lacking `repo`.  That erroneous
JSON file was deleted immediately; the remaining output path in the final
script is `Path(__file__).resolve().parent`, so current results are written
only to the assigned audit directory.
