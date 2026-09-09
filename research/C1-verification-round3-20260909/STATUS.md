# C1 PR41/43 independent verification, round three

Status: **RUNNING — no aggregate READY declaration yet**.

This is a non-author verification packet. C3 owns integration to main.
The current version contract is `frozen_theorem_v2.md`; v1 is retained history.

| Unit | Source | Initial review | Second review | Release status |
|---|---|---|---|---|
| PR41 R2-T1/R2-T2 and exact missing-edge identities | `6fd61dcd299417fc3a4eab3af682c03dd816b670` | CORRECT / ACCEPTED_SCOPED | CORRECT, fresh independent review | READY, ACCEPTED_SCOPED |
| PR43 E–H: indefinite rank two, sufficient statistic, conditional criterion, structured 3+3 | `7bd5962bbb2020ce47fbe286adda7dfe02f9645d` | Concavity/identities accepted; H correlation wording correction pending | Running in a fresh context | Not ready |
| PR43 D and I–N: diagonal sectors, Markov and quantum-channel statements | Same PR43 commit | CORRECT / ACCEPTED_SCOPED | Running in a fresh context | Pending second review |

PR41's accepted identity reduction does not settle the general connected
missing-edge inequality. No general finite-kernel entropy-concavity theorem,
novelty certification, or proof-assistant proof is declared here.

Repository coordination: [claim #46](https://github.com/randomcat4/dpp-entropy-tools/issues/46),
[integration queue #44](https://github.com/randomcat4/dpp-entropy-tools/issues/44),
[C2 computation #45](https://github.com/randomcat4/dpp-entropy-tools/issues/45).
C2 owns the full PR41 event/jet replay and the nested PR43 computation and
nonreversible LP. C1 owns only targeted proof checks and the root 3+3 fixture.
No C2 result is treated as evidence before its public output is inspected.

New general results receive independent second review after initial acceptance.
Upload is a checkpoint; outstanding scoped work continues.

The H wording issue is tracked in [the author PR](https://github.com/randomcat4/dpp-entropy-tools/pull/43#issuecomment-5600321387):
the allowed η=0 makes C diagonal, so the descriptive sufficient condition for
both blocks to be correlated needs η≠0. The concavity theorem permits η=0
and is not contradicted. The fixed explicit fixture already has η=1/1000.

Later PR43 commit `a7da3951a8ce02839dfa27f7205a1032d6f80f50` changes only
three historical-archive documentation notes; its full delta was inspected.
It changes no mathematical statement, proof, code, input or stored output.
