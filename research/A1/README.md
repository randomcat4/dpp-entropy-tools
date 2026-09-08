# A1: connected three-point real DPP entropy

Status: FIRST_MILESTONE_COMPLETE. Two restricted theorems and one exact
proof-shortcut obstruction passed independent fixed-object review. The original
general connected three-point target remains INCOMPLETE.

This lane continues the unresolved three-point boundary documented by PR #8,
without changing R1 artifacts. Its baseline is commit
`ba1227931521fa663f0d5b3f15906a985866877c`.

The target is full-event Shannon entropy of strictly interior real symmetric
3 by 3 marginal kernels. Positive endpoint-average minus midpoint entropy is
the counterexample sign. Numerical positives require strict certification.

## Verified results

1. For fixed c in (0,1), v in R^2 nonzero, the entropy of
   K(A,s)=[[A,sv],[sv^T,c]] is strictly concave on the feasible four-parameter
   domain. This controls full finite chords through connected triangular
   centers. [Statement](frozen_radial_slice_v1.md),
   [proof](proofs/radial_slice_v1.md).
2. At K_r=(1/2)I+r(J-I), abs(r)<1/4, the full four-dimensional subspace
   tr(V)=0, V12+V13+V23=0 has nonpositive entropy curvature, strict for
   r!=0,V!=0. This is local, not full-Hessian or finite-chord concavity.
   [Statement](frozen_standard_modes_v1.md), [proof](analytic/proof.md).
3. An explicit rational connected triangle has positive conditional
   acceleration despite negative total entropy curvature. Its rational log
   certificate refutes the shortcut of discarding conditional acceleration.
   [Statement](frozen_acceleration_obstruction_v1.md), [proof](probe/proof.md).

All three mathematical objects were frozen at
`58ee11adcf0afd8d183057d61f0168127093bcad` and reviewed by a fresh non-author
GPT-5.5 xhigh instance. Each received `STATUS: CORRECT`; the
[review](verifications/a1_fixed_object_review.md) records exact Git blob IDs
and independent symbolic/rational replays. Frozen author files retain their
original pending-review labels; this README and the review give current status.

The remaining symmetric-center problem is the explicit 2 by 2 block T in the
analytic proof. General nonsymmetric centers remain unresolved. No strict
real entropy counterexample, general real concavity, novelty, or Lean claim.

The bounded falsification denominator is 5612 conservatively counted
evaluations, with rejected-domain calls and certificate rechecks retained.
No positive total-entropy candidate was promoted. Some short diagnostic PIDs
were not captured; see [execution limitations](probe/provenance.md).

See [scope map](scope_map.md), [verdict](verdict.md),
[routes](route_registry.md), and [prior-work audit](prior_art.md).
