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
