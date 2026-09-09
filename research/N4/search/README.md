# N4 bounded search S1

Status: `INCOMPLETE`; one four-dimensional finite scout completed, no positive
candidate. This is neither a global exclusion nor a novelty claim.

The exact full-event identity is
`p(S)=(-1)^(4-|S|) det(K-diag(1_{i notin S}))`.
The implementation obtains the probabilities by signed log determinants and
the first and second derivatives by differentiating the 24-term Leibniz
polynomial. It does not use inclusion minors as event probabilities.
The self-test compares independent direct Mobius event inversion and a finite
difference of entropy; both pass. The ten symmetric coordinate matrices are
Frobenius orthonormal, so the full top Hessian eigenvalue has that normalization.

## Actual coverage

| Family | Kernels |
|---|---:|
| Complete graph, all 8 independent cycle-sign assignments after star gauge | 64 |
| Diamond graph, 4 assignments for 2 independent cycles | 16 |
| Moving spectral frames with 3 unequal-scale profiles and 4 scales | 48 |
| Near-product numerical controls | 16 |
| Adaptive perturbations of the 2 highest supported non-control ratios | 16 |

All 160 kernels were assessed with a complete 10 by 10 Hessian. Each retained
both its top curvature direction and the maximum acceleration/Fisher quotient
on the numerically supported Fisher range. Each direction has three genuinely
K-affine chords, at 0.025, 0.2, and 0.7 times its computed symmetric feasible
radius. Thus 320 directions and 960 chords were evaluated. Every K, D, t,
endpoint spectral margin, event contribution, and complement-pair contribution
is retained in [batch1/cases.jsonl](batch1/cases.jsonl).

The radius formula is
`min(1/||K^-1/2 D K^-1/2||op, 1/||(I-K)^-1/2 D (I-K)^-1/2||op)`.
This formula is mathematically exact; the saved values and feasibility checks
are numerical, not rational certificates. All saved arrays are round-trip
binary64 inputs. No certificate is inferred from floating sign checks.

## Results and limits

Maximum acceleration/Fisher ratio: `0.3618220383445623`, at adaptive case 151
descending from moving-frame case 116. Its ratio direction is positive definite
and noncommuting; the full top-Hessian direction is indefinite and noncommuting.
The ratio direction has Fisher `-11.3643102853`, acceleration `4.1118579118`,
and total curvature `-7.2524523735`. The top-Hessian direction instead has
curvature `-3.2196771412`. Positive acceleration alone does not approach failure
in this small batch.

Maximum curvature `-1.3248769963e-13` is a near-product control, not useful
evidence for a new mechanism. The maximum float gap was `-2.6645352591e-15`.
The Fisher threshold can discard weak directions, so its ratio is not a proof
over the discarded space; the full Hessian was separately retained for every
kernel. The closest-zero control and largest-ratio case were replayed at 100
decimal digits using inverse-trace derivatives instead of polynomial
derivatives. Both saved directions and all three chords remained negative.
This is an author arithmetic cross-check, not an independent or interval audit.

The finite batch supplies no evidence warranting n=5--8 expansion. A subsequent
unit, if assigned, should isolate a new coupling mechanism rather than enlarge
this same scan.

## Execution and provenance

See [batch1/manifest.json](batch1/manifest.json) for seed 2026090904, source SHA256,
base commit, actual environment, command, PID 158332, and elapsed 0.7303 seconds.
One Python process, all four BLAS/OpenMP thread settings 1, no GPU; no process
from another route was modified. Research and self-test together made 161 full
Hessian calls, 161 polynomial derivative calls, and 2083 entropy calls. There
were 160 proposals, 0 rejected evaluations, and 0 candidate files.

Python wrote its completed manifest with exit_code 0 and ended normally. The
first outer-shell exit-capture suffix was incorrectly escaped and printed a
backslash; its returned shell exit was 0, but that suffix is not independent
evidence of the Python exit. This limitation is retained rather than silently
rerunning the search. The selected 100-digit replay used corrected outer-shell
exit capture and returned 0; it added 4 directional curvature and 28 entropy
evaluations, corresponding to 448 event evaluations. No background job remains.

Source: [bounded_search.py](bounded_search.py),
[replay_selected.py](replay_selected.py), and
[batch1/selected_replay.json](batch1/selected_replay.json).
Only this search child authored these scripts and diagnostics; no independent
review is claimed.
