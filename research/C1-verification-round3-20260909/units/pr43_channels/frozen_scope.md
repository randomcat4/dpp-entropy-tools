# PR43 channel/extension verification frozen scope

Reviewer: C1 round-three reviewer 3, non-author, PR43 channel/extension unit.
Timestamp: 2026-09-09 18:10:53 +08:00

## Fixed source and authority order

- Current report-binding PR43 source commit: `7bd5962bbb2020ce47fbe286adda7dfe02f9645d`.
- Historical frozen PR43 source commit for unchanged proof/code/inputs: `4e1369ef2a59ccfaba3ca8fce95d85e78857bf78`.
- Current immutable source snapshot: `source-snapshots/pr43_7bd5962`.
- Historical immutable source snapshot: `source-snapshots/pr43`.
- Run-level freeze: `repo/research/C1-verification-round3-20260909/frozen_theorem_v1.md`.
- Primary PR43 statements for this unit: `continuation/frozen_statement_v3.md` version v3.1 and `continuation/CODEX_VERIFICATION_TASKS_v2.md`.
- For adjoint/reversibility, the explicit v3.1/v2-task corrections and `proof/07_markov_adjoint_and_reversible_obstruction.md` take precedence over older reversible-only wording.
- Imported C3 diagonal-anchor dependency is checked only from `sources/dependency_c3` at PR29 commit `648f1906468e3e548410f98a6b1a53a978f2ea11`, without using old reviews as evidence.

## Assigned claims

I review the old D--J channel/extension claims under their current v3.1 labels as distinct mathematical statements:

- D. External diagonal-anchor line concavity input; I only check PR43's usage against the dependency hypotheses.
- I. Diagonal active sector reduction for arbitrary rank, plus exact 3+5 fixture obligations where they bear on the statement.
- J. Strict diagonal anchor criterion for each conditioning event.
- K. Exterior-likelihood Markov forward map, density-adjoint intertwining, and Fisher/curvature identity.
- L. Walsh degree bounds for diagonal exterior kernels.
- M. Correlated two-point reversible-feature orthogonality obstruction with the stated `-125/78` value.
- N. Classical occupation-channel obstruction for quasi-free decay, including the two-input equal-occupation law and output `91/400` versus `99/400`; this is not a quantum data-processing counterexample.

## Boundaries

- I do not review the rank-two unit claims assigned elsewhere: strict real three-point indefinite-rank-two directions, the correlated dense 3+3 family, or compressed-Hessian identities except as dependencies for I--N.
- I do not merge, repair, or reinterpret old continuation summaries; parent/main handles author questions about publication-level relationships.
- I do not read `CONSISTENCY_AUDIT.md` as mathematical backing.
- I do not modify author files, source snapshots, or other reviewers' files.
- I do not start open-ended theory exploration, new LP/counterexample search, all-domain recomputation, or novelty review.
- After the parent update, I exclude the public C2 compute lane's work from my own execution: no duplicate full 256-event 3+5 run, no duplicate author verifier replay, and no duplicate task-D/nonreversible LP. I may later inspect public C2 evidence if it is placed in the shared run, but not private C2 directories.

## Evidence standard

Each claim receives `CORRECT` or `CRITICAL_GAPS`, mapped to `ACCEPTED_SCOPED`, `NEEDS_FIX`, `REFUTED`, or `INCOMPLETE`. I distinguish theorem falsehood from proof incompleteness and mechanism obstructions from entropy counterexamples. Author scripts are reviewed as material evidence only after their mathematical inputs and outputs are independently checked.
