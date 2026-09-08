# D10-B4 verdict

AUTHOR STATUS: REVISED_SUBCLASS_PROVED_AND_GLOBAL_OPEN, pending independent
re-verification after first audit.

## Strongest result

This work unit proves a non-degenerate continuous strict-negative-curvature
subfamily of the fixed-beta path-affine construction.

For fixed \(n\), a compact box \(0<a\le\tau_i\le b<1\), and a nonempty diagonal
heterogeneity margin

\[
0<\eta<1/a-1/b,\qquad
\left|\tau_1^{-1}-\tau_n^{-1}\right|\ge\eta,
\]

there is an \(\varepsilon(n,a,b,\eta)>0\) such that every sign chamber

\[
0<|\beta_i|<\varepsilon
\]

is strict feasible, connected as a tridiagonal path, heterogeneous, and has

\[
\frac{d^2}{dt^2}H(K_\beta(\tau+t\delta))\bigg|_{t=0}<0
\]

for every nonzero \(\delta\).  Because \(\tau\mapsto K_\beta(\tau)\) is affine,
this is a genuine \(K\)-space local chord statement.

The word connected here means every individual \(L\)-matrix has a connected
path graph.  The parameter set itself generally splits by the \(\beta\) sign
chamber and by the two \(\tau\)-branches
\(\tau_1^{-1}-\tau_n^{-1}\ge\eta\) and
\(\tau_1^{-1}-\tau_n^{-1}\le-\eta\).

The diagonal base bound is now stated non-strictly:

\[
H_0''(\tau)[\delta,\delta]\le -4\|\delta\|_2^2,
\]

with equality exactly when every nonzero \(\delta_i\) lies at
\(\tau_i=1/2\).  The curvature remains strictly negative for every nonzero
\(\delta\).

## Structural reduction

The exact-event entropy can be represented through a one-dimensional
selected-run recurrence.  Equivalently, with
\(\ell_S=\log\det L_S\), \(A_S=\ell_S'\), and \(B_S=\ell_S''\),

\[
H''
=-\operatorname{Var}(A)
-\operatorname{Cov}(\ell,B)
-\mathbb E\left[(\ell-\mathbb E\ell)(A-\mathbb EA)^2\right].
\]

The first term is always non-positive.  Any global positive curvature would
have to come from the last two sign-indefinite terms overwhelming
\(\operatorname{Var}(A)\).  This is the current analytic blocker.

## Evidence

The deterministic sanity script checks the \(\beta=0\) product-Bernoulli
Hessian against the corrected O(n²) jet interface and then checks a few fixed
small nonzero couplings.  These examples are only sanity checks for the proof's
limiting mechanism, not evidence for a global theorem.

Recorded output:

- `results/weak_coupling_sanity.json`
- status: `PASS`
- beta=0 formula vs jet: \(n=3,5,8,12\), max absolute error
  `3.9968028886505635e-14`
- small nonzero beta checks: \(n=3,5,8,12\), eps in
  `{1e-4, 1e-3, 1e-2}`, all \(H''<0\)
- denominator: 4 diagonal checks and 12 small-coupling deterministic checks
- role of evidence: implementation sanity only; the theorem uses compactness
  and continuity, not finite search

## Not claimed

- No global concavity theorem for the full fixed-beta family.
- No positive R3 counterexample candidate.
- No use of the n≤100 finite miss as a theorem.
- No reproof of Gu's rank-one concavity prior art; rank-one directions remain
  prior-art blocked.
- No claim that the full parameter domain is topologically connected.

## Status

`REVISED_SUBCLASS_PROVED_AND_GLOBAL_OPEN`
