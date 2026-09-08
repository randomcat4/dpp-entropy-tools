# U10e boundary analysis: full atom `F -> 0`

Status: INCOMPLETE, but the sharp boundary mechanism is now localized.

Write

```text
c = 1-s,       0<s<1,
a = x sqrt((1-s)/2).
```

Then the spectral/full-atom boundary is `s -> 0`, and the full atom is

```text
F = x^3 s.
```

For fixed `0<x<1/2`, it is the only vanishing atom.  The other five distinct
atoms have positive `s=0` limits:

```text
E0 = (1-x)(1-2x)
U0 = x(1-3x/2)
W0 = x(1-x)
V0 = x^2/2
Z0 = x^2.
```

The centered endpoint `x=1/2,s=0` is more singular because `E` also vanishes;
that edge is already covered away from the endpoint by U10d and is not used
as a new proof here.

## 1. Leading singular rank-one term

For the even coordinates `(d,e,h,k)`, the full-atom derivative is

```text
jF = x^2 ((1+s)d + e - 2 sqrt(2) sqrt(1-s) h + (1-s)k).
```

Hence its Fisher contribution is exactly

```text
jF jF^T / F = (x/s) w_s w_s^T,
```

where

```text
w_s = (1+s, 1, -2 sqrt(2) sqrt(1-s), 1-s).
```

Thus the raw Hessian matrix has a positive rank-one `1/s` explosion.  Any
negative or vanishing mechanism must live near the moving tangent hyperplane
`jF=0`; it cannot come directly from the full atom itself.

## 2. Stable Schur formula

Let `B_even = R + jF jF^T/F`, where `R` contains the five non-full Fisher
terms and the logarithmic cofactor part.  In the U10d transverse basis
`[T0,e0]`, write

```text
C = T0^T R T0,
b = T0^T R e0,
d = e0^T R e0,
u = T0^T jF,
v = e0^T jF.
```

When `C` is invertible, Sherman--Morrison gives the exact identity

```text
sigma =
  d - b^T C^-1 b
  + (v - u^T C^-1 b)^2 / (F + u^T C^-1 u).                  (SM)
```

This is the numerically stable form used in `asymptotic_probe.py`.  It avoids
subtracting matrices of size `1/s` to recover an `O(1)` scalar.

The remaining proof task near this boundary is not the full atom blow-up; it
is to prove that the right side of (SM) stays positive uniformly in the
two-scale corner.

## 3. Fixed `x`, `s -> 0`

Let `L_s=log(1/s)`.  For fixed `0<x<1/2`,

```text
Lambda = -L_s + Lambda0(x) + O(s),
n      =  x L_s + n0(x) + O(s L_s),
m      =  x L_s + m0(x) + O(s L_s),
q      = -x(ell0(x)+kappa0(x)) L_s + O(1).
```

Here `ell0,kappa0` are the `s=0` limits of `log(EV/UW)` and
`log(EZ/U^2)`.  In all sampled fixed-`x` profiles the stable sigma stays
positive and eventually grows with `L_s`.  This gives no negative mechanism
for fixed `x`, but I did not prove the positive leading coefficient.

## 4. Power scales `s=x^p`

For sampled fixed powers `p in {1/2,1,2,4,8}`, as `x -> 0`,

```text
x sigma(x,x^p) -> 1.
```

Thus every tested polynomial approach to the corner sends
`sigma -> +infinity`.  This rules out, as scout evidence only, the idea that
ordinary algebraic rates `s=x^p` are the dangerous scale.

## 5. Exponential scale `s=exp(-beta/x)`

The sharp scale is instead

```text
s = exp(-beta/x),       beta>0 fixed.
```

Then, as `x -> 0`, the logarithmic variables have finite nontrivial limits
after the `x Lambda` cancellation:

```text
Lambda = -beta/x + log 4 + o(1),
n      -> beta + log 2,
m      -> beta,
q      -> beta log 2.
```

Consequently the weighted-trace covector has a finite limit:

```text
eta_d -> (beta+2log2)/(log2 (beta+log2)),
eta_e -> (beta+log2)/(beta log2),
eta_h -> -2sqrt(2)/log2,
eta_k -> beta/(log2 (beta+log2)).
```

The stable formula (SM) then shows numerically an `O(1)` positive valley
rather than the `+infinity` seen on power scales.  At `x=10^-4`, beta
refinement over `0.05,0.06,...,1.50` gave the smallest sampled value at

```text
beta = 0.58,
sigma ≈ 26.5811258707653919.
```

This is the most important output of the boundary probe: if a counterexample
or proof obstruction exists at the full-atom boundary, it must beat this
exponential-scale positive limiting profile, not just the raw `F=0` atom.

## 6. Remaining open item

The true unresolved analytic item is now:

> Derive the limiting exponential-scale scalar `phi(beta)` from (SM), prove
> `phi(beta)>0` for all `beta>0`, and prove a uniform positive remainder for
> the neighboring two-scale region.

No such closed expression or remainder bound is supplied here.  The present
tables are high-precision scouts, not interval certificates and not a proof.
