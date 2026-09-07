# R1: unrestricted real-symmetric finite DPP entropy

Status: **VERIFIED_FOR_STRUCTURAL_FAMILIES / no counterexample found**. Tracking issue: #7.

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

- Three bounded optimizer batches made 55,780 formal objective calls in 240
  restarts across `n=3,...,10`. Each call computed the maximum eigenvalue of
  the full numerical Hessian over all real-symmetric directions. No candidate
  passed the fixed `1e-6` promotion threshold. The second-stage maximum,
  `5.930937647366978e-15`, was at its eigen-residual scale and its two direct
  chord gaps were negative.
  A non-author commit-bound audit of the source, ledger summary, accounting,
  and complement signs returned `STATUS: CORRECT`.
- An independent probability/derivative implementation passed an exact
  rational Mobius/L-ensemble check and `n=2,...,5` finite-difference checks.
- A rational certificate tool correctly distinguishes strict negative gap,
  unresolved zero gap, and infeasible endpoints. No positive candidate was
  supplied to it.
- Two auxiliary diagonal-center results are commit-bound and independently
  verified: a full Hessian formula and a strict finite-chord exclusion. They
  are not statements of global real-symmetric concavity.
- A third commit-bound theorem strictly extends part of that exclusion: at any
  block-diagonal strict midpoint, every nonzero pure cross-block feasible
  chord has strictly negative midpoint gap. A non-author review returned
  `STATUS: CORRECT`.
- Phase-2 certificate stress tests covered strict spectral margins with event
  mass down to `1e-12`, exact zero gap, deliberately unseparated tiny gap,
  boundary endpoints, and invalid floating input. All conservative status
  expectations passed.

Finite non-hits are retained only as denominators, never as a global theorem.
See the subdirectory READMEs for replay commands and dependency limits.
