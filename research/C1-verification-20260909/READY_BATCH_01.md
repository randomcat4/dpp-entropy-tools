# Ready batch 01: W1 first round

Verdict: **ACCEPTED_SCOPED**.

Accepted input: PR32, commit `7c6e40bb3ba6dd0537f3c49bba83c718f86462fb`,
`research/I05-W1-20260909/result/`, Theorem T. The later PR32 head
`a8c337826ec87cf09a0cf63ea5dcd4de5de70dc8` leaves this directory unchanged
and adds a separate R2 directory. R2 is not included in this acceptance.

For fixed Hermitian strict contractions A,C and fixed vectors u,v, the
whole-configuration Shannon entropy along
`K(t)=[[A,t u v*],[t v u*,C]]` is concave on the full feasible interval.
The review accepts the stated strict Jensen conclusion for a nonzero
cross block, and the stated nonstrict closed-boundary extension by
continuity. It does not assert `H''(0)<0`: the proof gives `H''(0)=0`.

The fresh nonauthor review checked the event determinant formula, all-event
rank-one Schur identity, positivity and inverses in the interior, fixed
marginals, relative-entropy curvature argument, and endpoint passage.
[The full report](children/w1/W1_INDEPENDENT_REVIEW.md) records exact source
locations and exclusions.

An independently written exact/high-precision check passed all 16 events,
inclusion-exclusion, both fixed marginals and the curvature identity. PID
167055 exited 0. Script, fixed inputs embedded in that script, complete
stdout/stderr, structured outputs and runtime record are retained under
`children/w1/`. The diagnostic rank-two examples in that same script are
not universal concavity certificates and do not support acceptance of R2.

Review boundary: no unrestricted cross-block theorem, arbitrary rank-two
rotation reduction, stationary entropy-rate claim, or novelty priority is
certified by this batch. No review of C1's own PR30 is included.

This is an incremental handoff. W1 R2, W4, and C3's two separate claims
remain under review. Only the designated integrator may merge to main.
