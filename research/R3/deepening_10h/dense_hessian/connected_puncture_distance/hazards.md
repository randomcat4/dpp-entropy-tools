# D10-U5 hazards

## Exact-event semantics

All entropy calculations must use exact DPP atoms from inclusion-determinant
Möbius inversion.  Principal minors are inclusion probabilities, not atom
probabilities.

## Author status

This is an author route.  Nothing here is self-certified as CORRECT.  P4 and
the `n=4` classification require non-author fresh-context review.

## P4 full Hessian versus single entry

U4 only had a P4 endpoint-coordinate scout.  U5 must check the full Hessian:
diagonal coordinates, supported edges, distance-two missing edges, the
distance-three endpoint edge, and all mixed blocks under anisotropic scaling.

## Coordinate scaling

The off-diagonal coordinate for a pair at graph distance `d` is scaled by
`|epsilon|^-d`.  A mixed Hessian entry can affect the limiting block if its
order is exactly `epsilon^(d(e)+d(f))`; lower order would break the scaling,
higher order vanishes.  This order bookkeeping is the main fragile point.

## General connected graphs

The diagonal shortest-path rule, even if true, does not by itself prove the
general connected theorem.  Same-distance off-diagonal blocks may contain
overlapping-path terms.  No proof of their universal negative definiteness is
currently available.

## Multiple shortest paths

The candidate diagonal formula sums over shortest paths with positive squared
edge weights.  Cross terms between different shortest paths are expected to be
killed by character orthogonality unless they have the same vertex support.
This needs a clean general graph lemma before being promoted to theorem.

## Floating false positives

Naive double-precision finite-difference Hessians near `epsilon=0` are
unreliable: distance-three and distance-four eigenvalues are of order
`epsilon^6` or `epsilon^8`, often below roundoff/noise.  The retained scout is
exact rational coefficient extraction, not finite-difference spectral testing.

## Strict feasibility

The punctured ray is inside the strict kernel domain only after shrinking
`epsilon` so that `|epsilon| ||A||_op < min_i{x_i,1-x_i}`.  No boundary kernels,
zero edge weights, or uniform threshold as edge weights tend to zero are
claimed.

## Finite scout scope

The n≤5 checks are deterministic exact scouts.  They can catch coefficient
errors and suggest the distance rule; they do not prove the arbitrary-n
connected-support theorem.
