# Analytic neighborhoods of arbitrary product diagonals

## Theorem

Fix `0<eta<1/2`.  There are positive constants `epsilon_eta,a_eta,b_eta`
such that, for

```text
K(d,e)=[[d1,x,y],[x,d2,z],[y,z,d3]],
d_i in (eta,1-eta),             max(|x|,|y|,|z|)<epsilon_eta,
```

the kernel is strict and, for every real-symmetric test direction

```text
V=[[u1,q1,q2],[q1,u2,q3],[q2,q3,u3]],
```

the complete-event DPP entropy satisfies

```text
D^2H(K)[V,V]
<=-a_eta sum_i u_i^2-b_eta sum_j w_j q_j^2,            (1)

w1=x^2+y^2z^2,     w2=y^2+x^2z^2,     w3=z^2+x^2y^2.
```

Consequently the Hessian is negative semidefinite throughout this whole
convex tube and negative definite exactly when the off-diagonal support graph
is connected.  Nevertheless `H` is strictly concave on the entire tube: every
nonconstant chord contained in it has strict midpoint loss.

This is a neighborhood theorem, not global concavity for all strict `3 x 3`
kernels.  No radius uniform as `eta` tends to zero is asserted.

Choose `epsilon_eta<eta/4`.  The off-diagonal perturbation has operator norm
at most `2epsilon_eta`, so both spectral margins are positive.

## Exact event density

Under the product probability `Q_d`, let `X_i` be independent Bernoulli
variables of means `d_i`, set `v_i=d_i(1-d_i)`, and put

```text
psi_i=(X_i-d_i)/v_i,
g2=-x^2 psi1 psi2-y^2 psi1 psi3-z^2 psi2 psi3,
g3=2xyz psi1 psi2 psi3,             g=g2+g3.
```

Boolean Mobius inversion gives, for every complete event,

```text
p_K(S)=Q_d(S)(1+g(S)).                                  (2)
```

Equivalently, with `s_i=2*1_{i in S}-1` and `r_i=d_i` or `1-d_i` according as
`i` is present or absent,

```text
p_K(S)=r1r2r3-x^2s1s2r3-y^2s1s3r2-z^2s2s3r1
       +2xyzs1s2s3.
```

The one-point marginals remain `d_i`; hence

```text
H(K)=sum_i h(d_i)-E_Q[(1+g)log(1+g)],                  (3)
```

where `h` is binary entropy.  On the compact diagonal cube the `psi_i` are
uniformly bounded.  For small uniform `epsilon_eta`, `|g|<1/2` on all eight
events, so the series and all derivatives used below converge uniformly and
are jointly analytic in `(d,e)`.

## Leading Taylor structure

Using

```text
(1+g)log(1+g)=g+g^2/2-g^3/6+g^4/12-...,
```

the degree-four, six, and seven terms are

```text
H=sum_i h(d_i)
 -1/2[x^4/(v1v2)+y^4/(v1v3)+z^4/(v2v3)]
 -1/6[kappa12 x^6+kappa13 y^6+kappa23 z^6]
 -3x^2y^2z^2/(v1v2v3)
 +2xyz[x^2y^2(1-2d1)/(v1^2v2v3)
       +x^2z^2(1-2d2)/(v1v2^2v3)
       +y^2z^2(1-2d3)/(v1v2v3^2)]
 +O(||e||^8),                                           (4)

kappa_ij=(1-2d_i)(1-2d_j)/(v_i^2v_j^2).
```

The degree-five term vanishes exactly.  These finite identities are replayed
by `certificate/phase4/scripts/diagonal_perturbation_exact.py`.

For a pure off-diagonal test direction, the first Hessian terms include

```text
-6[x^2q1^2/(v1v2)+y^2q2^2/(v1v3)+z^2q3^2/(v2v3)]
```

and the missing-edge direction of a path center first appears with the strict
negative term `-6x^2y^2q3^2/(v1v2v3)`.  A crude radial remainder is
insufficient for anisotropic approaches to an axis, so the proof below uses
the weights in (1).

The diagonal and mixed blocks begin as

```text
H_dd=-diag(1/v_i)+O(||e||^4),
H_{d_i,e_ij}=2e_ij^3(1-2d_i)/(v_i^2v_j)+O(||e||^5).    (5)
```

The center displacement `e` and test direction `q` are independent here.

## Exact disconnected degeneracy

At a single-edge center, for example `(x,0,0)`, the Hessian on the two
cross-block directions `y,z` is exactly zero, including their mixed entry and
all entries joining them to `d` or `x`.  Indeed,

```text
g=-x^2psi1psi2,
g_y=g_z=0,
g_yy=-2psi1psi3,        g_zz=-2psi2psi3,
g_yz=2xpsi1psi2psi3.
```

Every relevant second derivative of (3) is an expectation of a function of
`(X1,X2)` times `psi3`, and is zero.  The same holds under permutations.  At a
product center all three pure-off-diagonal Hessian directions are zero.

## Monomial classification of the full remainder

Set

```text
a1=1/(2v1v2),       a2=1/(2v1v3),       a3=1/(2v2v3),
b=3/(v1v2v3),
H=sum_i h(d_i)-sum_j a_j e_j^4-bx^2y^2z^2+R(d,e).     (6)
```

The complete analytic remainder is a sum, with permutations, of

```text
(i)   x^6 A(d,x^2),
(ii)  x^4y^4 B(d,x^2,y^2),
(iii) x^4y^2z^2 C(d,x^2,y^2,z^2),
(iv)  x^3y^3z D(d,x^2,y^2,z^2).                       (7)
```

All coefficient functions are analytic near zero with uniform `d`-derivative
bounds on the compact cube.

To prove (7), conjugation by diagonal sign matrices shows that every nonzero
edge monomial has either three even exponents or three odd exponents.  A
one-edge even monomial starts at degree four; after removing that term it has
type (i).  A two-edge even monomial cannot have exponent two on either edge,
because its second derivative would violate the exact single-edge-axis
cross-block cancellation; hence it has type (ii).  A three-edge even monomial
is divisible by `x^2y^2z^2`; after removing its constant coefficient, analytic
division by one of the three squared coordinates gives type (iii).  For an
odd monomial, two exponents cannot both equal one, by the same single-edge-axis
mixed-derivative cancellation.  At least two exponents are at least three,
giving type (iv).  Absolute convergence on a smaller polydisc permits a
disjoint collection of all monomials into these four types.

## Uniform weighted remainder

For `|x|,|y|,|z|<=epsilon<=epsilon_0<=1`, there is a uniform constant `C`
such that

```text
|R_ee[q,q]|<=C epsilon^2 sum_j w_jq_j^2.               (8)
```

No positive lower bound on an individual edge or on a ratio of edge sizes is
used.  The elementary bounds

```text
sqrt(w1)>=|x|,        sqrt(w1)>=|yz|,        w1>=2|xyz|
```

and their cyclic versions control each generator in (7).  For example:

- `d_xx(x^6)=30x^4<=30epsilon^2w1`;
- all second derivatives of `x^4y^4` are bounded by `Cepsilon^2` times the
  corresponding weight or geometric mean;
- the diagonal derivatives of `x^4y^2z^2`, such as `12x^2y^2z^2` and
  `2x^4z^2`, are bounded by `12epsilon^2w1` and `2epsilon^2w2`; its mixed
  derivatives satisfy the geometric-mean analogues;
- for `x^3y^3z`, the first two diagonal derivatives use `w1,w2`, the `zz`
  derivative vanishes, and, for example,
  `3|x^2y^3|<=3epsilon^2sqrt(w1w3)`.

Multiplying by further even powers preserves these bounds.  The sole new
`zz` derivative of type (iv) after a positive `z^2` power is controlled by
`|x^3y^3z|<=epsilon^3w3`.  Differentiation factors grow only quadratically in
degree.  On a polydisc strictly inside the absolute convergence radius, their
coefficient-weighted sum is finite uniformly in `d`.  Off-diagonal entries are
converted to (8) using
`2sqrt(w_iw_j)|q_iq_j|<=w_iq_i^2+w_jq_j^2`.

The same argument with one or no edge derivative gives

```text
|(H-H0)_{d_i,e_j}|<=Cepsilon^2sqrt(w_j),
||(H-H0)_dd||<=Cepsilon^4,              H0=sum_i h(d_i). (9)
```

Derivatives in `d` only affect uniformly bounded analytic coefficients and
preserve all edge factors.

## Full six-dimensional Hessian

The explicit polynomial part of (6) has off-diagonal Hessian diagonal entries

```text
-12a1x^2-2by^2z^2,
```

and cyclic versions.  Its mixed entries come only from the sextic product.
For example, the `xy` contribution to the quadratic form satisfies

```text
8b|xy|z^2|q1q2|
<=4bz^2(x^2q1^2+y^2q2^2).
```

After shrinking `epsilon`, these mixed losses and (8) are absorbed by the
negative diagonal terms, giving

```text
H_ee[q,q]<=-c0/2 sum_jw_jq_j^2                         (10)
```

for a uniform `c0>0`.  Equation (9) and the product Hessian give

```text
H_dd[u,u]<=-a0||u||^2,
|H_de[u,q]|<=C1epsilon^2||u||sqrt(sum_jw_jq_j^2).
```

Young's inequality applied to twice the mixed block yields an
`O(epsilon^4)` multiple of the weighted off-diagonal norm, which is absorbed
by (10) after one final decrease of `epsilon`.  This proves (1).

## Graph strata and strict chords

For three vertices, all `w_j` are positive exactly when at least two edges are
nonzero, i.e. the support graph is connected.  Equation (1) then gives a
negative-definite Hessian.  At a single-edge center, the active diagonal and
edge directions are strict and the two exact cross-block directions form the
Hessian kernel.  At a product center, exactly the three pure-off-diagonal
directions form the kernel.

The tube

```text
U_eta={K(d,e):d_i in (eta,1-eta), |e_j|<epsilon_eta}
```

is open, convex, full dimensional, and contained in `0<K<I`.  Along a
nonconstant affine chord, if the diagonal direction `u` is nonzero then (1)
is strict everywhere.  Otherwise choose `j` with `q_j!=0`; the affine center
coordinate `e_j` vanishes at at most one parameter value, and `w_j>=e_j^2`.
Thus curvature is strictly negative except possibly at one point.  Integrating
with the positive chord kernel proves strict midpoint loss and strict
concavity throughout `U_eta`.

## Verification boundary

The exact script verifies the eight event identities and the finite degree
four, six, and seven entropy coefficients, with degree five absent.  The
uniform analytic remainder argument above is a human proof, not a script
claim.  Two independent nonauthor contexts audited the monomial
classification, weighted remainder, mixed-block absorption, graph strata, and
strict chord integration; both returned `CORRECT`.

This theorem covers only a sufficiently small tube around the compact product
diagonal cube.  General strict connected `3 x 3` entropy concavity remains
open.
