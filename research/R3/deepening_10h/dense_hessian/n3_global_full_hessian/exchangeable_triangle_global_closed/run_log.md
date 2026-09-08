# D10-U10k replay log

Date: 2026-09-09.

The standard-library replay was run from the repository root with the bundled
Python 3.12 runtime:

```text
python research/R3/deepening_10h/dense_hessian/n3_global_full_hessian/
  exchangeable_triangle_global_closed/sanity.py
```

Result: `PASS_SCOUT_NOT_PROOF`.

Seven frozen rational pairs were checked, including both parameter orders,
four strongly asymmetric edge/corner points, and the near-diagonal pair

```text
alpha=500001/1000000, beta=499999/1000000.
```

At every point, direct differentiation of the four event layers agreed with
the quartic-over-positive-denominator formula.  With 100 decimal digits, the
largest displayed identity error was below `3e-96`; all five evaluated
coefficients and `Delta_T` were positive.  The near-diagonal determinant was
approximately `1.7066666666841e-10`, confirming that the replay resolves the
quadratic opening rather than rounding it to zero.

This finite replay is supplementary.  The universal result rests on the
coefficient proof and the two independent exact reconstructions recorded in
`verifications/fresh_audit.md`.
