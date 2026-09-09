# PR60 independent certificate implementation

This directory contains the independent checker source for the PR60 full-r
issue52 machine unit.  The script constructs the short Schur matrix chain from
the displayed formulas, extracts a fresh `P` from `det(Ahat)` using polynomial
ring arithmetic, and only then compares with `inputs/reference_P_components.json`.

It does not import or execute `inputs/pr60/certificate.py` or
`inputs/pr60/bridge_checks.py`.

Suggested guarded launch from the repository root:

```bash
python research/C2/pr60_independent52/implementation/pr60_independent_certificate.py \
  --input-root research/C2/pr60_independent52/inputs \
  --out research/C2/pr60_independent52/execution/independent52_run \
  --wall-seconds 2700
```

Expected terminal result is exit code 0 plus `PASS.json`.  A mismatch or
deadline breach exits nonzero and leaves the completed layer checkpoints in the
chosen output directory.  Checkpoints are JSON files written atomically.
