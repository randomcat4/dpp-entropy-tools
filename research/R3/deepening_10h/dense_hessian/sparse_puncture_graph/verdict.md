# D10-U4 author verdict

ANALYTIC STATUS: `CORRECT` for diameter-at-most-two connected support,
disconnected obstruction, and the n=3 classification.  A fresh non-author
audit is preserved under `verifications/`.
GENERAL CONNECTED-GRAPH SUFFICIENCY: INCOMPLETE.
FINITE SYMBOLIC COMPUTATION: SCOUT / EXACT SANITY ONLY.

The candidate theorem extends U3 beyond complete support: every connected
support graph of diameter at most two produces full-Hessian-negative kernels
X+epsilon A for all sufficiently small nonzero epsilon, at every strict
diagonal X and with arbitrary nonzero real weights on the support edges.
The tested Hessian directions are ALL real symmetric matrices, including
directions on the missing edges and directions changing the diagonal.

This includes stars of arbitrary size, paths on three vertices, and complete
bipartite graphs. The threshold may depend on X and all edge weights; a compact
strict-box/fixed-support/unit-weight family with positive edge margin admits
a common threshold. Each allowed nonzero point also has an ordinary open
full-Hessian-negative neighborhood, not one uniform neighborhood containing X.

At n=3 there is a complete candidate classification:

- triangle: succeeds (already U3, also covered here);
- path / three-vertex star: succeeds, with missing-edge curvature leading at
  negative order epsilon^4 rather than order epsilon^2;
- a single edge plus an isolated vertex: fails, with an exact zero-curvature
  cross-component direction;
- empty support: fails.

Thus connected support is necessary and sufficient in n=3. In every dimension,
disconnected support is an exact obstruction; connectedness is not yet proved
sufficient beyond the diameter-two class.

The analytic mechanism is the orthogonal exact-likelihood expansion. Its
entire degree-five entropy term is zero even at heterogeneous diagonals. The
degree-six triangle term is -3 w_i w_j w_k z_ij^2 z_ik^2 z_jk^2. It gives
a missing pair ij a negative epsilon^4 Hessian coefficient precisely when it
has a common neighbor, via a sum of squared path-weight products. A three-scale
congruence, rather than an unchecked sign in a Schur complement, proves full
negative definiteness.

For distance at least three this sixth-order argument has a zero leading
coefficient. A bounded n=4 P4 calculation gives missing-endpoint curvature
-(600/49)epsilon^6 at the chosen rational parameters, but this single-entry
SCOUT is not a full-Hessian proof or a graph classification. No counterexample
to general connected-support sufficiency is claimed.

Exact sanity retained 52 atom polynomials across the general jets and two
targeted sparse checks. Every comparison passed, no random draws. These
computations do not establish the general analytic theorem on their own.

Most vulnerable review obligations: the signed determinant likelihood;
orthogonality with heterogeneous third moments; the complete list of edge
triples in E[R2^3]; exclusion of lower xM/EM terms; invertibility and limit of
the anisotropic scaling; and the block-marginal argument for exact flatness.
The independent audit rebuilt the likelihood expansion, fifth/sixth-order
coefficients, missing-edge leading terms, multiscale congruence, and exact
disconnected zero direction without importing the author sanity module.  It
found no blocking gap.  No novelty certification is claimed.
