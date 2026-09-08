# N3 review run log

## Working Copy

| Field | Value |
| --- | --- |
| Local checkout | `C:\game\gameproject\showa100\math\i05-successors-20260909\N3\children\review\repo` |
| Branch | `research/N3-review-20260909` |
| Initial baseline | `fa504ec74e16843fafc395880d7ba99b4c1d2129` |
| Fixed candidate commit reviewed | `424b4efcec0052ad8d79ac71c69b334dcfb03bb8` |
| Python used | `C:\Users\UIO\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe` |
| Python version | `3.12.14` |
| NumPy version | `2.3.5` |
| Thread environment | `OMP_NUM_THREADS=1`, `OPENBLAS_NUM_THREADS=1`, `MKL_NUM_THREADS=1`, `NUMEXPR_NUM_THREADS=1` |

No GPU, server process, system package installation, or global environment
change was used.

## Source Versions

| File | SHA / Blob |
| --- | --- |
| `research/N3/review/verify_n3_formulas.py` | `cb9ce09e0fae407cb6f3208d2e5863dff38b2e99f27307bfe2185aeccdeaa9a4` |
| `research/N3/review/verify_score_obstruction.py` | `c466b23943fe1495d9cdb278c975879eca13454aaf6aac8a12f97c61d4b1d13e` |
| `424b4ef:research/N3/frozen_theorem_v1.md` | `3edfa72b1a5cc11db28e419b70e633b9f683aefa` |
| `424b4ef:research/N3/main/conditional_score_lemma_v1.md` | `7202917271534297bf6ac7527e830e50946f66fd` |
| `424b4ef:research/N3/main/certify_score_obstruction.py` | `b27a15fcff15a98d78b94a9d663f7b512b5bbcf7` |
| `424b4ef:research/N3/main/score_obstruction_certificate.json` | `f51a96cf32faf70a170824e93eeb383e380f5c22` |

## Commands

An initial placement mistake ran the formula script before it had been moved
into this checkout. That invocation exited `2` with no mathematical coverage;
no script PID was recorded by the failed script because it did not start.

```powershell
$env:OMP_NUM_THREADS='1'
$env:OPENBLAS_NUM_THREADS='1'
$env:MKL_NUM_THREADS='1'
$env:NUMEXPR_NUM_THREADS='1'
& 'C:\Users\UIO\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' `
  'research\N3\review\verify_n3_formulas.py' `
  --output 'research\N3\review\formula_audit_results.json'
```

Exit status: `0`.

Recorded PID: `43040`.

Actual coverage:

| Check | Count |
| --- | ---: |
| Event formula vs Mobius inversion | 4 samples |
| Six-coordinate first/second jets | 32 direction checks |
| Conditional covariance squares, floating | 24 identities |
| Conditional covariance squares, exact rational | 12 identities |
| Direct `B` vs `F-2tr(N adj D)` | 4 samples |
| Direct `B` vs Schur/rank-one representation | 3 connected samples |
| Equal-softening boundary probes | 6 probes |

```powershell
$env:OMP_NUM_THREADS='1'
$env:OPENBLAS_NUM_THREADS='1'
$env:MKL_NUM_THREADS='1'
$env:NUMEXPR_NUM_THREADS='1'
& 'C:\Users\UIO\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' `
  'research\N3\review\verify_score_obstruction.py' `
  --output 'research\N3\review\score_obstruction_audit_results.json'
```

Exit status: `0`.

Recorded PID: `42164`.

Actual coverage:

| Check | Count |
| --- | ---: |
| Fixed commit objects read | 4 |
| Exact score-projection samples | 3 |
| Conditioning coordinates per sample | 3 |
| Table projection identities per sample | 6 |
| DPP square and derivative specializations per sample | 6 |
| Exact obstruction centers | 1 |
| Log interval terms | 70 |

## Result Files

| File | Purpose |
| --- | --- |
| `formula_audit_results.json` | Machine-readable formula audit result; status `PASS`. |
| `verify_n3_formulas.stdout.txt` | Formula audit stdout. |
| `score_obstruction_audit_results.json` | Machine-readable fixed-candidate score audit; status `PASS`. |
| `verify_score_obstruction.stdout.txt` | Score audit stdout. |
| `formula_and_score_review_v1.md` | Self-contained `CORRECT/CRITICAL_GAPS` review. |

## Non-Coverage

The runs did not prove global `rho<=1`, did not certify the constrained
optimizer direction, did not run Lean, did not produce an interval-global
certificate, and did not turn finite or boundary probes into a full-domain
theorem.

