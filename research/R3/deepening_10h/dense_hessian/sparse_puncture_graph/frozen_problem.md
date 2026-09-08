# D10-U4 sparse puncture graph

AUTHOR STATUS: PROOF_CANDIDATE_PENDING_INDEPENDENT_REVIEW.

Fix n>=2, X=diag(x) with every 0<x_i<1, and a real symmetric zero-diagonal
A. Its support graph G has edge ij iff A_ij!=0. The curve is
K_epsilon=X+epsilon A for both signs of sufficiently small epsilon.
The Hessian acts on every real symmetric observation-coordinate direction D,
not just on directions supported in G or commuting with K_epsilon.

The general question is whether connected G suffices for negative-definite
full entropy Hessian at every sufficiently small nonzero epsilon. That question
is not presumed true. Exact-event entropy always means inclusion-determinant
Mobius inversion, or a proved equivalent formula.

Candidate outcomes of this work:

1. Disconnected support cannot produce a negative-definite full Hessian: there
   is a nonzero cross-component symmetric direction with curvature exactly zero.
2. If G is connected and has diameter at most two, its punctured ray DOES have
   negative-definite full Hessian for all sufficiently small nonzero epsilon.
3. In n=3 this classifies every support: triangle and path/star succeed;
   single-edge-plus-isolated and empty graph fail. Thus connected support is
   necessary and sufficient in dimension three.
4. The bridge is a general-n sixth-degree entropy expansion, including the
   fact that the entire fifth-degree term vanishes, not merely at x_i=1/2.

The general connected case of diameter>=3 remains INCOMPLETE. A bounded
degree-eight P4 calculation is only SCOUT evidence for its first missing-edge
curvature, not proof that all connected graphs work. No novelty or author
self-CORRECT claim is permitted. No boundary kernels are included.
