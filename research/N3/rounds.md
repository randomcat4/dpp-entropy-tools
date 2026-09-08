# Work units

- U1: 12 exact rational asymmetric centers; true trace optimizer tested against
  conditional-score bound. Executed all 12, zero rejections, no entropy candidate.
- U2: 36 asymmetric centers; full averaged projected quadratic form tested.
  20 averaged-bound failures, including 14 all-three-bound failures.
- U3: rational simplification and rigorous logarithm-interval certification of
  one actual DPP shortcut counterexample. Feasible K and nearby affine chord.

These units change neither the frozen target nor its premises. The initial
all-direction shortcut is retired, not repaired by hiding additional premises.
- U4: all one/two-site score projection, reusing 36 U2 centers. One
  all-direction failure, zero failures at the actual trace optimizer. An
  independent author then proved an analytic rank-two boundary obstruction
  and strictly certified one point at epsilon=10^-12.
- U5: targeted interior minimization of the conditional-score gap at the
  actual A optimizer: four fixed starts, 128 calls each, 512 executed calls,
  zero rejections, 164 negative projected gaps. Every optimizer reached its
  call limit; these are not global optimization results.
- U6: a second simple rational kernel, with the exact A optimizer enclosed
  using outward dyadic arithmetic, rigorously refutes all three Q_k bounds
  at that optimizer. True entropy curvature remains negative.
- Inequality units: a written covariance-score decomposition, then the
  Sherman-Morrison optimization formula and score-suppression identity.
  The missing DPP alignment inequality was not closed; its exact scalar
  expression is marked EQUIVALENT_BLOCKER rather than a solved theorem.

The independently owned 180-center boundary scout and its diagnostic repeats
are detailed in `falsification/run_log.md`. Its non-hits do not survive as an
open Q_k sufficient candidate after U6. Two structurally different projection
schemes now have explicit obstructions; increasing the same scans cannot
supply the missing coupling argument. Final audit and job closure are the
remaining administrative work for this round.
