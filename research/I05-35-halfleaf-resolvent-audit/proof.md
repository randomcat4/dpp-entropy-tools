# Exact eight-event audit and the surviving entropy target

## 1. Strict half-leaf and true affine direction

Let

```text
K=[[1/2,0,b],[0,1/2,c],[b,c,z]],
b^2=A/4, c^2=B/4,
z=q+(A+B)/2,
A,B,q,qbar=1-A-B-q>0.
```

For a real symmetric direction

```text
D=[[d11,d12,d13],
   [d12,d22,d23],
   [d13,d23,d33]],
```

all derivatives below are taken on the physical line `K+tD`. No
conditional parameter is varied independently.

For a complete configuration `x in {0,1}^3`, let
`Z_x={k:x_k=0}`. The complete DPP atom is

```text
p_x(t)=(-1)^|Z_x| det(K+tD-I_Zx).                    (1)
```

This cubic determinant law simultaneously includes occupied and vacant
events. It also fixes every Fisher and acceleration term.

## 2. Four leaf marginals and conditional jets

Use signs `s1,s2 in {+1,-1}`, with `+1` denoting an occupied leaf. Put

```text
P_s=p_s0+p_s1,
q_s=p_s1/P_s.
```

At the half-leaf center,

```text
P_s=1/4,
q_s=q+A(1-s1)/2+B(1-s2)/2.                           (2)
```

Directly summing the two event polynomials in (1) gives

```text
P_s' =(s1 d11+s2 d22)/2,
P_s''=2 s1 s2(d11 d22-d12^2).                        (3)
```

There is an independent check of the conditional jets. Let
`M_s(t)` be the signed two-leaf complete-event matrix
`K_{12}(t)-I_Z`. At the half-leaf center

```text
M_s(0)^(-1)=2 diag(s1,s2).
```

The conditional selected probability is the Schur complement

```text
q_s(t)=K33(t)-v(t)^T M_s(t)^(-1)v(t).
```

Writing

```text
e1=d13-[s1 sqrt(A)d11+s2 sqrt(B)d12],
e2=d23-[s1 sqrt(A)d12+s2 sqrt(B)d22],
```

matrix differentiation gives

```text
q_s' =d33+A d11+B d22+2s1s2 sqrt(AB)d12
       -2s1 sqrt(A)d13-2s2 sqrt(B)d23,               (4)

q_s''=-4(s1 e1^2+s2 e2^2).                           (5)
```

The checker does not use (4)-(5) to construct the obstruction. It first
forms the four exact quotients `p_s1/P_s` from (1), differentiates those
quotients, and only then asserts exact equality with (2), (4), and (5).

## 3. Direct differentiation of the proposed resolvent

For `r>0`, define the pointwise one-sided resolvent functional

```text
Phi_r(t)=sum_s P_s(t)^2/[p_s1(t)+rP_s(t)]
        =sum_s P_s(t)/[q_s(t)+r].                    (6)
```

The first expression is used in the independent event calculation. If
`N=P^2` and `Q=p+rP`, then

```text
(N/Q)''
 =N''/Q-2N'Q'/Q^2-NQ''/Q^2+2N(Q')^2/Q^3,            (7)

N'=2PP', N''=2[(P')^2+PP''].
```

Equivalently, substituting (2)-(5) and `P_s=1/4` gives

```text
Phi_r''=
 sum_s [
   P_s''/R_s
  -2P_s'q_s'/R_s^2
  -q_s''/(4R_s^2)
  +(q_s')^2/(2R_s^3)
 ],
R_s=q_s+r.                                            (8)
```

Equations (7) and (8) are checked to agree exactly.

## 4. Exact strict counterexample to pointwise positivity

Set

```text
A=1/4, B=16/25, q=109/1000, qbar=1/1000,
sqrt(A)=1/2, sqrt(B)=4/5,
D=(d11,d22,d33,d12,d13,d23)=(-18,-72,40,146,108,5),
r=1/50000.
```

Every parameter is rational and the square roots in (4)-(5) are rational.
The eight center atoms are all positive. Formula (7), applied to the
eight event polynomials from (1), gives

```text
Phi_r''=
-47488558049748267993080620088778228551027375300000000000
/2044542058422113103788725284171055940635901533282467
<0.                                                     (9)
```

Thus the universal assertion that every matrix of `Phi_r''` is positive
definite, for every `r>0` and every strict half-leaf, is false. In
particular no correct all-positive Sylvester-coefficient certificate can
establish that assertion on the stated domain.

This conclusion is exact and all six physical coordinates of `D` are
active. It is not a restriction to the missing-edge tangent slice.

## 5. Why (9) is not an entropy counterexample

Let

```text
G1=sum_s P_s q_s log q_s,
G0=sum_s P_s(1-q_s)log(1-q_s).
```

The eight-event entropy decomposes exactly as

```text
H=H(P)-G1-G0.                                         (10)
```

For `phi(u)=u log u`, direct differentiation gives

```text
[sum_s P_s phi(q_s)]''
 =sum_s [
   P_s'' phi(q_s)
  +2P_s' phi'(q_s)q_s'
  +(1/4){(q_s')^2/q_s+phi'(q_s)q_s''}
 ].                                                    (11)
```

For the vacant side replace `(q,q',q'')` by
`(1-q,-q',-q'')`. Formula (11) retains both Fisher and acceleration.

The four leaf probabilities equal `1/4`, while (3) implies their first
derivatives. Since their second derivatives sum to zero against the
constant center log weight,

```text
-H(P)''=sum_s (P_s')^2/P_s
       =4(d11^2+d22^2).                               (12)
```

Combining (10)-(12),

```text
-H''=4(d11^2+d22^2)+G1''+G0''.                       (13)
```

The checker encloses every logarithm by

```text
log y=2 sum_{j=0}^{n-1} w^(2j+1)/(2j+1)+R_n,
w=(y-1)/(y+1),
0<=R_n<=2w^(2n+1)/[(2n+1)(1-w^2)]
```

after exact powers-of-two range reduction. With `n=32`, it certifies the
strictly positive intervals printed in `output/verify_mobius_obstruction.txt`
for `G1''`, `G0''`, and (13).

Therefore (9) is solely a method/certificate counterexample. Negative
values of the pointwise resolvent integrand can be compensated elsewhere
in its integral, and the complete Shannon curvature has a large positive
margin in this direction.

## 6. Exact remaining problem

The audit invalidates the proposed route

```text
Phi_r'' positive for each r
    => integrate in r
    => one-sided convexity
    => full entropy concavity.
```

It does not decide the weaker intermediate statement `G1''>=0`, and it
does not decide the still weaker full target (13).

Any continuation must therefore work with one of the following exact
objects:

1. the integrated one-sided logarithmic Hessian (11);
2. a valid power-perspective interpolation whose full `K+tD`
   accelerations are retained; or
3. the paired occupied/vacant/marginal Schur complement.

A finite collection of negative or positive sampled values cannot settle
these open-domain statements. Failure of an auxiliary certificate cannot
be relabeled as a Shannon counterexample.

Final status: (9) and (13) are **PROVED BY AUTHOR / PENDING EXTERNAL
REVIEW**; general one-sided convexity, all-half-leaf Shannon concavity,
unequal leaves, and general real three-point concavity remain open at this
checkpoint.
