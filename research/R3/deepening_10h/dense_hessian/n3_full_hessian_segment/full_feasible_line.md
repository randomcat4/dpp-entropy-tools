# D10-S8e stitched full-feasible-line corollary

STATUS: `CORRECT`. A fresh non-author dependency audit is preserved under
`full_line_verifications/`.

Consider the frozen M8 line

```text
K(t)=(1/5+t/5)U + (1/2+t/3)V + (4/5+2t/3)W,
```

where `U,V,W` are the frozen mutually orthogonal rank-one projections. Its
three eigenvalues show that the exact strict feasible interval is

```text
-1 < t < 3/10.
```

Three independently reviewed interval certificates now partition and cover
that entire interval:

- S8d: `-1 < t <= -29/100`;
- S8b: `-29/100 <= t <= 29/100`;
- S8c: `29/100 <= t < 3/10`.

Each certificate concerns the complete six-dimensional observation-coordinate
Hessian on `Sym(3)`, not merely the line tangent, commuting directions, or the
PSD cone. Their overlaps include both stitching points. Therefore

```text
Hess H(K(t)) is strictly negative definite on Sym(3)
for every strictly feasible t in (-1,3/10).
```

This is an exact statement about one nontrivial maximal feasible affine line.
It is not a theorem on the whole three-dimensional DPP kernel domain. By
openness of strict negative definiteness, every point of the line has an
ordinary ambient negative-Hessian neighborhood. No single uniform ambient
radius is claimed over the noncompact open interval, especially as either
spectral endpoint is approached.
