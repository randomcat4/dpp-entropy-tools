# Lemma dependency ledger

| Lemma | Status before audit | Role and dependency |
|---|---|---|
| Finite KL data processing | KNOWN, re-proved by log-sum | Product-channel sign |
| r_i partial_i D = Jeffreys(nu,E_i nu) | PROVED_HERE_CANDIDATE | Exact marginal cancellation |
| Mixed retention derivatives of relative entropy are nonnegative | PROVED_HERE_CANDIDATE | Idempotence, commutation, data processing |
| Simultaneous product replacement Shannon entropy is concave | PROVED_HERE_CANDIDATE | Hessian entry signs and affine cross-entropy |
| Replacement output is DPP B+t(K-B) | PROVED_HERE_CANDIDATE | Inclusion moments and diagonal determinant expansion |
| Whole feasible ray concavity | PROVED_HERE_CANDIDATE | Half-rays plus differentiability at diagonal anchor |
| Radial fixed-symbol rate concavity | PROVED_HERE_CANDIDATE | Finite Jensen and stationary subadditivity |
| General nonradial scalar rate concavity | OPEN | Not inferred from entrywise signs |
| Gauge affine acceleration identity | PROVED_HERE, independently reconstructed | Finite diagnostic only |
| Infinite past residual control | Auxiliary child analysis | Not used by radial theorem |

No unproved assertion equivalent to the full conjecture is used in the radial
proof. Novelty labels are deliberately separate from proof labels.

相对原命题: the radial statement has an additional constant-anchor restriction.
EQUIVALENT_BLOCKER: none is imported into its proof. 外部定理条件核验:
finite KL contraction is re-proved, stationarity gives finite entropy
subadditivity, and the numerical certificate's separate DPP conditioning
assumptions are mapped in rate/certificate_theory.md.
