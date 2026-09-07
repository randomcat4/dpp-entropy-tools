# R1: unrestricted real-symmetric finite DPP search

Status: **RUNNING / INCOMPLETE**.

Tracking issue: #7. Branch: `research/R1`.

This lane studies the Shannon entropy of a finite DPP with a real-symmetric strict positive-contraction marginal kernel. It searches dimensions `3 <= n <= 10` without restricting the kernel to previously tested symmetry families.

For each subset `S`, the exact event probability is obtained from the inclusion probabilities by Boolean-lattice Möbius inversion:

```text
p_K(S) = sum_{A superset S} (-1)^(|A|-|S|) det(K_A).
```

Principal minors are not treated as exact event probabilities.

The target is a fixed rational chord `K_- = K_0 - tV`, `K_+ = K_0 + tV` with `0 < K_-, K_0, K_+ < I` and

```text
Delta = (H(K_-) + H(K_+))/2 - H(K_0) > 0.
```

A positive value of `H(K_0) - (H(K_-) + H(K_+))/2` is not a counterexample. Floating-point curvature or gap values are candidate diagnostics only. Promotion requires an independent probability implementation, a fixed rational input, strict feasibility, an outward-rounded entropy-gap certificate, and fresh-context review of the frozen commit.

The first bounded work unit separates parameter search, probability/derivative checks, and rigorous certification. Search denominators and failed batches will be retained. A finite non-hit is not evidence of global concavity.
