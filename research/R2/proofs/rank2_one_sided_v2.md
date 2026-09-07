# Rank-two tomography-kernel seal for one-sided branches

Status: PROVED for the high-rank `r=2` one-sided pure-deletion branch
`Y=0`, and for the particle-hole dual low-rank `s=2` one-sided branch
`X=0`.

This file does **not** claim a sign theorem for general simultaneous
`X,Y` cross directions.

## 1. Rank-two structure of `ker M_U`

Let `r=2`, and write the `i`-th row of `U` as

```text
u_i=(u_{i1},u_{i2}) in R^2.
```

For a one-hole event `{i}`, the cofactor vector is, up to the harmless fixed
sign convention,

```text
alpha_i = J u_i,
J = [ 0  -1 ]
    [ 1   0 ].
```

Thus `M_U(X)=0` says

```text
alpha_i^T X alpha_i = 0       for every row i.
```

Summing over `i` gives

```text
tr X = sum_i alpha_i^T X alpha_i = 0,
```

because `sum_i alpha_i alpha_i^T = J(U^T U)J^T=I_2`.

If `X != 0`, then `X` is a nonzero real symmetric traceless `2 x 2` matrix.
Its eigenvalues are `lambda,-lambda`, and its null cone is the union of two
orthogonal lines.  Every nonzero `alpha_i` lies on this null cone, hence every
nonzero row `u_i=J^T alpha_i` also lies on the union of two orthogonal lines.

After an orthogonal change of basis in the high subspace, the rows of `U` have
disjoint-axis form

```text
u_i=(xi_i,0)            i in I,
u_j=(0,eta_j)           j in J,
u_k=0                  k outside I union J,
```

with

```text
sum_{i in I} xi_i^2 = 1,
sum_{j in J} eta_j^2 = 1.
```

Below write the squared weights

```text
p_i=xi_i^2,
q_j=eta_j^2,
sum_{i in I} p_i = 1,
sum_{j in J} q_j = 1.
```

In the same basis, `M_U(X)=0` forces the diagonal entries of `X` to vanish:

```text
X = [ 0  x ]
    [ x  0 ],
```

with `x != 0`.

This proves the structural closure: a nonzero high-rank-two tomography-kernel
direction exists only in disjoint-support coordinates.

## 2. Pure-deletion `C2` reduces to the small-kernel coefficient

Consider the one-sided branch `Y=0`; `C` may be fixed but is not varied.  The
`C2` decomposition from `b_zero_c2_decomposition_v2.md` has no active mixed
term `q_S(X,Y)`, no low one-flip/two-flip variation, and a zero-support cross
term `C_0UV<=0`.  It remains to compute the pure high-deletion contribution.

Write

```text
A = [ a  b ]
    [ b  c ],
X = [ 0  x ]
    [ x  0 ].
```

Endpoint feasibility is `A+X>=0` and `A-X>=0`.  If `x!=0`, this implies
`a>0` and `c>0`.

The active projection events are pairs `{i,j}` with `i in I`, `j in J`, and

```text
a_{ij}=p_i q_j.
```

Since `tr(X^2)=2x^2`, the active high part contributes

```text
x^2 sum_{i,j} p_i q_j (1+log(p_i q_j)).
```

The one-hole rates are

```text
m_i(A)=p_i c,       m_i(X^2)=p_i x^2,       i in I,
m_j(A)=q_j a,       m_j(X^2)=q_j x^2,       j in J.
```

Therefore the one-hole finite correction contributes

```text
-x^2 sum_{i in I} p_i(1+log(p_i c))
-x^2 sum_{j in J} q_j(1+log(q_j a)).
```

The row-weight entropy terms cancel against the active contribution, leaving

```text
-x^2(1+log(ac)).
```

There is only one two-hole coordinate event, the empty event.  Its rates are

```text
det A,
det(A+X),
det(A-X).
```

Thus the full pure high-deletion coefficient is

```text
Gamma_U(A,X)
 = -x^2(1+log(ac))
   + f(det A)
   - (1/2)f(det(A+X))
   - (1/2)f(det(A-X)),
```

where `f(t)=t log t` and `f(0)=0`.

This is exactly the ordinary `2 x 2` small-kernel two-point coefficient for
the chord `A-X, A+X` around `A`: the diagonal product is `ac`, and

```text
( det(A+X)+det(A-X) )/2 = det A - x^2.
```

By the small-kernel two-point theorem already proved in
`small_kernel_two_point_v1.md`,

```text
Gamma_U(A,X) < 0
```

whenever `X!=0` and both endpoints are PSD.  Boundary cases such as
`det(A+X)=0` or `det(A-X)=0` are covered by the convention `f(0)=0` and by the
small-kernel theorem's boundary analysis.

The total one-sided `Y=0` coefficient is

```text
C2(Y=0) = Gamma_U(A,X) + C_0UV,
```

with `C_0UV<=0`.  Hence

```text
C2(Y=0) < 0
```

for every nonzero `X in ker M_U`.  If `X=0`, the varied high branch is
identical and this one-sided contribution is zero.

Thus all high-rank-two one-sided pure-deletion branches are sealed.

## 3. Low-rank-two particle-hole dual

The same argument applies when the low rank is `s=2` and
`Y in ker M_V` is nonzero.

Let `Q=[U,V]` be the full orthogonal eigenbasis.  For an `(r+1)`-event `T`,
the one-particle cofactor vector

```text
beta_T = ( det([U,v_j]_T) )_j
```

is, up to a global sign from Jacobi's complementary minor identity, the
one-hole cofactor vector for the complementary single row of `V`.  Therefore
`M_V(Y)=0` imposes the same rank-two null-cone condition on the rows of `V`.

After an orthogonal change of basis in the low subspace, the rows of `V` lie
on two disjoint coordinate axes, and

```text
Y = [ 0  y ]
    [ y  0 ].
```

For the one-sided branch `X=0`, the same computation gives

```text
C2(X=0) = Gamma_V(C,Y) + C_0UV,
```

where `Gamma_V(C,Y)` is the ordinary `2 x 2` small-kernel two-point
coefficient for `C-Y, C+Y` around `C`, and `C_0UV<=0`.  Hence

```text
C2(X=0) < 0
```

for every nonzero `Y in ker M_V` with PSD endpoints.

## 4. Boundary of the seal

This rank-two seal covers:

1. all high-rank `r=2` one-sided deletion branches `Y=0`;
2. all low-rank `s=2` one-sided insertion branches `X=0`;
3. singular PSD endpoints, via the same `f(0)=0` boundary convention used in
   the small-kernel theorem.

It does not cover simultaneous nonzero `X,Y`.  In that genuinely crossed
case, the active-support term

```text
sum_{p_P(S)>0} (log p_P(S)) q_S(X,Y)
```

from the general `C2` decomposition remains signed, and the argument above
does not turn it into a small-kernel Jensen gap.

