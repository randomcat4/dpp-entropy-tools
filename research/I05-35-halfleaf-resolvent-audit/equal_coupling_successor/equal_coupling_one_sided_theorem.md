# Equal-coupling half-leaf: global one-sided convexity and full Shannon concavity

Status: **PROVED BY AUTHOR / PENDING INDEPENDENT REVIEW**. This is a post-checkpoint continuation of the exact pointwise-resolvent obstruction. It does not revive the false assertion that `Phi_r''` is positive for every `r`. Instead it proves positivity only after the resolvent has been integrated into the actual one-sided logarithmic functional. No PR81/PR104 checker, finite sample, interval scan, spectral entropy, or nonphysical path is used. Novelty is not assessed.

## 1. Statement

Consider a strict half-leaf arrow with equal squared couplings

```text
K = [[1/2, 0,   b],
     [0,   1/2, c],
     [b,   c,   q+A]],

b^2=c^2=A/4,
A>0, q>0, qbar=1-2A-q>0.
```

Signs of `b,c` are immaterial by diagonal sign conjugation. For the four leaf configurations write

```text
P_ij = P(X1=i,X2=j),
p_ij1 = P(X1=i,X2=j,X3=1),
G1(K) = sum_ij p_ij1 log(p_ij1/P_ij).
```

### Theorem 1: one-sided strict convexity

For every nonzero real symmetric physical direction `D`, on the true affine line `K+tD`,

```text
G1''(K;D)>0.                                          (1)
```

The same assertion holds for the vacant side

```text
G0(K)=sum_ij p_ij0 log(p_ij0/P_ij)
```

by full complementation. Consequently the complete eight-event configuration Shannon entropy satisfies

```text
-H''(K;D)
 =4(D11^2+D22^2)+G1''(K;D)+G0''(K;D)>0.             (2)
```

Thus every strict equal-coupling half-leaf arrow has a strictly negative complete Shannon Hessian. This is an all-`q`, all-`A` continuum theorem under `A,A,q,qbar>0`, not the previously accepted fixed shape.

## 2. Exact normalization and all six jets

For `lambda>0`, put `S_lambda=diag(1,1,sqrt(lambda))`. Complete-event inclusion-exclusion gives exactly

```text
G1(S_lambda K S_lambda)
 =lambda G1(K)+lambda log(lambda) K33,

G1''(S_lambda K S_lambda;S_lambda D S_lambda)
 =lambda G1''(K;D).                                  (3)
```

The second term in the first line is affine. Taking `lambda=1/q` reduces (1) to the auxiliary positive-definite arrow whose four selected conditional corners are

```text
1, 1+a, 1+a, 1+2a,     a=A/q>0.                     (4)
```

The auxiliary matrix need not be a contraction; (3) is an exact selected-event scale identity and all four selected masses and leaf marginals remain positive. The direction map is invertible.

For the normalized problem define six coordinates

```text
x=D11, y=D22,
u=D33+a x+a y,
w=2a D12,
r=2 sqrt(a) D13,
s=2 sqrt(a) D23.                                     (5)
```

For leaf signs `eps,eta in {+1,-1}`, where `+1` means occupied, the complete-event/Mobius jets are

```text
P=1/4,
P'=(eps x+eta y)/2,
P''=2 eps eta [x y-w^2/(4a^2)],

q_eps,eta=1+a(1-eps)/2+a(1-eta)/2,
T_eps,eta=q'eps,eta=u+eps eta w-eps r-eta s,

E1=r-2 eps a x-eta w,
E2=s-eps w-2 eta a y,
q''eps,eta=-eps E1^2/a-eta E2^2/a.                  (6)
```

These formulas follow either by differentiating the four signed `3 by 3` complete-event determinants or by the four `2 by 2` Schur complements. They retain `D12,D13,D23` and both leaf diagonals.

For `phi(t)=t log t`, direct differentiation of all four perspectives gives

```text
G1''=sum_eps,eta [
 P'' phi(q)+2P'(log q+1)T
 +(1/4){T^2/q+(log q+1)q''}
].                                                   (7)
```

No `P''`, Fisher, or acceleration term is removed.

## 3. Leaf-swap block reduction

Put

```text
C=log(1+2a),
V=2log(1+a)-log(1+2a).
```

Both are positive and `V<C`. Introduce

```text
x_plus =(x+y)/sqrt(2),   x_minus=(x-y)/sqrt(2),
r_plus =(r+s)/sqrt(2),   r_minus=(r-s)/sqrt(2).
```

Expanding (7) gives an exact orthogonal direct sum. The antisymmetric block, in `(x_minus,r_minus)`, is

```text
M_minus = [[(a+1)V,                    -V/2],
           [-V/2, [C(a+1)+4a]/[4a(a+1)]]].          (8)
```

Its determinant is

```text
det M_minus
 =V[C(a+1)+4a-aV]/(4a)>0,                           (9)
```

because `0<V<C`. Hence `M_minus>0`.

The symmetric block, in `(x_plus,u,w,r_plus)`, is

```text
M_plus = [[2aC-(a+1)V, -C/sqrt(2), 0, V/2],
          [-C/sqrt(2), y11, y12, y13],
          [0,          y12, y22, y23],
          [V/2,        y13, y23, y33]],              (10)
```

where

```text
y11=(a^2+4a+2)/[2(a+1)(2a+1)],
y12=a^2/[2(a+1)(2a+1)],
y13=-sqrt(2)a/[2(2a+1)],

y22=y11+V(a+1)/(2a^2),
y23=-sqrt(2)[(2a+1)V+2a^2]/[4a(2a+1)],
y33=(a+1)/(2a+1)+C/(4a).                            (11)
```

Let `Y` be the lower-right `3 by 3` block of (10). Its three leading principal minors are

```text
m1=(a^2+4a+2)/[2(a+1)(2a+1)],

m2=[V(a^2+4a+2)+4a^2]/[4a^2(2a+1)],

m3=[(a+1)C-aV+4a]
   [V(a^2+4a+2)+4a^2]
   /[16a^3(a+1)(2a+1)].                             (12)
```

They are strictly positive, so `Y>0`. It remains only to prove `det M_plus>0`.

## 4. The scalar determinant polynomial

Set

```text
rho=a/(1+a) in (0,1).
```

Then

```text
C=log[(1+rho)/(1-rho)],
V=-log(1-rho^2).                                     (13)
```

Direct determinant reduction gives

```text
det M_plus=(1-rho) P(rho,C,V)/[16 rho^3(1+rho)],     (14)
```

with

```text
P = C^3 V rho^2-C^3 V+C^3 rho^4-2C^3 rho^2
   -C^2 V^2 rho^3+C^2 V^2 rho+2C^2 V rho^3
   +C V^2 rho^2-2C V^2
   -8C V rho^4+12C V rho^2+32C rho^4
   +4V^2 rho^3-8V^2 rho-16V rho^3.                  (15)
```

The rest is a scalar analytic certificate for (15), with no parameter subdivision.

Define

```text
Gamma=rho C-V
     =(1+rho)log(1+rho)+(1-rho)log(1-rho),           (16)
```

and view (15), after `V=rho C-Gamma`, as a quadratic polynomial `P_rho,C(Gamma)`. Its second derivative is

```text
partial_Gamma^2 P_rho,C
 =-2 Q,

Q=(2-rho^2)(C+4rho)-C^2 rho(1-rho^2).               (17)
```

Write `rho=tanh u`, `u>0`, so `C=2u`. Since `cosh u>u`,

```text
C^2(1-rho^2)=4u^2/cosh(u)^2<4.
```

Therefore

```text
Q>(C+4rho)-4rho=C>0.                                (18)
```

Thus `P_rho,C` is strictly concave as a function of `Gamma`.

## 5. The exact interval for Gamma

From (13), `Gamma'(rho)=C(rho)` and `Gamma(0)=0`. Since `C'(rho)=2/(1-rho^2)>2`,

```text
Gamma>rho^2.                                         (19)
```

For the upper bound put `F(rho)=2rho^2-Gamma(rho)`. Then

```text
F'=4rho-C,
(4rho-C)'=4-2/(1-rho^2).
```

The last derivative is positive before `rho=1/sqrt(2)` and negative afterwards. Hence `4rho-C` rises from zero, then decreases strictly to minus infinity and has one later zero. Consequently `F` first increases and then decreases. Its endpoint values are

```text
F(0)=0,
lim_rho->1 F(rho)=2-2log2>0.
```

Thus

```text
rho^2<Gamma<2rho^2,   0<rho<1.                       (20)
```

The elementary inequality `log2<1` is sufficient at the right endpoint.

Because `P_rho,C` is concave, its minimum on the interval in (20) is attained at one of the two endpoints. It remains to prove positivity at `Gamma=rho^2` and `Gamma=2rho^2`.

## 6. Two explicit endpoint certificates

Put

```text
k=C/rho,
omega=1-rho^2,
R=k^2 omega.                                         (21)
```

Exact substitution into (15) gives

```text
P_rho,C(rho^2)
 =rho^5 { k[19-omega-R(5-2omega)]
          +R(9-omega-R)+12-4omega },                 (22)

P_rho,C(2rho^2)
 =rho^5 { k[4(5-omega)-2R(3-2omega)]
          +R[4(4-omega)-R]+16(1-omega) }.            (23)
```

Again write `rho=tanh u`, and put `X=cosh u`. Then

```text
omega=1/X^2,
R=4u^2/sinh(u)^2<4.                                  (24)
```

The two sharper inequalities needed in (22)-(23) are

```text
R < (19-omega)/(5-2omega),                           (25)
R < 2(5-omega)/(3-2omega).                           (26)
```

After clearing positive denominators, (25) and (26) are respectively equivalent to

```text
N0(u)=(19X^2-1)(X^2-1)-4u^2(5X^2-2)>0,              (27)
N2(u)=2(5X^2-1)(X^2-1)-4u^2(3X^2-2)>0.              (28)
```

They have the exact even-power expansions

```text
N2(u)=4u^2
 +sum_{n>=2} 4^n[5*4^n-4-6(2n)(2n-1)]
             u^(2n)/[4(2n)!],                       (29)

N0(u)=6u^2
 +sum_{n>=2} 4^n[19*4^n-4-20(2n)(2n-1)]
             u^(2n)/[8(2n)!].                       (30)
```

Every displayed coefficient is positive. For (29), the bracket at `n=2` is `4`, and its successive increment is

```text
15*4^n-48n-12>0,   n>=2.
```

For (30), the bracket at `n=2` is `60`, and its successive increment is

```text
57*4^n-160n-40>0,  n>=2.
```

This proves (25)-(26) without numerical evaluation.

Now every term in braces in (22) is positive: the first bracket is positive by (25),

```text
9-omega-R>9-1-4=4,
12-4omega>8.
```

Likewise (26) makes the first bracket in (23) positive, while

```text
4(4-omega)-R>12-4=8,
16(1-omega)>0.
```

Hence both endpoint values are strictly positive. Concavity in `Gamma` and (20) give

```text
P(rho,C,V)>0.                                        (31)
```

Equations (12), (14), and (31) imply `M_plus>0`. Together with (8)-(9), the full six-dimensional matrix of `G1''` is positive definite. Scaling back by (3) proves Theorem 1 for every `q>0`. Complementation proves the vacant-side assertion, and the exact retained decomposition proves (2).

## 7. Unequal-leaf continuation

Use the general missing-edge coordinates

```text
b^2=A x(1-x),
c^2=B y(1-y),
z=q+A(1-x)+B(1-y),
qbar=1-A-B-q.
```

### Corollary 2: open unequal-leaf tube

Every strict equal-coupling half-leaf point

```text
x=y=1/2, A=B=a, a>0, q>0, 1-2a-q>0
```

has a relative open neighborhood in the full strict missing-edge parameter domain on which the complete six-direction Shannon Hessian remains strictly negative. The neighborhood contains points with `x!=y` and with `A!=B`.

More uniformly, every compact set of such equal-coupling half-leaf points admits one common positive neighborhood radius.

Proof. All eight complete atoms and all entries of the six-dimensional Hessian are continuous on the strict domain. Theorem 1 gives a positive minimum of `-H''` on the unit direction sphere at each center. Compactness gives a positive uniform minimum on a compact set, and continuity preserves it in a sufficiently small parameter tube. No boundary point is included and no explicit radius is claimed.

This corollary is not a general unequal-leaf theorem. It records open full-parameter neighborhoods generated by the global equal-coupling spine.

## 8. Scope

Proved here at author level:

- global one-sided strict convexity for every normalized equal-coupling shape `a>0`;
- full complete-event Shannon concavity for every strict physical half-leaf with `A=B` and arbitrary legal `q`;
- relative open neighborhoods containing unequal leaf diagonals and unequal coupling strengths;
- the explicit scalar certificate (15), (17), (20), and (22)-(30).

Not proved:

- pointwise positivity of `Phi_r''`; the exact PR120 witness disproves it;
- one-sided convexity for arbitrary `A/B`;
- all half-leaf arrows, all unequal-leaf arrows, or general real three-point concavity;
- any entropy counterexample, novelty claim, or formal verification.
