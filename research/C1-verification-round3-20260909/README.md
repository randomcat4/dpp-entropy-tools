# PR41/43 new-claim verification

Read [STATUS.md](STATUS.md), then the [current frozen contract](frozen_theorem_v2.md)
and [claim ledger](lemma_ledger.md). Unit reports keep distinct conclusions.

- PR41 [first review](units/pr41/review_report.md) and
  [fresh second review](units/pr41_second/review_report.md): READY within scope.
- [PR43 channel/extension first review](units/pr43_channels/verification_report.md):
  D/I–N accepted, fresh second review running.
- [PR43 rank-two first review, corrected report](units/pr43_rank2/review_report_v2.md):
  E–H concavity/identities accepted, H's correlation descriptor needs η≠0.
- [Fixed-check process-record repair](main/provenance_replay/RESULT.md):
  same script/input passed with observed PID and exit; original failed metadata retained.
- [Formal feasibility](formal/README.md): environment probe only, no new formal proof.
- [External dependencies](prior_art.md): no novelty certification.
- [Known handoff hazards](hazards.md).

Immutable author sources:

- [PR41 round2 source](https://github.com/randomcat4/dpp-entropy-tools/tree/6fd61dcd299417fc3a4eab3af682c03dd816b670/research/N3/round3/I05-W4-20260909/round2).
- [PR43 current source](https://github.com/randomcat4/dpp-entropy-tools/tree/7bd5962bbb2020ce47fbe286adda7dfe02f9645d/research/I05-W1-20260909-R2).
- [PR43 original frozen source](https://github.com/randomcat4/dpp-entropy-tools/tree/4e1369ef2a59ccfaba3ca8fce95d85e78857bf78/research/I05-W1-20260909-R2).
- [Imported C3 diagonal-anchor proof](https://github.com/randomcat4/dpp-entropy-tools/tree/648f1906468e3e548410f98a6b1a53a978f2ea11/research/C3).

`source-snapshots/pr41` in unit reports means the immutable PR41 directory
above, with identical line numbering. PR43 reports explicitly name either
the original snapshot or its new-commit overlay. Operational paths in public
report copies are normalized; original local reviewer records are retained.
