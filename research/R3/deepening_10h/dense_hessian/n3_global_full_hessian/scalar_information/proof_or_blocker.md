# D10-U10b scalar-information route for the n=3 Fisher bound

STATUS: INCOMPLETE / BLOCKER_FROZEN / INDEPENDENTLY_AUDITED.

This note is an independent route attempt for the U8 scalar obstruction.  It
does not modify the U8 proof files, audits, `scalar_direct`, or shared indexes.
The goal is to prove, or reduce without hiding constants, the connected-domain
scalar inequality

```text
rho(K)=det(N) eta^T [F_K+det(N)G_N]^{-1} eta <= 1.
```

No proof of the global inequality is obtained here.  The usable outcome is an
exact Hilbert-space/ridge-regression reformulation plus a rational blocker
showing that the tempting Fisher-only Bessel shortcut is false.  A fresh
implementation under `audit_nonauthor/` independently reconstructed both the
normalization and the blocker and returned `CORRECT_SCOPED`.

## 1. Exact atoms and score matrices

For a strict real symmetric `3x3` DPP kernel `0<K<I`, let the eight exact atoms
be

```text
p_S = sum_{T superset S} (-1)^{|T|-|S|} det(K_T).
```

For each atom write its first variation as

```text
dot p_S(D) = <M_S,D>_F,
```

where the observation coordinates are

```text
E11, E22, E33, E12+E21, E13+E31, E23+E32.
```

The event Fisher form is

```text
F_K(D,D)=sum_S dot p_S(D)^2/p_S.
```

Use the U8 cofactor matrix

```text
N=-diag(l23,l13,l12)-Lambda K,
```

with

```text
l12=log(p0 p12/(p1 p2)),      l13=log(p0 p13/(p1 p3)),
l23=log(p0 p23/(p2 p3)),
Lambda=log(p123 p1 p2 p3/(p0 p12 p13 p23)).
```

On connected strict support, the earlier reviewed U8 reduction gives `N>0` and

```text
B_K(D,D)=F_K(D,D)+det(N)||N^{-1/2}DN^{-1/2}||_F^2
          -det(N)tr(N^{-1}D)^2.                              (1)
```

Thus the whole remaining problem is the norm of the trace functional in the
positive form before the final negative rank-one subtraction.

## 2. Bessel/ridge reformulation

Put

```text
Y=N^{-1/2}DN^{-1/2},
C_S=N^{1/2}M_SN^{1/2}/sqrt(det(N)p_S).
```

Then

```text
F_K(D,D)/det(N)=sum_S <C_S,Y>_F^2.
```

Therefore

```text
rho(K) = <I, (I + sum_S C_S otimes C_S)^{-1} I>_F.            (2)
```

Here `C_S otimes C_S` denotes the rank-one operator
`Y -> <C_S,Y>_F C_S` on `Sym(3)`.  Indeed, after dividing the positive part of
(1) by `det(N)`, the quadratic form before the final trace subtraction is

```text
<Y, (I + sum_S C_S otimes C_S)Y>_F.
```

The squared dual norm of `Y -> tr(Y)=<I,Y>_F` in that form is exactly the
quantity in (2), which is the coordinate scalar `rho/det(N)` multiplied back by
`det(N)`.

Equivalently, by the standard ridge/Bessel identity,

```text
rho(K)= min_alpha [ ||I - sum_S alpha_S C_S||_F^2
                    + sum_S alpha_S^2 ].                     (3)
```

The proof of (3) is just completing the square in the Hilbert space
`Sym(3) plus R^8`: the normal equation for the minimizer is
`(I+CC^*)alpha=CI`, and the attained value equals
`<I,(I+C^*C)^{-1}I>`.  This is Bessel/ridge geometry, not a DPP-specific
inequality yet.

In unnormalised atom-score variables `g_S`, this is

```text
rho(K)= min_g [
  ||I - N^{1/2}(sum_S g_S M_S)N^{1/2}||_F^2
  + det(N) sum_S p_S g_S^2 ].                                (4)
```

Adding a constant to all `g_S` does not change `sum_S g_S M_S`, because
`sum_S M_S=0` is the first derivative of total mass.  It only increases the
score cost unless the constant is zero, so the optimizer is automatically a
mean-zero atom function.

This is the clean information-theoretic form that U10b was looking for: a
global proof of `rho<=1` is exactly the construction, for every connected
strict `K`, of atom weights `g_S` whose residual-plus-score energy in (4) is at
most one.

However, (3)/(4) are still equivalent to the original scalar inequality.  The
optimal `g` is the ridge solution, so merely writing the minimum does not prove
the bound.  A non-circular proof still needs an explicit construction or a
structural inequality forcing that minimum to be `<=1`.

## 3. The Fisher-only score projection shortcut fails

A natural stronger attempt is to represent the trace functional using scores
alone, without the residual term in (4).  In coordinates this would be the
sufficient inequality

```text
det(N) eta^T F_K^{-1} eta <= 1,                              (5)
```

whenever the Fisher matrix is invertible.  If true, (5) would imply `rho<=1`
because adding the positive `det(N)G_N` term only decreases the inverse.

This shortcut is false even at a strict connected rational DPP:

```text
K =
[[1367/5000,   7/250,    723/2500],
 [   7/250, 2187/2500,  -33/2500],
 [ 723/2500, -33/2500, 7231/10000]].
```

The independent exact-event sanity script gives

```text
min atom                  = 1823557317 / 125000000000
min LDL pivot of N         = 0.0185981408270674...
rho with full A            = 0.6364350521741917...
det(N) eta^T F^{-1} eta    = 1.6324286014007979...
min LDL pivot of B         = 0.0723278981106564...
```

So the actual U8 scalar is safely subunit at this point, but the Fisher-only
projection norm is larger than one.  Any successful proof must use the combined
score-plus-geometric residual in (4), not just a score-only Bessel argument.

This is not a positive-curvature candidate and not evidence against the global
`rho<=1` conjecture.  It is only a blocker for a plausible proof shortcut.

## 4. What remains open

The remaining proof obligation is now precise:

```text
For every connected strict 3x3 DPP kernel K, construct atom weights g_S such
that

  ||I - N^{1/2}(sum_S g_S M_S)N^{1/2}||_F^2
  + det(N) sum_S p_S g_S^2 <= 1,

with strict inequality in the connected interior if positive definiteness is
desired.
```

The conditional-odds square identities control the signs needed for `N>0`, but
in this route they do not yet yield the residual-plus-score energy bound.  The
rank-one boundary asymptotic also shows that no proof can rely on a uniform
margin `rho<=c<1`.

No counterexample with `rho>1` is produced here.
