# Locked-odds degeneracy addendum

This addendum corrects the degeneracy discussion in
`lambda_tangent_locked_odds_lemma.md` without editing that historical file.

## Correct degeneracy statement

For one positive two by two slice

```text
x=(a,b,c,d),       m=a+b+c+d,       delta=ad-bc,
g=(d-2delta/m, -c-2delta/m, -b-2delta/m, a-2delta/m),
psi=(1/a, -1/b, -1/c, 1/d),
V=sum x_r g_r^2,
W=sum x_r psi_r^2,
R=W-m^2/V,
```

one has

```text
V>0,       R>=0.
```

If `R=0`, it does not follow that the covariance root is zero.  Instead,
`psi` is exactly the Fisher-metric projection of the odds score onto the
determinant score:

```text
psi = (m/V) g.
```

Consequently every actual centered slice score obeys the identity

```text
E = mL/V,
```

where

```text
L=<g, dot x - x dot m/m>,
E=<psi, dot x - x dot m/m>.
```

For example, positive slices with `a=d` and `b=c` satisfy

```text
g = ab psi,
R = 0,
delta = a^2-b^2,
```

so `delta` can be nonzero.

## Proof

The slice mean identities are

```text
sum x_r g_r = 0,       sum x_r psi_r = 0.
```

The Fisher inner products are

```text
<g,g> = V,
<psi,psi> = W,
<g,psi> = m.
```

The identity `<g,psi>=m` follows by direct summation:

```text
d-2delta/m + c+2delta/m + b+2delta/m + a-2delta/m = m.
```

Since all slice masses are positive, the Fisher inner product is positive
definite on slice functions.  The vector `g` cannot vanish: if `g=0`, then
`a=d=2delta/m` and `b=c=-2delta/m`, impossible with positive
`a,b,c,d`.  Hence `V=<g,g> > 0`.

Now

```text
R = W-m^2/V
  = <psi - (m/V)g, psi - (m/V)g>.
```

Thus `R>=0`.  Equality holds exactly when
`psi=(m/V)g`, and then every centered score `s` satisfies

```text
E=<psi,s>=(m/V)<g,s>=mL/V.
```

## Two-slice locked term

For the two slices conditioned on `X_k=0` and `X_k=1`, the locked-odds
improvement was written as

```text
(A_0-A_1)^2/(R_0+R_1),       A_e=m_e L_e/V_e.
```

If `R_0+R_1>0`, this is the usual minimised Fisher cost under the exact lock
`E_0=E_1` coming from `Lambda'[D]=0`.

If `R_0+R_1=0`, then both `R_0=R_1=0`.  The equality case above gives

```text
E_0=A_0,       E_1=A_1.
```

The Lambda lock `E_0=E_1` therefore forces `A_0=A_1`.  In this degenerate
case the displayed improvement term is defined to be `0`.  With that
definition the lower bound remains valid:

```text
C_0+C_1 >= L_0^2/V_0 + L_1^2/V_1.
```

No claim is made that arbitrary approaches to the degenerate point have a
unique limiting value for the extra term.  The statement needed here is only
the valid lower bound at the actual degenerate score.

## Consequence for the round 2 route

The addendum preserves the proven lower bound `F>=Q_k^lock`.  It only
corrects the degenerate interpretation of the final locked-odds residual.
The main instance's frozen counterexample
`c6568dfe1c0c57aaf0b627e84601c35b79b22434` refutes the further dominance
claim

```text
max_k Q_k^lock(D) >= 2 tr(N adj D)
```

on an exact Lambda-tangent direction, and therefore also refutes every
convex combination using only the same three `Q_k^lock` terms at that
`K,D`.  It does not refute `F>=Q_k^lock`.
