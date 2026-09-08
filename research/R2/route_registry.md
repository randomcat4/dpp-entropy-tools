# Route registry

## Round 3: frozen v2 general `C_2` decision

| Route | Structural fingerprint | First decisive object | Status |
|---|---|---|---|
| R3-A | exterior-minor algebra / sum-of-squares | weighted quadratic-form blocker | INCOMPLETE; superseded by R3-C structure |
| R3-B | exact counterexample optimization | 892 fully gated signed-formula trials | INCOMPLETE; no positive value |
| R3-C | coordinate components / exact cofactor-pair decomposition | universal sum of scalar Jensen defects | PROVED; two reviews CORRECT |

Resolved bottleneck: the full tomography kernel forces directions between
orthogonal coordinate components.  Componentwise Parseval identities absorb
the second-order drift into nonpositive scalar Jensen defects.

## R2-A: transverse exterior-algebra expansion

- Frozen version: v1
- Status: PROMOTED
- Representation: projection Slater amplitudes plus one-particle/hole spectral
  defects
- Key lemmas: L1, L2, L3
- Closure: compute every `epsilon log(1/epsilon)` coefficient and bound `Z`
- Fastest falsification: exact `n<=6` event enumeration against the predicted
  normalized limit
- Likely failure: missing size-`r` events with vanishing base Plucker coordinate
- Evidence: frozen coefficient formula awaiting proof and fresh review

## R2-B: probability-scale entropy lemma

- Frozen version: v1
- Status: SCOUT
- Representation: finite probability vectors grouped by base scale
- Key lemma: L2
- Closure: turn coefficient identities into an `O(epsilon)` entropy remainder
- Fastest falsification: a probability with fractional or cancellation scale
  omitted by the grouping
- Likely failure: non-uniform constants if the fixed-data convention is lost

## R2-C: exact boundary certificate

- Frozen version: v1
- Status: SCOUT
- Representation: rational/algebraic small matrices and exact Mobius inversion
- Key lemmas: L1 and the coefficient formula
- Closure: independent bounded diagnostic, then fresh read-only review of the
  unchanged candidate
- Fastest falsification: a feasible endpoint whose normalized sign disagrees
  for decreasing epsilon
- Likely failure: floating cancellation mistaken for a certificate

## Cross-category bridge probes

The faithful encodings being audited are: fermionic Slater-state leakage,
Grassmannian tangent geometry, singular perturbation of finite probability
simplexes, and Schur-complement contraction geometry.  These are representation
probes, not independent proofs.
