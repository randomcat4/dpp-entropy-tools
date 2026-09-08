# D10-U10j: quantitative noncompact exponential wedges

AUTHOR PROOF CANDIDATE PENDING INDEPENDENT AUDIT. No CORRECT label is claimed.
This is a quantitative extension of the U10i constrained-minimum argument,
not an inference from its compact-parameter big-O notation.

## Frozen claim and all quantifiers

Use exactly U10i's path, even coordinates, weighted-trace normalization and
sigma. Put s=exp(-beta/x), beta>0, l=log2 and R=2+beta+beta^(-1).
The candidate is: there exist UNIVERSAL positive constants c,C,x0 such that
for EVERY 0<x<x0 and EVERY beta>0 satisfying

```text
x R^6 <= c,       s <= x^2,
```

one has

```text
|sigma(x,s)-phi(beta)| <= C sqrt(x) R^6,
phi(beta)=(beta+l+2)(beta+l)^4/(2 beta^2 l^2).               (A)
```

The constants are existential, not numerically evaluated. Their existence
is justified by the uniform inequalities below; it is not imported from
an unspecified beta-dependent constant in U10i.

For EVERY fixed theta with 0<theta<1/12, there consequently exist
X_theta>0 and C_theta>0 such that for EVERY 0<x<X_theta and EVERY

```text
x^theta <= beta <= x^(-theta),
```

the path is strict, its full Sym(3) entropy Hessian is strictly negative,
and

```text
sigma=phi(beta)+O_theta(x^(1/2-6theta)).                    (B)
```

The O_theta constant is uniform over the whole displayed beta interval.
The value X_theta is not supplied numerically. Theta=1/24 gives the explicit
power O(x^(1/4)), not an explicit numerical starting x.

## 1. Uniform coefficient bounds, independent of beta

All norms below are finite-dimensional Euclidean/operator norms; the fixed
conversion to the repeated-entry Frobenius coordinates changes only universal
constants. The letter C may increase between inequalities.

Cancel the explicit powers of x in E,U,W,V,Z from U10i. Their normalized
forms, and the logarithms of all resulting positive ratios, are smooth on
the closed rectangle 0<=x,s<=1/16. Every normalized atom is bounded below
there by a positive universal constant. Thus all first derivatives needed
below are bounded by one universal finite constant, by compactness.

Writing Lambda=-beta/x+g(x,s), these observations give
ell=-l+O(x+s), kappa=O(x+s), g=log4+O(x+s), with UNIVERSAL O constants.
Let N0(beta) be the explicit limiting matrix in U10i. Then

```text
||N-N0|| <= C(x+beta s) <= Cx,                             (1)
```

because s<=x^2 and xR<=1, implied after shrinking c. Directly from N0's
reflection blocks,

```text
lambda_max(N0) <= C(beta+l),
lambda_min(N0) >= c1/R,
det N0=beta l(beta+l).
```

If xR is universally small, (1) implies (1/2)N0<=N<=2N0. In particular,

```text
||N^(-1)|| <= CR,
||N^(-1)-N0^(-1)|| <= CxR^2,
det(N)G_N(D,D) >= (c2/R)||D||_F^2.                        (2)
```

For the last inequality use det(N)/lambda_max(N)^2 bounded below by a
constant times beta/(beta+l), which is at least a constant/R. Using only
the separate crude determinant/eigenvalue bounds would lose unnecessary
powers here.

The weighted-trace coefficients satisfy
||eta-eta0||<=CxR^2. The limiting h,k,d coefficients are universally
bounded; only eta0_e=(beta+l)/(beta l) can grow, and it is <=CR.
Also, by the Loewner comparison,

```text
det(N) eta_e^2 <= C det(N0) eta0_e^2 <= CR^2.              (3)
```

## 2. Uniform trial and minimizer bounds

Let z0=(0,0,h0,2sqrt2 h0) be U10i's limiting direction, where
h0=-(beta+l)^2/(2sqrt2 beta l), so ||z0||<=CR.

Use U10i's exact trial with d=e=0, k=2sqrt2 h/sqrt(1-s),
eta(z)=eta_e and w_s dot z=0. Its denominator zeta has limit
zeta0=-2sqrt2/(beta+l), hence |zeta0|>=c3/R. Its perturbation is at most
CxR^2. Therefore xR^3 sufficiently small makes it invertible and gives

```text
||z_trial-z0|| <= CxR^5,    ||z_trial|| <= CR.             (4)
```

The second bound follows from the first when xR^4 is small. These conditions
all follow from xR^6<=c, with a universally small c. The exact trial energy
coefficient from U10i is 4(beta+l+2)+O(x): the extra beta s term is <=x.
Consequently

```text
B(z_trial)<=CR^3,
|B(z_trial)-phi(beta)|<=CxR^7.                            (5)
```

Let z_min minimize B subject to eta(z)=eta_e. On that constraint the exact
U8 identity is
B=F_full+det(N)G_N-det(N)eta_e^2. The first two terms are nonnegative.
Using (2),(3),(5) gives, without presupposing sigma>0,

```text
F_full(z_min)<=CR^3,       ||z_min||<=CR^2.                (6)
```

The singleton forms jU=d+O(x)||z|| and jW=e+O(x)||z|| have denominators
comparable to x. The full-atom Fisher term is (x/s)(w_s dot z)^2. Hence

```text
|d_min|+|e_min| <= C sqrt(x)R^2,
|w_s dot z_min| <= C sqrt(s/x)R^(3/2) <= C sqrt(x)R^2.     (7)
```

Now solve the two exact constraints for h,k. Their limiting 2x2 coefficient
matrix has bounded entries and determinant -2sqrt2/(beta+l); its inverse
norm is <=CR. Its perturbation is <=CxR^2, so its inverse remains <=CR.
The first right-hand side error is bounded by
CR(|d_min|+|e_min|)+CxR^2||z0||<=C sqrt(x)R^3.
The second error is bounded by (7) plus s||z0||. Thus

```text
||z_min-z0|| <= C sqrt(x)R^4.                             (8)
```

Since sqrt(x)R^3<=sqrt(c), shrink the universal c once more in (8) to obtain
the improved bound ||z_min||<=CR. This is not circular: first choose a
provisional small c for all inverse comparisons, derive a finite universal
constant in (8), then shrink c below the reciprocal square of that constant.
All earlier inequalities remain valid after this shrinking.

## 3. Energy error and the sixth power of R

Retain the V-pair Fisher contribution and the cofactor form, discarding
only nonnegative Fisher terms. The normalized V-pair quadratic matrix is
universally bounded and differs from its limiting matrix by O(x).
The cofactor matrix is linear in N, has norm <=CR, and differs from its
limiting matrix by O(x), by (1).

Using (8) and ||z_min||+||z0||<=CR, its energy error is at most

```text
(CR)(CR)(C sqrt(x)R^4)+CxR^2 <= C sqrt(x)R^6.             (9)
```

The V-pair error costs only C sqrt(x)R^5+CxR^2. At z0 these two limiting
forms sum exactly to phi(beta), including the U10i cofactor cancellation.
Therefore sigma>=phi-C sqrt(x)R^6. The trial gives the opposite bound from
(5), because xR^7<=sqrt(x)R^6 whenever sqrt(x)R<=1. This proves (A).

All uses of smallness in this proof are finitely many universal inequalities
in xR, xR^3, xR^4, or sqrt(x)R^3. A single sufficiently small universal c
in xR^6<=c enforces all of them. This explains the constants' existence
without claiming explicit numerical c or C.

## 4. Continuous noncompact wedges and what remains excluded

If x^theta<=beta<=x^(-theta), then R<=4x^(-theta). Thus
xR^6<=4^6 x^(1-6theta)->0 and the error in (A) is at most
4^6 C x^(1/2-6theta)->0 for theta<1/12. Also
s<=exp(-x^(theta-1))<=x^2 eventually, uniformly over this beta interval.
The last fact is the elementary domination of log(1/x) by the positive
power x^(-(1-theta)). Since phi>8(log2+2), sigma is eventually positive
uniformly. The reviewed path block reduction then proves full-Hessian
strictness, not just a fixed-direction result.

This covers beta=x^gamma and beta=x^(-gamma) for every fixed 0<gamma<1/12,
and all fixed powers of log(1/x) or their reciprocals. Multiplicative fixed
constants can be absorbed by choosing a slightly larger theta<1/12.

It does NOT cover, by this proof, beta=x^gamma with gamma>=1/12, beta growing
as x^(-gamma) with gamma>=1/12, or all intermediate/nonregular sequences.
The endpoint 1/12 is a bound of THIS ESTIMATE, not a physical transition.
In particular s=x^p corresponds to beta=p x log(1/x), outside the proved
wedge; the earlier power-rate profile remains only a scout. Beta=O(x)
does not even force s->0. Very large beta and the faster-small-beta corner
still need different uniform estimates. No adverse sign is claimed there.

The entire original path problem remains INCOMPLETE. The present result is
only a new author candidate continuous subdomain with explicit rate exponents.
