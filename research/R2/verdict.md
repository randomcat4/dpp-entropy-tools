# Verdict

Stage status: `VERIFIED` for frozen theorem v1; `PROVED_HERE` for frozen
theorem v2 pending one commit-bound gate; global real-kernel question
`INCOMPLETE`.

For fixed finite `(n,r,P,U,V,B,tau)` in frozen v1,

```text
Delta_epsilon
  = tau^2 (Z-2||B||_F^2) epsilon log(1/epsilon) + O(epsilon),
0 <= Z <= ||B||_F^2.
```

Hence every nontrivial frozen transverse family has `Delta_epsilon<0` for all
sufficiently small positive `epsilon`; the trivial direction has zero gap.
This strictly excludes one balanced near-projection family and does not prove
global concavity or produce a counterexample.

Correctness: the unchanged candidate commit `693c290` received two independent
`CORRECT` reviews.  Computation: a 30-chord rational-law diagnostic checked
1,200 exact event masses with zero failures, and a separate implementation
certified two finite rational fixtures with strict log enclosures.  Novelty:
unconfirmed and not claimed.

Round 2 closes mixed fixed longitudinal/transverse blocks, all feasible
singular residuals of the exact two-term family, unequal scalar approach
rates, the first two logarithmic layers of the zero-transverse branch, every
fixed small-kernel chord, paired-frame tomography kernels with arbitrary
fixed PSD inward matrices, and
rank-two one-sided kernels. The central new result map is in
`boundary_theorems_v2.md`.

Round 3 closes the former fixed-scale blocker.  The complete tomography kernel
is the off-block space between coordinate-graph components.  On this space all
high/low cross terms vanish, and the ordinary coefficient is an exact sum of
scalar component-pair convexity defects.  Hence

```text
C_2<=0,
C_2<0 if (X,Y)!=(0,0).
```

Two non-author reviews found no critical gap; the formal status remains
`PROVED_HERE` until those reviews are bound to the fixed candidate commit.
Moving frames, varying data, other boundary geometries, and arbitrary interior
chords are outside the proved scope.

No certificate/SHA gate was run for Round 2.  Because Round 3 is a major
closure, it receives one commit-bound gate.  Novelty remains unconfirmed and
is not claimed.
