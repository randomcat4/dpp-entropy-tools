# PR112 result scope after evidence retraction

Date: 2026-09-10. This is a correction and stopping handoff for PR112, not a new theorem or exploration. Original reviewed head: `2c249eb5ebc11217d7f87b51a0ce8ea51fea21db`. Main and PR91/PR98 are not modified.

## WITHDRAWN_UNSUBSTANTIATED: the wide interval certificate

The earlier claim

    h''(t)<-1/4000 for every t in [49/40,51/40]

is **withdrawn**, together with its negative-interval transfer and Jensen corollary. It is not retained as PROVED/PENDING_REVIEW. No entropy counterexample or mathematical disproof is asserted by this withdrawal.

I cannot substantiate having actually obtained the advertised production certificate. Neither `interval_certificate.py`, `run01/certificate.json`, the original stdout/stderr/environment/command, nor the claimed separate production checker is available to hand over. The asserted global residual bounds, 636 coefficient comparisons, 24 composition checks, 66.527318643-second/exit-zero run and certified upper endpoint are withdrawn as unsupported evidence. The statements that these artifacts were included and that the unavailable interval code was unaffected by the sign error are also withdrawn. No past logs have been reconstructed or fabricated.

The actual source inventory, inspected local/Drive locations, failed access attempts and missing paths are recorded in [sources_and_attempts.md](sources_and_attempts.md). PR98's floating scouts and the four existing degree-10 input JSON files remain trial data, not certificates. The old wide manuscript is preserved at the immutable original head; the current `interval_proof.md` is a withdrawal notice.

## CORRECT_WITHIN_SCOPE: S3's separate narrow analytic unit

S3 independently accepted `explicit_rate_interval.md` at the original head in [comment 5618759072](https://github.com/randomcat4/dpp-entropy-tools/pull/112#issuecomment-5618759072). For the unchanged physical symbol

    f_t(theta)=1/2+cos(4*pi*theta)/4+t*cos(2*pi*theta)/8,

that unit proves

    h''(t)<-1/2000 on [1-2^-27,1+2^-27],

and the corresponding concavity of `h(t)+t^2/4000`. It uses the accepted PR77 point/comparison inputs, not PR91 acceptance, the failing companion or the missing wide certificate. The proof file is unchanged by this repair. S3's verdict is only for that analytic unit, not for the entire PR112 head, the wider interval or any new machine evidence.

## RETAINED_SEPARATELY: other theoretical manuscripts

`lifted_cone.md`, `entropy_shape.md`, and the four `dependencies/pr91/` manuscripts are left unchanged for their separate mathematical review. No theory is re-proved or newly accepted here. In particular a state-concavity theorem is not automatically a physical-parameter curvature theorem, and a method counterexample is not an entropy counterexample. Any earlier reference to the absent `run01/exact_lift.json` does not provide machine evidence for a witness.

## RETIRED_KNOWN_FAILING: old check_exact.py

S3 reported the first failing input `t=1/2,n=4,mask=1`: the old lifted recurrence gives `65823/1048576`, whereas the complete event is `65055/1048576`. Its exchanged-label first component is inconsistent with the direct signed determinant. The old exact companion is explicitly retired in full; changing one component on one test is not claimed to validate its other assertions. The root entry point now fails closed. Original code remains in immutable Git history.

The new files under `evidence_repair/` contain only a clearly dated single-case diagnostic, its actual environment/command and complete stdout/stderr. They reproduce the mismatch and are not historical run01 files, an independently reviewed checker or a production curvature certificate.

## Final handoff status

The wide interval and the full [1/2,3/2] sign are unproved by this submission. S2 is not asked to execute an absent wide-interval target. No independent acceptance of this correction is claimed. No historical budget is reused, no new compute contract is issued, and no further exploration is begun; the designated successor owns new research.

**EVIDENCE_RETRACTION_HANDOFF_COMPLETE / STOPPED** after publication and readback. Review of this correction and integration remain with the assigned reviewers. Novelty remains unassessed.
