# Verdict

Stage status: `VERIFIED` for frozen theorem v1; `PROVED_HERE` for the broader
v2 fixed-boundary hierarchy; global real-kernel question `INCOMPLETE`.

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
fixed small-kernel chord, paired-frame tomography kernels, and
rank-two one-sided kernels. The central new result map is in
`boundary_theorems_v2.md`.

The exact remaining fixed-scale blocker is a general non-paired
zero-transverse direction satisfying both complete cofactor tomography-kernel
conditions. Its `epsilon` and `epsilon^2 log(1/epsilon)` coefficients vanish;
the ordinary `epsilon^2` coefficient has a finite exterior-minor formula but
no universal sign. Corrected bounded searches found no positive value. Moving
frames, varying data, and higher-order paths are also outside the proved
scope.

No new certificate/SHA gate was run for Round 2. The v2 label is therefore
`PROVED_HERE`, not `VERIFIED`. Novelty remains unconfirmed and is not claimed.
