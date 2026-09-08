# A2: moving physical frames and nonuniform boundary limits

First milestone: **VERIFIED within the frozen v2 and v3 scopes**. The finite
unrestricted real-kernel question remains **INCOMPLETE**. No positive entropy
counterexample is claimed.

This route uses the full exact-event DPP law and the counterexample-oriented
gap Delta=[H(K_-)+H(K_+)]/2-H((K_-+K_+)/2). A positive gap is required for a
counterexample. Physical observation coordinates remain fixed.

## An explicit path outside the old fixed hierarchy

The four-dimensional rational rotation in [frozen v2](frozen_theorem_v2.md)
has exactly feasible endpoints and their genuine arithmetic midpoint.
Midpoints at distinct parameter values do not commute. This rules out direct
representation by the two fixed-data midpoint hierarchies in PR #11, even
under a common scalar reparameterization or one fixed orthogonal representation.

The complete [16-event proof](proofs/rational_frame_v2.md) gives

    Delta(t,x)=-[x^2+(1-x^2)log(1-x^2)]t^2
               +O_J(t^3 log(1/t)),

uniformly for x in every compact interval J inside (0,1). The first coefficient
is strictly negative. This is a new checked path exclusion, with the same
scalar leading coefficient as an older paired case. It does not cover a
direction x(t) tending to zero or one.

## Uniform estimates and an exact scaling obstruction

[Frozen v3](frozen_theorem_v3.md) and its [proof](proofs/uniform_event_bounds_v3.md)
provide a zero-safe full-event entropy error bound, a matrix perturbation
bound, and sufficient quantitative conditions for extending the transverse
negative sign to bounded moving data. The conditions explicitly control the
smallest active projection probability and the size of the direction.

An exact two-coordinate crossover then shows why a shrinking direction cannot
simply be substituted into a fixed-data leading term. With b=epsilon^kappa,
the three leading gaps are

| Fixed kappa | Leading Delta |
| --- | --- |
| 0<kappa<1/2 | -(1-2kappa)epsilon^(1+2kappa)log(1/epsilon) |
| kappa=1/2 | -(2log 2-1)epsilon^2 |
| kappa>1/2 | -epsilon^(4kappa)/2 |

The proof includes a common exact crossover expression and an explicit error
bound. Its purpose is the nonuniformity obstruction, not a new two-dimensional
sign exclusion. All three regimes remain negative.

## Verification and reproduction

One independent GPT-5.5 xhigh reviewer, who did not create either proof,
returned two commit-bound `CORRECT` reports:

- [v2 review](verifications/final_v2_review.md), candidate `ab4d57c`;
- [v3 review](verifications/final_v3_review.md), candidate `5084d39`, covering
  proof Sections 1--4. Sections 5--7 remain contextual material.

The [exact-event checker](artifacts/README.md) records seven distinct rational
chords with strict negative outward enclosures, and 48 symbolic event
functions. Those finite checks support, but do not prove, the family theorem.
The [partial Lean check](formal/README.md) verifies only five fixed integer
matrix identities; it does not formalize the entropy statements.

All candidates, failed inferences and actual coverage are retained in
[rounds](rounds.md), [provenance](provenance.md), and the
[frame attempt ledger](artifacts/frame_attempts.md). Novelty remains unaudited.
Public coordination: [issue #12](https://github.com/randomcat4/dpp-entropy-tools/issues/12)
and [Draft PR #13](https://github.com/randomcat4/dpp-entropy-tools/pull/13).
