# I05-22 R5 continuation: a four-scalar rectangle Gram inequality and a fixed-shape determinant audit

Status: **PROVED (author; PENDING_REVIEW)** for the rectangle inequality in Sections 2-3, the exact relaxed non-sufficiency witness in Section 5, and the same-q edge-placement inequality in Section 6. **INCOMPLETE** for the actual full determinant sign away from already accepted scopes. Numerical values in Section 4 are diagnostics only, not independent evidence or interval certificates. Novelty is unassessed.

This continuation stays on PR81's branch and uses the accepted PR70 full core exactly as inherited in `proof.md`: complete eight-event Shannon entropy, true kernel-affine directions, the complete paired Fisher `F`, the positive update `R`, marginal Fisher `diag(1/v,1/w)`, and all mixed directions are retained. No PR60 Lambda-zero arithmetic is rerun. Issue73's 273 points / three filaments / shared 2700-second contract is not started or duplicated.

## 1. Fixed actual shape and exact q-derivative ledger

For the requested concrete test choose

```text
x=y=1/2,
A=1/4,
B=4/9,
r=1-A-B=11/36,
0<q<r,
qbar=r-q.
```

This is the second rational shape already named in issue73, but **no filament scan is run here**. We use it only for symbolic one-point diagnostics and analytic identities. The corresponding physical arrows have

```text
b=1/4, c=1/3,
z=q+A/2+B/2=q+25/72,
K(q)=[[1/2,0,1/4],[0,1/2,1/3],[1/4,1/3,z]].
```

The four paired quantities from `proof.md` obey, for every fixed `A,B` when `x=y=1/2`,

```text
ell' = 1/2 [ f(q+A+B)-f(q+B)+f(q+A)-f(q) ],
k'   = 1/2 [ f(q+A+B)-f(q+A)+f(q+B)-f(q) ],
lambda' = f(q+A+B)-f(q+B)-f(q+A)+f(q) = J''(q),
J' = lambda,
```

where `f(t)=1/[t(1-t)]`. Thus all q-derivatives of the transcendental four-tuple are rational functions of `(q,A,B)` except the already present value `lambda=J'`. No side log is differentiated separately.

At the illustrative exact point

```text
q*=r/4=11/144,
qbar*=11/48,
```

these three rational derivatives are

```text
ell'    = -565563230208 / 141900356675,
k'      = -642389409792 / 141900356675,
lambda' = 1600526352384 / 141900356675.
```

In particular at this point `ell'<0`, `k'<0`, `lambda'>0`, while `J'=lambda<0` by the already proved imbalance theorem. The determinant chain rule therefore has a distinguished potentially harmful `J` channel: a negative `partial_J det(E_H)` multiplies the negative `J'=lambda` and contributes positively while the shape moves toward the complement-balanced point. A second potentially harmful `lambda` channel can occur near the rare-event boundary because `partial_lambda det(E_H)` is not sign-fixed by the previous independent bounds. The new inequality below couples exactly these quantities instead of bounding them independently.

## 2. A one-dimensional Gram lemma for a DPP edge integral

Let

```text
f(t)=1/[t(1-t)],
g'(t)=f(t),
h_A(t)=g(t+A)-g(t)=int_0^A f(t+a) da,
```

on `0<A<1` and `0<t<1-A`. Then `h_A(t)>0`.

### Lemma 2.1

`u_A(t)=h_A(t)^(-1/2)` is strictly concave on `(0,1-A)`.

### Proof

The special binary-logit Hessian satisfies the pointwise identity

```text
f''(t) = 2 f'(t)^2/f(t) + 2 f(t)^2.                 (1)
```

Put

```text
Q_A(t)=int_0^A f'(t+a)^2/f(t+a) da,
I_A(t)=int_0^A f(t+a)^2 da.
```

Cauchy-Schwarz in the positive measure `f(t+a) da` gives

```text
h_A'(t)^2
 = [int_0^A f'(t+a) da]^2
 <= h_A(t) Q_A(t).                                  (2)
```

Integrating (1),

```text
h_A'' = 2 Q_A + 2 I_A.
```

Hence

```text
2 h_A h_A'' - 3 h_A'^2
 = 4 h_A Q_A + 4 h_A I_A - 3 h_A'^2
 >= h_A Q_A + 4 h_A I_A
 > 0.                                               (3)
```

Direct differentiation gives

```text
u_A'' = [3 h_A'^2 - 2 h_A h_A'']/(4 h_A^(5/2)) < 0.
```

This proves strict concavity. The proof is a genuine Gram/Cauchy estimate on the actual logit edge integral; it does not relax the four DPP corner values independently.

## 3. The four-scalar rectangle inequality

For any strict legal rectangle `q>0`, `q+A+B<1`, define

```text
J = int_0^B h_A(q+b) db.
```

By strict concavity of `u_A=h_A^(-1/2)`, for `0<b<B`,

```text
u_A(q+b)
 > (1-b/B) u_A(q) + (b/B) u_A(q+B).
```

Since `s -> s^(-2)` is decreasing on positive reals,

```text
h_A(q+b)
 < 1 / [(1-b/B)u_A(q)+(b/B)u_A(q+B)]^2.
```

Integrating the elementary reciprocal-square affine function yields

```text
J < B / [u_A(q)u_A(q+B)]
  = B sqrt(h_A(q) h_A(q+B)).                        (4)
```

For `x=y=1/2`, the opposite A-edge integrals are exactly

```text
h_A(q)   = ell - lambda/2,
h_A(q+B) = ell + lambda/2.
```

Therefore

```text
J^2 < B^2 (ell^2-lambda^2/4).                       (5)
```

Swapping the two leaf axes gives independently

```text
J^2 < A^2 (k^2-lambda^2/4).                         (6)
```

Equivalently,

```text
lambda^2 + 4 J^2/B^2 < 4 ell^2,
lambda^2 + 4 J^2/A^2 < 4 k^2.                       (7)
```

These are strict on every connected strict arrow with `x=y=1/2`, `A,B>0`. They simultaneously couple the same four paired scalars that enter the accepted full `E_H`; in particular they are strictly stronger than the separate trapezoid consequences `J<B ell` and `J<A k`. They apply to the whole nonzero-Lambda half-leaf family as well as the fixed shape above, but they do **not** assert entropy concavity.

This also gives a useful determinant-facing parameterization. Define

```text
rho_B = J/[B sqrt(ell^2-lambda^2/4)],
rho_A = J/[A sqrt(k^2-lambda^2/4)].
```

Then every actual strict half-leaf arrow has `0<rho_A,rho_B<1`. Any relaxation of `(ell,k,lambda,J)` that ignores these two correlations enlarges the determinant domain beyond realizable DPP rectangles.

## 4. What happens at the actual fixed point

At `q*=11/144`, direct evaluation of the exact accepted PR70 formulas (same-author diagnostic, ordinary high precision, no interval claim) gives approximately

```text
ell    = 1.4487657547684307,
k      = 2.256710740500806,
lambda = -0.6382494477232565,
J      = 0.5157432250048831,

det E_H = 22.628228448401828,
eig(E_H) approx (4.38384371, 5.16173247).
```

A chain-rule diagnostic at the same actual point, varying the four paired values only for the purpose of identifying sensitivity and holding the rational Fisher shape fixed, gives

```text
partial_ell det   approx +0.26358749,
partial_k det     approx +0.69585634,
partial_lambda det approx -0.03405463,
partial_J det     approx -0.21876945,
explicit-q channel approx -12.54285715.
```

Combining with the exact derivative signs above gives approximate channel contributions

```text
ell channel     -1.05056,
k channel       -3.15017,
lambda channel  -0.38411,
J channel       +0.13963,
explicit rational/Fisher channel -12.54286,
```

for total `d/dq det E_H approx -16.98808` at `q*`. Thus the first concrete obstruction to a proof by independent scalar monotonicity is visible: the `J` channel has the wrong sign even at a benign interior actual point. The full derivative is nevertheless negative because the correlated edge/Fisher channels dominate. This is diagnostic, not a global sign proof.

Near the rare-event side the `lambda` sensitivity can also change sign, so a proof that treats `J` and `lambda` independently cannot be closed merely from `J''>=32AB` and `sign(lambda)`. Inequalities (5)-(7) are designed precisely to retain their rectangle correlation with `ell,k`.

## 5. Exact relaxed negative point: the new Gram inequalities are useful but not sufficient alone

It is important not to mistake positivity on a relaxed sample for the DPP theorem. Conversely, a negative point in a relaxation is not an entropy counterexample unless it is realizable by the same DPP rectangle.

At the same exact shape and the same rational `q*=11/144`, freeze the rational Fisher block `F(q*)` from the accepted formula and replace only the four log scalars by the rational relaxed tuple

```text
ell=10,
k=15,
lambda=-8,
J=4/3.
```

This tuple satisfies the new four-way Gram inequalities strictly:

```text
B^2(ell^2-lambda^2/4)-J^2 = 400/27 >0,
A^2(k^2-lambda^2/4)-J^2   = 1625/144 >0.
```

It also satisfies the coarse R5 positivity/imbalance bounds at this q, including the lower imbalance magnitude. Form `L,C,R,Y=F+R,E_H` exactly with `x=y=1/2`, `A=1/4`, `B=4/9`, `q=11/144`. The four leading Sylvester minors of `Y` are

```text
1007133237504/141900356675,
73499877824256/1560903923425,
16957014248520/62436156937,
1966230941289057/3567780396400,
```

all positive. Nevertheless

```text
det E_H
 = -121782415397102417605 / 391498427421110016
 < 0.                                                  (8)
```

So (5)-(7), even together with the previous coarse independent bounds and positive pivot, do **not** by themselves imply the full determinant sign. This is an exact logical non-sufficiency witness only; it is not a DPP entropy counterexample.

The tuple is provably not realizable at this fixed q. Indeed actual realizability requires

```text
ell+lambda/2 = h_A(q+B)
             = int_0^A f(q+B+a) da.                  (9)
```

For the relaxed tuple the left side is `6`. But on the exact interval

```text
q+B <= q+B+a <= q+A+B
75/144 <= t <= 111/144 = 37/48,
```

`f(t)` is increasing because this interval lies above `1/2`, so

```text
h_A(q+B)
 <= A f(37/48)
 = (1/4) * 2304/407
 = 576/407
 < 2 < 6.                                             (10)
```

Thus (8) lies outside the actual DPP one-parameter curve. It identifies the next missing correlation exactly: after imposing the four-way Gram constraint, the determinant can still fail if the **absolute placement of the opposite edge integrals** is detached from the same rational corner interval. The required same-q identities are

```text
ell-lambda/2 = h_A(q),
ell+lambda/2 = h_A(q+B),
k-lambda/2   = h_B(q),
k+lambda/2   = h_B(q+A).                              (11)
```

These are the minimal realizability data not captured by the previous global scalar bounds or by (5)-(7).

## 6. Same-q edge-placement inequality

The same strict concavity used above gives more than the rectangle integral estimate. For any positive concave differentiable `u`, the secant slope lies between its endpoint derivatives. Applying this to `u_A=h_A^(-1/2)` on `[q,q+B]` gives

```text
u_A'(q)
 > [u_A(q+B)-u_A(q)]/B
 > u_A'(q+B),                                        (12)
```

with strict inequalities because `u_A` is strictly concave and `B>0`. Since

```text
u_A'(t)=-h_A'(t)/(2 h_A(t)^(3/2)),
h_A'(t)=f(t+A)-f(t),                                 (13)
```

(12) is an explicit same-q constraint whose derivative coefficients are rational functions of the four DPP corners. For `x=y=1/2`, substitute

```text
h_A(q)=ell-lambda/2,
h_A(q+B)=ell+lambda/2
```

to obtain

```text
-[f(q+A)-f(q)]/[2(ell-lambda/2)^(3/2)]
 > { 1/sqrt(ell+lambda/2)-1/sqrt(ell-lambda/2) }/B
 > -[f(q+A+B)-f(q+B)]/[2(ell+lambda/2)^(3/2)].       (14)
```

Swapping A and B yields the companion inequality for `k±lambda/2`:

```text
-[f(q+B)-f(q)]/[2(k-lambda/2)^(3/2)]
 > { 1/sqrt(k+lambda/2)-1/sqrt(k-lambda/2) }/A
 > -[f(q+A+B)-f(q+A)]/[2(k+lambda/2)^(3/2)].         (15)
```

Unlike a free scalar range, (14)-(15) knows exactly where each opposite edge sits in the same rational q-rectangle. Together with (5)-(7), they give a strictly stronger realizability envelope while still being analytic and one-dimensional.

For the relaxed negative tuple of Section 5, the A-edge values would be

```text
h_A(q)=14,
h_A(q+B)=6.
```

At the fixed rational q, the exact endpoint derivatives are

```text
h_A'(q)=f(q+A)-f(q)<0,
h_A'(q+B)=f(q+A+B)-f(q+B)>0.
```

Numerically the concavity secant test would require

```text
u_A'(q) > secant > u_A'(q+B),
```

but gives approximately

```text
0.09187 > 0.31722 > -0.05627,
```

whose left inequality fails. This is only a compact display; exact nonrealizability was already proved rationally by (10). The point is structural: the new secant inequality rejects the same false determinant point for the correct reason—its two opposite edge integrals cannot occur at the same q.

## 7. Concrete mathematical outcome and next analytic target

This continuation therefore gives more than a renamed interface:

1. a proved strict Cauchy/Gram theorem, (5)-(7), simultaneously coupling `ell,k,lambda,J` on an actual nonzero-Lambda DPP family;
2. an exact fixed-shape q-derivative ledger showing the wrong-sign `J` channel in the actual determinant derivative;
3. an exact positive-pivot relaxed negative determinant satisfying the new Gram constraints, followed by an exact proof that the tuple is not realizable;
4. proved same-q secant constraints (14)-(15), which add the missing absolute edge placement relative to the rational corners;
5. a narrowed next bridge: a successful determinant proof on the fixed shape must exploit the edge-placement information, not merely independent ranges, strong convexity of `J`, or the two Gram ellipses.

The next analytic task is to insert (14)-(15) into the exact derivative of `det E_H` for the fixed shape and determine whether the wrong-sign `J`/near-boundary `lambda` channels can be absorbed by the rational Fisher and edge channels. A full long-filament interval verification remains reserved to issue73 and is not launched here.

Final classification: **PROVED (author; PENDING_REVIEW)** for Lemma 2.1, inequalities (4)-(7), the exact relaxed non-sufficiency/nonrealizability witness (8)-(10), and same-q inequalities (12)-(15). **INCOMPLETE** for `det E_H>=0` on the actual fixed shape and for the general missing-edge entropy theorem.