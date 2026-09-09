# RESULT — fixed two-harmonic true-rate unit

Date: 2026-09-10.

Base: `main@9dcb6e9079ca57f94e0e30d63161cda89ca61fae`.

## PROVED (AUTHOR PROOF), NOT INDEPENDENTLY REVIEWED

Let

```text
f_t(theta)=1/2+(1/4)cos(4*pi*theta)+(t/8)cos(2*pi*theta).
```

### Strict legality

For every `|t|<=3/2`,

```text
119/512<=f_t(theta)<=15/16,
min{f_t(theta),1-f_t(theta)}>=1/16.
```

Thus the whole frozen parameter interval consists of strict scalar Toeplitz DPPs.

### Fixed true entropy-rate Jensen gap

For complete-configuration Shannon entropy rate per original lattice coordinate,

```text
h(f_1)-[h(f_{1/2})+h(f_{3/2})]/2 > 1/10000.
```

The three symbols are fixed and do not depend on a window or approximation depth. The proof uses depth-18 complete-event conditional entropies with exact integer determinants, directed logarithm enclosures, and the analytic uniform error

```text
0<=H(X_0|X_1,...,X_r)-h(f_t)
 <=(256/15)(1033420800/1263214441)^2(49/64)^(4r-12).
```

This is a true-rate result in the concave direction. It is not a finite-sample extrapolation and not a counterexample.

### Exact response and certification interfaces

The manuscript independently derives the full normalized RPF response

```text
h''=-nu(psi^2)+nu((psi^2-xi)v)-2nu(psi R(psi v)),
v=R log G,
```

retaining conditional Fisher information, acceleration, and invariant-measure response. It also proves a summable closed bound for the difference between finite-memory conditional curvature and the true entropy-rate curvature.

## INCOMPLETE

This work does not yet prove

```text
h''(t)<0 for every 1/2<=|t|<=3/2,
```

nor does it produce a positive true-rate Jensen counterexample. A single strict midpoint gap does not imply curvature on every subinterval.

Heavy outward-rounded continuum certification is frozen in issue #74. No result from that issue is assumed by the author proof.

## Review boundary

At the start of this unit PR59 had no substantive nonauthor review comment. No statement here inherits acceptance from PR59. The exact complete-event/RPF formulas needed here are rederived in `proof.md`. `verification.md` is an author audit contract only. Novelty and priority are unassessed.