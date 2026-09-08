# Frozen theorem v1: bridge-supported imaginary curvature

Status: FROZEN by the T1 main instance, 2026-09-07. Proof authors must not change these premises.

## Objects and all quantifiers
For every integer n >= 1, let K be a real symmetric n by n matrix with 0 < K < I in the strict Loewner order. Its off-diagonal support graph G(K) has vertex set [n] and edge {u,v} exactly when u != v and K_uv != 0. An edge is a bridge when deleting it increases the number of connected components. Disconnected graphs are allowed.

Let A be any real skew-symmetric matrix such that A_uv = 0 whenever {u,v} is not a bridge of G(K). Put D = i A. This is a Hermitian matrix with zero diagonal. In particular, adding a previously absent edge is excluded by this version.

For every real t in a sufficiently small open neighborhood of zero, K(t) = K + tD is a strict Hermitian contraction and defines the full-subset DPP probability

p_S(K(t)) = (-1)^{|S^c|} det(K(t) - I_{S^c}),   S subset [n].

The Shannon entropy in natural logarithms is H(K(t)) = -sum_S p_S(K(t)) log p_S(K(t)). The sum concerns the complete random subset, not its cardinality or spectral/quantum entropy. All event probabilities are positive in this neighborhood.

## Conclusion and success standard
The ordinary second derivative at t = 0 satisfies

H''(K)[D] <= 0,

with equality if and only if D = 0. Equivalently every nonzero direction permitted above has strictly negative curvature.

Deliver a self-contained proof, an algorithm deciding these structural premises without enumerating all 2^n events, and an application to arbitrarily many dense real blocks linked by a tree of single edges.

## Input and computational interface
The mathematical input is the exact pair (K,A), including exact zero information. The implementable certificate interface accepts rational entries encoded as integers or rational strings. It checks symmetry/skew-symmetry, strict positivity of K and I-K, and bridge support. The sign conclusion does not require evaluating H or any event probability. Arithmetic-operation complexity, exact bit complexity, and floating-point diagnostics must be distinguished.

## Excluded interpretations
No statement is made for cyclic-edge imaginary perturbations, general complex centers, real perturbations, arbitrary new edges, boundary kernels with zero probabilities, global concavity along the whole line, all real kernels, or stationary entropy rates. Failed applicability is not a curvature counterexample. An author-supplied proof is not independent verification; no novelty claim is frozen.
