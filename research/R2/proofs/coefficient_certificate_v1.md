# General coefficient certificate for finite probability families

This note isolates the part of the argument that is not specific to DPPs.

Let `Omega` be finite and let

```text
p_i^-(epsilon), p_i^0(epsilon), p_i^+(epsilon),  i in Omega,
```

be probability vectors.  Put

```text
Delta(epsilon)
  = (H(p^+(epsilon))+H(p^-(epsilon)))/2 - H(p^0(epsilon)),
H(p) = -sum_i p_i log p_i.
```

Assume that every coordinate has a finite asymptotic expansion in powers of
`epsilon` up to the first order needed below, with a remainder bounded by a
higher power times at most `log(1/epsilon)`.  This holds automatically for
the DPP paths used in the transverse theorem because each exact event
probability is a finite polynomial in the entries of `K`, and the path has a
Puiseux expansion in `sqrt(epsilon)`.

## Single-coordinate expansion

If

```text
p(epsilon) = c epsilon^alpha + R(epsilon),
c > 0, alpha > 0,
|R(epsilon)| <= C epsilon^(alpha+rho)
```

for some `rho>0`, then

```text
-p log p
  = alpha c epsilon^alpha log(1/epsilon)
    - c epsilon^alpha log c
    + O(epsilon^(alpha+rho) log(1/epsilon)).
```

If `0 <= p(epsilon) <= C epsilon^beta`, then

```text
0 <= -p log p <= C_beta epsilon^beta log(1/epsilon).
```

If a finite family satisfies `0 <= p_i(epsilon) <= C epsilon^alpha` and

```text
sum_i p_i(epsilon) = A epsilon^alpha + O(epsilon^(alpha+rho)),
```

then

```text
sum_i -p_i log p_i
  = alpha A epsilon^alpha log(1/epsilon) + O(epsilon^alpha).
```

The last form is useful when only the total mass of a rare cardinality class
is needed.

## Sign rule

At a fixed exponent `alpha`, write `c_i^sigma(alpha)` for the coefficient of
`epsilon^alpha` in branch `sigma`, with value `0` if that coordinate has no
term at this exponent after all smaller exponents have already been accounted
for.  The logarithmic contribution to the chord gap at that exponent is

```text
L_alpha =
  alpha sum_i ((c_i^+(alpha)+c_i^-(alpha))/2 - c_i^0(alpha)).
```

If `alpha` is the smallest exponent at which any unmatched entropy term
appears and `L_alpha != 0`, then the sign of `Delta(epsilon)` for all
sufficiently small `epsilon` is the sign of `L_alpha`, since
`epsilon^alpha log(1/epsilon)` dominates finite `epsilon^alpha` terms and all
higher powers.

If `L_alpha=0`, the finite coefficient at that same exponent is

```text
C_alpha =
  sum_i c_i^0(alpha) log c_i^0(alpha)
  - (1/2) sum_i [c_i^+(alpha) log c_i^+(alpha)
                 + c_i^-(alpha) log c_i^-(alpha)],
```

with `0 log 0=0`, plus any analytic active-coordinate contribution of the same
power.  Then `C_alpha` decides the sign only if all smaller powers and
logarithmic terms vanish.

In particular, if

```text
c_i^0(alpha) = (c_i^+(alpha)+c_i^-(alpha))/2
```

coordinatewise for all rare coordinates at the first scale, then the rare
finite coefficient is non-positive by convexity of `x log x`.  A positive
leading singular contribution needs the endpoint average rare mass to exceed
the midpoint rare mass at the first unmatched scale.

## Derivative warning

For a fixed positive `epsilon`, the map `t -> H(p(t,epsilon))` is smooth as
long as all coordinates remain positive.  Its Taylor coefficients need not be
uniform as `epsilon -> 0`.  If a coordinate has

```text
p(0,epsilon) = a epsilon^d + o(epsilon^d),
p(t,epsilon) = p(0,epsilon) + b t^2 + higher terms,
```

then the fixed-`epsilon` Hessian sees `log p(0,epsilon) ~ -d log(1/epsilon)`.
But a finite chord with `t_epsilon^2 ~ epsilon` and `d>1` changes the
coordinate to scale `epsilon`, so the entropy contribution has only one power
of `log(1/epsilon)`.  Thus the limits `t -> 0` and `epsilon -> 0` cannot be
interchanged without a uniform smallness condition such as
`t_epsilon^2 = o(epsilon^d)` for that coordinate.

