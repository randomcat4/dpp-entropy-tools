# T1 bridge-direction curvature tool

Verified bridge-direction theorem and exact rational applicability checker.
Status: VERIFIED for frozen v1 and the checker; two separate fresh proof reviews
returned CORRECT. See verdict.md and verifications/.

For real K with 0<K<I and D=iA supported on existing bridge edges of K's
off-diagonal graph, the theorem asserts negative entropy curvature if A!=0.
The checker uses no event probabilities. It returns INCONCLUSIVE outside its
graph condition and OUTSIDE_DOMAIN for a non-strict contraction.

From the repository root, with Python 3.12 (standard library only):

```sh
python3 research/T1/tools/bridge_check.py research/T1/artifacts/triangles_10.json
python3 research/T1/tools/validate_bridge.py
```

Inputs are JSON matrices K and A, where the actual direction is iA. Entries
must be integers or exact rational strings such as "1/40". Floats are rejected.
Output includes exact positive LDL pivots, support bridges, active edges, and
the theorem-based sign. It is a theorem applicability certificate, not an
interval enclosure of the curvature magnitude or a formal proof certificate.

The implementation uses O(n^3) rational arithmetic operations for positivity,
O(n^2) matrix storage/construction, and O(n+m) graph traversal. Exact-rational
bit costs can grow and are not included in this arithmetic-operation count.

Examples: chains of 2 and 10 dense triangles, i.e. n=6 and n=30. The latter
has 2^30 events, none enumerated by the structural test. The regression harness
enumerates only the n=6 example for a floating-point diagnostic. The general
bridge-block family is justified analytically in the proof.

Scope exclusions: cycles with active edges, absent-edge directions, boundary
kernels, general real directions, all-kernel concavity, and entropy rates.
Known failures and run denominators are in rounds.md and artifacts/validation.json.


Stage priority: practical usefulness, correctness, and explicit applicability. Novelty is not a requirement or a gate for delivery. Existing results are reusable with accurate attribution and checked hypotheses.

Programmatic entry point (from the repository root):

```python
from research.T1.tools.bridge_check import check
result = check({
    "K": [["1/2", "1/8"], ["1/8", "1/2"]],
    "A": [[0, 1], [-1, 0]],
})
assert result["status"] == "APPLICABLE"
assert result["curvature_sign"] == "negative"
```

Downstream callers should branch on `status`: `APPLICABLE` supplies the
proved sign; `INCONCLUSIVE` supplies no sign; `OUTSIDE_DOMAIN` fails strict
contraction; `INVALID_INPUT` fails the exact matrix interface. A small nonzero
entry is an actual graph edge and must never be rounded away to obtain a
bridge certificate. The sign is for the second derivative at t=0 only.