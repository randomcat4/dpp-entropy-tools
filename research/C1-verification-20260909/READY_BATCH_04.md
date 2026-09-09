# Ready batch 04: W4 T1--T3

Verdict: **ACCEPTED_SCOPED**.

Frozen mathematical input: PR33 commit
`0f06eef1dc723058b46596ff9b704d7e97d3522f`, result package in
`research/N3/round3/I05-W4-20260909/`. The later head
`a0869b44bdce75acb8c2438806b21d3cf013e508` adds only AUTHOR_CHECKPOINT.md;
the mathematical payload and scripts are unchanged. The acceptance covers
the frozen T1--T3 body at either version, not checkpoint plans.

For a real symmetric three-point kernel, write `x_i=K_ii` and
`v_i=x_i(1-x_i)`. The accepted domain Omega is exactly

```
0 < x_i < 1,
|K_ij| <= (1/4) sqrt(v_i v_j)   for i<j.
```

These constraints imply `0<K<I`. For every real symmetric direction D,
the full configuration entropy along the actual affine path K+tD obeys

```
-H''(K;D) >= (7/10)(S+U+V) >= 0,
```

with S,U,V defined in the frozen statement. All six independent directions
are included even at the constraint boundary; D need not be tangent to
Omega. The accepted corollaries are convexity of Omega and entropy chord
concavity on its closure, and a negative definite six-dimensional Hessian
when the nonzero-edge graph is connected. Two nonzero edges suffice:
the missing edge direction is controlled by V. Closure concavity does not
assert a finite Hessian at singular endpoints.

[The fresh nonauthor report](children/w4/REVIEW.md) checks the eight events,
full Fisher term, true affine acceleration, Rayleigh identity, three-point
log bound, two-edge and edge-diagonal estimates, the exact coefficient
merge, zero-edge degeneracies and endpoint continuity. It finds no
remaining blocking obligation in this scope.

The corrected independent certificate reconstructs the eight probabilities
and the complete Hessian and proves positivity of the residual by rational
log bounds and outward Decimal interval LDL. Seven fixed centers cover
all-zero edges, one edge, a connected two-edge path, both cycle signs at
the interaction boundary, a rare-event center, and a noncommuting example.
All passed; disconnected null rows were verified symbolically. PID 169057
exited 0 with one thread, an 8 GiB limit and a 240-second timeout.

The original full attempt timed out with exit 124. A first minimized
interval attempt was rejected after the main reviewer found ordinary
reciprocal rounding. Both original versions and outputs are retained.
The corrected computation uses explicit 90-digit floor/ceiling division
and full lower endpoints. [The main implementation review](main/W4_INTERVAL_IMPLEMENTATION_REVIEW.md)
records the defect and verified fix. Neither failed attempt supports
acceptance, and finite-center evidence does not replace the analytic proof.

Exclusions: kernels outside Omega, general real three-dimensional entropy
concavity, dimensions above three, complex kernels, stationary entropy
rates, novelty, PR30, and the new checkpoint plans. None is certified here.

This completes the five frozen C1 review units. It is a new review batch
after PR36 and PR38; only the designated integrator may merge to main.
