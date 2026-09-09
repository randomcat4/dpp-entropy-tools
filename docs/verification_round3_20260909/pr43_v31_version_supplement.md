# PR43 v3.1 claim-map supplement

Status: **ACCEPTED_SCOPED** for the version-entry/interface map. This is not a mathematical acceptance of the PR43 theorems. The new frozen successor is PR43 head `7bd5962bbb2020ce47fbe286adda7dfe02f9645d`, with previous head `4e1369ef2a59ccfaba3ca8fce95d85e78857bf78` (`SOURCE.json:2-5`).

The prior report `dependency_version_map.md` is intentionally preserved verbatim. Its `NEEDS_FIX` finding was the v3 entry-point ambiguity around the three-point indefinite rank-two and correlated non-coordinate `3+3` files. The v3.1 declaration delta resolves that ambiguity at the claim-map level.

## Delta read

I compared the two frozen source manifests and inspected only the changed/added continuation Markdown documents. The delta is exactly 12 Markdown documents under `research/I05-W1-20260909-R2/continuation/`:

- `attempts_continuation.md`
- `CODEX_VERIFICATION_TASKS_v2.md`
- `CONSISTENCY_AUDIT.md`
- `frozen_statement_v3.md`
- `HANDOFF.md`
- `proof_v3.md`
- `proof.md`
- `README_v3.md`
- `RESULT_CONTINUATION.md`
- `RESULT_FINAL.md`
- `sources_continuation.md`
- `verification.md`

`CONSISTENCY_AUDIT.md:27-35` says the successor only updates scope/integration declarations, proof indices, verification summaries, review tasks, handoff/attempt notes, sources, and marks the old continuation result as historical. `CONSISTENCY_AUDIT.md:37-43` says it does not modify the mathematical proof files `04_three_point_indefinite_rank2.md`, `05_diagonal_and_feature_routes.md`, `06_correlated_3plus3_family.md`, does not add a theorem beyond those files, does not upgrade author checks to nonauthor review, and does not merge or repackage.

## Version-entry resolution

The old ambiguity is resolved by the new entry points:

- `README_v3.md:7-12` lists the current authority set and says `frozen_statement_v3.md` now includes the three-point indefinite rank-two theorem, exterior sufficient-statistic/Hessian material, the three-point condition criterion, and the correlated `3+3` family.
- `README_v3.md:17-24` explicitly lists these as current author-level continuation positive results or strict obstructions.
- `proof.md:3-16` states that the stable proof entrance is `proof_v3.md`, and specifically warns that the complete proof includes the early continuation files `proof/04_three_point_indefinite_rank2.md` and `proof/06_correlated_3plus3_family.md`.
- `proof_v3.md:3-18` gives a 10-item proof order covering all PR43 author-level claims and says no main theorem exists only in a summary.
- `RESULT_CONTINUATION.md:1-12` is now explicitly marked as a historical snapshot, replaced by `RESULT_FINAL.md`, `frozen_statement_v3.md`, `proof_v3.md`, and `CONSISTENCY_AUDIT.md`.
- `CODEX_VERIFICATION_TASKS_v2.md:3,17-29` now requires independent review of the previously omitted three-point, sufficient-statistic, and `3+3` files.

The previous `NEEDS_FIX` should therefore be closed as a documentation/version-entry issue at head `7bd5962bbb2020ce47fbe286adda7dfe02f9645d`. The remaining status is still **PARTIAL / independent proof review pending**, because v3.1 only fixes the map.

## Unified claim labels at v3.1

| Label | Current claim or role | Exact v3.1 declaration lines | Review/dependency mapping |
|---|---|---|---|
| Prior W1-R2 inputs | Conditional Schur/radial lift, `m x 2`, two observed-coordinate support, and rank-two exterior likelihood remain prior/second-round author material in this PR. | `frozen_statement_v3.md:8`; `RESULT_FINAL.md:15-38`; `proof_v3.md:5-7`. | Keep separate from new continuation claims. Existing reviewed PR32/38 scope does not automatically certify rewritten PR43 files. |
| D | External diagonal-anchor line concavity through a strict diagonal Hermitian contraction. | `frozen_statement_v3.md:10-18`; `RESULT_FINAL.md:11`; `sources_continuation.md:5-13`. | External accepted input only; PR43 uses it, does not reprove it. |
| E | Real three-point indefinite rank-two full-chord concavity. | `frozen_statement_v3.md:20-43`; `RESULT_FINAL.md:42-65`; `proof_v3.md:8`. | Live v3.1 PR43 author-level theorem. Semidefinite rank-two directions are excluded. |
| F | Rank-two exterior sufficient statistic and compressed Hessian with full Fisher plus one exterior scalar. | `frozen_statement_v3.md:45-88`; `RESULT_FINAL.md:67-92`; `proof_v3.md:9`. | Live v3.1 interface theorem/formula. It does not freeze a general high-dimensional sign theorem. |
| G | Three-point condition-direction criterion: each `M_S` is rank≤1, indefinite rank2, or lies on a line through a strict diagonal anchor. | `frozen_statement_v3.md:90-112`; `RESULT_FINAL.md:94-108`; `proof_v3.md:10`. | Live v3.1 sufficient condition; depends on Schur/radial lift, E, and D. |
| H | Correlated non-coordinate `3+3` rank-two structure family and explicit algebraic example. | `frozen_statement_v3.md:114-169`; `RESULT_FINAL.md:110-161`; `proof_v3.md:10`. | Live v3.1 theorem family. It exceeds `m x 2`, two-coordinate support, and one-side active diagonal coverage, but it is not the arbitrary `3+3` rank-two theorem. |
| I | Diagonal active-sector arbitrary cross-rank theorem. | `frozen_statement_v3.md:171-189`; `RESULT_FINAL.md:163-167`; `proof_v3.md:11`. | Live v3.1 theorem; depends on Schur/radial lift and D. |
| J | Per-condition-line diagonal-anchor criterion. | `frozen_statement_v3.md:191-205`; `RESULT_FINAL.md:163-167`; `proof_v3.md:11`. | Live v3.1 sufficient condition; depends on Schur/radial lift and D. |
| K | General rank-two exterior Markov density-adjoint intertwining and generator/Fisher interface. | `frozen_statement_v3.md:207-262`; `RESULT_FINAL.md:171-175`; `proof_v3.md:12-13`. | Live v3.1 conditional interface. The adjoint direction supersedes the older reversible-only formulation. |
| L | Diagonal-kernel exterior degree closure. | `frozen_statement_v3.md:264-282`; `proof_v3.md:12`; `verification.md:55-64`. | Support/exact-degree claim for the Markov route; not a replacement for D. |
| M | Reversible exterior semigroup obstruction via `-125/78`. | `frozen_statement_v3.md:284-299`; `RESULT_FINAL.md:177-190`; `proof_v3.md:13`. | Live v3.1 obstruction. It only rules out universal reversible exterior noise, not entropy concavity. |
| N | Quasi-free decay does not descend to a uniform classical occupation channel. | `frozen_statement_v3.md:301-318`; `RESULT_FINAL.md:192`; `proof_v3.md:14`. | Live v3.1 obstruction to a proof route; not a DPP concavity counterexample. |
| Open scope | General two-sided correlated, general non-coordinate rank-two radial concavity/counterexample remains open outside the G/H/I/J sufficient sectors. | `frozen_statement_v3.md:320-322`; `RESULT_FINAL.md:194-198`; `HANDOFF.md:16,61`. | Do not present PR43 as solving the general rank-two target. |

## Updated minimal second-review units after C1 first pass

1. **Three-point indefinite rank-two theorem E.** Review `proof/04_three_point_indefinite_rank2.md` against `frozen_statement_v3.md:20-43` and the checklist in `CODEX_VERIFICATION_TASKS_v2.md:31-46`. This is now a live claim and is a dependency for G/H.

2. **Rank-two exterior sufficient statistic and compressed Hessian F.** Review `proof/05_diagonal_and_feature_routes.md` against `frozen_statement_v3.md:45-88` and `CODEX_VERIFICATION_TASKS_v2.md:48-56`. Keep the full Fisher term and the “no general high-dimensional sign” boundary.

3. **Three-point condition criterion G plus correlated `3+3` family H.** Review after E. Use `frozen_statement_v3.md:90-169`, `RESULT_FINAL.md:94-161`, and `CODEX_VERIFICATION_TASKS_v2.md:58-95`. Split G from H if E or the Jacobi/inertia step becomes the failure point.

4. **Diagonal active sector I and per-condition anchor J.** Review `proof/04_diagonal_active_sector.md` against `frozen_statement_v3.md:171-205` and `CODEX_VERIFICATION_TASKS_v2.md:97-106`. This is the direct dependency-transfer unit from external D through Schur/radial lift.

5. **Markov density-adjoint K and reversible obstruction M.** Review the adjoint direction and the v2 correction together, then the `-125/78` obstruction separately if needed. Use `frozen_statement_v3.md:207-262,284-299`, `proof_v3.md:12-13`, and `CODEX_VERIFICATION_TASKS_v2.md:97-106,151-159`.

6. **Quasi-free obstruction N.** Review `proof/06_quantum_measurement_obstruction.md` only as a route obstruction, against `frozen_statement_v3.md:301-318` and `RESULT_FINAL.md:192`. It should not be elevated into a DPP entropy counterexample.

7. **Counterexample-search boundary.** If later search starts, exclude all already declared sufficient sectors: small block, two-coordinate support, diagonal active sector, G, and H, as required by `CODEX_VERIFICATION_TASKS_v2.md:161-171`.

## Head-bound conclusion

**ACCEPTED_SCOPED**: for PR43 successor head `7bd5962bbb2020ce47fbe286adda7dfe02f9645d`, the earlier version-entry `NEEDS_FIX` is resolved. The unified v3.1 map explicitly includes the root three-point indefinite rank-two theorem, rank-two sufficient-statistic/Hessian material, the three-point condition criterion, and the correlated non-coordinate `3+3` structure family as live PR43 author-level claims. No theorem is accepted by this supplement; all new PR43 claims remain pending C1/nonauthor mathematical review.
