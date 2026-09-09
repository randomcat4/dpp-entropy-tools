# C2 issue52 structure note

Status: INCOMPLETE.  This note records one bounded analytic route from the
literal issue52 matrix

```text
M = d/du Fmat + Q
```

only.  It does not verify the all-event derivation of that formula, does not
prove global positivity, and does not give an entropy counterexample.  Any
global proof or obstruction built from this reduction still needs fresh
nonauthor review.

## Domain and positive denominators

The standing domain is

```text
|mu| < 1, |nu| < 1, |r| < 1, 0 < u < 1,
a=(1+r)/2, b=(1-r)/2,
v=(1-mu^2)/4, w=(1-nu^2)/4,
J=1-u^4, L=1-r^2 u^4.
```

The following denominator factors are positive throughout the open domain:

```text
a, b, v, w, u, J, L,
L+rJ = (1+r)(1-r u^4),
L-rJ = (1-r)(1+r u^4).
```

Consequently

```text
n1 = 4u(1/J-r/L) = 4u(L-rJ)/(JL) > 0,
n2 = 4u(1/J+r/L) = 4u(L+rJ)/(JL) > 0,
n3 = 4u^3(1-r^2)/(JL) > 0.
```

A public author hint says the raw matrix entries have common clearing
denominator `8*J^2*L^2`.  I did not use that as a verified result.  It is
consistent with the displayed formula because `d/du(1/J)` and `d/du(1/L)`
produce only `J^2` and `L^2`, while `Q` has denominator `JL`.

For any compact-domain certificate, use open coordinates such as
`x=(1+mu)/2`, `y=(1+nu)/2`, `s=u^2`, `a=(1+r)/2`.  Boundary factors
`a,b,v,w,u,J` may vanish only on the boundary, so a closed-box nonnegative
certificate is not by itself a strict interior proof unless all possible
interior zeros of the residual factors are excluded.

## Conditional-polynomial reduction

For the four Bernoulli atoms put

```text
e = i-(1+mu)/2,     f = j-(1+nu)/2.
```

The exact two-point identities are

```text
e^2 = v - mu e,     f^2 = w - nu f.
```

For a direction `zeta=(alpha,beta,gamma,eta,xi,omega)` in the fixed issue52
coordinates, the scalar `q_ij dot zeta` is therefore the bilinear conditional
polynomial

```text
T(e,f) = m + p e + q f + h e f
```

with

```text
m = gamma + u^2 a v alpha + u^2 b w beta,
p = -u^2 a mu alpha - 2u a xi,
q = -u^2 b nu beta - 2u b omega,
h = 2u^2 a b eta.
```

This change of variables from `(alpha,beta,gamma,eta,xi,omega)` to
`(alpha,beta,m,p,q,h)` is invertible for `u,a,b>0`.  The inverse is

```text
gamma = m - u^2 a v alpha - u^2 b w beta,
eta   = h/(2u^2ab),
xi    = -(p + u^2 a mu alpha)/(2ua),
omega = -(q + u^2 b nu beta)/(2ub).
```

Let `rho=1/J`, `lambda=1/L`, `d0=(rho+lambda)/2`,
`d1=(rho-lambda)/2`, and `y=(m,p,q,h)^T`.  Then

```text
zeta^T Fmat zeta = 4 y^T G y,
```

where

```text
G = d0*diag(1,v,w,vw) + d1*S
```

and

```text
S =
[[ mu*nu,       2v*nu,       2w*mu,        4vw],
 [ 2v*nu,      -mu*nu*v,    4vw,          -2mu*vw],
 [ 2w*mu,       4vw,       -mu*nu*w,      -2nu*vw],
 [ 4vw,        -2mu*vw,    -2nu*vw,        mu*nu*vw]].
```

This is a direct moment calculation using independence of the two leaf
Bernoulli variables and the parity representation of the denominator:

```text
1/den_ij = d0 + d1*(2e+mu)*(2f+nu).
```

In the normalized basis `(1,e/sqrt(v),f/sqrt(w),ef/sqrt(vw))`, multiplication
by `2e+mu` and `2f+nu` is by two reflections.  Equivalently, without radicals,
if `D=diag(1,v,w,vw)`, then

```text
S D^{-1} S = D.
```

Thus the denominator part has only two eigenvalues, `1/J` and `1/L`, each with
multiplicity two.  This is the main shape-elimination identity: the dependence
on `mu,nu` in the conditional Fisher denominator is only a change of
orthogonal/reflection coordinates.

## Fixed-u derivative bookkeeping

The derivative must be taken with the original direction coordinates fixed.
In the variables above this means

```text
y' = U_alpha alpha + U_beta beta + R y,
R = diag(0,1/u,1/u,2/u),
U_alpha = (2uav, -ua mu, 0, 0)^T,
U_beta  = (2ubw, 0, -ub nu, 0)^T.
```

Since the reflections depend only on `mu,nu`, not on `u`,

```text
zeta^T Fmat' zeta = 8 y'^T G y + 4 y^T G' y,
```

where

```text
G' = d0'*diag(1,v,w,vw) + d1'*S,
d0' = (4u^3/J^2 + 4r^2u^3/L^2)/2,
d1' = (4u^3/J^2 - 4r^2u^3/L^2)/2.
```

This formula is safe because no moving direction change is used before
differentiating.  The subsequent transformations are only pointwise
congruences for inertia.

## Positive two-dimensional invisible block

The conditional Fisher image sees only `(m,p,q,h)`.  On its nullspace,

```text
m=p=q=h=0,
eta=0,
xi=-u mu alpha/2,
omega=-u nu beta/2,
gamma=-u^2(av alpha+bw beta).
```

On this two-dimensional subspace `Fmat'=0`, so `M=Q`.  Substitution into the
literal sparse `Q` gives

```text
Q|ker =
  (n2*a*u^2*v/2) alpha^2
+ (n1*b*u^2*w/2) beta^2
+ 2vw*(u^2(n2*b+n1*a)-n3) alpha beta.
```

The mixed coefficient vanishes exactly because

```text
u^2(n2*b+n1*a) = n3.
```

Therefore the invisible block is the positive diagonal form

```text
d_alpha alpha^2 + d_beta beta^2,
d_alpha = n2*a*u^2*v/2 > 0,
d_beta  = n1*b*u^2*w/2 > 0.
```

This is a genuine local certificate for the two directions killed by the
conditional-polynomial map.  It is not a certificate for the full six-by-six
matrix.

## Exact four-dimensional remaining matrix

Write the full quadratic form in variables `(alpha,beta,y)` as

```text
zeta^T M zeta
= d_alpha alpha^2 + d_beta beta^2
  + alpha L_alpha(y) + beta L_beta(y)
  + y^T R0 y.
```

The two linear couplings simplify to

```text
theta = a*nu + b*mu,

L_alpha(y) = 8u*v*d1*(-2b*m + theta*p + 2a*w*h),
L_beta(y)  = 8u*w*d1*(-2a*m + theta*q + 2b*v*h).
```

The simplification uses only the displayed matrix `G` and the identities above.
Before simplification these couplings are

```text
L_alpha = 8 U_alpha^T G y - 2n2 v m + n2 mu v p,
L_beta  = 8 U_beta^T  G y - 2n1 w m + n1 nu w q.
```

The remaining four-variable block is

```text
R0 = 4(R^T G + G R + G')
     + diag(0, n2*v/(2u^2a), n1*w/(2u^2b), n3*vw/(2u^4ab)).
```

Since `d_alpha,d_beta>0`, the full issue52 matrix is positive definite if and
only if the following explicit four-by-four Schur complement is positive
definite:

```text
Rstar =
R0
- (1/(4d_alpha)) ell_alpha ell_alpha^T
- (1/(4d_beta))  ell_beta  ell_beta^T,
```

where `ell_alpha` and `ell_beta` are the coefficient rows of `L_alpha` and
`L_beta` in the variable order `(m,p,q,h)`.

Equivalently, if a negative vector `y` is found for `Rstar`, an exact negative
six-vector for `M` is recovered by

```text
alpha = -L_alpha(y)/(2d_alpha),
beta  = -L_beta(y)/(2d_beta),
gamma = m - u^2 a v alpha - u^2 b w beta,
eta   = h/(2u^2ab),
xi    = -(p + u^2 a mu alpha)/(2ua),
omega = -(q + u^2 b nu beta)/(2ub).
```

Thus the sign problem should not start with the raw six-by-six determinant.
First form `Rstar`, clear the known positive factors, and only then compute
principal minors or a polynomial certificate.

## Suggested bounded computation order

1. Rebuild the event formula independently, then check that the four-event
   conditional Fisher equals `4 y^T G y` using `e^2=v-mu e`,
   `f^2=w-nu f`, and `S D^{-1}S=D`.
2. Change variables to `(alpha,beta,m,p,q,h)` after forming `M`; this is a
   pointwise congruence, not a differentiated moving coordinate system.
3. Verify the null-block identities
   `u^2(n2*b+n1*a)=n3`,
   `d_alpha=n2*a*u^2*v/2`, and
   `d_beta=n1*b*u^2*w/2`.
4. Build the four-by-four `Rstar`.  For a global proof, certify all principal
   minors of `Rstar` after clearing only positive denominator factors.  For an
   obstruction, search `Rstar` first and reconstruct the six-vector with the
   formulas above.
5. In the `r=0` partial case, use
   `a=b=1/2`, `L=1`, `n1=n2=4u/J`, `n3=4u^3/J`, and
   `theta=(mu+nu)/2`.  This is a useful low-cost check but remains partial.

## What is verified here versus conjectural

Verified from the literal issue52 rational formula:

- the identities `e^2=v-mu e` and `f^2=w-nu f`;
- the conditional-polynomial map `q_ij dot zeta = m+p e+q f+h ef`;
- the Gram representation `zeta^T Fmat zeta = 4*y^T G y`;
- the reflection identity `S D^{-1}S=D`;
- the positivity of `n1,n2,n3,d_alpha,d_beta`;
- the exact cancellation of the `alpha beta` term on the Fisher-invisible
  two-plane;
- the four-by-four Schur complement formula for the remaining sign problem.

Not verified or not proved here:

- the all-eight-event derivation of `M=Fmat'+Q`;
- positive definiteness of `Rstar` on the full domain;
- any determinant nonvanishing or inertia-continuation certificate;
- any exact rational negative direction;
- any entropy Hessian or Jensen counterexample.

## Determinant bookkeeping: reviewed supplement

Let `T` in this paragraph be the six-by-six forward linear coordinate map
`zeta=(alpha,beta,gamma,eta,xi,omega)` to
`x=(alpha,beta,m,p,q,h)`. This matrix is distinct from the scalar polynomial
`T(e,f)` above. Let `M_red` represent the already formed quadratic form in the
new coordinates. Since `x=T zeta`, the orientation is

```text
M_red = T^{-T} M T^{-1},
M = T^T M_red T.
```

The first two coordinates are unchanged. The remaining pivots, in the output
order `(m,p,q,h)`, are `1,-2ua,-2ub,2u^2ab`; the corresponding permutation has
positive sign. Thus

```text
det T = 8*u^4*a^2*b^2,
det M_red = d_alpha*d_beta*det Rstar,
det M = (det T)^2*det M_red
      = 16*n1*n2*u^12*a^5*b^5*v*w*det Rstar.
```

Every prefactor is strictly positive in the stated open domain. This gives
equivalence of determinant signs and nonvanishing there; it does not prove
that the remaining determinant is nonzero.

The supplement was checked in the separate first-review addendum and derived
afresh in [C3's second analytic audit](https://github.com/randomcat4/dpp-entropy-tools/blob/7f705d608e2f77ca6749b660ec2e7f97e29fe615/docs/verification_round3_20260909/followon/pr55_structure_second/review_report.md).
The prior reduction is unchanged; the Gram summary above now uses its explicit
quadratic-form notation to avoid reusing `T` for a four-row map.
