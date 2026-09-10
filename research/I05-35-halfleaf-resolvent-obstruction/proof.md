# Exact pointwise-resolvent obstruction from all eight complete events

## 1. True affine half-leaf and complete-event jets

Let

```text
K=[[1/2,0,b],[0,1/2,c],[b,c,q+(A+B)/2]],
b^2=A/4, c^2=B/4,
A,B,q,qbar=1-A-B-q>0.
```

For a real symmetric physical direction, use the six observation-coordinate entries

```text
D=(d11,d22,d33,d12,d13,d23).
```

For leaf signs `s1,s2 in {+1,-1}`, where `+1` means occupied, let

```text
P_s(t)=P_{K+tD}(X1=s1,X2=s2),
p_s(t)=P_{K+tD}(X1=s1,X2=s2,X3=1),
q_s(t)=p_s(t)/P_s(t).
```

At `t=0`, principal-minor Möbius inversion gives

```text
P_s=1/4,
q_s=q+A(1-s1)/2+B(1-s2)/2.                         (1)
```

The two-leaf complete events give, without suppressing the moving missing edge,

```text
P'_s=(s1 d11+s2 d22)/2,
P''_s=2 s1 s2(d11 d22-d12^2).                       (2)
```

To obtain the conditional jets directly, put

```text
M_s(t)=(K+tD)_{12,12}-I_{vacant leaves},
v(t)=((K+tD)13,(K+tD)23)^T.
```

Then the complete-event determinant ratio is the Schur complement

```text
q_s(t)=(K+tD)33-v(t)^T M_s(t)^(-1)v(t).             (3)
```

At the half-leaf center, `M_s(0)^(-1)=2 diag(s1,s2)`. Differentiating (3) gives

```text
q'_s=d33+A d11+B d22+2s1s2 sqrt(AB)d12
     -2s1 sqrt(A)d13-2s2 sqrt(B)d23,                 (4)

e1=d13-(s1 sqrt(A)d11+s2 sqrt(B)d12),
e2=d23-(s1 sqrt(A)d12+s2 sqrt(B)d22),
q''_s=-4(s1 e1^2+s2 e2^2).                          (5)
```

The checker independently derives the same jets from all eight Möbius event polynomials. Thus (2)--(5) are not a conditional-kernel substitution for the complete event law.

## 2. Exact negative direction for the old pointwise claim

For `r>0`, define

```text
Phi_r=sum_s P_s^2/(p_s+rP_s)=sum_s P_s/(q_s+r).
```

Writing `R_s=q_s+r` and differentiating at the half-leaf center yields

```text
Phi_r''=sum_s[
 P''_s/R_s
 -2P'_s q'_s/R_s^2
 -(1/4)q''_s/R_s^2
 +(1/2)(q'_s)^2/R_s^3].                             (6)
```

Take

```text
A=1/4, B=16/25, q=109/1000, qbar=1/1000,
r=1/50000,
D=(-18,-72,40,146,108,5).
```

All square roots in (4)--(5) are rational:

```text
sqrt(A)=1/2, sqrt(B)=4/5, sqrt(AB)=2/5.
```

Substitution into (6), or direct differentiation of the eight-event rational functions, gives exactly

```text
Phi_r''=
-47488558049748267993080620088778228551027375300000000000
/2044542058422113103788725284171055940635901533282467
<0.                                                     (7)
```

The kernel is strict because `A,B,q,qbar>0`, and `D` uses all six physical coordinates. Equation (7) disproves the universal pointwise-in-`r` positive-definiteness assertion. Consequently no claimed all-positive Sylvester polynomial for that assertion can be a valid certificate on the stated domain.

This does not determine the sign of

```text
G1''=integral_0^infinity r Phi_r'' dr.
```

A negative integrand at one `r` can be outweighed elsewhere. The checker rigorously finds `G1''>0` for the displayed direction, so (7) is not even a one-sided integrated counterexample.

## 3. Two emitted states and the leaf marginal

For `phi(x)=x log x`, define

```text
G1=sum_s P_s phi(q_s),
G0=sum_s P_s phi(1-q_s).
```

The complete entropy factors exactly as

```text
H=H(P)-G1-G0.                                        (8)
```

For either side, direct differentiation gives

```text
[sum_s P_s phi(q_s)]''
=sum_s[
 P''_s phi(q_s)
 +2P'_s phi'(q_s)q'_s
 +(1/4){(q'_s)^2/q_s+phi'(q_s)q''_s}].              (9)
```

For the vacant side replace `(q_s,q'_s,q''_s)` by
`(1-q_s,-q'_s,-q''_s)`. This keeps the complete Fisher square and the full acceleration.

The two-leaf marginal has four equal masses at the center. Since the sum of their second derivatives is zero,

```text
-H(P)''=sum_s (P'_s)^2/P_s=4(d11^2+d22^2).          (10)
```

Combining (8)--(10) gives the lossless full-curvature identity

```text
-H''=4(d11^2+d22^2)+G1''+G0''.                      (11)
```

For the exact witness of Section 2, rational logarithm intervals from the checker give

```text
G1''  > 46683.1772178615470,
G0''  > 12761038.5854685968,
-H(P)''=22032,
-H''  > 12829753.7626864583.
```

The same positive full value is reconstructed directly from the eight complete-event formula

```text
-H''=sum_x p'_x^2/p_x+sum_x p''_x log p_x.
```

Thus the old route fails strictly while the true Shannon curvature at this witness remains strictly concave.

## 4. What survives and what does not

Proved here at author level:

- the event and conditional jets (1)--(5) for every six-direction half-leaf line;
- the exact physical counterexample (7) to pointwise `Phi_r''>=0`;
- the complete two-side-plus-marginal identity (11);
- rigorous positivity of the true full curvature on the same witness.

Not proved:

- universal nonnegativity of the integrated one-sided block `G1''`;
- universal half-leaf Shannon concavity;
- any unequal-leaf theorem;
- a Shannon entropy counterexample;
- novelty or formal verification.

The viable continuation is to analyze the paired logarithmic Hessian in (11), or an exact low-dimensional Schur complement of it. Proving each `Phi_r''` separately is an invalid stronger target.
