# Lemma ledger

| ID | Statement | Status | Relation to target | Evidence |
|---|---|---|---|---|
| L0 | Inclusion-exclusion reconstructs the complete event law | KNOWN | STRICTLY_WEAKER | Definition and finite Mobius inversion |
| L1 | H''=-sum (p')^2/p-sum p'' log p on a positive event path | KNOWN | STRICTLY_WEAKER | Twice differentiating finite Shannon entropy |
| L2 | Strict real two-point entropy is concave | KNOWN in baseline | STRICTLY_WEAKER | R1 frozen_n2_concavity_v1 and fixed-object review |
| L3 | 1 by 1 / 2 by 2 block midpoints have negative nontrivial chord gap | KNOWN in baseline | STRICTLY_WEAKER | R1 block composition proof and review |
| L4 | Connected three-point full Hessian is negative semidefinite | OPEN | EQUIVALENT to local target | No claimed proof |

The exact new reduction and any remaining sublemma will be added with its
actual strength after the first isolated unit.

## New exact objects, pending fixed-object review

- L5: Strict concavity on a fixed-site radial coupling slice.
  PROVED_CANDIDATE; 相对原命题 STRICTLY_WEAKER (restricted four-parameter
  affine subdomains). Proof: proofs/radial_slice_v1.md. 外部定理条件核验:
  both conditional kernels are strict real 2 by 2 contractions, and the
  conditional acceleration is kept explicitly.
- L6: Exact full-six-dimensional S3 decomposition at exchangeable centers.
  PROVED_CANDIDATE identity; its sign problem remains an EQUIVALENT_BLOCKER
  within that center family only. Proof: analytic/proof.md, equation (1).
- L7: Negative standard-mode curvature at half-filled triangle centers.
  PROVED_CANDIDATE; STRICTLY_WEAKER. Proof: analytic/proof.md, sections 2-3.
  No external concavity theorem is needed; the log derivative ratio and
  m>2 ell>0 give the sign directly.
- L8: Conditional acceleration is always nonpositive at fixed c.
  Candidate DISPROVED by frozen_acceleration_obstruction_v1.md. This was a
  proposed sufficient shortcut, not the original entropy-concavity claim.
