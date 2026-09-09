# Final scoped verification result

The assigned mathematical review is complete. Three first reviews and three
subsequent fresh-context second reviews examined the actual proofs. No critical
gap was found in the scoped entropy-concavity or identity proofs. One literal
correlation descriptor in PR43 H is false as written and needs a local fix.

## Accepted scope

| Source and claim | Final C1 verdict |
|---|---|
| PR41 R2-T1: strong-coupling three-point centers, both sign choices, every real symmetric direction | CORRECT / ACCEPTED_SCOPED; READY |
| PR41 two-point conditional entropy and R2-T2 full six-direction block-plus-singleton Hessian identity | CORRECT / ACCEPTED_SCOPED; READY |
| PR41 general missing-edge coordinates, Jacobian and complete Fisher identities | CORRECT / ACCEPTED_SCOPED as identities only |
| PR43 E: real three-point indefinite rank-two affine directions | CORRECT / ACCEPTED_SCOPED; READY |
| PR43 F: exact exterior sufficient statistic, KL/mutual-information preservation, compressed Hessian | CORRECT / ACCEPTED_SCOPED; READY |
| PR43 G: three conditional-direction alternatives and true t-affine lift | CORRECT / ACCEPTED_SCOPED under inherited strict block hypotheses; READY |
| PR43 H: structured 3+3 concavity theorem, explicit dense fixture and exact legal radius | CORRECT / ACCEPTED_SCOPED; READY for this exact scope |
| PR43 H: both blocks correlated under only α≠β and off-diagonal M0 | NEEDS_FIX; excluded from acceptance |
| PR43 D: imported diagonal-anchor theorem's actual use | CORRECT dependency match only; no new proof of C3 |
| PR43 I/J: diagonal coordinate reducing sector at arbitrary rank and per-condition strict diagonal anchor | CORRECT / ACCEPTED_SCOPED; READY |
| PR43 K/L: stationary density-adjoint exterior intertwining, full Fisher curvature identity, diagonal degree closure | CORRECT / ACCEPTED_SCOPED; READY |
| PR43 M/N: reversible exterior mechanism obstruction and occupation-channel obstruction | CORRECT / ACCEPTED_SCOPED; READY within these obstruction scopes |

## Required author correction

At PR43 `7bd5962bbb2020ce47fbe286adda7dfe02f9645d`,
`continuation/frozen_statement_v3.md:153` and
`proof/06_correlated_3plus3_family.md:69` omit η≠0 from the sufficient
condition for A and C both to be non-diagonal. The theorem allows η=0,
in which case C=D0 is diagonal. The displayed n, α=2/5, β=1/2 and B,
with D0=(2/5)I and η=0, satisfy every other hypothesis and refute only
that descriptive sentence.

Add η≠0 to the correlated-subfamily descriptor and any duplicates. Keep η=0
in the concavity theorem's parameter domain. The explicit correlated fixture
already uses η=1/1000 and remains valid. Both independent rank-two reviews
agree on this distinction; C3's separate statement mapping also found it.
The first reviewer initially missed the descriptor; its revised report v2
and original historical report are both retained.

The author was notified in
[PR43 comment](https://github.com/randomcat4/dpp-entropy-tools/pull/43#issuecomment-5600321387).
No author correction was observed in final source checking. C1 does not alter
the author's proof or silently certify a proposed correction as a new source.

## Version and evidence binding

PR41: `6fd61dcd299417fc3a4eab3af682c03dd816b670`; C3 has merged it at
`13d6c09d5d3fcf8c19cd0b01e5d735fd8778cdb6`.

PR43: the full v3.1 statement/proof package is reviewed at
`7bd5962bbb2020ce47fbe286adda7dfe02f9645d`. Its successor
`a7da3951a8ce02839dfa27f7205a1032d6f80f50` changes only three archive
documentation notes; the complete delta was read and contains no change to
the mathematical statements, substantive proofs, code or exact inputs.
Thus the exact scoped verdicts and the outstanding descriptor issue also
apply to that successor. Future changes need a recorded delta check.

C1's fixed symbolic/rational checks pass. Original process-record failures
remain visible; identical guarded replays provide directly captured PID and
exit records. See `main/provenance_replay/RESULT.md`. Numerical curvature
values are diagnostics only. The universal claims are supported by the
analytical proof reviews, not by sampled signs.

C2's published exact event/jet and nested replay evidence was read at
`1ddc775d8ceebf46ddd0335f04df282b58c1e8f7`; scope mapping is in
`main/c2_evidence_read.md`. C1 does not claim to have independently rerun
C2's entire verifier or approved its separate directed-flow certificate.

## Interpretation limits

- K's divided curvature identity is an interior s=t²>0 identity. At t=0,
  use strict-kernel analyticity and zero-mean exterior identities; legal
  endpoints use finite-entropy continuity. No direct division by zero is used.
- G's concise statement inherits strict block/legal-interval assumptions.
  Those assumptions should be repeated if the clause is excerpted standalone.
- General connected missing-edge, arbitrary dense two-sided rank two,
  unrestricted finite real or complex kernels, general exterior-acceleration
  signs and automatic entropy-dissipation curvature remain outside this review.
- M/N do not refute DPP entropy concavity or quantum data processing.
- Novelty and priority are unassessed. Lean/Lake feasibility is L0 only;
  no new formal proof is claimed.

The review records and exact accepted scopes are READY for C3. PR43's literal
uncorrected descriptor remains NEEDS_FIX. C3 alone decides and performs main
integration. There is no remaining C1 reviewer or computation job and no new
open-ended research is started.
