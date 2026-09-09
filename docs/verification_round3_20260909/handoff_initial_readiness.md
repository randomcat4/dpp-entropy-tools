# Round 3 handoff execution-readiness audit

Reviewer scope: bounded execution-readiness review only. I inspected local source
snapshots for PR41 and PR43, their `SOURCE.json` files, handoff/task documents,
and code/input interfaces. I did not run mathematical jobs, audit the proofs, or
duplicate C2's implementation audit.

## Frozen sources

| PR | Head | Local snapshot completeness |
|---|---:|---|
| PR41 | `6fd61dcd299417fc3a4eab3af682c03dd816b670` | `SOURCE.json` present; 13 files listed under `research/N3/round3/I05-W4-20260909/round2/`. |
| PR43 | `4e1369ef2a59ccfaba3ca8fce95d85e78857bf78` | `SOURCE.json` present; 62 files listed under `research/I05-W1-20260909-R2/`. |

Path prefixes used below:

- PR41: `research/N3/round3/I05-W4-20260909/round2/`
- PR43: `research/I05-W1-20260909-R2/`

## Readiness table

| Source task | Intended owner | Readiness | Reason |
|---|---|---|---|
| PR41 `HANDOFF.md` task A, independent R2-T1 review (`research/N3/round3/I05-W4-20260909/round2/HANDOFF.md:5-27`) | C1/proof reviewer | Not a C2 computation job | It asks for independent mathematical reconstruction and proof review. It has exact objects and pass criteria, but no finite computation deliverable beyond author-side symbolic checks. |
| PR41 `HANDOFF.md` task B, R2-T2/general missing-edge review (`.../HANDOFF.md:28-49`) | C1/proof reviewer | Not a C2 computation job | Same issue: proof review and formula audit, with an explicit warning not to upgrade the unproved `6x6` Schur complement inequality. |
| PR41 author verifier (`.../code/verify_symbolic.py:321-335`, `.../inputs/exact_inputs.json:1-33`) | C2 optional cross-check | Ready only as a finite cross-check | Inputs and exact checks are specified, but `HANDOFF.md:50-52` says simple rerun is not independent review. C2 can safely claim only an independent exact reimplementation/cross-check, not theorem certification. |
| PR43 old `CODEX_TASKS.md` A (`research/I05-W1-20260909-R2/CODEX_TASKS.md:5-20`) | C1/proof reviewer | Not a C2 computation job | Independent theorem review; no computation handoff beyond exact reconstruction. |
| PR43 old `CODEX_TASKS.md` B, related `3+3` exact recomputation (`.../CODEX_TASKS.md:22-35`, `.../inputs/continuation_fixture.json:1-35`) | C2 | Mostly ready finite cross-check | Exact fixture, checks, two diagnostic `t` values, and 100-digit diagnostic requirement are specified. It lacks runtime/checkpoint expectations, but the job is finite and self-contained. It should not certify the theorem. |
| PR43 old `CODEX_TASKS.md` C, high-dimensional `Lambda<0` search (`.../CODEX_TASKS.md:36-52`) | C2/search | Not ready | It gives target dimensions and certificate standard but no parameterization, search box, sample budget, seed, optimizer, timeout, or stopping criterion. |
| PR43 old `CODEX_TASKS.md` D, general rank-two counterexample threshold (`.../CODEX_TASKS.md:54-68`) | C2/search | Not ready | It says "fixed rational `A,C,B`" but does not provide them. No search box, candidate source, or recovery/checkpoint plan is specified. |
| PR43 `HANDOFF.part01.md` task 1, weighted conditional concavity/反例 (`.../HANDOFF.part01.md:5-37`) | Theory/C1 first | Not ready for C2 | It quantifies over arbitrary `C,V,G` and asks for proof or strict rational反例. No fixed finite instance or parameter box is given. |
| PR43 `HANDOFF.part01.md` task 2, graded block-noise channel/Farkas (`.../HANDOFF.part01.md:38-67`) | Superseded/needs version choice | Not ready as written | It asks "for any" block marginal and `U`; the finite `A,U` is to be found by the executor. Later v2 tasks replace the reversible-priority part, so this should not be claimed without author clarification. |
| PR43 continuation `HANDOFF.md` task 1, exact Markov generator (`research/I05-W1-20260909-R2/continuation/HANDOFF.md:15-27`) | C2/LP | Needs version fix before relying on handoff text | It asks for "reversible conductance" language, while `CODEX_VERIFICATION_TASKS_v2.md:67-116` changes the task to nonreversible directed stationary flows and explicitly says not to impose `r_xy=r_yx`. |
| PR43 continuation `CODEX_VERIFICATION_TASKS_v2.md` B, exact verifier and independent implementation (`.../continuation/CODEX_VERIFICATION_TASKS_v2.md:31-49`) | C2 finite verification | Ready with one command/version question | Exact objects are listed. However `proof_v3.md:15-20` says to run both `verify_continuation.py` and `verify_continuation_v2.py`, while v2 tasks list only the older command and older success line. |
| PR43 continuation v2 C, reversible obstruction `-125/78` (`.../continuation/CODEX_VERIFICATION_TASKS_v2.md:50-66`) | C2 small exact check or C1 proof note | Ready | Fixed `C,V`, exact event law, exact moment, and proof obligation are specified. This is a safe finite job. |
| PR43 continuation v2 D, nonreversible stationary-flow LP/Farkas (`.../continuation/CODEX_VERIFICATION_TASKS_v2.md:67-116`) | C2/LP | Text is mathematically actionable; interface has a concrete mismatch | The v2 document gives fixed `C,V`, state order, directed flow variables, balance equations, four eigenfunction equations, and exact rational feasible/Farkas outcomes. But the checked-in JSON and helper-generated LP payload still advertise reversible conductances; see mismatch details below. |
| PR43 continuation v2 E, full-interval entropy-dissipation certificate if D feasible (`.../continuation/CODEX_VERIFICATION_TASKS_v2.md:118-159`) | C2 strict entropy | Await C2/author clarification | C2 has already raised the boundary-zero and `1e-20` interpretation questions. I do not duplicate those here. |
| PR43 continuation v2 F, true `3+3` counterexample search (`.../continuation/CODEX_VERIFICATION_TASKS_v2.md:160-189`) | C2/search | Await C2/author clarification | C2 has already raised the missing finite-candidate/search-box issue. I do not duplicate it here. |
| PR43 continuation v2 G delivery (`.../continuation/CODEX_VERIFICATION_TASKS_v2.md:191-193`) | C2 | Good delivery checklist | Commit, environment, threads, command, exit code, exact input, machine-readable certificate, and failure object are requested. |

## Additional concrete contract issues

1. PR43 D has a version/interface mismatch that can change the LP. The latest
   v2 task says to use directed stationary flows
   `r_xy=mu(x)q_xy>=0` and explicitly says not to impose `r_xy=r_yx`
   (`continuation/CODEX_VERIFICATION_TASKS_v2.md:89-116`). But the handoff still
   asks for "reversible conductance" output (`continuation/HANDOFF.md:15-27`),
   `rational_examples.json` still names
   `"reversible_conductance_variables": "w_xy=w_yx>=0 for unordered state pairs"`
   (`continuation/inputs/rational_examples.json:34-45`), and the helper that
   writes the LP interface still emits
   `"conductances": "w_xy=w_yx>=0; ..."` (`continuation/code/verify_continuation.py:221-229`;
   `continuation/code/verify_continuation_v2.py:43-44` calls the same writer).
   If C2 uses the generated JSON/interface as the source of truth, it will solve
   the obsolete reversible LP. The public task should explicitly say v2 text
   overrides those stale interface fields, or the fields should be updated.

2. PR43 D should freeze the state-bit convention for the order
   `000,001,010,011,100,101,110,111`
   (`continuation/CODEX_VERIFICATION_TASKS_v2.md:81`). The helper labels states
   by `reversed(bits(mask,3))`, so the rightmost character corresponds to matrix
   row/coordinate 1 (`continuation/code/verify_continuation.py:18-19,208-214`).
   The task text lists the state order but not this coordinate convention. This
   does not change the abstract LP if every row is relabeled consistently, but it
   can make an external certificate fail to match the author's `C,V` rows.
   Please freeze the convention in the task or require the certificate to include
   its coordinate-to-bit map.

3. For PR43 v2 exact verification, should C2 run both commands listed in
   `proof_v3.md:15-20`, or only the older command listed in
   `continuation/CODEX_VERIFICATION_TASKS_v2.md:33-40`? If both, please update
   the expected terminal success lines to include
   `ALL CONTINUATION V2 CHECKS PASSED`.

4. For PR43 old `CODEX_TASKS.md:54-68`, are there intended fixed rational
   `A,C,B` objects? The text says they are fixed but does not provide them. If
   this is superseded by v2 F, please mark it superseded.

5. For PR41, should C2 do any finite computation at all, or should PR41 be routed
   entirely to C1-style proof review? `HANDOFF.md:50-52` says rerunning
   `code/verify_symbolic.py` is not independent review. A safe C2 scope would be
   an independent exact reimplementation against `inputs/exact_inputs.json`,
   reported only as a cross-check.

## Minimal finite jobs C2 can safely claim now

1. PR43 v2 C reversible obstruction: compute `mu=p_C`, all four
   `G(T)=(C-E_{T^c})^{-1}`, `d(T)=det G(T)`, verify
   `<d,G12>_mu=-125/78`, and attach the two-line self-adjoint eigenfunction
   orthogonality argument. Scope: mechanism obstruction only, not entropy
   counterexample.

2. PR43 v2 D nonreversible LP assembly/solve, using v2 task text rather than the
   stale reversible interface fields: build the exact rational linear system for
   directed stationary flows in state order `000,001,010,011,100,101,110,111`;
   return either a rational feasible flow table or rational Farkas certificate,
   with an explicit coordinate-to-bit map.

3. PR43 v2 B finite independent implementation, after command/version
   clarification: independently reconstruct complete event probabilities from
   inclusion determinants for the listed `3+5`, diagonal-refresh, quasi-free,
   and reversible-obstruction checks. Scope: exact finite implementation
   cross-check, not proof certification.

4. PR43 old `CODEX_TASKS.md` B: independently recompute the fixed
   `continuation_fixture.json` structural claims and the two high-precision
   diagnostic curvature values. Scope: exact fixture validation and diagnostic
   consistency only.

5. PR41 optional exact symbolic cross-check: independently implement the finite
   event-polynomial and input-manifest checks corresponding to
   `code/verify_symbolic.py` and `inputs/exact_inputs.json`. Scope: cross-check
   of the author interface only; the R2-T1/R2-T2 theorem review remains C1.

## Readiness conclusion

PR43 v2 contains one genuinely C2-ready finite obstruction check and one
actionable exact LP/Farkas job, provided C2 follows the v2 directed-flow text
instead of the stale reversible JSON/helper interface. PR41's handoff is
primarily for independent proof review; C2 should only claim narrowly scoped
finite cross-checks unless the author freezes a computation-specific task.

