# Independent verification index

Status: CORRECT for the scoped support/BSC and top-budget objects below;
the global question is INCOMPLETE. This index summarizes one non-author
reviewer's reports and is not a second independent review.

- [Support/lift v2](../review/support_lift_proof_v2_review.md):
  CORRECT for support, analyticity, Hessian shell and conditional BSC lift.
- [Top-budget](../review/top_layer_budget_review.md):
  CORRECT_BOUND_ONLY, not complete face concavity.
- [Coarsening](../review/coarse_identity_review.md):
  CORRECT_IDENTITY_ONLY. Finite polynomial checks and general derivation
  scope must be read separately; see the
  [general derivation supplement](../review/presentation_and_identity_supplement.md).
- [Projection q](../review/n5_projection_q_certificate.md):
  exact weights and rational-log sign H(q)>3/2.
- [Negative diagnostic](../review/finite_noncommuting_bsc_certificate.md):
  one noncommuting face chord and its common strict BSC lift are negative.

Initial decimal bounds were printed through binary64; they are approximate
displays, not outward endpoints. The separate exact-rational presentation
supplement corrects this limitation while preserving the original files.
See review/run_ledger.md and
[outward rational bounds](../review/interval_presentation_supplement.json).

Reviewed frozen source blobs are in proofs/index.md. Search self-checks
are not independent reviews. No main theorem was submitted for second
review or Lean checking; formal/README.md records toolchain smoke only.
