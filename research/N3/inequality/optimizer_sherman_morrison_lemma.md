# Optimizer Sherman-Morrison lemma

## Status

`PROVED_HERE` as a finite-dimensional optimisation lemma.

`INCOMPLETE` as a proof of the frozen N3 inequality, because the needed DPP
alignment bound is still open.  In the final closure, the `SM-close`
condition below is classified as `EQUIVALENT_BLOCKER`, not as a solved
subproblem.

## Setup

Work in the six-dimensional real vector space of symmetric three by three
directions.  Let

```text
c(D) = tr(N^-1 D),
d = det(N),
G(D,E) = tr(N^-1 D N^-1 E).
```

Use the score projection decomposition supplied by the main instance:

```text
F(D,D) = F2(D,D) + v(D)^2,
v(D) = Lambda'[D]/sqrt(Z),
Z = sum_S 1/p_S.
```

Here

```text
Lambda = log(p_123 p_1 p_2 p_3/(p_empty p_12 p_13 p_23)).
```

Define

```text
H(D,E) = F2(D,E) + d G(D,E),
A(D,E) = H(D,E) + v(D)v(E).
```

Thus the frozen trace-normalised target is

```text
A(D,D) >= d        whenever c(D)=1.
```

Let `D_A` be the true trace-constrained minimiser of `A`, not the minimiser
of `H`.  Let `H^-1` denote the inverse Riesz map for the quadratic form `H`,
and set

```text
alpha = c(H^-1 c),
beta  = v(H^-1 c),
gamma = v(H^-1 v),
s     = alpha - beta^2/(1+gamma).
```

By Cauchy's inequality in the `H` metric, `beta^2<=alpha gamma`.

## Lemma

The true `A`-minimiser is

```text
D_A = (H^-1 c - (beta/(1+gamma)) H^-1 v)/s,
```

and

```text
c(D_A) = 1,
A(D_A,D_A) = 1/s,
v(D_A) = beta/((1+gamma)s).
```

Let `D_H=H^-1 c/alpha` be the `H`-only constrained minimiser.  Then the
normalised Lambda-score is always suppressed at the true `A`-minimiser:

```text
|v(D_A)| <= |v(D_H)|.
```

More explicitly,

```text
|v(D_A)|/|v(D_H)| = alpha/((1+gamma)s) <= 1
```

when `beta != 0`, and both scores are zero when `beta=0`.

The full target at the true optimiser is equivalent to the scalar inequality

```text
s <= 1/d.
```

Equivalently, if the `H`-only form has trace-mode deficit

```text
alpha - 1/d > 0,
```

then the retained `v v^T` term closes that deficit exactly when

```text
beta^2/(1+gamma) >= alpha - 1/d.                 (SM-close)
```

This is an exact equivalence for rank-one repair at the optimiser.  It is not
progress unless a separate DPP argument lower bounds the left side.

Finally, the stronger statement

```text
F2(D_A,D_A) >= 2 tr(N adj D_A)
```

is equivalent to

```text
alpha - ((2+gamma) beta^2)/(1+gamma)^2
  >= d (alpha - beta^2/(1+gamma))^2.             (F2-at-DA)
```

This last condition is a sufficient and necessary scalar test for `F2` alone
to dominate the cofactor term at the true `A`-optimiser.

## Proof

Sherman-Morrison gives

```text
A^-1 = H^-1 - (H^-1 v v H^-1)/(1+gamma).
```

Therefore

```text
A^-1 c = H^-1 c - (beta/(1+gamma)) H^-1 v,
c(A^-1 c) = alpha - beta^2/(1+gamma) = s.
```

The constrained minimiser of a positive quadratic form `A` under `c(D)=1` is
`A^-1 c / c(A^-1 c)`, giving the displayed formula for `D_A` and
`A(D_A,D_A)=1/s`.

Applying `v` to `A^-1 c` gives

```text
v(A^-1 c) = beta - gamma beta/(1+gamma) = beta/(1+gamma),
```

so `v(D_A)=beta/((1+gamma)s)`.

For the suppression claim, `v(D_H)=beta/alpha`.  If `beta=0` there is
nothing to prove.  Otherwise

```text
|v(D_A)|/|v(D_H)| = alpha/((1+gamma)s).
```

Since

```text
(1+gamma)s = (1+gamma)alpha - beta^2 >= alpha
```

by `beta^2<=alpha gamma`, the ratio is at most one.

The full target at the optimiser is `A(D_A,D_A)>=d`, hence `1/s>=d`, or
`s<=1/d`.  Substituting the value of `s` gives `(SM-close)`.

For the `F2`-only statement, use

```text
2 tr(N adj D) = d(c(D)^2 - G(D,D)).
```

At `c(D_A)=1`,

```text
F2(D_A,D_A) >= 2 tr(N adj D_A)
```

is equivalent to

```text
F2(D_A,D_A) + d G(D_A,D_A) >= d,
```

that is, `H(D_A,D_A)>=d`.  The numerator of `H(D_A,D_A)` is

```text
H(A^-1 c, A^-1 c)
  = alpha - 2 beta^2/(1+gamma) + gamma beta^2/(1+gamma)^2
  = alpha - ((2+gamma) beta^2)/(1+gamma)^2.
```

Dividing by `s^2` and multiplying by `s^2` gives `(F2-at-DA)`.

## DPP interpretation and exact blocker

This lemma is not a new name for the old rho condition.  The old full target
is the single scalar condition `s<=1/d`; by itself that is still the original
problem.  The new information is the decomposition of the rank-one correction:

```text
rank-one improvement = beta^2/(1+gamma).
```

If `H` alone fails, then `alpha>1/d`, and the discarded Lambda score can
repair the trace-mode deficit only through its `H^-1` alignment `beta` with
the trace functional `c`.  If `beta=0` and `alpha>1/d`, the rank-one term
cannot repair the failure.  Thus any proof using `F2+v v^T` must prove a
genuine DPP lower bound on this alignment, not just quote positivity of
`v v^T`.

For the actual DPP score,

```text
v(D)^2 = (Lambda'[D])^2/Z,
Z = sum_S 1/p_S,
```

and the event-space vector

```text
h_S = (-1)^(3-|S|)/p_S
```

is Fisher-orthogonal to constants and to all statistics of degree at most
two.  Hence `v v^T` is exactly the one score direction lost by projecting
from full Fisher to `F2`.

This also explains the rank-two boundary obstruction reported by the main
instance.  If `p_123=epsilon` is rare while the other event probabilities
stay bounded and `dot p_123` is not forced to vanish, then

```text
Z = epsilon^-1 + O(1),
Lambda'[D] = dot p_123/epsilon + O(1),
v(D)^2 = dot p_123^2/epsilon + O(1).
```

Dropping `v v^T` removes the rare-event Fisher pole.  The optimisation lemma
shows what has to replace it: either the scalar `F2-at-DA` condition, or the
alignment inequality `(SM-close)` for the actual DPP `H`, `v`, and `c`.
No corresponding lower bound on `beta^2/(1+gamma)` is proved in this unit.
Thus `(SM-close)` is an `EQUIVALENT_BLOCKER` for the frozen theorem.
