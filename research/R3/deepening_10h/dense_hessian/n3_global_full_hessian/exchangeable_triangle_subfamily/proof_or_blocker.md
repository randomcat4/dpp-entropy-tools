# Exchangeable triangle: block reduction, local theorem, and blocker

AUTHOR STATUS:

```text
INCOMPLETE for the full exchangeable triangle domain at this unit's freeze.
The later [U10k unit](../exchangeable_triangle_global_closed/proof.md) closes
the remaining determinant globally; the scoped results below are retained as
the reviewed reduction on which that proof depends.
PROVED_CANDIDATE for the S3 block reduction and the punctured diagonal
neighborhood theorem below.
```

This note is deliberately not a certification.  A fresh non-author verifier
must check the derivation before any `CORRECT` label is attached.

## 1. Exact atoms by cardinality

For

```text
K=xI+a(J-I),
alpha=x+2a,  beta=x-a,
```

the inclusion determinants are symmetric by cardinality.  Mobius inversion gives
the exact atom probability of one fixed subset of size `m`:

```text
p0 = (1-alpha)(1-beta)^2,
p1 = (1-beta)(alpha+2 beta-3 alpha beta)/3,
p2 = beta(2 alpha+beta-3 alpha beta)/3,
p3 = alpha beta^2.
```

The total count probabilities are `p0, 3p1, 3p2, p3`.  Positivity is immediate
for `0<alpha,beta<1`, because

```text
alpha+2 beta-3 alpha beta
  = alpha(1-beta)+2 beta(1-alpha) > 0,
2 alpha+beta-3 alpha beta
  = 2 alpha(1-beta)+beta(1-alpha) > 0.
```

This is the exact-event law.  It is not the list of inclusion probabilities.

## 2. S3 representation split of the full six-dimensional Hessian

At an exchangeable kernel, the DPP law and therefore the Hessian form `B`
commute with the natural `S3` permutation action on coordinates.  Decompose

```text
Sym(3) = T direct_sum W,
T = span{ I, J-I },
W = {D: sum_i D_ii = 0 and sum_{i<j} D_ij = 0}.
```

Here `T` is the two-dimensional trivial-isotypic part, while `W` is the direct
sum of the two standard copies: one from diagonal contrasts and one from edge
contrasts.  By invariance, `B(T,W)=0`.

The reviewed U8 structural reduction gives, at every connected strict
three-dimensional kernel,

```text
B(D,D)
 = F_K(D,D)
   + det(N) tr(N^{-1}D N^{-1}D)
   - det(N) tr(N^{-1}D)^2,                       (1)
```

where `F_K` is the exact-event Fisher form and `N>0`.

For exchangeable `K`, the matrix `N^{-1}` is itself exchangeable:

```text
N^{-1}=uI+v(J-I).
```

Therefore every `D in W` satisfies

```text
tr(N^{-1}D)=u sum_i D_ii + 2v sum_{i<j}D_ij = 0.
```

Substitution in (1) yields

```text
B(D,D)
 = F_K(D,D) + det(N) tr(N^{-1}D N^{-1}D) > 0
```

for all nonzero `D in W`.

Thus the full six-dimensional triangle question is exactly reduced to checking
the two-dimensional invariant block on `T`.  No finite search is used in this
reduction.

## 3. The two-dimensional invariant block

Use coordinates `(alpha,beta)` on `T`.  A tangent vector
`(dot alpha,dot beta)` corresponds to

```text
dot x = (dot alpha+2 dot beta)/3,
dot a = (dot alpha-dot beta)/3.
```

Let `m=(1,3,3,1)` be the cardinality multiplicities and let
`p=(p0,p1,p2,p3)` be the per-subset atoms above.  Define

```text
C_ij(alpha,beta)
 = sum_{r=0}^3 m_r [
     (partial_i p_r)(partial_j p_r)/p_r
     + (partial_ij p_r) log p_r
   ],
```

where `i,j in {alpha,beta}`.  This is exactly the invariant `B` block.

The derivative table is:

```text
p0_alpha = -(1-beta)^2
p1_alpha = (1-beta)(1-3 beta)/3
p2_alpha = beta(2-3 beta)/3
p3_alpha = beta^2

p0_beta = -2(1-alpha)(1-beta)
p1_beta = (2-4 alpha-4 beta+6 alpha beta)/3
p2_beta = (2 alpha+2 beta-6 alpha beta)/3
p3_beta = 2 alpha beta

p0_alpha_alpha = p1_alpha_alpha = p2_alpha_alpha = p3_alpha_alpha = 0

p0_alpha_beta = 2(1-beta)
p1_alpha_beta = (-4+6 beta)/3
p2_alpha_beta = (2-6 beta)/3
p3_alpha_beta = 2 beta

p0_beta_beta = 2(1-alpha)
p1_beta_beta = (-4+6 alpha)/3
p2_beta_beta = (2-6 alpha)/3
p3_beta_beta = 2 alpha.
```

The entry `C_alpha_alpha` is pure Fisher and hence strictly positive.  Therefore
the full exchangeable triangle theorem is equivalent to the single scalar
two-variable log inequality

```text
Delta_T(alpha,beta)
 := C_alpha_alpha C_beta_beta - C_alpha_beta^2 > 0
```

for all

```text
0<alpha,beta<1,  alpha != beta.                  (2)
```

This is the smallest remaining blocker found in this unit.  The formula is
explicit and contains only rational functions and the four logarithms
`log p0, log p1, log p2, log p3`.

Important correction recorded for future verifiers: the derivative

```text
partial_alpha p2 = beta(2-3 beta)/3,
```

not `2 beta(1-beta)/3`.

## 4. Punctured diagonal neighborhood theorem candidate

Although the global inequality (2) is not closed here, the exchangeable
triangle is proved in a genuine open subdomain around the diagonal line.

Claim.  For every compact interval `x in [r,1-r]` with `0<r<1/2`, there exists
`epsilon_r>0` such that

```text
K=xI+a(J-I),   x in [r,1-r],   0<|a|<epsilon_r
```

has `B(K)>0` on all of `Sym(3)`.

Proof candidate.  The `W` block is already strictly positive for every nonzero
connected triangle by Section 2, so only the invariant block needs a local
check.  Direct Taylor expansion of the exact atoms at fixed `x` gives, in the
basis `(I,J-I)`,

```text
B_xx(x,a) = 3/[x(1-x)] + O(a),
B_xa(x,a) = O(a^2),
B_aa(x,a) = 18 a^2/[x^2(1-x)^2] + O(a^3).
```

Consequently

```text
det B_T(x,a)
 = 54 a^2/[x^3(1-x)^3] + O(a^3).
```

The leading coefficients are uniformly positive for `x in [r,1-r]`.  By
continuity of the exact-event Hessian on the strict domain, after possibly
shrinking `epsilon_r`, the invariant block is positive definite for every
`0<|a|<epsilon_r`.  Combining with the positive `W` block proves the claim.

This is a local theorem near the disconnected diagonal ridge, not a proof of
the full triangle domain.

## 5. Boundary and symmetry notes

The complement map sends

```text
(alpha,beta) -> (1-alpha, 1-beta),
K=xI+a(J-I) -> I-K=(1-x)I-a(J-I).
```

Entropy Hessians are invariant under this complement operation.  Therefore any
subdomain proof or obstruction has a mirrored complement statement.

The rank-one boundary `beta -> 0` with fixed `alpha=theta in (0,1)` is the
exchangeable specialization of the earlier n=3 rank-one boundary mechanism.
This unit did not re-prove that asymptotic theorem.  It only records that the
finite scout below is consistent with positivity near such boundaries.

The diagonal line `alpha=beta` is excluded by the triangle condition and is a
real degeneracy: off-diagonal Hessian directions are flat exactly at diagonal
kernels.  Floating-point evaluation near this line is severely ill-conditioned
because the smallest invariant eigenvalue is quadratic in `alpha-beta`.

## 6. Finite scout

`exchangeable_triangle_sanity.py` independently rebuilds exact atoms and jets
and checks:

- the cardinality formulas above against direct six-coordinate Mobius jets;
- the `S3` block split numerically on fixed samples;
- `177360` deterministic grid / boundary-biased random points in
  `(alpha,beta)`;
- the local coefficients near `a=0` for several `x`.

The run found no credible negative eigenvalue.  It did record thousands of
near-diagonal floating cancellation warnings at `~1e-13` scale, which are not
sign gates and not counterexamples.

The scout is finite evidence only.

## 7. Verdict of this author unit

The full statement

```text
B(K(x,a))>0 for every strict exchangeable triangle a != 0
```

remains `INCOMPLETE` in this unit.

What is frozen for non-author review:

1. exact atom formulas and derivative table;
2. exact `S3` reduction showing the four-dimensional standard part is
   automatically positive;
3. equivalence of the full triangle question to the scalar determinant
   inequality (2);
4. punctured diagonal compact-neighborhood theorem candidate;
5. finite `SCOUT_NO_COUNTEREXAMPLE` ledger.
