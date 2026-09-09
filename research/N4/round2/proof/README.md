# N4 round-two proof child

State: `PROVED_SCOPED_LEMMAS`; the universal N4 face-concavity claim remains
`INCOMPLETE`.

This directory contains the proof-child object for the fixed rank-three
four-point face in `../frozen_theorem_v1.md`.

- `support_lift_proof_v2.md` is the current proof object. It proves the exact
  support statement, deletion of the full event and all its face derivatives,
  analyticity of `H_face`, the six-coordinate Hessian identity, and the
  strict-kernel lift via the bit-flip channel gate `Delta(e)>=Delta_face-4h_b(e)`.
- `support_lift_proof_v1.md` is retained as the earlier continuity-gate
  version.
- `review_packet.md` is a compact checklist for an independent reviewer of v2.
- `checkpoint.md` records scope, status, and remaining obligations.

No numerical positive candidate is claimed here. These lemmas do not prove
face concavity and do not transfer a Hessian limit from the boundary to strict
kernels.
