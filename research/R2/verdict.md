# Verdict

Stage status: VERIFIED for frozen theorem v1; bounded route complete.

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

The main escape routes are moving `P_epsilon` or `D_epsilon`, mixed
longitudinal/transverse blocks, and jointly changing zero-Plucker valuations.
