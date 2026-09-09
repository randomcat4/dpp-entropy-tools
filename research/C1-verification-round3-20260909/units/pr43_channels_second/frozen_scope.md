# Frozen scope -- PR43 channels second review

Reviewer role: fresh non-author mathematical reviewer for PR43 claims D and I--N only.

Date: 2026-09-09.

Mode: analytical proof review. No descendants, no novelty search, no full verifier replay, no new LP search, no merge or publication action.

Primary frozen PR43 source:

- `sources/pr43_7bd5962`, bound by `SOURCE_BINDING.json` to PR #43 commit `7bd5962bbb2020ce47fbe286adda7dfe02f9645d`, prefix `research/I05-W1-20260909-R2/`.
- Canonical statement: `sources/pr43_7bd5962/continuation/frozen_statement_v3.md`, version `v3.1`.

Imported external input D source:

- `sources/dependency_c3`, bound by `C1_SOURCE_BINDING.json` to PR #29 commit `648f1906468e3e548410f98a6b1a53a978f2ea11`, prefix `research/C3/`.
- Files used: `frozen_statement_v2.md` and `proof.md`.

PR43 proof files used:

- `proof/01_conditioning.md`
- `proof/02_two_point_input.md`
- `proof/03_lifting_and_exterior.md`
- `proof/04_diagonal_active_sector.md`
- `proof/05_exterior_markov.md`
- `proof/06_quantum_measurement_obstruction.md`
- `proof/07_markov_adjoint_and_reversible_obstruction.md`

External quantum-map source used only for checking the stated quasi-free channel hypothesis mapping:

- Dierckx, Fannes, and Pogorzelska, "Fermionic Quasi-free States and Maps in Information Theory", arXiv:0709.1061, especially Section 5.1 and Proposition 8.

Explicit exclusions:

- I did not use initial reviewer reports, other children reports, or `continuation/CONSISTENCY_AUDIT.md` as evidence.
- I did not assess novelty beyond recording that novelty is unassessed.
- I did not run full verifier replays, 256-event checks, LP searches, or infrastructure/publishing tasks.

Review questions:

- D: whether PR43 uses the imported diagonal-anchor theorem only within its actual hypotheses.
- I: arbitrary-rank diagonal active-sector theorem and the exact `3+5` analytic fixture, including original-coordinate and `t` versus `s=t^2` issues.
- J: per-conditional strict diagonal-anchor criterion and strictness of the anchor requirement.
- K: stationary density-adjoint Markov intertwining, continuous generator, full Fisher term, and the `2 I'' + I'` curvature identity.
- L: diagonal exterior-degree closure.
- M: reversible obstruction for the correlated two-point example, including the value `-125/78`.
- N: occupation-channel obstruction, including the `91/400` versus `99/400` event probabilities and its limited scope.

Verdict labels in `review_report.md`:

- Per claim: `CORRECT` or `CRITICAL_GAPS`.
- Overall scoped verdict: `ACCEPTED_SCOPED`, `NEEDS_FIX`, `REFUTED`, or `INCOMPLETE`.
