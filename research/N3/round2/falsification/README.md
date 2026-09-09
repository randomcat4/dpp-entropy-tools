# Round-two directed beta-zero falsification

STATUS: INCOMPLETE for the frozen global B0 implication.
NEW PARTIAL OBJECT: an exact beta-zero exists on an explicit strictly
feasible connected affine segment, with d alpha<1 on its whole certified
root bracket. See [the self-contained proof](beta_zero_existence.md) and
[the rational interval certificate](root_certificate.json).

The first bounded batch predeclared twelve affine segments, with nine
rational parameters per segment: three diagonal sweeps, three edge-sign
sweeps, three unequal-endpoint rank-one-to-twisted-complement segments,
and three weak-bridge rotations. Endpoints have exact rational positive
definiteness checks; convexity certifies the whole segments. All 108 sampled
points were connected and accepted. Six had negative beta, all from
softened rank-one endpoints and their twisted-complement endpoint copies.
The count six therefore must not be represented as six unrelated mechanisms.

This new sign mechanism disproves universal positivity of beta. It is
compatible with positivity in a fixed-mean, fixed-edge-ratio weak-coupling
limit, and with full complement preserving beta's sign. The seed is absent:
all parameter lists and bisection choices are deterministic.

Only the already-hit epsilon=1/100 affine family was followed up. Forty-two
bisection evaluations fixed one rational root bracket. Five outward-rational
interval evaluations certified opposite endpoint signs and d alpha<1 on
the full bracket. A floating-point approximation was never called an exact
zero. No new family, random optimization, or unbounded continuation followed.

The finite batch had max d alpha approximately 0.910003, below one, and
produced no main-theorem counterexample. The positive partial result does
not show that every beta zero satisfies the desired inequality. The precise
remaining obligation is to control d alpha on all other connected strict
zero components, or to find and certify a component with d alpha>1.

All code, source bindings, event matrices, interval bounds, PIDs and actual
coverage are preserved here. The independent author's round-one objects
were read as fixed dependencies and were not changed. This unit is handed
back to the parent for a fresh nonauthor review; no background job remains.
