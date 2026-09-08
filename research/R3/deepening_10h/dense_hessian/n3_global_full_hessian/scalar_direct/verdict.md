# U10a verdict

GENERAL CONJECTURE: **INCOMPLETE**.

NEW ANALYTIC RESULTS: **CORRECT_SCOPED_AFTER_INDEPENDENT_REVIEW**.

The main advance is an explicit eight-event projection form and an exact
three-contrast correction formula for its scalar. Trace-only and fixed
five-category shortcuts have analytic boundary obstructions. The adaptive
five-category shortcut also has an exact rational/log-interval obstruction.
None is a DPP counterexample: actual B(D)>28.680 is certified in the frozen
witness direction. The actual scalar still approaches one from below, so
uniform-gap arguments remain excluded.

FINITE CHECKS: **SCOUT / SANITY ONLY**, not general proofs. The standalone
standard-library script evaluates 29 fully recorded rational kernels:
4 exchangeable centers, 6 centered paths, 15 dense rank-one boundary points,
and 4 complementary boundary points. All input feasibility checks are exact
Fraction LDL; all eight atoms and first derivatives are exact Fractions.
Logarithms and solves use 140 or 220 decimal digits. One-parameter variance
and Woodbury identities are checked against independent matrix solves.
Every full rho is below one. The fixed-oriented coarse certificate passes
23/29, failing at two centered paths and four complementary boundary points.
The trace-capacity test passes 15/29. The six-category certificate passes
29/29, which is only SCOUT and is not an all-domain theorem.

SEPARATE EXACT GATE: one of those rational path points has a Fraction/log
interval certificate for both the proxy's negative B_T(D) and the actual
positive B(D), plus D>0 and the entire |t|<=1/100 chord's 1/1000 margin.
Its result is not categorized as a floating counterexample to entropy
concavity. The missing global condition is explicitly equation (27) in
derivation.md; it is equivalent to the original scalar bound, not progress
masquerading as a weaker lemma.

No novelty claim or CORRECT self-certification is made. Review derivation.md,
especially its gradient conventions, equality case, and boundary transfer.
