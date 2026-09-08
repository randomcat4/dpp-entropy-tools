# D10-U10e verdict

STATUS: INCOMPLETE.

No negative value of the remaining scalar `sigma(x,a)` was found in the
reduced domain

```text
0 < x <= 1/2,     0 < a < x/sqrt(2).
```

The work unit did produce a cleaner reduced formulation:

```text
c = 2a^2/x^2,     0 < c < 1,
```

so the search domain is rectangular, the exact atoms are explicit positive
polynomials, and the unresolved condition is the single scalar

```text
sigma(x,c)>0.
```

Using the U10d/U8 input `C0>0` on the weighted-trace-zero subspace, this is
equivalent to `det B_even(x,c)>0` for the explicit four-dimensional
reflection-even Hessian.

## Evidence frozen

`search.py` ran a 120-digit Decimal profile over:

- `142` reduced `x` values;
- `181` reduced `c` values;
- `25,702` high-precision grid evaluations;
- `120,000` deterministic float scout proposals, seed `20260908`;
- four boundary regimes: `c->0`, `c->1`, `x->0`, and `x->1/2`.

No negative sigma occurred.  The best high-precision grid value was

```text
sigma = 4.00000000000000000000000000000000000000000000000083...
```

at `x=1/2`, `c=10^-12`, i.e. approaching the disconnected `a=0` boundary.
This supports, but does not prove, the stronger conjectural lower bound
`sigma>=4`.

## Boundary picture

- `c->0`: sigma tends to `1/[x(1-x)]`, so the smallest boundary limit in the
  reduced half-domain is `4` at `x=1/2`.
- `x->1/2`: covered by the U10d centered proof.
- `x->0` with fixed `c<1`: profile is consistent with `x sigma -> 1`, so no
  small-`x` negative mechanism was seen.
- `c->1`: the full atom `F=x^3(1-c)` vanishes.  Fixed-`x` profiles remain
  positive; for small `x`, the approach is two-scale and nonmonotone before
  eventual growth, making this the sharpest unresolved boundary.

## Current blocker

The next proof obligation is a genuine two-variable logarithmic inequality:

```text
det B_even(x,c)>0
```

or equivalently `sigma(x,c)>0`, after clearing the Schur inverse.  I did not
find a positive-term decomposition, log-integral domination, or rigorous
interval subdivision covering the whole rectangle.  Therefore the full
symmetric path family is not certified by this unit.

Finite search evidence remains SCOUT only.
