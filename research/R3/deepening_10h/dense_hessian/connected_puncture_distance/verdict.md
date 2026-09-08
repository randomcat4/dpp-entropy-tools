# D10-U5 verdict

STATUS: `CORRECT` for the P4 small-puncture full-Hessian theorem and, together
with the already verified U4 results, the `n=4` connected-if-and-only-if
classification. A fresh non-author audit is preserved under `verifications/`.

GENERAL CONNECTED-GRAPH SUFFICIENCY: `INCOMPLETE`.
FINITE GRAPH BATCHES: `SCOUT` / exact sanity only.

What is new relative to U4:

- The four-vertex path `P4` is promoted from a single endpoint-coordinate scout
  to a verified full-Hessian theorem.
- Combining U4 with P4 gives the verified `n=4` classification: connected
  supports succeed and disconnected supports fail.
- A general shortest-path diagonal coefficient rule was isolated:

```text
H_{ij,ij}(X+epsilon A)
  = -6 epsilon^(2d_G(i,j))
      sum_{P shortest i-j path}
        (prod_{v in P} w_v)(prod_{e in P} A_e^2)
    + higher order.
```

This rule is exact-checked through all connected labelled `n=4` graphs and
selected `n=5` graphs, including a distance-four P5 endpoint.  It remains a
candidate structural lemma, not a theorem.

The general connected-support sufficiency question remains open.  The current
blocker is not the sign of individual distance-coordinate diagonal entries;
those appear negative.  The blocker is proving that each same-distance limiting
block after multi-scale congruence is negative definite for arbitrary connected
graphs and arbitrary nonzero real weights, including overlapping shortest-path
diagrams.

No counterexample was found in this unit. The finite exact checks are SCOUT
only. The P4 theorem does not rely on their coverage: the audit independently
reconstructed a 94-term formal-parameter entropy certificate, all 36 scaled
off-diagonal Hessian entries, the mixed-block orders, and the congruence limit
for arbitrary strict diagonal entries and arbitrary nonzero path weights.
