# D10-U10i boundary_exponential_limit fresh audit

STATUS: SCOPED_CORRECT_GLOBAL_INCOMPLETE

The scoped exponential-boundary result checks out: the closed limiting
function, its positivity and unique minimizer, and the compact-beta
exponential wedge conclusion are correct within the stated dependencies.
The full two-parameter path domain remains INCOMPLETE.

## Closed limit

With `l=log 2`, the claimed formula

```text
phi(beta) = (beta+l+2)(beta+l)^4 / (2 beta^2 l^2), beta>0
```

is correct for the frozen normalization `eta(z)=eta_e`.

The positivity proof is elementary and sound: all factors are positive, and
`(beta+l)^2 >= 4 beta l` gives

```text
phi(beta) >= 8(beta+l+2) > 8(l+2) > 0.
```

The log-derivative has the sign of

```text
3 beta^2 + (l+4) beta - 2l(l+2).
```

This quadratic is strictly increasing on `beta>0`, negative at zero, and
positive at infinity; hence there is exactly one positive critical point,
the global minimizer:

```text
beta_star = 0.58027763529240563357583603000459967717...
phi_min   = 26.603760120630927814166018565902794785...
```

The script verifies the stationary polynomial at `beta_star` to zero at
180-digit precision.

## Stable constrained-energy interpretation

The positive-matrix Sherman--Morrison formula is consistent with the
constrained variational statement:

```text
sigma = min_{eta(z)=eta_e} B(z,z).
```

The full-atom term is handled as a positive rank-one penalty, not by
subtracting two singular Schur complements.  In the independent samples, the
trial direction satisfies both constraints,

```text
eta(trial)-eta_e = 0,     w_s dot trial = 0,
```

to high precision, and its energy is never below the computed constrained
minimum.

The limiting trial/minimizer is

```text
h0 = -(beta+l)^2/(2 sqrt(2) beta l),
k0 = 2 sqrt(2) h0.
```

The audit samples show `z_min -> z0` at the asserted `sqrt(x)` scale.

## Uniform remainder and wedge scope

The proof of

```text
sigma(x, exp(-beta/x)) = phi(beta) + O_J(sqrt x)
```

is valid for every fixed compact interval `J=[b0,b1]` contained in
`(0,infinity)`.

The key quantifiers are correctly limited:

- `s=exp(-beta/x)` is uniformly smaller than every power of `x` only because
  `beta>=b0>0`.
- `N` stays uniformly positive definite only because `beta` remains in a
  compact subset of `(0,infinity)`.
- U8 coercivity gives bounded true minimizers on that fixed compact `J`.
- Singleton Fisher terms force `d,e=O_J(sqrt x)`.
- The full-atom penalty forces `w_s dot z=O_J(sqrt(s/x))`.
- The remaining two-by-two constraint for `(h,k)` has a uniformly nonzero
  limiting determinant on `J`.

Therefore each compact beta interval has a genuine continuous exponential
wedge with full `Sym(3)` negative-Hessian strictness for sufficiently small
`x`.  The constants may deteriorate with the endpoints of `J`.

This does not cover noncompact regimes such as `beta=beta(x)->0` or
`beta=beta(x)->infinity`, and it does not prove the full path domain.

## Old finite minimum versus limiting minimum

The old finite profile value is correctly distinguished from the limit:

```text
beta = 0.58, x = 1e-4:
sigma ≈ 26.58112587076539

phi(0.58) ≈ 26.60376358740434
phi(beta_star) ≈ 26.60376012063093
```

At `beta=0.58, x=1e-6`, the independent recomputation gives

```text
sigma ≈ 26.60353703684734,
```

which is much closer to `phi(0.58)`.  Thus `26.581...` is finite-`x` scout
behavior, while `26.603760...` is the closed limiting minimum.

## Remaining limitations

- This audit did not reprove the earlier path reduction or U8 identity; it
  checks U10i under those already reviewed dependencies.
- The author sanity denominator `3` rational Möbius gates + `28` exponential
  points remains finite SCOUT.
- The compact-beta wedge is not a noncompact beta theorem.
- The full symmetric path domain remains unresolved.

No critical gap was found in the scoped U10i exponential-limit proof.
