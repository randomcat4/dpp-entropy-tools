# Frozen-v1 risks

1. The graph is the off-diagonal support of the marginal kernel K, not the
   L-ensemble kernel. A bridge must be an existing nonzero edge.
2. Conditioning on all other events needs positive conditioning probability,
   correct exclusion signs, invertible signed principal matrices, and a valid
   conditional two-point probability table.
3. Prove that the marginal distribution of the conditioned-away sites and both
   conditional diagonal entries are independent of the changing single bridge.
4. Multiple changing bridges require a joint smooth local parameterization and
   justification that mixed terms vanish at second order. Single-edge concavity
   alone is insufficient.
5. Phase gauge transformations must leave event probabilities invariant and
   must not alter a cycle within a dense block.
6. Strictness requires both a nonzero original edge and nonzero direction;
   p'=0 by conjugation alone gives no strictness or sign conclusion.
7. Strict contractions ensure a two-sided feasible affine neighborhood; zero
   probabilities at boundary kernels must not enter log or inverse formulas.
8. Counts of arithmetic operations do not bound exact-rational bit complexity.
9. The graph checker must handle disconnected graphs, isolated vertices,
   cycles, absent edges, and the zero direction without false certification.
10. The 64-event numerical check is diagnostic only. The 30-point application
    checks structure without enumerating any of its 2^30 events.
11. No implication about entropy rates, all real directions, or all imaginary
    directions is licensed by this restricted theorem.
