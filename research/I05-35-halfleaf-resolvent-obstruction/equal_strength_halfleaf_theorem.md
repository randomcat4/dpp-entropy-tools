# Equal-strength half-leaf theorem after the pointwise-resolvent failure

Status: **PROVED BY AUTHOR / PENDING INDEPENDENT REVIEW**. This is a post-checkpoint continuation of the exact obstruction in `proof.md`. It proves a new continuum theorem; it does not restore pointwise positivity of `Phi_r`, and it does not claim all unequal strengths or all unequal leaf diagonals.

## 1. The theorem

Let

```text
K=[[1/2,0,b],[0,1/2,c],[b,c,z]],
b^2=c^2=lambda/4,
z=q+lambda,
lambda,q,qbar=1-q-2lambda>0.
```

Then for every nonzero real symmetric physical direction `D`, the complete-configuration Shannon entropy satisfies

```text
-H''(K;D)>0.                                         (1)
```

Independent signs of `b,c` are covered by diagonal sign conjugation. Thus every strict equal-strength half-leaf arrow is a strict concavity point in all six physical directions, for its whole legal `q` interval.

The proof is stronger on each emitted side: both integrated one-sided quadratic forms `G1''` and `G0''` are separately positive definite. This does not imply that their pointwise resolvent integrands are positive.

## 2. One-sided normalization and exact six-coordinate identity

For the occupied side, put

```text
G1=sum_s P_s q_s log q_s,
```

where `s` ranges over the four leaf configurations, `P_s` is the leaf event probability, and `q_s=P(X3=1|s)`.

Scaling `q_s` by the rare-corner value reduces the proof to positive auxiliary corners

```text
1, 1+a, 1+a, 1+2a,       a=lambda/q>0.              (2)
```

Indeed, replace

```text
b,c,D13,D23,z,D33
```

by

```text
b/sqrt(q), c/sqrt(q), D13/sqrt(q), D23/sqrt(q), z/q, D33/q,
```

while keeping the two-leaf block and its direction fixed. For every leaf event and every line parameter, the leaf mass is unchanged and the conditional selected mass is divided by `q`. Hence

```text
G1_normalized''=G1''/q;                              (3)
```

the extra `-(log q) P(X3=1)/q` term has zero second derivative because `P(X3=1)=K33` is affine. Thus signs and strictness are preserved.

At the normalized object use the invertible coordinates

```text
D11=d, D22=e, D12=gamma/(8a),
D13=-alpha/(4sqrt(a)), D23=-beta/(4sqrt(a)),
D33=m-a(d+e).
```

The four conditional first derivatives are

```text
T00=m-alpha/2-beta/2+gamma/4,
T10=m+alpha/2-beta/2-gamma/4,
T01=m-alpha/2+beta/2-gamma/4,
T11=m+alpha/2+beta/2+gamma/4.                        (4)
```

Put

```text
u=log(1+a), v=log(1+2a),
J=(1+2a)v-2(1+a)u>0.                                (5)
```

For one actual edge with log increment `h`, endpoint reciprocal weights `fX,fY`, and corner scores `X,Y`, define

```text
E_h(X,Y;delta)
 =a h delta^2-h delta(X+Y)/2
  +h(X-Y)^2/(16a)+(fX X^2+fY Y^2)/8.               (6)
```

Direct substitution of the four complete selected-event jets gives the exact identity

```text
G1''=2Jde-J gamma^2/(32a^2)
 +E_(v-u)(T00,T10;d) + E_u(T01,T11;d)
 +E_(v-u)(T00,T01;e) + E_u(T10,T11;e),             (7)
```

where the high edge has `(fX,fY)=(1/(1+2a),1/(1+a))` and the low edge has `(fX,fY)=(1/(1+a),1)`. Equation (7) is an all-event identity: its reciprocal terms are the full Fisher contribution and its remaining terms are the complete acceleration contribution.

## 3. Leaf-swap decomposition: the antisymmetric block

The quadratic form (7) is invariant under leaf exchange

```text
d <-> e, alpha <-> beta,
```

with `m,gamma` fixed. Its symmetric and antisymmetric eigenspaces are orthogonal for the associated bilinear form.

On the antisymmetric space

```text
e=-d, beta=-alpha, m=gamma=0,
```

the matrix in `(d,alpha)` is

```text
M_-=[ 2(a+1)(2u-v),                    (2u-v)/2
      (2u-v)/2, (av+4a+v)/(8a(a+1)) ].              (8)
```

Since

```text
2u-v=log((1+a)^2/(1+2a))>0,
```

the first pivot is positive, and

```text
det M_-
 =(2u-v)[4a+v+2a(v-u)]/(4a)>0.                      (9)
```

Thus the complete antisymmetric two-dimensional block is strictly positive for every `a>0`.

## 4. Symmetric block and the retained two-edge chain

On the symmetric space set

```text
e=d, beta=alpha,
X=T00, Y=T10=T01, Z=T11,
Delta=X-2Y+Z=gamma.
```

The map `(m,alpha,gamma) <-> (X,Y,Z)` is invertible. Equation (7) becomes

```text
G1''=2Jd^2-J Delta^2/(32a^2)
     +2E_(v-u)(X,Y;d)+2E_u(Y,Z;d).                  (10)
```

Each edge has the exact completion

```text
E_h(X,Y;d)
 =a h[d-(X+Y)/(4a)]^2
  +[fX X^2+fY Y^2-2(h/a)XY]/8.                     (11)
```

The endpoint matrix in the second line is positive definite. For endpoints `0<p<r`, its off-diagonal log mean is

```text
m=log(r/p)/(r-p)<1/sqrt(pr),                         (12)
```

because, after writing `r/p=exp(2t)`, inequality (12) is `t<sinh t`.

Discard only the nonnegative completed squares and `2Jd^2`. The two retained endpoint residuals form

```text
R(X,Y,Z)=[X,Y,Z] M [X,Y,Z]^T,

M=(1/4)*[
  1/(1+2a), -(v-u)/a,       0
  -(v-u)/a,  2/(1+a),      -u/a
  0,         -u/a,          1
].                                                        (13)
```

The two positive edge matrices imply `M>0`. If `c=(1,-2,1)^T`, the optimal coefficient in

```text
R(X,Y,Z)>=kappa_chain (X-2Y+Z)^2                    (14)
```

is

```text
kappa_chain=1/(c^T M^(-1)c).                        (15)
```

It remains to compare this exact chain coefficient with the shared-cell loss.

## 5. Exact one-variable gap

Set

```text
r=a/(1+a) in (0,1),
w=-log(1-r^2)=2u-v.
```

A direct three-by-three inversion of (13) gives

```text
kappa_chain-J/(32a^2)
 =(1-r) N(r)/[32 r^2 D(r)],                         (16)
```

where

```text
D=r^2 w^2+4r^2 w+8r^2-4rv-w^2,

N=16r^4-r^3 v w^2+4r^3 v w-8r^3 v
  +r^2 w^3+8r^2 w+r v w^2-4r v w-w^3.              (17)
```

The denominator is positive without a separate approximation: exact matrix algebra gives

```text
c^T adj(M)c=(1-r)D/[16r^2(1+r)]>0                  (18)
```

because `M>0`.

We now prove `N>0` analytically. Put `x=r^2` and define

```text
A(x)=atanh(sqrt(x))/sqrt(x)=sum_(n>=0) x^n/(2n+1),
C(x)=-log(1-x)/x          =sum_(n>=0) x^n/(n+1),
E(x)=2A(x)-C(x).                                      (19)
```

Then `v=2rA`, `w=xC`, and exact simplification of (17) gives

```text
N=x^2 F(x),
F=16-8E-(1-x)[4C^2+4CE-x C^2 E].                    (20)
```

The continuous value is `F(0)=0`. The differential identities

```text
2x A'+A=1/(1-x),
x C'+C=1/(1-x),
x E'=(C-E)/2                                            (21)
```

yield

```text
F'(x)=C(x)L(x)/(2x),                                  (22)

L=24(A-1)-4xC-6xAC+2x^2 AC+4xC^2-2x^2 C^2.          (23)
```

It remains only to show `L>0`. Let `H_n=sum_(j=1)^n 1/j`, with `H_0=0`. The elementary convolution identities

```text
[x^k](A C)=2H_(2k+2)/(2k+3),
[x^k](C^2)=2H_(k+1)/(k+2)                            (24)
```

give, for every `n>=1`,

```text
ell_n=[x^n]L
 =24/(2n+1)-4/n-12H_(2n)/(2n+1)
  +4H_(2n-2)/(2n-1)+8H_n/(n+1)-4H_(n-1)/n.          (25)
```

Define

```text
R_n=2(16n^3+8n^2-19n+1)/[n(n+1)(2n-1)(2n+1)],
alpha_n=4(n-1)/[n(n+1)],
beta_n=16(n-1)/[(2n-1)(2n+1)].                      (26)
```

Writing

```text
Y_n=H_(n-1),
Z_n=H_(2n-2)-H_(n-1),
```

formula (25) is exactly

```text
ell_n=R_n-(beta_n-alpha_n)Y_n-beta_n Z_n.            (27)
```

Here `beta_n>=alpha_n`, while the termwise bounds

```text
0<=Y_n<=n-1,
0<=Z_n<= (n-1)/n                                    (28)
```

give

```text
ell_n
 >=6(10n^2-5n-3)/[n(n+1)(2n-1)(2n+1)]
 >0.                                                  (29)
```

Thus every nonconstant Taylor coefficient of `L` is strictly positive. Hence `L(x)>0` on `(0,1)`, so (22) gives `F'(x)>0`; with `F(0)=0`, equations (20) and (17) give `N(r)>0` for every `0<r<1`.

Equations (16)--(18) therefore prove

```text
kappa_chain>J/(32a^2).                               (30)
```

The retained chain alone strictly absorbs the negative shared-cell term in (10). If `(X,Y,Z)` is nonzero, `R>0`; if it is zero, the positive `d` terms in (10) handle every nonzero `d`. The symmetric four-dimensional block is therefore positive definite.

Together with Section 3 and the scaling relation (3), this proves `G1''>0` in all six nonzero directions for every equal-strength occupied-side rectangle.

## 6. Vacant side, full entropy, and a local unequal-leaf consequence

Complementation sends the vacant contribution of `K` to the occupied contribution of `I-K`; the latter is again an equal-strength half-leaf with rare corner `qbar>0`, up to diagonal sign conjugation. Hence

```text
G0''>0                                                   (31)
```

in every nonzero direction as well.

The exact complete-event decomposition from `proof.md` is

```text
-H''=4(d11^2+d22^2)+G1''+G0''.                       (32)
```

Equations (31)--(32) prove the theorem (1), with all occupied and vacant events, Fisher terms, accelerations, and leaf marginals retained.

There is also a precise, but local, unequal-leaf extension. On every compact subset of the strict equal-strength family, the least eigenvalue of the six-by-six matrix `-H''` has a positive minimum. Complete-event probabilities and the Hessian depend continuously on all strict kernel entries. Therefore a single open neighborhood of that compact set inside

```text
[[x,0,b],[0,y,c],[b,c,z]]
```

still has `-H''>0`; this neighborhood contains kernels with `x!=y` and with unequal edge strengths. No explicit radius, boundary-uniform radius, or global unequal-leaf theorem is claimed.

## 7. Scope

Proved here at author level:

- separate positive definiteness of `G1''` and `G0''` for every strict equal-strength half-leaf;
- strict full Shannon concavity in all six physical directions on that entire family;
- compact-local persistence into genuinely unequal leaf diagonals and unequal edge strengths.

Still open:

- arbitrary `A!=B` on the half-leaf;
- a boundary-uniform unequal-leaf radius;
- general missing-edge and general real three-point Shannon concavity;
- any Shannon entropy counterexample;
- novelty and formal verification.

The pointwise resolvent assertion remains disproved by the exact witness in `proof.md`; this theorem succeeds only after integrating and retaining the true edge/cell structure.
