# I05-30 multiple-endpoint continuation

Base: `main` at `8f4acd31d0ce4d37defafbfcff22fa2b21356f72`.

Status: new claims are **author proofs / author finite evidence, PENDING_REVIEW**. Novelty is **NOT_ASSESSED**. This branch is a successor to PR95 and does not modify PR94 or PR95 evidence under review.

## Files

- `RESULT.md`: arbitrary-multiplicity finite affine DPP endpoint theorem; rank-two vanishing-order analysis; explicit dense correlated 3+3 rank-two double-K-endpoint whole chord.
- `ADDENDUM_TWO_SCALE_STABILITY.md`: uniform moving maximal-chord stability when repeated rank-two endpoints split, including simultaneous K / I-K activity.
- `ADDENDUM_SIMULTANEOUS_ENDPOINT.md`: explicit dense correlated 3+3 rank-two chord with `dim ker K=dim ker(I-K)=2` simultaneously at both endpoints; complete 13-type proof and two true cardinality Fisher groups give `H''<=-(1/10)t^2` on the whole strict chord.
- `SOURCES_AND_FAILURES.md`: accepted-premise boundary, primary sources, structurally different method comparison, and preserved failures.
- `input/fixture.json`: exact rational construction of the first new 3+3 double-K-endpoint object.
- `input/simultaneous_fixture.json`: exact rational construction with simultaneous double K / double complement endpoints.
- `code/verify_double_endpoint_fixture.py`: author exact checker for the first fixture.
- `code/verify_simultaneous_endpoint_fixture.py`: author exact checker for the simultaneous fixture, including all 64 complete laws, 13 likelihood types, endpoint orders, cardinality groups and compact/end-band rational inequalities.
- `output/verify_double_endpoint_fixture.stdout.txt`: clean retained author stdout for the first fixture; not independent computation.
- `output/verify_simultaneous_endpoint_fixture.stdout.txt`: author-side exact-check summary for the simultaneous fixture. Its Mobius/event and logarithm assertions were also recomputed during author development; it is not an independent S2/Codex certificate and is not presented as external raw evidence.

## Main author conclusions

1. For every finite true affine DPP path entering a legal boundary from a strict interior, complete Shannon curvature satisfies `H'' -> -infinity` at the boundary. Repeated zero/one spectral multiplicities and simultaneous K / I-K activity are allowed.
2. In cross rank two, a double complete atom really has an adverse logarithmic acceleration divergence, but a strict-interior DPP necessarily has a simple-order complete-event group whose Fisher pole dominates it.
3. The first explicit new dense correlated 3+3 rank-two path has maximal legal chord `[-1,1]`, K-nullity two at both endpoints, lies outside PR94's exact grouped-channel shape, and satisfies the author whole-chord bound `H''(t)<=-(1/100)t^2` for `0<|t|<1`.
4. Around any rank-two seed with a positive whole-interior normalized curvature margin, endpoint multiplicity is no longer a stability obstruction: a two-scale full/adjacent-cardinality Fisher estimate yields a relative-open neighborhood whose members retain a fixed fraction of the margin on their own maximal chords.
5. A second exact 3+3 seed has both `K` and `I-K` nullity two at the same endpoints. Its empty and full events are both double zeros with adverse acceleration logs, while the true `|X|=1` and `|X|=5` groups supply the dominating Fisher poles. The full maximal chord satisfies the stronger author bound `H''(t)<=-(1/10)t^2`.

## Scope limits

The general dense correlated rank-two whole-chord theorem remains **INCOMPLETE**, because the compact strict interior can still fail to have a known universal sign. I05-30 removes endpoint multiplicity—including simultaneous spectral activity—as an endpoint obstruction; it does not prove the missing universal interior theorem. Cross rank greater than two, a uniform higher-rank multi-scale hierarchy, entropy-rate claims, and novelty are not asserted.
