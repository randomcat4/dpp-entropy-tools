# D10-U10b `scalar_information` fresh non-author audit

STATUS: CORRECT_SCOPED.

Scoped meaning: the information/ridge reformulation in
`proof_or_blocker.md` lines 73-120 is correct, and the Fisher-only shortcut
blocker in lines 151-168 is a valid blocker.  The global inequality
`rho(K)<=1` remains INCOMPLETE / not proved.

I did not import or call `scalar_information_sanity.py` or any U8
author/search/gate module.  The author sanity script was read only by hashing.

## What was independently rebuilt

`audit.py` reconstructs from the exact-event definitions:

- all eight Möbius atoms;
- exact first jets in the observation coordinate basis
  `(11,22,33,12,13,23)`;
- the matrices `M_S` with the correct Frobenius convention, namely
  off-diagonal matrix entries are half of the coordinate derivative;
- the Fisher matrix `sum_S dp_S dp_S^T/p_S`;
- `l12,l13,l23,Lambda`, `N`, `A`, `eta`, `B=A-det(N)eta eta^T`, and `rho`;
- the Hilbert-space operator forms for equations (2), (3), and (4).

Exact mass and first-jet checks passed on all audited rational cases:

```text
sum_S p_S = 1
sum_S dp_S = 0
sum_S M_S = 0
all atoms positive
```

## Equations (2), (3), and (4)

The constants and normalizations are correct.

The independent check uses a Frobenius-orthonormal six-coordinate basis
`E11,E22,E33,(E12+E21)/sqrt(2),(E13+E31)/sqrt(2),(E23+E32)/sqrt(2)`.
For each atom,

```text
C_S = N^{1/2} M_S N^{1/2} / sqrt(det(N) p_S)
```

then verifies:

```text
rho = <I,(I + sum_S C_S otimes C_S)^(-1)I>
    = min_alpha ||I - sum_S alpha_S C_S||_F^2 + sum_S alpha_S^2
    = min_g ||I - N^{1/2}(sum_S g_S M_S)N^{1/2}||_F^2
            + det(N) sum_S p_S g_S^2.
```

The relation between variables is

```text
g_S = alpha_S / sqrt(det(N) p_S),
```

which confirms the `det(N) p_S` coefficient in equation (4).

Maximum discrepancy between the coordinate rho and the three information-space
versions across the audited rational cases:

```text
5.773159728050814e-15
```

This is a floating square-root/operator check of constants, backed by exact
Fraction atom/jet construction and Decimal coordinate recomputation.

## Mean-zero gauge note

`proof_or_blocker.md` lines 123-126 are acceptable if read as a gauge statement
at the optimizer.  More explicitly, shifting `g` by a constant does not change
`sum_S g_S M_S`; the score cost changes by

```text
det(N) * (2c sum_S p_S g_S + c^2).
```

Therefore the optimal representative satisfies `sum_S p_S g_S=0`.  For an
arbitrary non-mean-zero `g`, a constant shift can decrease the score term.  This
is not a critical gap because the conclusion “the optimizer is mean-zero” is
correct and the script confirms the optimal weighted mean is numerically zero.

## Fisher-only shortcut blocker

The blocker kernel from `proof_or_blocker.md` lines 153-158 is strict and
connected:

```text
K =
[[1367/5000,   7/250,    723/2500],
 [   7/250, 2187/2500,  -33/2500],
 [ 723/2500, -33/2500, 7231/10000]]
```

Exact LDL pivots:

```text
K:   1367/5000, 2979829/3417500, 12368800183/29798290000
I-K: 3633/5000, 161047/1297500, 1823557317/11273290000
```

All off-diagonal entries are nonzero, so the support graph is complete.

Exact atom positivity:

```text
min atom = p0 = 1823557317 / 125000000000
```

Decimal checks:

```text
min LDL pivot of N      = 0.018598140827067429328489868953828701468957916588592404375518520106143053174919079223628980928958962097130975698
true rho                = 0.63643505217419175524081760065272273255259480503872645482486062119311349425326465830316908934233303867966280939
score-only scalar       = 1.6324286014007979109002061346170951729134949189841867364081162817699295761556763994718169346616261532557938644
min LDL pivot of B      = 0.072327898110656445619959129575780642326986128115745655846995764588243010641715831715278993530947152121559913549
```

Thus the Fisher-only sufficient inequality

```text
det(N) eta^T F^{-1} eta <= 1
```

is genuinely false at a strict connected DPP, while the actual U8 scalar remains
below one and the true Hessian form `B` is positive definite.  This blocker
rejects only the Fisher-only proof shortcut; it is not a positive-curvature
candidate.

## “Equivalent rewrite” versus proof

No critical issue found.  The author explicitly says at lines 133-136 that
equations (3)/(4) are equivalent to the original scalar inequality and do not
prove the bound.  The verdict also keeps `rho<=1` as `INCOMPLETE`.

Layered conclusion:

- Information-space/ridge formulas (2), (3), (4): CORRECT.
- Constants and normalizations, including the `det(N)p_S` score cost: CORRECT.
- Fisher-only shortcut blocker: CORRECT.
- Claim that the rewrite proves `rho<=1`: not made by the author.
- Global connected-domain inequality `rho(K)<=1`: INCOMPLETE / still open.

## Files

- `audit.py`
- `results.json`
- `run_log.md`
- `verdict.md`
