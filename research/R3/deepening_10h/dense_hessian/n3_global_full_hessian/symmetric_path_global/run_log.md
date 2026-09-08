# D10-U10e run log

## Scope

- Directory written:
  `research/R3/deepening_10h/dense_hessian/n3_global_full_hessian/symmetric_path_global/`
- No author files, shared indexes, or previous audit directories were edited.
- No subagents were spawned.
- No remote computation or dependency installation was used.
- `C:\canglan\` was not accessed, searched, traversed, or modified.

## Inputs read

- `repo/AGENTS.md`
- `symmetric_path_subfamily/audit_nonauthor/verdict.md`
- `symmetric_path_subfamily/derivation.md`

`profile.json` records the current input hashes:

- U10d audit verdict:
  `95d01060ae54783f1ce3315905c95e0166ea573ae835a32c010ac9f0b7557074`
- Current U10d derivation:
  `12be41712d9161c106ba817f0c089a670d3bb278e82a4477d384ca91bf3cc9c5`

Note: the current U10d derivation hash differs from the older hash embedded
inside the U10d audit verdict.  This unit used the reviewed U10d verdict as
the main dependency and independently recomputed the formulas used here.

## Commands

From `C:\game\gameproject\showa100\math\i05-real-20260908\R3\repo`:

```powershell
$env:OMP_NUM_THREADS='1'
$env:OPENBLAS_NUM_THREADS='1'
$env:MKL_NUM_THREADS='1'
& 'C:\Users\UIO\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' `
  'research\R3\deepening_10h\dense_hessian\n3_global_full_hessian\symmetric_path_global\search.py'
```

First run: exit code `1`, caused by a double-precision scout division by zero
at an extremely near-singular random proposal.  The high-precision grid had
already completed; the scout exception handling was patched to skip such
floating degeneracies.

Second run: exit code `0`.

Output:

- `profile.json`
- status `NO_NEGATIVE_SIGMA_FOUND__GLOBAL_PROOF_INCOMPLETE`
- high-precision evaluations `25,702`
- float scout proposals `120,000`
- negative hits `0`

## Denominator and role

The deterministic high-precision profile used a product grid in reduced
coordinates `(x,c)`:

- `142` `x` values, including uniform values plus `10^-k` and
  `1/2-10^-k` boundary probes.
- `181` `c` values, including uniform values plus `10^-k` and
  `1-10^-k` boundary probes.

This is a reproducible scout profile, not a rigorous interval certificate.
