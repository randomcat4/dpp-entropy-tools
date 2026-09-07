# Hazard Ledger

Listed hazards are not exhaustive. Verification begins with the generic core
checks and then applies the DPP-specific checks below.

## Generic Core

- Quantifiers: v1 certifies only the explicitly listed finite input and covered
  chord points or intervals. It does not quantify over all kernels or paths.
- Domains and degeneracies: repeated eigenvalues, zero probabilities, endpoint
  kernels, singular minors, and tiny entropy gaps must be covered or refused.
- Choice and definability: all subsets of `E` must be enumerated deterministically.
- Reduction reversibility: principal minors are inclusion probabilities; exact
  event probabilities need Mobius inversion or an equivalent derivation.
- External theorem assumptions: any interval, Sturm, Bernstein, or eigenvalue
  theorem must have its hypotheses recorded before use.
- Finite to general: finite examples cannot be promoted to global concavity,
  entropy-rate, or real-symmetric claims.
- Circularity: an unproved statement saying "all exact masses are feasible" is
  not a certificate unless every mass or an equivalent condition is actually
  checked.

## DPP And Entropy Specific

- Exact event formula: for marginal kernel `K`, exact mass is
  `sum_{T superset S} (-1)^(|T|-|S|) det(K_T)`, not generally `det(K_S)`.
- Normalization: `sum_S q_t(S)` must be checked. For exact arithmetic this
  should simplify to 1; numeric enclosures must prove containment of 1.
- Feasibility: negative exact masses invalidate a finite DPP point certificate.
  A spectral `[0,1]` check is acceptable only when its own proof is rigorous.
- Zero probability: evaluate `-p log p` at `p=0` by limit; no epsilon patch.
- Log enclosure: monotonicity of `-p log p` changes at `p = exp(-1)`, so interval
  bounds must split or reason around that maximum.
- Chord orientation: this route defines positive gap as
  `H(tm) - ((1-alpha)H(t0)+alpha H(t1))`; any opposite sign must be labeled.
- Path interval: pointwise chord feasibility does not certify feasibility on the
  entire interval.
- Symmetry: input must be symmetric or refused; real nonsymmetric determinants
  do not define the intended marginal-kernel DPP.
- Precision metadata: dependency versions, command, exit code, and certificate
  hash must describe the actual run, not the planned run.
