# Three fixed nonzero true entropy-rate curvature points

Status: **PROVED (AUTHOR PROOF), NOT INDEPENDENTLY REVIEWED**.

This file strengthens the fixed midpoint result but does not close the continuum `1/2<=|t|<=3/2`.

For

```text
f_t(theta)=1/2+(1/4)cos(4*pi*theta)+(t/8)cos(2*pi*theta),
```

the true complete-configuration entropy rate is twice differentiable on a neighborhood of the strict target interval and satisfies

```text
h''(1/2)<-1/2500,
h''(1)  <-1/1000,
h''(3/2)<-1/500.                                      (1.1)
```

By evenness, the same bounds hold at the three negative parameters.

## 1. Finite conditional curvature, not finite-window normalization

For `r>=0`, put

```text
h_r(t)=H(X_0|X_1,...,X_r)=H_{r+1}(f_t)-H_r(f_t).     (1.2)
```

The exact complete-event formulas in `proof.md` show that `h_r` is analytic on every strict real interval. At the three rational parameters, scaling every event matrix by `32` gives integer entries. The script

```sh
python research/I05-DPP-21-fixed-harmonic-20260909/code/certify_point_curvatures.py --depth 18
```

enumerates, for lengths `18` and `19`, the exact integer triples

```text
(N,N',N'')
```

for every complete event, where

```text
p=N/32^n,
p'=N'/32^n,
p''=N''/32^n.                              (1.3)
```

It verifies exactly

```text
sum N=32^n,
sum N'=sum N''=0.                                     (1.4)
```

Therefore

```text
H_n''=-(1/32^n)sum_events[N'^2/N+N'' log N].          (1.5)
```

The omitted `-N'' n log 32` term sums to zero by (1.4). The Fisher fraction is enclosed by directed decimal division. Each `log N` is evaluated at decimal precision `100`, widened by `10^-90`, and then multiplied and summed with separate floor/ceiling rounding. Thus the resulting interval for

```text
h_18''=H_19''-H_18''                                  (1.6)
```

contains the exact finite conditional curvature.

The jet automaton is independently checked through length six by exact polynomial interpolation of direct signed-event determinants. The value-only automaton is additionally compared with direct Bareiss determinants through length eight.

## 2. Point-specific complex inverse bounds

The true-rate error is much smaller than the earlier uniform whole-interval bound when the complex disk and comparison ratio are chosen at each fixed parameter. Use the following data:

| `t_*` | complex radius `d` | `max |z|` | comparison ratio `rho` |
| --- | --- | --- | --- |
| `1/2` | `1/4` | `3/4` | `2/3` |
| `1` | `1/8` | `9/8` | `2/3` |
| `3/2` | `1/16` | `25/16` | `3/4` |

On the corresponding disk, the absolute first off-diagonal of an event matrix is at most

```text
a=max|z|/16,
```

and the absolute second off-diagonal is `b=1/8`. Let `H` be the comparison M-matrix with diagonal `1/2` and off-diagonals `-a,-b`. For the vector `v_i=rho^|i-j|`, the exact residuals at distances `0,1,2` and at all larger distances are as follows.

### `t_*=1/2`, `a=3/64`, `rho=2/3`

```text
r_0=47/144,
r_1=251/1728,
r_2=71/2592,
r_far/rho^distance=71/1152.                           (2.1)
```

### `t_*=1`, `a=9/128`, `rho=2/3`

```text
r_0=85/288,
r_1=385/3456,
r_2=25/5184,
r_far/rho^distance=25/2304.                           (2.2)
```

### `t_*=3/2`, `a=25/256`, `rho=3/4`

```text
r_0=109/512,
r_1=311/4096,
r_2=37/16384,
r_far/rho^distance=37/9216.                           (2.3)
```

All are positive. As in `proof.md`, comparison and the near/far Schur formula give

```text
|q_R(z)-q_r(z)|<=C_* rho^(2r-6),                     (2.4)
```

where, with `C=1/r_0`,

```text
C_* = C^3(a rho+b)^2(a rho+b+b rho)^2.               (2.5)
```

For reference, the factors in (2.5) are

```text
t=1/2: C=144/47, a rho+b=5/32,  a rho+b+b rho=23/96;
t=1:   C=288/85, a rho+b=11/64, a rho+b+b rho=49/192;
t=3/2: C=512/109,a rho+b=203/1024,a rho+b+b rho=299/1024.
```

Cauchy's formula at the disk center gives

```text
|partial_t^j(q_R-q_r)|
 <=j! d^(-j) C_* rho^(2r-6),       j=0,1,2.           (2.6)
```

No event probability or typical-word estimate occurs in this bound.

## 3. Closed curvature tail

Write

```text
d_r=h_r-h_{r+1}
   =I(X_0;X_{r+1}|X_1,...,X_r).                       (3.1)
```

For the real target symbols, all finite and infinite conditionals lie in `[1/16,15/16]`, and the direct event-inverse calculation in `proof.md gives

```text
|q_r'|<=U1=9/8,
|q_r''|<=U2=37/8.                                     (3.2)
```

Let

```text
M2=256/15,
M3=57344/225,
M4=27656192/3375                                     (3.3)
```

be the exact suprema of the second through fourth derivatives of binary negative entropy on that interval. Put

```text
kappa1=d^(-1),
kappa2=2d^(-2),
e_r=C_*rho^(2r-6),

A0=M2/2,
A1=kappa1 M2+M3 U1/2,
A2=M2(kappa1^2+kappa2)+2kappa1 M3 U1
   +(M4 U1^2+M3 U2)/2.                                (3.4)
```

To justify (3.4), use the Bregman integral

```text
d(a||b)=(a-b)^2 integral_0^1(1-s)F''((1-s)b+sa)ds.
```

The derivative of the interpolated argument is the convex combination `(1-s)b'+sa'`, so its first and second derivatives are bounded by `U1,U2`; no unrecorded `Delta'` term is dropped.

For an `(r+1)`-site complete event, signed accretivity gives

```text
|S|<=2(r+1),
|S'|<=4(r+1),
|p''/p|<=4(r+1)^2+4(r+1).                             (3.5)
```

Two differentiations of (3.1) therefore yield

```text
|d_r''|
 <=[A2+4(r+1)A1+(4(r+1)^2+4(r+1))A0]e_r^2.           (3.6)
```

The right side is a quadratic polynomial in `r` times `(rho^4)^r`. The script evaluates its infinite sum from `r=18` by the exact identities for `sum q^r`, `sum r q^r`, and `sum r^2q^r`. Hence

```text
|h''(t_*)-h_18''(t_*)|<=Tail_18(t_*)                 (3.7)
```

with a rational right side.

## 4. Directed conclusion

For each of the three parameters, the script forms

```text
upper(h_18''(t_*))+Tail_18(t_*).                      (4.1)
```

It exits zero only if (4.1) is strictly below the corresponding rational threshold in (1.1). The recorded execution exited zero under CPython 3.13.5. No third-party package, random sampling, finite-window normalization, or unbounded numerical tolerance is used.

This proves (1.1). The continuum between the three points remains open because isolated negative curvatures and one midpoint Jensen gap do not exclude a positive-curvature interval between them.