# Frozen scope

## Version binding

- Repository: `randomcat4/dpp-entropy-tools`
- Pull request: `#82`
- Reviewed head: `290a84064eaae2e857d637f58531e95f4ca3cb3b`
- Previously reviewed source baseline: `365347e`
- Live-head check was performed before publication.

The compare contains exactly two paths:

1. `research/I05-DPP-31-pr66-lowreg-20260910/c4_response_spatial_truncation_p4_multiscale.md`
   - blob `a81fa2349ef122d7c9ccbda43ddd70e8dfab402f`
   - 381 added lines
   - mathematical/source review included
2. `research/I05-DPP-31-20260910/README.md`
   - blob `18de8b1338ca23688207d87c6e9c95cd1105ab79`
   - static integration review included

## Accepted dependency boundary

This delta review does not re-prove the earlier qualitative `p>4` theorem.  It treats the following prior source and review state as the frozen premise:

- `c4_response_p4_boundary_correction.md`, blob `b15a6a26ea89d6f02272428ef5e1d4195a0fd347`;
- `c4_response_p4_one_loss.md`, blob `8ac6d2ada008474aaa6bd05cf7ebd2ed7eff419d`;
- the prior successor review `research/C1-verification-round8-20260910/units/pr82/successor_3653_review.md`, blob `caf6db5cbccb3a67e17d96f8825c0926b3e4383c` at PR90 head `5b32943874e0633f87fa67e7150b01e134a1581e`;
- the public qualitative integration checkpoint `docs/verification_round4_20260909/pr82_6ecc_checkpoint.md`, blob `bf89bd57afd3729c6a354def47760285ee77000b` as observed on `main`.

Only the new multiscale passage from uniform spatial kernel error to stationary response convergence was freshly audited.

## Explicit exclusions

- no arithmetic or checker execution;
- no finite-window DPP curvature computation;
- no claim that the frozen compatible law is a finite-section DPP;
- no re-review of the rejected Dobrushin A1/A2 route;
- no extension to `p<=4`;
- no endpoint rate `a(a-2)/(a+1)`;
- no novelty, priority, optimality, formal proof, SECOND, or merge judgment.

A later PR82 head requires a fresh delta binding.
