# Issue74 PR91 Hessian point-obstruction unit

Final status: `STOPPED_MATHEMATICAL_IMPLEMENTATION_MISMATCH`.

The raw attempt-3 obstruction output is invalidated by `INVALIDATION.md` and
must not be used as mathematical evidence.  No curvature sign or trial-scheme
obstruction was certified.

This unit tests the frozen PR98 degree-10 trial against the accepted-scoped
PR91 Hessian-only residual gate.  It does not estimate or assert the sign of
the physical entropy-rate curvature.

The decisive logic is one-sided.  Any valid whole-domain bounds obey

```text
e02 >= ||D_Q^2 r0(Q,t)||op,
e12 >= ||D_Q^2 r1(Q,t)||op,
e20 >= |r2(Q,t)|
```

at every legal point.  For a Frobenius-unit coordinate direction, the absolute
second directional derivative is a rigorous lower bound on the Hessian
operator norm.  Hence a positive value of

```text
c2/2 + lower(e02)/2 + 9 lower(e12)/100 + lower(e20)/2
```

at `Q=0` and either endpoint proves that this frozen trial cannot satisfy the
strict negative gate on any gap-free cover of `[1/2,3/2]`.

All algebraic calculations use exact rational arithmetic.  The four required
logarithms use Python's correctly rounded `Decimal.ln` at 96 decimal digits,
then widen by an explicit rational pad that dominates the three rounding
steps in `ln(numerator)-ln(denominator)`.  This exceeds 256-bit precision.
There is no sampling or finite differencing.

Frozen sources:

- PR91: `c7a072ec4eea0c5b0f445bca5796873a9e234948`.
- PR98: `55649309437a78d9e5174386d8d260a4ee9c02a1`.
- Input paths: PR98 `degree10/meta.json`, `degree10/u.json`,
  `degree10/v.json`, and `degree10/w.json`.

The public issue claim and absolute deadline are recorded in issue #74.  The
exact executable commit, PID, command, and literal input bindings must be
posted there before this program is launched.
