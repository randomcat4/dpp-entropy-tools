# C1 PR41/43 independent verification, round three

Status: **REVIEW COMPLETE — scoped proof results READY; PR43 H wording NEEDS_FIX**.

This is a non-author verification packet. C3 owns integration to main.
The current version contract is `frozen_theorem_v2.md`; v1 is retained history.

| Unit | Source | Initial review | Second review | Release status |
|---|---|---|---|---|
| PR41 R2-T1/R2-T2 and exact missing-edge identities | `6fd61dcd299417fc3a4eab3af682c03dd816b670` | CORRECT / ACCEPTED_SCOPED | CORRECT, fresh independent review | READY, ACCEPTED_SCOPED |
| PR43 E–H: indefinite rank two, sufficient statistic, conditional criterion, structured 3+3 | `7bd5962bbb2020ce47fbe286adda7dfe02f9645d` | Concavity/identities accepted; H correlation wording correction pending | Same conclusion in a fresh independent context | READY for exact concavity/identity scope; H descriptor NEEDS_FIX |
| PR43 D and I–N: diagonal sectors, Markov and quantum-channel statements | Same PR43 commit | CORRECT / ACCEPTED_SCOPED | CORRECT / ACCEPTED_SCOPED, fresh context | READY, ACCEPTED_SCOPED |

PR41's accepted identity reduction does not settle the general connected
missing-edge inequality. No general finite-kernel entropy-concavity theorem,
novelty certification, or proof-assistant proof is declared here.

Repository coordination: [claim #46](https://github.com/randomcat4/dpp-entropy-tools/issues/46),
[integration queue #44](https://github.com/randomcat4/dpp-entropy-tools/issues/44),
[C2 computation #45](https://github.com/randomcat4/dpp-entropy-tools/issues/45).
C2 owns the full PR41 event/jet replay and the nested PR43 computation and
nonreversible LP. C1 owns only targeted proof checks and the root 3+3 fixture.
The C2 public reports and machine-readable result records at `1ddc775d` have
now been read; see `main/c2_evidence_read.md` for exact scope and limitations.

All three scoped units have completed fresh independent second review.
There is no remaining C1 proof-review or computation job. Author correction
of H's descriptor and C3's integration decision are the remaining external
handoff items; no general theory search is started.

The H wording issue is tracked in [the author PR](https://github.com/randomcat4/dpp-entropy-tools/pull/43#issuecomment-5600321387):
the allowed η=0 makes C diagonal, so the descriptive sufficient condition for
both blocks to be correlated needs η≠0. The concavity theorem permits η=0
and is not contradicted. The fixed explicit fixture already has η=1/1000.

Later PR43 commit `a7da3951a8ce02839dfa27f7205a1032d6f80f50` changes only
three historical-archive documentation notes; its full delta was inspected.
It changes no mathematical statement, proof, code, input or stored output.

PR41 was merged by C3 as `13d6c09d5d3fcf8c19cd0b01e5d735fd8778cdb6`.
PR43 remains open at a7da3951; no η correction has been observed at the final
source check. This packet never gives blanket acceptance to that literal
uncorrected descriptor. The review records themselves are ready for C3.
