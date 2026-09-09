# N3 round2 review run log

## Working Copy

| Field | Value |
| --- | --- |
| Local checkout | `C:\game\gameproject\showa100\math\i05-successors-20260909\N3\children\review\repo` |
| Branch | `research/N3-review-20260909` |
| Starting HEAD | `28b5576972d18a41f519b3bb95b76a307f148471` |
| Round2 frozen file read | `C:\game\gameproject\showa100\math\i05-successors-20260909\N3\repo\research\N3\round2\frozen_theorem_v1.md` |
| Frozen baseline named there | `e476db1bb056af57e883a47f470ea0f4443c1837` |
| Weak-edge candidate commit | `3087eb189237ec0a2d60127d0c35128f0cbcd91c` |
| Weak-edge candidate blob | `6a69ce2ba0ecc0f0826489501f126356708778f5` |
| Python used | `C:\Users\UIO\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe` |
| Python version | `3.12.14` |
| NumPy version | `2.3.5` |
| Thread environment | `OMP_NUM_THREADS=1`, `OPENBLAS_NUM_THREADS=1`, `MKL_NUM_THREADS=1`, `NUMEXPR_NUM_THREADS=1` |

No GPU, server job, system package installation, or global environment change
was used.

## Source Versions

| File | SHA256 |
| --- | --- |
| `research/N3/round2/review/verify_round2_definitions.py` | `680acb0024b90eef80747025d6113d9e7bfc593a58fa514101bb05b295a5094f` |
| `research/N3/round2/review/verify_weak_edge_candidate.py` | `575d8496987c9a826b902c9c156c40e82a5d26f8eed98c87bc3a2d768d326ffb` |

## Definition Audit Command

```powershell
$env:OMP_NUM_THREADS='1'
$env:OPENBLAS_NUM_THREADS='1'
$env:MKL_NUM_THREADS='1'
$env:NUMEXPR_NUM_THREADS='1'
& 'C:\Users\UIO\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' `
  'research\N3\round2\review\verify_round2_definitions.py' `
  --output 'research\N3\round2\review\round2_definition_audit_results.json'
```

Exit status: `0`.

Recorded PID: `9708`.

Actual coverage:

| Check | Count |
| --- | ---: |
| Deterministic strict kernels | 3 |
| Connected zero-edge samples | 1 |
| Complete round2 quantity rebuilds | 3 |
| Pair projection cross-checks | 3 |
| Affine derivative identity groups | 3 |
| Rayleigh polynomial pairs | 9 |

## Weak-Edge Audit Command

The first invocation of `verify_weak_edge_candidate.py` completed the
mathematical calculations but failed while writing JSON because a `numpy.bool_`
value was not converted to a native JSON boolean. It exited `1`; no script PID
was printed. The script was patched only to add safe JSON conversion and was
rerun with the same mathematical checks.

```powershell
$env:OMP_NUM_THREADS='1'
$env:OPENBLAS_NUM_THREADS='1'
$env:MKL_NUM_THREADS='1'
$env:NUMEXPR_NUM_THREADS='1'
& 'C:\Users\UIO\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' `
  'research\N3\round2\review\verify_weak_edge_candidate.py' `
  --output 'research\N3\round2\review\weak_edge_audit_results.json'
```

Final exit status: `0`.

Recorded PID: `64148`.

Actual coverage:

| Check | Count |
| --- | ---: |
| Fixed candidate objects | 1 |
| Sign branches | 2 |
| Exact density checks | 2 |
| Asymptotic probe points | 6 |
| Probe t-values | `1/100`, `1/200`, `1/400` |

## Result Files

| File | Purpose |
| --- | --- |
| `round2_definition_audit_results.json` | Machine-readable definition and exact-constraint audit; status `PASS`. |
| `verify_round2_definitions.stdout.txt` | Definition audit stdout. |
| `weak_edge_audit_results.json` | Machine-readable weak-edge candidate audit; status `PASS`. |
| `verify_weak_edge_candidate.stdout.txt` | Weak-edge audit stdout. |
| `round2_review_v1.md` | Self-contained review report. |

## Non-Coverage

This unit did not prove B0, did not find or certify an exact beta-zero root,
did not prove global `rho<=1`, did not run Lean, and did not perform a random
or all-domain scan.

