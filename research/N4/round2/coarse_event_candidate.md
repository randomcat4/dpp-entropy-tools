# Exact co-rank-one event coordinates and entropy decomposition

Status: PROOF_CANDIDATE_PENDING_NONAUTHOR_REVIEW. Author: N4 parent.
Scope: the frozen four-point rank-three face; this is an identity, not a sign theorem.

Let r_i in R^3 be the transpose of row i of U, and w_ij=r_i cross r_j.
Let z be a unit null vector, q_i=z_i^2, d=det A, and adj denote the classical
adjugate. Since U is an isometry, sum q_i=1 and all q_i>0. For 0<A<I:

```
p_empty = det(I-A),
p_{i} = r_i^T [A^2+(1-tr A)A+d I] r_i,
p_{ij} = w_ij^T [adj A-d I] w_ij,
p_{[4] minus i} = q_i d,
p_{[4]} = 0.
```

## Derivation
Set B=A(I-A)^-1. Then L=K(I-K)^-1=U B U^T, because L is zero on z
and equals B on range U. The L-ensemble exact event formula is
p_S=det(I-A)det(L_S). For one row this is r_i^T A adj(I-A) r_i.
The characteristic polynomial of the three-dimensional A gives
A adj(I-A)=A^2+(1-tr A)A+dI, proving the singleton formula.

For a pair, the cross-product/compound identity gives
det((U B U^T)_{ij})=w_ij^T adj(B) w_ij.
Since det(I-A)adj(B)=d B^-1=adj(A)-dI, the pair formula follows.
For a triple, the square of the corresponding U minor is q_i by the
orthogonal-complement cofactor identity, and det(I-A)detB=d. The empty
and full formulas are immediate.

The three-point conditional law, given cardinality three, is the fixed law q.
Collapse all four triple events into a single symbol *. The resulting strictly
positive 12-symbol probability vector P consists of the empty, four singletons,
six pairs, and P_*=d. Its total is one and its entropy H(P) obeys

```
H_face(A;U)=H(P(A;U))+d(A) H(q).
```

Indeed -sum_i q_i d log(q_i d)=-d log d+d H(q). Since U and q are fixed
along any affine A chord, for any symmetric V this yields exactly

```
H_face''[V,V]
 = -sum_s (P_s')^2/P_s -sum_s P_s'' log P_s + H(q) d''.
```

The full event and its derivatives do not enter this identity. The grouped
triple Fisher contribution equals -(d')^2/d, exactly the sum of its four
original contributions; no Fisher term is discarded.

## Consequence to test, not to assume
The extra term H(q)d'' may be positive. This isolates the fixed full-size
projection law's contribution, without claiming it wins against other layers.
H(P) is not assumed concave. The 12 masses are constrained polynomials of the
same six entries of A, not independently affine simplex coordinates.
Changing U to alter q changes the observation law. A bounded second unit may
separate this determinant acceleration from empty/singleton/pair contributions,
but a finite no-hit cannot prove its universal domination.
