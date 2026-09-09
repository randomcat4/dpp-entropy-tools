# Soundness of the finite certificate arithmetic

This integration note explains the error enclosure in the included
mechanism/scripts/sparse_rational_certificate.py. It does not assert the
global B0 inequality or a new asymptotic theorem.

Every interval endpoint is a Python Fraction, hence an exact rational.
The constructor rounds a rational lower endpoint down and upper endpoint
up to multiples of 2^-620. Addition, negation and multiplication use the
ordinary endpoint enclosure formulas, followed by the same outward rounding.
Division is only performed after excluding zero from the denominator
interval, using the reciprocal interval [1/upper,1/lower]. Induction on
the finite arithmetic expression therefore proves containment of every
exact value, even though repeated uses of a dependent input can widen it.

For logarithms, write x=2^k y with 1<=y<2 and integer k. For
z=(y-1)/(y+1) in [0,1/3], the convergent atanh series gives

    log(y)=2 sum(j>=0) z^(2j+1)/(2j+1).

With n=110 retained terms, its nonnegative remaining tail is at most

    2 z^(2n+1)/[(2n+1)(1-z^2)].

Indeed each remaining denominator is at least 2n+1 and the remaining
powers form a geometric series with ratio z^2. The same formula bounds
log(2), using z=1/3. Thus log(x)=log(y)+k log(2) has rational lower and
upper bounds; the endpoints of k log(2) are reversed for negative k.
Monotonicity of log extends this to positive input intervals by using the
lower input's lower log bound and the upper input's upper log bound.
All these endpoints are then rounded outward. No floating log is used
to decide a certified sign.

The exact p and coordinate Jacobian polynomials are evaluated through
these interval operations. Positive atom bounds make all divisions and
logs valid. Positive leading principal minors prove N>0 on the complete
input q interval by Sylvester's criterion. The formula reconstruction
then gives d>0, Fpair>=0, and M=Fpair+dG>0. Alternatively the actual
Gaussian interval elimination records pivot intervals avoiding zero at
every step; hence for each concrete q, its exact elimination and solution
are enclosed by the computed intervals. A residual interval containing
zero is a consistency check, not a substitute for pivot or positivity
arguments.

The exact identities Htilde=dM, a=d eta reduce the solve to
Htilde h=a, with h=M^-1 eta, beta sqrt(Z)=g^T h, and d alpha=a^T h.
The resulting endpoint sign enclosures and whole-bracket bound therefore
apply to the genuine optimizer. Floating bisection is used only to propose
the rational bracket; strict endpoint signs are recomputed by the exact
interval procedure. Since all quantities are continuous and nonsingular
throughout that bracket, the intermediate value theorem supplies an exact
beta zero. No numerical near-zero is promoted to equality.

The JSON's exact Fraction endpoints are authoritative. Its decimal fields
are also rounded outward explicitly by floor/ceiling on a decimal grid.
The weaker decimal bounds in RESULT.md deliberately preserve that direction.
