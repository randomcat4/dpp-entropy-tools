# D10-S5 independent audit

Date: 2026-09-08. Non-author audit; no author module was imported or executed.

## Layered verdict

1. **CORRECT:** the specified rational K_* has a negative-definite exact-event
   entropy Hessian on the full six-dimensional real symmetric direction space.
   The certificate is not limited to commuting or PSD directions.
2. **CORRECT:** the open-neighborhood consequence follows uniformly over all
   directions from matrix continuity, not from a grid. No explicit radius has
   been proved or claimed by the author.
3. **CORRECT:** the reported D_* curvature and the rationalized scout direction's
   PSD property and normalized curvature independently recompute.
4. **SCOUT ONLY:** the finite numerical PSD search and proposed rank-one optimizer.
   The exact Frobenius-unit PSD optimizer is not certified. There is a concrete
   gradient-metric defect in the code: its update is **INCORRECT if described as
   the Frobenius projected-gradient ascent**. This does not invalidate the
   feasible scout samples, their correctly evaluated objective values, or the
   independently verified full-Hessian theorem.

## Frozen author version

The independent script records SHA256 before and after computation and requires
them to agree. This report applies only to these versions:

| File | SHA256 |
| --- | --- |
| frozen_problem.md | 1fe6a11acd311a0a665edfa85e30fab9007395584f745f46fdeaf85326febb0e |
| analysis.md | d4808dcb3acd74ae8ca3641ea2d33450baae3b2b8f59561804dbf43b03c27b3a |
| verdict.md | 9d4add17bde0a883f77d75a410c2ca4072ac3bbf4ff762df8141148e95f14e3e |
| run_log.md | 3be0796ccbe6a115a0f2f342605d1f42d11326a48e943f35a24f162afb67822b |
| full_psd_hessian.py | a76cbf601ac20a386fe50f1486da1570094bb2cd10c0ab405c1d463dacafe152 |
| hessian_scout.json | b2ce1b3d4ebf6cb8c4eecad86587cae04a84b32fe18e0aa0f198738c260fac7f |

No author-version drift occurred during the check. This is not a stamp on
unseen subsequent revisions.

## Independent atom and Hessian reconstruction

I reconstruct K_* from the rational orthogonal projectors U=J/3,
V=(1,2,-3)(1,2,-3)^T/14, W=I-U-V, with eigenvalues (1/5,7/10,71/100).
Projector orthogonality and trace one are checked exactly. The spectral distance
to {0,1} is 1/5, proving strict feasibility. The reconstructed matrix agrees
entrywise with the author matrix.

The independent calculation uses a six-variable polynomial ring, not the
author's univariate direction jets and polarization. Write a,b,c for the three
diagonal entries and u,v,w for the three symmetric off-diagonals. The full
inclusion determinant is built explicitly as

    abc + 2uvw - a w^2 - b v^2 - c u^2.

The three pair inclusion determinants are ab-u^2, ac-v^2, bc-w^2. Mobius
inversion of these eight inclusion polynomials produces all exact atoms as
multivariate polynomials. Their sum is exactly one, including all nonconstant
coefficients. In bitmask order 0,...,7 the base atoms are

    87/1250, 4159/35000, 4099/35000, 5631/35000,
    3999/35000, 2803/17500, 5591/35000, 497/5000.

Thus the minimum atom is exactly 87/1250. All rational coefficients, first
partials, and second partials are retained in `independent_results.json`.

The coordinate convention is x=(D11,D22,D33,D12,D13,D23). In an off-diagonal
basis direction BOTH matrix entries change by one; it is Eij+Eji, not half
that matrix and not divided by sqrt(2). For a monomial x_i^2 the second
partial is twice its coefficient; for x_i x_j with i!=j it is its coefficient.
Using these derivatives gives directly

    (-Hess H)_ij = sum_S (partial_i p_S)(partial_j p_S)/p_S
                   + sum_S (partial_ij p_S) log p_S.

This covers arbitrary real x and hence every symmetric D. The absence of a
factor two in a mixed partial and its presence in diagonal second partials
were independently implemented, rather than inherited from polarization.

## Independent exact logarithms and full-space certificate

The author uses range-reduced log intervals. The independent script instead
uses, directly for 0<p<1,

    log p = -2 sum_{k>=0} z^(2k+1)/(2k+1), z=(1-p)/(1+p).

With 128 terms the positive tail before negation is at most
2 z^257/[257(1-z^2)]. Therefore log p lies between minus partial minus tail
and minus partial. Every operation is Fraction arithmetic. Outward rounding
to rational multiples of 10^-28 reduces output size without losing inclusion.

The resulting exact rational Gershgorin row margins for -Hess H are:

| Coordinate | Certified lower margin |
| --- | ---: |
| 11 | 4.1067291326709275928204988417 |
| 22 | 4.095156481648653843673763 |
| 33 | 4.0760425599838582111009572353 |
| 12 | 1.9390872394796737691206907303 |
| 13 | 1.8005313724156545239976107628 |
| 23 | 1.7200075505038613350333965767 |

These finite decimals are exact rational lower bounds, not heuristic displayed
eigenvalues. In particular every row is strictly larger than 43/25=1.72.
Real symmetry and Gershgorin prove

    H''_{K_*}[D,D] <= -(43/25)||x(D)||_2^2
                    <= -(43/50)||D||_F^2 < 0, D!=0.

The norm conversion follows from ||D||_F^2 = sum diagonal^2 + 2 sum offdiagonal^2
<=2||x||_2^2. Its inequality direction is correct after multiplication by the
negative bound. The independent 90-digit Hessian differs from the author's
100-digit matrix by at most 2.2910981477e-89.

This establishes negative curvature also for noncommuting PSD examples such
as E11: K_* has nonzero first-row off-diagonals, so E11 does not commute with
it. More generally the matrix proof imposes no PSD, rank, commutation, or
spectral-basis condition on D. Every fixed D has a small feasible affine
interval because K_* is a strict contraction.

## D_* and rationalized scout point

The independently reconstructed D_* has projector eigenvalues (1/5,1/3,2/3),
so is positive definite and has Frobenius norm squared 134/225. Its curvature is

    -2.264361218158924839989580424355442546407060002577797282171348...

The exact rational logarithm interval is stored; the Decimal value agrees
with the author to more than 80 decimal places. This number is NOT normalized
to Frobenius unit norm; comparisons to unit PSD scout values must first divide
by 134/225.

The saved rationalized direction is symmetric. All seven nonempty principal
minors recompute strictly positive, so it is genuinely positive definite even
though its floating precursor was effectively rank one. Its per-Frobenius-norm
squared curvature independently equals

    -2.285108948085504855207731325829938649580764389068453907498998...

The rational matrix, all principal minors, and an independent curvature
interval are retained. Thus denominator-limited rationalization did not break
PSD for this saved point. This does not prove that rounding always preserves
PSD or that the resulting point is the optimizer.

## Scout defect and normalization boundary

At `full_psd_hessian.py:361-362`, the author computes g=2Ax and puts its
off-diagonal coordinates directly into a symmetric matrix G. But

    df(D)[E] = sum_diag g_ii E_ii + sum_off g_ij E_ij,
    <G,E>_F = sum_diag G_ii E_ii + 2 sum_off G_ij E_ij.

The Frobenius gradient therefore has G_ii=g_ii and G_ij=g_ij/2 for i<j.
The saved implementation omits this division, while its projection and
normalization use the Frobenius geometry. At D=I/3 the incorrect excess in
its three off-diagonal entries is approximately

    (-0.0130496816861, -0.0175765083619, -0.0200890968396),

so this is not a vacuous discrepancy. It should either be corrected or
described as a projected coordinate-preconditioned heuristic, without claims
of standard gradient-ascent or optimization guarantees. The update still
projects to feasible PSD matrices and its objective evaluation x^T A x is
correct; the full-Hessian certificate does not call this routine.

Likewise the author's ordinary eigenvalues of the 6-coordinate matrix use the
Euclidean x norm, not the Frobenius norm. They must not be compared as the same
constrained Rayleigh quotient to Frobenius-unit PSD values. No such comparison
is needed for Gershgorin or for the stated negative-definiteness theorem.

The source loops account for 4000 rank-one proposals and 400 projected starts
of 300 steps. I did not replay that random search, and do not certify its
claimed best as a global optimum or an exhaustive cone result. Its scope
remains SCOUT. Exact saved-point values and the full-space certificate, not
the finite search denominator, justify the mathematical conclusions above.

## Uniform local neighborhood

Each atom is a polynomial in the six coordinates, and every base atom is
strictly positive. There is a ball around K_* lying inside 0<K<I with all
atoms positive. On that ball the Hessian entries are continuous. The map into
6 by 6 matrices is consequently continuous in operator norm. Shrinking the
ball so that ||Hess H(K)-Hess H(K_*)||_op<43/50 gives a uniform coordinate
curvature bound at every point of that ball and simultaneously for every
direction. This supplies the unit-direction compactness/operator-norm step
that a merely pointwise continuity argument would omit. It does not assign
a numerical radius. The original existential neighborhood statement is valid.

Nothing here establishes global concavity outside that neighborhood or the
full feasible chord of any arbitrary direction.

## Commands, exact denominators, and independent evidence

Command from the repository root (local bundled Python 3.12):

```
python research/R3/deepening_10h/dense_hessian/n3_full_psd_local/verifications/independent_check.py
```

Exit 0; elapsed 0.04538369178771973 seconds; no failed assertions. The calculation
uses only the standard library and writes only this verification directory.
It retains 8 exact atoms, 48 first partials, 288 second partials, 36 rational
Hessian entry intervals, 6 exact row margins, and 2 direction-curvature checks.

Independent script SHA256:
`dee49be06dd5fd3c859376277ff3fcb01fbf8f644fdf67ab8b3273bd8b32ab2c`

Independent results SHA256:
`96c33e7860bdb10f203219a3912e3f3b024f2a4b51a1577947571710e9c406de`

The JSON contains complete rational denominators and the frozen author hashes.
No author's source or shared index was modified. No external theorem beyond
elementary differentiation, the log-series bound, Gershgorin and continuity is
needed for this local full-Hessian certificate.
