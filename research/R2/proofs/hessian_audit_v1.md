# Hessian audit: fixed center versus finite near-boundary chord

Status: PROVED as a boundary-use warning.

This audit is independent of the public author proof and is meant to prevent
misusing the interior Hessian at a center whose probabilities approach zero.

## 1. Interior event-jet identity

For fixed `epsilon>0`, `M_epsilon` is a strict contraction.  Therefore all
exact event probabilities are positive in a small interval
`M_epsilon+tD_gen`, and

```text
H_epsilon''(0)
  = - sum_S (p_S'(0))^2 / p_S(0)
    - sum_S p_S''(0) log p_S(0),                                  (1)
```

where `p_S(t)=p_{M_epsilon+tD_gen}(S)`.  The missing `-sum_S p_S''(0)` term is
zero because `sum_S p_S(t)=1`.

If some rare coordinate satisfies

```text
p_S(0) = c_S epsilon + O(epsilon^2),
p_S'(0) = a_S + O(epsilon),
```

then the first term in (1) contributes

```text
- a_S^2 / (c_S epsilon) + O(1).
```

This is the possible negative `1/epsilon` divergence.  It occurs for
longitudinal directions that change the large holes or small particles
linearly.  In the diagonal spectral toy case,

```text
h(1-epsilon+t a)'' at t=0 = -a^2/(epsilon(1-epsilon)),
h(epsilon+t c)'' at t=0   = -c^2/(epsilon(1-epsilon)).
```

Thus a general near-projection Hessian may have the form

```text
H_epsilon''(0)
  = - C_{-1}/epsilon + C_log log(1/epsilon) + O(1),
```

with `C_{-1} >= 0` in the event-jet sense.

## 2. Pure transverse frozen direction

For the frozen direction

```text
D = U B V^T + V B^T U^T,
```

there is no longitudinal compression on either `P` or `Q`.  Consequently the
order-`epsilon` size `r-1` and size `r+1` masses have zero first derivative in
`t` at `t=0`; the `1/epsilon` term vanishes for this pure transverse family.

The transverse direction changes the large holes and small particles
quadratically:

```text
sum_large (1-lambda_j(t))
  = r epsilon - t^2 ||B||_F^2 + O(epsilon^2 + epsilon t^2 + t^4),
sum_small lambda_j(t)
  = s epsilon - t^2 ||B||_F^2 + O(epsilon^2 + epsilon t^2 + t^4).
```

The two cardinality-leakage classes therefore contribute

```text
-4 ||B||_F^2 log(1/epsilon) + O(1)
```

to `H_epsilon''(0)`.

Now let `S` be an `r`-subset with `psi_S=0` and `phi_S != 0`.  At the midpoint,
the all-top Plucker coordinate vanishes.  The first nonzero midpoint event
mass comes from one top/bottom spectral swap, hence

```text
p_S(0) = rho_S epsilon^2 + O(epsilon^3),   rho_S > 0.
```

Along the transverse direction,

```text
p_S(t) = p_S(0) + t^2 phi_S^2 + higher terms in t and epsilon,
```

so `p_S'(0)=0` and `p_S''(0)=2 phi_S^2+O(epsilon)`.  The second term in (1)
then gives

```text
-p_S''(0) log p_S(0)
  = 4 phi_S^2 log(1/epsilon) + O(1).
```

Summing over zero Plucker coordinates gives the pure transverse fixed-center
Hessian asymptotic

```text
H_epsilon''(0)
  = 4 (Z - ||B||_F^2) log(1/epsilon) + O(1).                       (2)
```

This formula is only a fixed-`epsilon`, infinitesimal-`t` statement.

## 3. Why Taylor and `t_epsilon ~ sqrt(epsilon)` do not commute

For a zero Plucker coordinate, the midpoint baseline is order `epsilon^2`,
but the finite frozen chord has

```text
t_epsilon^2 = tau^2 epsilon(1-epsilon) ~ tau^2 epsilon.
```

Thus the endpoint probability is raised from scale `epsilon^2` to scale
`epsilon`:

```text
p_S(t_epsilon)
  = tau^2 phi_S^2 epsilon + O(epsilon^(3/2)).
```

The finite-chord entropy contribution is therefore

```text
tau^2 phi_S^2 epsilon log(1/epsilon) + O(epsilon),
```

not

```text
(t_epsilon^2/2) * 4 phi_S^2 log(1/epsilon)
  = 2 tau^2 phi_S^2 epsilon log(1/epsilon).
```

The factor-of-two mismatch is not an error in either calculation.  It records
the non-uniformity of Taylor expansion near a vanishing probability.  The
Taylor approximation around `t=0` requires `t^2=o(epsilon^2)` for these
coordinates, while the frozen chord has `t_epsilon^2` of order `epsilon`.

For the size `r-1` and `r+1` classes, whose midpoint baseline is already order
`epsilon`, the logarithmic part of the Hessian does match the finite-chord
logarithmic coefficient.  The non-commutation is specifically forced by the
Plucker-zero `r`-events.

Combining this with the direct finite-chord proof gives

```text
finite chord coefficient:        Z - 2 ||B||_F^2,
fixed-center Hessian log half:   2Z - 2 ||B||_F^2.
```

The latter must not be used to decide the former.

## 4. Consequence for positive-gap searches

For a general varying family, a positive `Delta` can only be certified by the
first unmatched coefficient in the actual finite-chord probability scales.
Interior Hessian signs at centers `M_epsilon` are not enough unless the
Taylor remainder is uniform at the chosen chord width.

In the frozen pure transverse family, the actual first unmatched coefficient
is

```text
tau^2 (Z - 2 ||B||_F^2),
```

which is strictly negative when `tau B != 0`.

