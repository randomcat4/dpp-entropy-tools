# Lemma ledger

## L1: exact Schur feasibility

- Statement: the v1 affine chord is feasible exactly on the interval stated in
  Claim 1.
- Status: VERIFIED for frozen v1 by `verifications/fresh_v1/report.md` and
  `verifications/domain_v1.md`
- Relative strength: strictly weaker than the original all-real problem
- Method: block singular-value decomposition / `2 x 2` Schur conditions

## L2: finite probability-scale entropy expansion

- Statement: for a fixed finite family of nonnegative event polynomials with
  identified leading `epsilon` coefficients, the logarithmic entropy
  coefficient is the sum of those leading coefficients, with an
  `O(epsilon)` remainder after the v1 event partition.
- Status: VERIFIED in the frozen-v1 event partition; a more general
  probability-family version remains supplementary
- Relative strength: strictly weaker
- Main risk: events with a hidden scale between `epsilon` and `epsilon^2`

## L3: exterior tangent leakage

- Statement: `sum_{|S|=r} phi_S^2=||B||_F^2`, hence
  `0<=Z<=||B||_F^2`.
- Status: VERIFIED for frozen v1 by two commit-bound reviews
- Relative strength: strictly weaker
- Method: norm of the derivative of the normalized decomposable `r`-vector

## L4: logarithmic chord coefficient

- Statement: Claim 3 of frozen v1.
- Status: VERIFIED for frozen v1 at candidate commit `693c290`
- Relative strength: equivalent to the frozen bounded objective, strictly
  weaker than the original all-real problem
- Dependencies: L1-L3 and full event-class coefficient bookkeeping
