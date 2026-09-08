# U7 proof risks frozen before completion

1. A surviving entropy monomial has even degree >=4 at each active vertex, but this alone is NOT enough to bound a mixed Hessian entry by graph distances. Two marked chords can connect remote disconnected parts of the support graph. The required extra statement is full block-diagonal Hessian locality, including all cross-component directions and their mixed terms.
2. Locality must apply to the residual support AFTER differentiating twice. Prove coefficient extraction by restricting all other kernel variables to zero; do not confuse the support of the original entropy monomial with the residual support.
3. Mixed entries with unequal distances matter as much as same-distance blocks. Any term below the sum of the two distance exponents would invalidate the congruence.
4. Multiple shortest paths can have signed weights. Their contributions must be proved to add as positive squares, not the square of a signed sum. Equality-case vertex counting must rule out distinct shortest paths on the same vertex set.
5. The doubled-cycle entropy coefficient is -3 for cycle length >=3, but a supported edge has quartic coefficient -1/2. Their second derivatives both give the -6 Hessian factor by different multiplicities.
6. A scalar determinant polynomial must be related back to exact event entropy through the common vertex-moment factor. Merely studying log(det K) is not sufficient.
7. Any chromatic-polynomial argument must justify extension from positive integer powers to a formal real exponent before differentiating at one.
8. Mixed diagonal/off-diagonal derivatives require coefficient identities valid in x on an open set. A pointwise cancellation at one x cannot be differentiated in x.
9. The scaling is a congruence, not an eigenvalue similarity; it is invertible only for nonzero epsilon. Its limiting diagonal signs do not give an unscaled uniform curvature margin at epsilon=0.
10. Strict feasibility, two-sided epsilon limits and full Sym(n) scope must be explicit. All finite sanity outputs remain SCOUT; the proposed general theorem rests on the analytic lemmas.
