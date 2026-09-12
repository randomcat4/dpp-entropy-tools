# Finite DPP counterexample mechanism versus stationary Toeplitz slices

## 1. Executive verdict

- The three exact finite counterexamples are geometrically far from Hermitian Toeplitz structure: midpoint relative Frobenius distances are 0.732, 0.714, and 0.583.
- Their violating directions are farther still: relative distances are 0.970, 0.939, and 1.000; the n=6 direction has zero Toeplitz projection.
- Positive curvature survives small direction deformations but is killed after moving the midpoint only about 0.1%–0.5% of the way toward its Toeplitz projection.
- In the tested hard stationary chords, the intermediate spectrum is not purely `O(log n)`: fixed symmetric-difference regions put the midpoint symbol exactly at 1/2 on positive measure, and the first Szego theorem gives `N_n/n -> s` for that plateau measure `s`.
- A finite `a n+b log n+c` diagnostic has fitted `a` close to `s`; no logarithmic remainder theorem is claimed.
- Positive coherence/prediction correction remains large but below the negative spectral increment in every computed window.
- Four fixed increment sequences remain negative through n=24, and the closest-to-zero object remains negative through n=26.
- A 57,120-call fixed-seed stochastic Toeplitz search found no positive n=5 or n=6 Hessian; all four optimizers reached their iteration limits.
- The evidence supports the stationary concavity direction more than the counterexample direction, but it is finite and does not determine the entropy-rate Hessian.

## 2. Task 1: transition spectrum

Three frozen reflection-generated near-symmetric hard chords were used.  Their
midpoint is even and their direction odd.  The midpoint equals 1/2 on the
symmetric difference of the two endpoint sets; the exact interval lengths are
0.00290875 (m=2), 0.01519190 (m=3), and 0.02546367 (m=4). Therefore, for
epsilon<delta<1/2, the first Szego eigenvalue-distribution theorem rigorously
gives `N_n(delta)/n -> s`, where `s` is the displayed plateau measure. Nothing
below proves a sharper remainder.

For epsilon=0.002 and delta=0.05, least-squares fits over n>=64 give:

| family | half-level measure | log-only slope | log-only max residual | fitted a in `a n+b log n+c` | fitted b | two-scale max residual |
|---|---:|---:|---:|---:|---:|---:|
| m=2 | 0.002909 | 2.571 | 1.52 | 0.002650 | 1.200 | 0.97 |
| m=3 | 0.015192 | 9.087 | 7.31 | 0.013846 | 1.923 | 1.06 |
| m=4 | 0.025464 | 15.602 | 13.47 | 0.025077 | 2.626 | 2.34 |

The fitted linear coefficients differ from the exact half-level measures by
about 1.5%–8.9%. The finite two-scale diagnostic improves the residual for m=3
and m=4; its fitted `b` and constant are descriptive only. The m=2 sequence looks approximately logarithmic through n=1024 but
then rises from N=12 at n=1024 to N=16 at n=2048; the predicted linear mass is
already about six modes there.  This is a concrete counterexample to treating
all intermediate modes in these fixed hard chords as a pure Landau–Widom
boundary layer. The rigorous statement used here is only `N_n=s n+o(n)`.

Rows with delta=epsilon are retained but explicitly marked roundoff-sensitive
and excluded from all fits. At that inclusive threshold, last-bit eigenvalue
changes between NumPy 2.3.5 and 2.5.3 alter some counts. The main
epsilon=0.002, delta=0.05 comparison is separated from the floor and is stable.

At n=22, epsilon=0.002 and delta=0.05, the three families have N=5,8,9.  Their
coherence corrections are 0.0001353, 0.0045231, and 0.0062014, while the total
increment curvatures are respectively -4.16e-5, -4.86e-4, and -4.71e-4.
Correction per counted mode is not family-universal.  Over n=8..22, a linear
diagnostic against n has R-squared 0.973–0.999 for these small-epsilon cases,
whereas the same diagnostic against N_n(0.05) has R-squared 0.150–0.726.
The window is short and the predictors are correlated, so this does not prove
causation; it gives no support to the claim that N alone controls correction.

## 3. Task 2: distance to Toeplitz

| example | relative K distance | relative A distance | spectrum of K_Toep | original H'' |
|---|---:|---:|---|---:|
| canonical n=5 | 0.7317 | 0.9702 | [0.1451, 0.6508] | 0.005206 |
| larger-gap n=5 | 0.7136 | 0.9385 | [0.1116, 0.6943] | 2.914e-8 |
| larger-gap n=6 | 0.5833 | 1.0000 | [0.1187, 1.0360] | 0.525669 |

The diagonal-average construction passed direct Hermitian, Toeplitz, and
Frobenius-orthogonality checks.  The two n=5 projections remain positive
contractions; the n=6 projection violates K<=I, and no extra spectral clipping
was applied.

With the original direction fixed, H'' stays positive at s=0.001 and is
negative by s=0.002 for the canonical n=5 and n=6 examples.  For the optimized
n=5 example it is positive at s=0.002 and negative by s=0.005.  Thus the sign is
more sensitive than the large endpoint distance alone suggests.  At s=0,
moving only the direction toward its Toeplitz projection preserves the sign to
r=0.05 for the canonical example and r=0.1 for the optimized n=5 example.  In
the n=6 example A_Toep=0, so this path merely rescales the positive Hessian by
(1-r)^2 until r=1.

The selected bounded finite-symbol class adds only a modest distance beyond
the Toeplitz linear projection for n=5 (1.0346 to 1.0381 and 1.0068 to 1.0159),
but more for n=6 (1.0082 to 1.0877).  Every explicit candidate has a positive
whole-circle Lipschitz lower margin.  Its Hessian is negative with both the
original and projected directions whenever the latter is nonzero.

This separates the obstructions: Toeplitz linear geometry is already large;
positive contraction adds an obstruction for n=6; bounded-symbol realizability
adds a smaller n=5 penalty; and the entropy sign flips long before the Toeplitz
endpoint is reached.

## 4. Task 3: asymptotic finite-window sequence

| fixed object | largest n | H_n'' | Delta_n | H_n''/n |
|---|---:|---:|---:|---:|
| m=2, epsilon=0.2 | 26 | -1.7182e-5 | -8.2164e-7 | -6.6083e-7 |
| m=3, epsilon=0.01 | 24 | -0.0048362 | -4.0943e-4 | -2.0151e-4 |
| m=4, epsilon=0.01 | 24 | -0.0039545 | -3.9957e-4 | -1.6477e-4 |
| m=4, epsilon=0.002 | 24 | -0.0047678 | -4.9474e-4 | -1.9866e-4 |

The m=2 increment is nearly flat and negative.  The substantive m=3/m=4
increments become more negative over the available windows and show no
sustained drift toward zero.  The complete recursion visited 67,108,863 nodes
for n=26 in 124.47 seconds.  Because each two-site extension multiplies cost by
four, the run stopped under the frozen complexity and stable-negative-trend
rules.  No iid-style confidence interval is attached to these deterministic
sequences.

## 5. Task 4: low-dimensional Toeplitz search

All base symbols obey a global Fourier-amplitude legality condition and an
independent 65,536-point Lipschitz remainder check. Directions are normalized
by `||T_n(g)||_F=1`. The search parameter requires pre-contraction rho>=25%;
because decoding multiplies by 0.98, the actual nonconstant Fourier-amplitude
floor is 24.5% of the available legality radius, excluding the known flat
independent layer.

| n | class | parameters | evaluations | maximum H'' | minimum whole-circle slack | local chord radius | optimizer |
|---:|---|---:|---:|---:|---:|---:|---|
| 5 | even f / odd g | 10 | 8,562 | -1.193e-8 | 0.0717 | 0.1045 | maxiter reached |
| 5 | general complex Toeplitz | 19 | 16,986 | -2.129e-7 | 0.0658 | 0.0627 | maxiter reached |
| 6 | even f / odd g | 12 | 10,274 | -5.848e-7 | 0.0690 | 0.1053 | maxiter reached |
| 6 | general complex Toeplitz | 23 | 21,298 | -4.147e-7 | 0.0694 | 0.0905 | maxiter reached |

All four SciPy optimizers report `success=False` because `maxiter=60` was
reached. The 57,120 calls are therefore only a fixed-seed stochastic objective
evaluation denominator; they are not exhaustive, converged, or globally
optimal. The parity cases have maximum complete-event first jet exactly zero
in the stored double calculation. No positive candidate occurred, so
high-precision and directed-interval promotion was not triggered. `NO_HIT`
describes this recorded search denominator only.

## 6. What is actually new

Existing repository work supplied the exact finite counterexamples, the parity
first-jet identity, the stationary candidate families, the n<=22 baseline, and
the conditional-DPP recursion.  This run newly supplies spectra through n=2048,
the linear-plus-log diagnosis, the Toeplitz-distance landscapes, explicit
bounded-symbol approximants, selected n=24/26 continuations, and the 57,120-call
fixed-seed intrinsic Toeplitz search.

The rigorous spectral conclusion is the leading positive-density law
`N_n/n -> s`. The data separately suggest, without proving, a logarithmic jump
boundary remainder and strong sensitivity of finite counterexample curvature
to Toeplitzizing the midpoint. There is no new theorem or counterexample.

## 7. Next mathematical step

1. Freeze a family in which the midpoint has no positive-measure 1/2 plateau,
   or subtract the `n * measure{f in [delta,1-delta]}` Szego term before testing
   the residual Landau–Widom count.  This isolates the actual O(log n) boundary
   modes.
2. Derive a polynomial-time representation or rigorous bound for the
   coherence-increment Hessian.  The current complete-prefix recursion cannot
   distinguish n=30 behavior economically.
3. Analyze the first derivative of H'' along midpoint Toeplitzization at the
   three exact examples.  The observed sign flip by s=0.002–0.005 is much more
   informative than the endpoint distance and may identify the specific
   non-Toeplitz tensor component carrying the violation.
