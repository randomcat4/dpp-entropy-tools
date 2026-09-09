# Lambda-tangent locked-odds Fisher lemma

## Status

`PROVED_HERE` for the Fisher lower bound on the exact hyperplane
`Lambda'[D]=0`.

`INCOMPLETE` for the proposed sufficient condition

```text
Lambda'[D]=0  =>  B(D,D) >= 0.
```

The new bound keeps actual event Fisher information.  It is not a Schur
projection restatement and does not delete the Qk residual.

## One 2 by 2 slice

For a positive unnormalised slice

```text
x=(a,b,c,d),       m=a+b+c+d,       delta=ad-bc,
```

and a tangent `dot x`, define

```text
dot m = dot a+dot b+dot c+dot d,
L = dot delta - 2 delta dot m/m,
E = dot ell,       ell=log(ad/(bc)).
```

Let

```text
g = (d-2delta/m, -c-2delta/m, -b-2delta/m, a-2delta/m),
psi = (1/a, -1/b, -1/c, 1/d),
V = sum x_r g_r^2
  = ad(a+d)+bc(b+c)-4delta^2/m,
W = sum x_r psi_r^2
  = 1/a+1/b+1/c+1/d,
R = W - m^2/V.
```

Both `g` and `psi` have zero slice mean:

```text
sum x_r g_r = 0,       sum x_r psi_r = 0.
```

Their Fisher Gram matrix is

```text
[[ <g,g>,   <g,psi> ],
 [ <psi,g>, <psi,psi> ]]
=
[[ V, m ],
 [ m, W ]].
```

The identity `<g,psi>=m` is direct:

```text
d-2delta/m + c+2delta/m + b+2delta/m + a-2delta/m = m.
```

Therefore the conditional Fisher part of the slice satisfies

```text
sum_r (dot x_r - x_r dot m/m)^2/x_r
 >= L^2/V + (E - mL/V)^2/R.                    (1)
```

When `R=0`, the two test functions are dependent.  For real DPP slices this
degenerate case is interpreted by continuity; if the covariance root is zero,
then the Rayleigh square gives `L=0` for every affine real tangent in that
slice, so no division by the root is used.

## Two slices locked by Lambda'[D]=0

Fix a coordinate `k`, and let the two slices be `X_k=0` and `X_k=1`.  For the
remaining pair `{i,j}`, write their conditional log odds as

```text
ell_0 = log(p_empty p_ij/(p_i p_j)),
ell_1 = log(p_k p_123/(p_ik p_jk)).
```

In the frozen notation,

```text
Lambda = ell_1 - ell_0.
```

Hence the exact hyperplane condition `Lambda'[D]=0` locks the two odds
derivatives:

```text
E_0 = ell_0'[D] = ell_1'[D] = E_1.
```

Apply (1) to both slices.  If

```text
A_e = m_e L_e/V_e,      e=0,1,
```

then, after minimising over the common odds derivative, the two conditional
Fisher contributions obey

```text
C_0+C_1
 >= L_0^2/V_0 + L_1^2/V_1
    + (A_0-A_1)^2/(R_0+R_1).                  (2)
```

The last term is new relative to the round 1 Qk bound.  It is the Fisher cost
of making the two slice odds derivatives equal while their determinant-score
projections predict different odds derivatives.

Adding the marginal Fisher term of `X_k` gives the Lambda-tangent lower bound

```text
F(D,D) >= Q_k^lock(D)
```

where

```text
Q_k^lock
 = D_kk^2/(K_kk(1-K_kk))
   + L_0^2/V_0 + L_1^2/V_1
   + (m_0L_0/V_0 - m_1L_1/V_1)^2/(R_0+R_1).
```

If `R_0+R_1=0`, the final term is interpreted by the same projection
continuity.  In the real DPP degenerate slice case the corresponding
covariance-root derivative has `L_e=0`; if both residual norms vanish, the
locked-odds residual contributes no finite extra term.

This is an actual event-Fisher lower bound under `Lambda'[D]=0`.  It is
strictly stronger than the previous `Q_k` bound whenever the locked-odds
residual is nonzero.

## Connection to real Rayleigh squares

For real DPP slices, the determinants are the exact conditional covariance
squares

```text
delta_0 = p_empty p_ij - p_i p_j
        = -((1-K_kk)K_ij+K_ikK_jk)^2,
delta_1 = p_k p_123 - p_ik p_jk
        = -(K_kkK_ij-K_ikK_jk)^2.
```

Thus

```text
L_e = -2 omega_e (omega_e' - omega_e m_e'/m_e),
```

with

```text
omega_0=(1-K_kk)K_ij+K_ikK_jk,
omega_1=K_kkK_ij-K_ikK_jk.
```

These formulas are polynomial in the affine `K+tD` variables.  They are
compatible with the full real constraint

```text
T^2=4uvw,       u=a^2, v=b^2, w=c^2, T=2abc,
```

and its first and second jets; no division by an edge, by `T`, or by a
covariance root is required.

## Attempted closure and exact failure point

The proposed sufficient condition would follow if one could prove, for every
real strict connected `K` and every `Lambda'[D]=0`,

```text
max_k Q_k^lock(D) >= 2 tr(N adj D),
```

or a kernel-dependent convex combination of the three `Q_k^lock` lower bounds
dominating the same cofactor term.

This unit does not prove such a dominance.  The new locked-odds term controls
one concrete residual left out by Qk, but the cofactor expression still mixes
the three edge accelerations and diagonal directions through `adj(D)`.  The
Rayleigh identities force the edge-square jets to be realisable, and
`Lambda'[D]=0` locks the slice odds, but I did not find a sign argument that
turns these facts into a lower bound for `2 tr(N adj D)`.

The main instance has also strictly refuted the simpler pure-acceleration
shortcut `C<=0` on a Lambda-tangent real square path while keeping `B>0`.
That obstruction is consistent with the present result: the missing
positivity is in full Fisher information, not in a standalone acceleration
sign.

## Minimal remaining obligation

A non-equivalent proof of the hyperplane sufficient condition now needs one
of the following:

1. prove `max_k Q_k^lock(D) >= 2 tr(N adj D)` on the exact real
   `Lambda'[D]=0` hyperplane;
2. find explicit nonnegative weights depending only on `K` such that
   `sum_k theta_k Q_k^lock(D) >= 2 tr(N adj D)` on that hyperplane; or
3. add another event-Fisher projection, still under the exact Lambda lock,
   whose residual controls the remaining `adj(D)` terms.

Absent one of these, the route returns to the same unresolved
Fisher-versus-cofactor gap and must stop.
