# Frozen scope

Repository: `randomcat4/dpp-entropy-tools`

Pull request: PR136

Reviewed author head: `39098dac760cea2d27f2955bed31f80c87913810`

Author base: `3e27a09e9185cb63d8a42e4db022008ee9828136`

## Frozen target

For

`f_t(theta)=1/2+(1/4)cos(4 pi theta)+(t/8)cos(2 pi theta)`,

let `h(t)` denote the full complete-configuration Shannon entropy rate of the
stationary Toeplitz DPP, with natural logarithms and normalization per original
lattice coordinate.  The target is

`h''(t)<-1/3000` for every `t in [1/2,3/2]`.

## Authorized dependency

Only the public `ACCEPTED_SCOPED` analytic range of PR91 at author head
`c7a072ec4eea0c5b0f445bca5796873a9e234948` is imported:

- the four-branch complete-event Riccati representation and positivity;
- uniform state-ball contraction and coding-state first/second jets;
- the true complete Shannon entropy-rate identity with factor `1/2`;
- the full invariant-law second-response identity, including changing weights,
  state motion, acceleration, and nested response;
- the stated explicit analytic branch and weight derivative bounds.

No PR91 finite output or whole-interval curvature sign is imported.

## S1 / S2 boundary

S1 reviews the analytic theorem and the logical interface of all certificate
files.  S1 does not run or independently validate the 128 saved node
enclosures.  The unconditional theorem status therefore awaits S2's finite
evidence review.

## Exclusions

- novelty, priority, and publication-strength assessment;
- execution or reproduction of the author certificate;
- PR112 and PR115 interval evidence;
- spectral entropy or an affine `L`-kernel substitution;
- `D''(s)>=0` or `D'(s)>=0` separately;
- the gap `|t|<1/2`, the maximal legal interval, or general DPP concavity;
- merging into `main`.

