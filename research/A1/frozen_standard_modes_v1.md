# Frozen theorem: half-filled triangle standard modes, v1

Version date: 2026-09-08. Auxiliary statement under the unchanged A1 target.
Proof and verification instances may not alter or supplement its premises.

Let J be the real 3 by 3 all-ones matrix, and let

    K_r = (1/2) I + r (J-I),       -1/4 < r < 1/4.

Let V be any real symmetric 3 by 3 matrix such that

    tr V = 0,       V_12 + V_13 + V_23 = 0.

Use complete-event Shannon DPP entropy H, defined by Mobius inversion of
the inclusion minors and natural logarithms, as in frozen_theorem_v1.md.

Claims:

1. D^2 H(K_r)[V,V] <= 0 for all such r,V.
2. If r != 0 and V != 0, this inequality is strict.
3. At r=0, the exact value is -4 sum_i V_ii^2; thus purely off-diagonal
   directions in this subspace are flat at second order.

The subspace has dimension four (the standard isotypic component for
simultaneous site permutations), and all directions in it are included.
At r != 0 the center is a connected triangle strict contraction.

This is a local Hessian statement, not a finite-chord or full-Hessian
concavity theorem. The complementary two-dimensional symmetric component
and general nonsymmetric centers are not included in the claims. Finite
numerical evidence may check identities but cannot prove their signs.
No novelty claim.
