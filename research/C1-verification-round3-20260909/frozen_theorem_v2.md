# Frozen verification contract v2

This supersedes the source-map portions of v1; it does not issue a verdict.
All complete-event, real-coordinate, independence, resource and exclusion
requirements in v1 remain applicable.

## Exact source versions

- PR41 remains `6fd61dcd299417fc3a4eab3af682c03dd816b670`.
- PR43 changes from `4e1369ef2a59ccfaba3ca8fce95d85e78857bf78` to
  `7bd5962bbb2020ce47fbe286adda7dfe02f9645d`.
- Imported diagonal-anchor theorem: PR29
  `648f1906468e3e548410f98a6b1a53a978f2ea11`.

PR43's canonical continuation contract is now
`research/I05-W1-20260909-R2/continuation/frozen_statement_v3.md`, labelled
v3.1 by the author. It explicitly includes the root three-point and 3+3
claims formerly absent from the nested summary. Its current claim map is:

| Claim | Scope |
|---|---|
| D | Imported strict diagonal-anchor line-concavity theorem |
| E | Real three-point indefinite rank-two line concavity, continuous value extension at legal boundary |
| F | Exact exterior sufficient statistic / KL preservation and compressed Sym2 Hessian |
| G | Every conditional direction has rank at most one, indefinite rank two, or a strict diagonal anchor |
| H | The specified structured correlated 3+3 family and exact fixture interval |
| I | Coordinate reducing sector, diagonal active block, arbitrary cross-block rank |
| J | A possibly different strict diagonal anchor for each complete conditional event |
| K | Stationary density-adjoint intertwining; full Fisher curvature identity |
| L | Diagonal exterior degrees and independent coordinate refresh |
| M | Specified reversible-channel obstruction |
| N | Specified occupation-channel obstruction |

Former nested-v3 E–J correspond to current I–N. The nonreversible LP task
formerly D is now task G; this is the same fixed computational object, not
authorization for another LP or an arbitrary new kernel.

## Verified source delta

GitHub's commit comparison lists exactly 12 changed documentation files under
`continuation/`: CODEX_VERIFICATION_TASKS_v2.md, CONSISTENCY_AUDIT.md (added),
HANDOFF.md, README_v3.md, RESULT_CONTINUATION.md, RESULT_FINAL.md,
attempts_continuation.md, frozen_statement_v3.md, proof.md, proof_v3.md,
sources_continuation.md, verification.md. No substantive file in either
`proof/` directory, code, exact input or stored output changed. The two named
proof markdown files are reading indexes. Reviewers read the new canonical
statement; the author's consistency audit is not mathematical evidence.

The original snapshot is retained, and the new snapshot overlays exactly
these 12 files. Historical summaries do not override current quantifiers.
Future author commits require an explicit delta review.

## Release boundaries

Each claim receives its own mathematical verdict. A documentation or payload
defect is recorded separately from a false theorem or critical proof gap.
Finite computations validate the fixed object only. Novelty remains unassessed.
In particular, neither reversible nor occupation-channel obstructions refute
DPP entropy concavity, and no general high-dimensional exterior-acceleration
sign is claimed.
