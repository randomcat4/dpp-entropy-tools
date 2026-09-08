# N3 inequality first unit

Status for the frozen N3 target: `INCOMPLETE`.

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
