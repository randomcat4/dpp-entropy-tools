# D10-U10e derivation and blocker

Status: INCOMPLETE.  No negative value of the remaining scalar was found, but
the global inequality is not proved in this unit.

## 1. Reduced variables

For

```text
K(x,a) = [[x,a,0],
          [a,x,a],
          [0,a,x]]
```

sign conjugacy and complementation reduce the domain to

```text
0 < x <= 1/2,       0 < a < x/sqrt(2).
```

I use

```text
c = 2a^2/x^2,       0 < c < 1,
```

so `a=x sqrt(c/2)`.  The six distinct exact atoms become

```text
E = (1-x)((1-x)^2-cx^2)
F = x^3(1-c)
U = x(1-x)^2 + (1-2x)cx^2/2
W = x(1-x)^2 + (1-x)cx^2
V = x^2(1-x) - (1-2x)cx^2/2
Z = x^2(1-x) + cx^3
```

in event order `(E,U,W,V,U,Z,V,F)`.  This is the first useful
simplification: the strict domain is the rectangle
`0<x<=1/2, 0<c<1`, and every atom above is manifestly positive there except
for the expected open-boundary vanishings.

## 2. Rebuilt even-block scalar

For an even direction

```text
D = [[d,h,k],
     [h,e,h],
     [k,h,d]],
```

define the six derivative linear forms

```text
jF = 2(x^2-a^2)d + x^2 e - 4xa h + 2a^2 k
jQ = x(d+e)-2ah
jE = (4x-2)d + (2x-1)e - 4ah - jF
jU = (1-3x)d - xe + 2ah + jF
jW = -2xd + (1-2x)e + 4ah + jF
jV = jQ-jF
jZ = 2xd-jF.
```

Then the Fisher part is

```text
F_even = jE^2/E + 2jU^2/U + jW^2/W + 2jV^2/V + jZ^2/Z + jF^2/F.
```

With

```text
ell    = log(EV/UW)
kappa  = log(EZ/U^2)
Lambda = log(FU^2W/EV^2Z)
n      = -ell - x Lambda
m      = -kappa - x Lambda
```

the full even-block negative entropy Hessian is

```text
B_even =
  F_even - 4 n d e + 4 n h^2 - 2 m d^2 + 2 m k^2
         - 8 Lambda a h(d-k).
```

This expression was independently checked from exact-event jets in
`search.py`; no author sanity code is imported.

## 3. The one remaining scalar

Let

```text
q = nm - 2 Lambda^2 a^2
eta = (
  2(nm-Lambda^2 a^2)/(nq),
  n/q,
  4 Lambda a/q,
  2 Lambda^2 a^2/(nq)
).
```

This is `tr(N^{-1}D)` in the even coordinates `(d,e,h,k)`.  U10d, using the
reviewed weighted-trace-zero input from U8, reduces the problem to the
Schur complement in a transverse coordinate.  With columns

```text
t_d = (1,-eta_d/eta_e,0,0)
t_h = (0,-eta_h/eta_e,1,0)
t_k = (0,-eta_k/eta_e,0,1)
```

write

```text
C0 = T0^T B_even T0,
b0 = T0^T B_even e0,
d0 = e0^T B_even e0,       e0=(0,1,0,0).
```

The remaining scalar is

```text
sigma(x,c) = d0 - b0^T C0^{-1} b0.
```

Since `[T0,e0]` is an invertible basis change and `C0>0` is the imported
weighted-trace-zero theorem, the minimal unresolved inequality can be stated
equivalently as

```text
sigma(x,c)>0
```

or

```text
det B_even(x,c)>0
```

on `0<x<=1/2, 0<c<1`.  The second form may be a better target because it
removes the explicit inverse in `sigma`; however it is still a two-variable
logarithmic inequality.

## 4. Boundary information

The high-precision profile suggests the following boundary picture.

### `a -> 0` / `c -> 0`

For fixed `x`, the scalar tends to the diagonal Bernoulli curvature

```text
sigma(x,c) -> 1/[x(1-x)].
```

The profile shows the first visible correction is nonnegative in all sampled
points, with the global infimum approached at `x=1/2, c=0+`, where the limit
is `4`.  This limit lies on the excluded disconnected boundary, where the
weighted-trace decomposition is singular; it is evidence for the conjectural
bound `sigma>=4`, not a proof.

### `x -> 1/2`

At `x=1/2`, U10d gives a reviewed full proof for every `0<c<1`.  The present
calculation is continuous into that line away from `c=0,1`, and the best
finite values occur close to `x=1/2,c=0`.

### `x -> 0`

For fixed `c<1`, the profile is consistent with

```text
x sigma(x,c) -> 1.
```

This gives a positive escape to infinity as `x -> 0` when `c` stays bounded
away from the spectral boundary.  The convergence is not uniform as
`c -> 1`.

### `c -> 1` / spectral boundary

For fixed `x>0`, the full atom `F=x^3(1-c)` is the vanishing atom.  The
profile remains positive and usually grows for sufficiently tiny `1-c`, but
for small `x` it can decrease over a long pre-asymptotic range before turning
up.  This two-scale corner `(x,c)->(0,1)` is the main place where a proof by
naive monotonicity fails.

## 5. What did not close

I did not obtain a clean positive-term decomposition of `det B_even` or of
`sigma`.  The strongest remaining blocker is therefore:

> Prove the explicit scalar inequality `sigma(x,c)>0` on
> `0<x<=1/2, 0<c<1`, equivalently `det B_even(x,c)>0` given `C0>0`.

The finite profile gives no counterexample and points to the stronger
possible inequality `sigma(x,c)>=4`, with equality only as
`(x,c)->(1/2,0)`, but this stronger statement is only a conjectural guide.
