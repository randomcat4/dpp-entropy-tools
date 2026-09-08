# D10-M7 author verdict

GLOBAL: INCOMPLETE.

SUBCLASS: CORRECT_AFTER_INDEPENDENT_REVIEW. The independent checker rebuilt
the exact atoms and channel decomposition, verified the paired L1 constant,
classification and compactness quantifiers, and reproduced the rational
whole-interval certificate. No positive total-curvature candidate was found
or asserted. No random search was performed.

The main analytic outcome is Theorem E in `proved_subclass_or_blocker.md`:
for a strict real 3D DPP, if every singleton-conditional and pair-conditional
atom lies in [1/4,4/9], then every nonzero one-sign fixed-eigenvector spectral
direction has strictly negative total entropy curvature. This is a continuous
sufficient region, not a finite-point conclusion. Repeated eigenvalues and
exchangeability are not assumptions of this theorem.

The proof extracts the complement baseline 2 log(3) sum(v_i v_j), bounds the
paired acceleration L1 norm by 6 sum(v_i v_j), and uses the known count-entropy
concavity theorem plus explicit Fisher sums of squares. The resulting positive
coefficient is 2 log(81/64). On spectral margin epsilon the claimed uniform
barrier is 2 log(81/64) epsilon(1-epsilon) ||v||^2 / 9. A one-coordinate rate
is treated separately by strictly positive count Fisher information.

An explicit rational, connected, distinct-spectrum, unequal-diagonal kernel
and rank-three non-thinning direction satisfy the sufficient inequalities
throughout |t| <= 1/20. Twelve exact polynomial coefficient bounds certify the
whole interval, with spectral margin 19/100. Theorem E then gives the claimed
chord bound -134 log(81/64) h^2 / 22500. This is not extrapolation from sampled
chords. Complete rational matrices and coefficients are in `sanity_results.json`.

Auxiliary results are a uniform-layer strict barrier, a proved signed
exchangeable classification in the real 3D setting, and a uniform open
neighborhood in (Q,theta), including every normalized nonnegative rate.
Directions throughout mean commuting PSD/NSD directions; no result here
covers arbitrary noncommuting PSD directions.

The remaining global blocker is the residual outside the near-uniform
conditional region. Neither its sign nor domination by count/Fisher terms is
proved globally. Orthostochastic constraints have not been reduced to a finite
set of extreme cases. The already falsified global shortcut Psi'' <= 0 remains
falsified; it is only a valid consequence inside the new sufficient region.

Evidence scope: 35 deterministic rational cases, 280 exact events / 1120
polynomial coefficients checked against direct inclusion-Mobius inversion;
31 uniform-layer cases, 3 unrestricted identity-only cases, and one asymmetric
interval center. Twelve whole-interval inequalities and 3 actual negative
entropy chords passed. These checks are sanity evidence, not the proof of the
universal subclass statements. Zero failed assertions, exit code 0.

No novelty certification is claimed. The imported full count-entropy theorem
is Hillion--Johnson, Theorem 1.2, https://arxiv.org/pdf/1503.01570 . The fresh
audit and its standalone checker/output are frozen under `verifications/` and
pass the paired L1, count-score, quantifier and interval-certificate checks.
This does not alter the `GLOBAL: INCOMPLETE` verdict.
