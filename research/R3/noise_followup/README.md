# Follow-up on the `7.11e-15` midpoint gap

This directory separates two questions that float64 had conflated:

1. `diagnose_noise.py` recomputes ledger record 783 with arbitrary precision and
   scans smaller and larger steps along the recorded direction.  Its output can
   identify an ULP-scale sign flip without treating that diagnosis as a global
   concavity proof.
2. `local_refine.py` performs a bounded, checkpointed search on feasible chords
   around a selected ledger point.  It is used independently around the raw-gap
   point (783) and the weakest-curvature point (379).
3. `launch_remote_jobs.sh` starts four one-thread shards (800,000 total trials),
   each with its own PID, checkpoint, manifest, and append-only evidence logs.

Every floating candidate from the local search requires an independent
high-precision replay before it can be treated as mathematical evidence.

## Replayed result for ledger index 783

The recorded float64 midpoint gap is exactly two ULP at the scale of the three
entropy values:

- float64 gap: `+7.105427357601002e-15`;
- float64 ULP at the midpoint entropy: `3.552713678800501e-15`;
- 140-digit count-formula gap: `-9.8554731864878665e-16`;
- 140-digit centered curvature: `-0.0438911093074687...`;
- analytic float64 Hessian eigenvalue from the ledger: `-0.0438678918694138...`.

The arbitrary-precision gap stays negative for every tested step multiplier
from `2^-8` through `2^2`.  As the multiplier decreases, the centered curvature
converges to `-0.04386789...`.  The normalization residual at 140 digits is at
most about `2.2e-136`.  Thus this particular positive sign is explained by
subtraction quantization, while the broader concavity question remains open.

`index783_high_precision.json` contains all entropy values, normalization
checks, and the complete step scan.

The resume path was exercised on the server by running 20 trials and extending
the same checkpoint to 40 trials with the saved random-generator state before
the long shards were launched.

## Completed neighborhood search

All four shards completed normally: 800,000 feasible-chord proposals in total,
with no candidate records at the prespecified thresholds (`lambda_max > 1e-9`
or midpoint `gap > 1e-10`).

| shard | source | trials | best float64 lambda | finite-step gap |
|---|---:|---:|---:|---:|
| raw_a | 783 | 150,000 | `+1.393e-14` | `-6.310e-6` |
| raw_b | 783 | 150,000 | `+6.287e-15` | `-5.729e-7` |
| weak_a | 379 | 250,000 | `+6.746e-14` | `-9.199e-6` |
| weak_b | 379 | 250,000 | `+5.836e-15` | `-1.216e-5` |

The tiny positive Hessian values are themselves at the float64 floor.  In every
case the eigenvector is essentially a cross-block coordinate whose coupling has
been driven close to zero; the finite-step test along that same direction is
decisively negative.  The search therefore localized a second numerical issue:
near a decoupling/flat direction, eigensolver roundoff can make an approximately
zero local eigenvalue slightly positive even while the resolved finite chord is
negative.  `completed_search_summary.json` records the per-shard results.
