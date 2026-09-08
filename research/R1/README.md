# R1: unrestricted real-symmetric finite DPP entropy

Status: **N2_CONCAVITY_PROVED / VERIFIED_FOR_BLOCKS_OF_SIZE_AT_MOST_TWO / no general counterexample found**. Tracking issue: #7.

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

- The complete-event Shannon entropy of every strictly feasible real
  symmetric `2 x 2` DPP is globally concave in its marginal kernel.  The proof
  reduces the Hessian to a Fisher matrix pencil whose cubic determinant has an
  exact cancellation, then controls it by elementary log and AM--GM bounds.
  A non-author commit-bound review returned `CORRECT`.
- If a strict midpoint is block diagonal with every block of size one or two,
  every feasible real-symmetric chord has nonpositive midpoint gap, strict for
  every nontrivial chord.  The composition theorem actually bounds the global
  gap by the sum of all principal-block gaps and is strict whenever a
  cross-block entry is present.  A separate non-author commit-bound review
  returned `CORRECT`.
- A preregistered `n=2` boundary attack made 122,832 formal calls and two
  successful 90-digit rechecks.  It found no robust positive Hessian.  The
  largest raw floating value, `1.46e-11`, became `-5.23e-12` at 90 digits.
  This finite search is falsification evidence only; it is not used by the
  proof.
- The phase-4 connected `n=3` attack completed 136,898 continuous formal
  calls, all successful: 120,724 floating Hessians and 16,174 fixed-decimal
  90/140-digit reviews.  All 8,053 floating values above `1e-8` were reviewed;
  none passed the independent directional and finite-chord gate.  The raw
  maximum `0.0119709` became `-1.53765e-14` at 140 digits.  This is finite
  falsification evidence, not a proof.
- At a compound-symmetric `3 x 3` center, exact `S_3` symmetry splits the full
  six-dimensional Hessian into two `2 x 2` sign problems.  The two diagonal
  entries of the trivial block are proved strictly negative, but its
  determinant, the standard block, and the finite-midpoint step remain open.
  Separate probes checked 17,042 centers and 40,000 strict feasible chords
  without a robust positive.

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
