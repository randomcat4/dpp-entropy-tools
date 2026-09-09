# Final bounded certificate target: one existing non-scalar box

Status at freezing: acceptance pending complete persisted certificate and nonauthor output review. This selects an already frozen center and radius; it introduces no new search points and no new theorem assumptions.

Use the same rational 5x3 isometry U from W3. In coordinates (A11,A22,A33,A12,A13,A23), let

    A0 = [[41/100, -3/25, 0],
          [-3/25,  17/50, 0],
          [0,          0, 3/4]],
    rho = 1/2048.

A0 is the input center R12_boundary_mid: an exact rational orthogonal conjugate of diag(1/4,1/2,3/4). The target position set is every real symmetric A whose six independent entries differ from A0 by at most rho.

Required conclusion: for every such A and every nonzero real symmetric V, the complete configuration Shannon entropy of K=UAU^T satisfies H''_A[V,V] < 0 along the genuine affine path A+tV. The zero direction has derivative zero. There is no commutativity restriction.

The whole box is contained in 0<A<I because ||A-A0||op <= 3rho and its spectral envelope is [509/2048,1539/2048]. The box is not claimed wholly inside 1/4 I <= A <= 3/4 I. Its intersection with that target band is nonempty, since A0 itself lies there. The other eleven original requested centers are outside this final accepted-scope target unless separately certified.

Acceptance requires a complete exact interval Hessian/preconditioner/Gershgorin witness, positive lower bounds for all 26 positive-support events, the six constant-zero events, fixed source/input identity, and actual run completion. Decimal summaries alone are insufficient. No full spectral-domain coverage, positive-curvature counterexample, entropy-rate statement, novelty, or Lean claim follows from this certificate.
