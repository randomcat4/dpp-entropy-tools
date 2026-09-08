# Slice Fisher covariance lemma

## Result

Fix a strict real symmetric three-point DPP kernel `0<K<I`, and let `p_S`
be its exact event probabilities.  For every real symmetric direction `D`,
write `dot p_S=dp_S[D]` and

```text
F(D,D) = sum_S dot p_S^2 / p_S.
```

Choose a coordinate `k`, and let `{i,j,k}={1,2,3}`.  For a fixed value
`epsilon in {0,1}` of `X_k`, form the unnormalised two by two slice

```text
a = p_{X_i=0, X_j=0, X_k=epsilon},
b = p_{X_i=1, X_j=0, X_k=epsilon},
c = p_{X_i=0, X_j=1, X_k=epsilon},
d = p_{X_i=1, X_j=1, X_k=epsilon}.
```

Let

```text
m = a+b+c+d,
delta = ad-bc,
V = ad(a+d)+bc(b+c)-4 delta^2/m,
L_D = dot delta - 2 delta dot m/m.
```

Then `V>0` and

```text
F(D,D) >= D_kk^2/(K_kk(1-K_kk)) + sum_{epsilon=0,1} L_D(epsilon)^2/V(epsilon).
```

Call the right hand side `Q_k(D)`.

More precisely, this is an exact decomposition

```text
F(D,D) = Q_k(D) + R_k(D)
```

with `R_k(D)>=0`.  In a slice,

```text
R = sum_r (tilde x_r - (L_D/V) x_r g_r)^2/x_r,
tilde x_r = dot x_r - x_r dot m/m,
g = (d-2delta/m, -c-2delta/m, -b-2delta/m, a-2delta/m).
```

The full residual `R_k` is the sum of the two slice residuals.

For DPP slices the two determinants are exactly the two conditional
covariance squares:

```text
delta_0 = p_empty p_ij - p_i p_j
        = -((1-K_kk)K_ij + K_ik K_jk)^2,

delta_1 = p_k p_123 - p_ik p_jk
        = -(K_kk K_ij - K_ik K_jk)^2.
```

Consequently, if

```text
w_0 = (1-K_kk)K_ij + K_ik K_jk,
w_1 = K_kk K_ij - K_ik K_jk,
m_0 = 1-K_kk,
m_1 = K_kk,
```

then

```text
L_D(epsilon) = -2 w_epsilon
               (dot w_epsilon - w_epsilon dot m_epsilon/m_epsilon).
```

This is the exact square-root form of the same lower bound.

## Proof

All exact probabilities are positive because `0<K<I`.  Partition the eight
events by the value of `X_k`.  For one slice write the four probabilities as
`x=(a,b,c,d)`, their derivatives as `dot x`, and the slice mass as
`m=sum x_r`.

The Fisher contribution of this slice has the orthogonal decomposition

```text
sum_r dot x_r^2/x_r
  = dot m^2/m
    + sum_r (dot x_r - x_r dot m/m)^2/x_r.                 (1)
```

The first term records only the change of the slice mass.  Summing the two
slices gives

```text
dot m_0^2/m_0 + dot m_1^2/m_1
  = D_kk^2/(1-K_kk) + D_kk^2/K_kk
  = D_kk^2/(K_kk(1-K_kk)),
```

since `m_1=P(X_k=1)=K_kk`, `m_0=P(X_k=0)=1-K_kk`, and
`dot m_1=D_kk`, `dot m_0=-D_kk`.

It remains to lower bound the conditional part of a single slice.  Let

```text
g = (d-2delta/m, -c-2delta/m, -b-2delta/m, a-2delta/m).
```

Then

```text
sum_r x_r g_r = 0
```

and

```text
g dot dot x = dot delta - 2 delta dot m/m = L_D.
```

Because `g` has zero mean in the slice, replacing `dot x` by the centered
derivative `dot x - x dot m/m` does not change this pairing.  Cauchy's
inequality in the weighted Fisher metric gives

```text
L_D^2
 <= (sum_r (dot x_r - x_r dot m/m)^2/x_r) (sum_r x_r g_r^2).
```

The dual norm is exactly

```text
sum_r x_r g_r^2
 = ad(a+d)+bc(b+c)-4delta^2/m
 = V.
```

The same line gives the exact Pythagorean remainder.  Indeed, since
`sum_r x_r g_r^2=V`,

```text
sum_r (dot x_r - x_r dot m/m)^2/x_r
  = L_D^2/V
    + sum_r (tilde x_r - (L_D/V) x_r g_r)^2/x_r.
```

Thus the conditional Fisher contribution of the slice is `L_D^2/V` plus a
nonnegative residual.  Summing the two slices proves `F(D,D)=Q_k(D)+R_k(D)`
and hence the stated lower bound.

The positivity of `V` follows from the same representation as
`sum_r x_r g_r^2`.  If `V=0`, then all four positive weights force
`g=0`; this would imply simultaneously `a=d=2delta/m` and
`b=c=-2delta/m`, impossible for positive `a,b,c,d`.

Finally, the displayed DPP square identities are the frozen target's two
conditional covariance identities.  Differentiating `delta_epsilon=-w_epsilon^2`
and subtracting `2 delta_epsilon dot m_epsilon/m_epsilon` gives the
square-root form of `L_D`.

## Coupling to N

The same two slices also reconstruct the entries of `N`.  Let

```text
ell_0 = log(p_empty p_ij/(p_i p_j)),
ell_1 = log(p_k p_123/(p_ik p_jk)).
```

For the frozen notation, `ell_0=l_ij` and `ell_1=l_ij+Lambda`.  Therefore

```text
N_kk = -(1-K_kk) ell_0 - K_kk ell_1,
N_ij = -(ell_1-ell_0) K_ij.
```

Also `K_ij=w_0+w_1`.  Hence the diagonal and off-diagonal entries of `N`
are built from the same pair of conditional log-odds and covariance roots
that appear in `Q_k`.

This is only a coupling lemma.  It does not imply the target inequality by
itself.
