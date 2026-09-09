# N3 inequality first unit

Status for the frozen N3 target: `STOPPED_SUBSTANTIVE / INCOMPLETE`.

This route proves a new exact Fisher lower bound from the two conditional
covariance square identities.  It is a strict loss of information from the
eight-event Fisher form, so it is not a disguised form of the old rank-one
rho condition.  It also does not use a stronger pointwise sign assertion for
the cofactor terms.

The proved sublemma is in
[`slice_fisher_covariance_lemma.md`](slice_fisher_covariance_lemma.md).
It gives, for each coordinate k, a lower bound

```text
F(D,D) >= Q_k(D)
```

where `Q_k` consists of the Fisher information in the k-marginal plus one
centered determinant score from each of the two 2 by 2 slices conditioned on
`X_k=0` and `X_k=1`.  The lemma is recorded as an exact Pythagorean
decomposition `F=Q_k+R_k` with `R_k>=0`, not only as a Cauchy estimate.

The remaining gap is in [`verdict.md`](verdict.md).  A direct closure
`max_k Q_k(D) >= 2 tr(N adj D)` is false for arbitrary directions D.  The
clean rational sample reported by the main instance and locally rechecked here
still has positive true curvature `B=F-2 tr(N adj D)`.  The surviving possible
use of the lemma is therefore narrower: it must exploit the actual
trace-constrained optimal direction, a kernel-dependent convex combination, or
the positive residual `R_k`, not a full-direction `Q_k` dominance claim.

Command, version, seed, and exit-status records are in
[`command_log.md`](command_log.md).

The second proved sublemma is in
[`optimizer_sherman_morrison_lemma.md`](optimizer_sherman_morrison_lemma.md).
It gives the exact Sherman-Morrison formula for the true trace-constrained
optimiser of

```text
A = F2 + det(N)G + v v^T,
v(D)=Lambda'[D]/sqrt(Z),
```

and isolates the real remaining obligation: if `H=F2+det(N)G` has trace-mode
deficit `alpha-1/det(N)>0`, the rank-one Lambda score closes it exactly when

```text
beta^2/(1+gamma) >= alpha - 1/det(N).
```

The same lemma proves that the true `A` optimiser suppresses the normalised
`Lambda'` score relative to the `H`-only optimiser.  This does not prove the
frozen inequality; it turns the next step into a concrete DPP alignment
bound rather than another rho restatement.

Final closure update: the old maxQ candidate is now disproved even at the
true `A`-optimising direction, by the main instance's strict frozen
obstruction `449221bc3639c2de1239707f15dd938d6e230b9d`
(`main/stationary_obstruction_v1.md`).  This route keeps the original Qk
lemma as historical Fisher information only.  The Sherman-Morrison
`SM-close` condition is marked `EQUIVALENT_BLOCKER`; without a separate DPP
alignment lower bound for `beta^2/(1+gamma)`, it is the original trace
optimisation condition rewritten through the rank-one projection.  No active
local or server jobs were left by this route.
