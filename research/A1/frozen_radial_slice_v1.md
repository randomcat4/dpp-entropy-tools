# Frozen theorem: fixed-site radial coupling slices, v1

Version date: 2026-09-08. This is an auxiliary theorem, not a replacement of
`frozen_theorem_v1.md`. No three-point universal conclusion is claimed.
Proof and verification instances may not modify or add premises.

Fix c in (0,1) and a nonzero real vector v in R^2. Define the convex domain

    D(c,v) = { (A,s): A=A^T in R^(2x2), s in R,
                         0 < K(A,s) < I },
    K(A,s) = [[A, s v], [s v^T, c]].

Let H_d denote the Shannon entropy of the complete event law of the finite
d-point DPP, obtained from inclusion probabilities det(K[T]) by Mobius
inversion. Logs are natural.

Claim: F(A,s)=H_3(K(A,s)) is strictly concave on D(c,v). In particular,
for any distinct (A_-,s_-),(A_+,s_+) in D(c,v),

    (F(A_-,s_-)+F(A_+,s_+))/2
        - F((A_-+A_+)/2,(s_-+s_+)/2) < 0.

The result permits arbitrary symmetric variation of A and arbitrary real s;
v and c stay fixed. It includes connected triangular centers when s, v_1,
v_2, and A_12 are nonzero. It does not require those entries to stay nonzero
throughout the chord, and it is not limited to a block-diagonal midpoint.

Allowed background: the independently verified real two-point entropy
concavity theorem at R1 commit 603300c06059518961766c724377c3b9d1198fc5,
finite entropy differentiation, Schur complements, determinant rank-one
identities, and ordinary scalar concavity. The nonaffine conditional-kernel
acceleration must be explicitly retained. No floating evidence may replace
the proof. No novelty claim.
