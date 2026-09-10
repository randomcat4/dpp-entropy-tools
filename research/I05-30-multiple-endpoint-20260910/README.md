# I05-30 multiple-endpoint continuation

Base: `main` at `8f4acd31d0ce4d37defafbfcff22fa2b21356f72`.

Status: new claims are **author proofs / author finite evidence, PENDING_REVIEW**. Novelty is **NOT_ASSESSED**. This branch is a successor to PR95 and does not modify PR94 or PR95 evidence under review.

## Files

- `RESULT.md`: arbitrary-multiplicity finite affine DPP endpoint theorem; rank-two vanishing-order analysis; explicit dense correlated 3+3 rank-two double-endpoint whole chord.
- `ADDENDUM_TWO_SCALE_STABILITY.md`: uniform moving maximal-chord stability when repeated rank-two endpoints split, including simultaneous K / I-K activity.
- `SOURCES_AND_FAILURES.md`: accepted-premise boundary, primary sources, structurally different method comparison, and preserved failures.
- `input/fixture.json`: exact rational construction of the new 3+3 object.
- `code/verify_double_endpoint_fixture.py`: author exact checker for legality, all 64 complete laws, endpoint orders, continuum quadratic inequalities, moment/Fisher constants, logarithm comparisons, and PR94 nonproportionality witnesses.
- `output/verify_double_endpoint_fixture.stdout.txt`: clean retained author stdout. It is not independent computation.

## Main author conclusions

1. For every finite true affine DPP path entering a legal boundary from a strict interior, complete Shannon curvature satisfies `H'' -> -infinity` at the boundary. Repeated zero/one spectral multiplicities and simultaneous K / I-K activity are allowed.
2. In cross rank two, a double complete atom really has an adverse logarithmic acceleration divergence, but a strict-interior DPP necessarily has a simple-order complete-event group whose Fisher pole dominates it.
3. The explicit new dense correlated 3+3 rank-two path has maximal legal chord `[-1,1]`, K-nullity two at both endpoints, lies outside PR94's exact grouped-channel shape, and satisfies the author whole-chord bound `H''(t)<=-(1/100)t^2` for `0<|t|<1`.
4. Around any rank-two seed with a positive whole-interior normalized curvature margin, endpoint multiplicity is no longer a stability obstruction: a two-scale full/adjacent-cardinality Fisher estimate yields a relative-open neighborhood whose members retain a fixed fraction of the margin on their own maximal chords.

## Scope limits

The general dense correlated rank-two whole-chord theorem remains **INCOMPLETE**, because the compact strict interior can still fail to have a known universal sign. I05-30 removes the endpoint multiplicity obstruction; it does not prove the missing interior theorem. Cross rank greater than two, a uniform higher-rank multi-scale hierarchy, entropy-rate claims, and novelty are not asserted.
