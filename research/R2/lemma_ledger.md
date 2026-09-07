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

## L5: singular mixed-family feasibility

- Statement: eventual feasibility of the exact mixed two-term family is
  equivalent to nonnegative limiting Schur residuals plus their kernel
  annihilation by `B^T` and `B`.
- Status: PROVED_HERE in `proofs/mixed_boundary_v2.md`
- Main risk closed: a nonnegative singular residual alone is not sufficient

## L6: mixed and unequal-scale logarithmic coefficients

- Statement: fixed longitudinal directions do not change the coefficient
  `Z-2||B||_F^2`; unequal scalar powers give
  `max(alpha,beta)Z-(alpha+beta)||B||_F^2`.
- Status: PROVED_HERE in `proofs/mixed_boundary_v2.md` and
  `proofs/unequal_slack_v2.md`
- Relative strength: all fixed nonzero transverse directions in the displayed
  boundary blow-up hierarchies, still not moving data

## L7: zero-transverse tomography gates

- Statement: the order-`epsilon` gap is nonpositive, with equality exactly on
  the two complete cofactor measurement kernels; on that kernel the complete
  `epsilon^2 log(1/epsilon)` coefficient is zero.
- Status: PROVED_HERE in `proofs/tomography_second_log_v2.md`
- Method: coordinatewise entropy Jensen plus zero-Pluecker adjugate rank

## L8: small-kernel strict two-point theorem

- Statement: every fixed distinct PSD pair has a strictly negative small-kernel
  entropy chord for sufficiently small scale.
- Status: PROVED_HERE in `proofs/small_kernel_two_point_v1.md`
- Boundary scope: zero diagonal entries and zero `2 x 2` determinants included

## L9: paired-frame ordinary coefficient

- Statement: for all paired frames, arbitrary independent pair rotations,
  and arbitrary fixed PSD inward matrices, the full tomography-kernel `C_2`
  is a sum of two nonpositive small-kernel chord coefficients.  For diagonal
  inward matrices it is the negative pairwise `G_D` sum.
- Status: PROVED_HERE in `proofs/paired_frame_C2_v2.md`,
  `proofs/paired_rotations_v2.md`, and `proofs/paired_nondiagonal_v2.md`
- Sign: strict for every nonzero feasible fixed direction

## L10: general finite `C_2` decomposition

- Statement: after L7, the remaining coefficient splits into active-support,
  one-flip, two-flip, and zero-support cross terms; the last is nonpositive.
- Status: PROVED_HERE as a decomposition; its universal sign is closed by
  L11--L12
- File: `proofs/b_zero_c2_decomposition_v2.md`

## L11: complete tomography-component theorem

- Statement: the full one-hole tomography kernel consists exactly of
  symmetric blocks between connected components of the nonzero coordinate
  graph of `P`; the complementary one-particle kernel has the same component
  description.
- Status: PROVED_HERE in `proofs/tomography_components_v3.md`; two independent
  reviews are pending binding to the candidate commit
- Consequence: the active logarithmic cross term and every zero-support cross
  term vanish under the complete tomography gate

## L12: general component-pair `C_2` sign

- Statement: for every datum in frozen theorem v2, `C_2` is the sum of scalar
  component/cofactor-pair Jensen defects `gamma_D`, hence `C_2<=0`; it is
  strict whenever `(X,Y)!=(0,0)`.
- Status: PROVED_HERE in `proofs/component_pair_C2_v3.md`; two independent
  reviews are pending binding to the candidate commit
- Boundary scope: arbitrary non-paired frames, simultaneous directions,
  singular inward matrices and endpoints, and zero Pluecker coordinates
