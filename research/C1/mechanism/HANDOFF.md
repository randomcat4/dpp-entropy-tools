# HANDOFF

Recommended next tasks:

1. Prove the sparse phase root-tube asymptotic with a uniform remainder.  Start
   from the rational variant

       K=epsilon I+(7/10)uu^T, u=(3/5,4/5,q sqrt(epsilon)),

   and compare it to the analytic cue

       kappa_* = (3/7)(exp(40/21)-1),
       det(N)alpha = 1 - 1/(lambda log(1/epsilon)) + O(log(1/epsilon)^-2).

   The finite certificate here supplies an exact beta-zero point and a
   reproducible trend, but not the uniform expansion.

2. Run a fresh nonauthor audit of `scripts/sparse_rational_certificate.py` and
   `outputs/sparse_rational_certificate.json`.  The audit should independently
   rebuild the eight atoms, off-diagonal factor two, `Htilde=dM` scaling, exact
   endpoint signs, whole-bracket `det(N)alpha<1`, and the distinction between
   this rational finite-epsilon variant and the unit-normalized sparse family.

Optional extension after those two: improve the interval method with explicit
rank-one-plus-diagonal event formulas so epsilon=10^-12 can be certified with
a wider q bracket and less interval dependency.
