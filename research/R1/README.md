# R1: unrestricted real-symmetric finite DPP entropy

Status: **CANDIDATE / no counterexample found**. Tracking issue: #7.

R1 studies dimensions `3 <= n <= 10` without restricting the real-symmetric
strict positive-contraction kernel to previously tested symmetry families.
For each subset `S`, exact event probabilities are obtained from inclusion
probabilities by Boolean-lattice Mobius inversion:

```text
p_K(S) = sum_{A superset S} (-1)^(|A|-|S|) det(K_A).
```

Principal minors are not treated as exact event probabilities. The target sign
for a counterexample is

```text
Delta = (H(K_-) + H(K_+))/2 - H(K_0) > 0.
```

## Current result

- Two bounded optimizer batches made 13,202 objective calls in 176 restarts
  across `n=3,...,10`. Each call computed the maximum eigenvalue of the full
  numerical Hessian over all real-symmetric directions. No positive candidate
  passed the fixed `1e-6` promotion threshold. The best value was a negative
  near-flat `-6.245093781582534e-15`, whose direct chord gap was also negative.
- An independent probability/derivative implementation passed an exact
  rational Mobius/L-ensemble check and `n=2,...,5` finite-difference checks.
- A rational certificate tool correctly distinguishes strict negative gap,
  unresolved zero gap, and infeasible endpoints. No positive candidate was
  supplied to it.
- Two auxiliary diagonal-center results have candidate proofs: a full Hessian
  formula and a strict finite-chord exclusion. They are frozen separately and
  are not statements of global real-symmetric concavity.

Finite non-hits are retained only as denominators, never as a global theorem.
See the subdirectory READMEs for replay commands and dependency limits.
