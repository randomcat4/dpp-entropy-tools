# PR43 v3.1 handoff-map supplement

Bounded update only. I inspected the local PR43 v3.1 snapshot at head
`7bd5962bbb2020ce47fbe286adda7dfe02f9645d`. `SOURCE.json` records previous
head `4e1369ef2a59ccfaba3ca8fce95d85e78857bf78` and says only continuation
Markdown declaration/index/task files changed. The substantive `proof/` files,
code, rational input JSON, and saved outputs are unchanged. This supplement does
not authorize a new numerical solve; C2 issue #45 retains the same frozen
numerical object.

## Current task-letter map

| Old v2 task from prior audit | Current v3.1 location | Current meaning |
|---|---|---|
| Old broad analytic review A | `research/I05-W1-20260909-R2/continuation/CODEX_VERIFICATION_TASKS_v2.md:7-106` | Expanded into review-layer split A-E, now including previously omitted three-point and related `3+3` proof files. |
| Old exact verifier task B | `research/I05-W1-20260909-R2/continuation/CODEX_VERIFICATION_TASKS_v2.md:108-121` | Current F, author scripts plus independent exact implementation. |
| Old reversible obstruction task C | `research/I05-W1-20260909-R2/continuation/CODEX_VERIFICATION_TASKS_v2.md:97-106` and `research/I05-W1-20260909-R2/continuation/CODEX_VERIFICATION_TASKS_v2.md:108-121` | Folded into current E/F as a mechanism-obstruction check, not a standalone LP. |
| Old nonreversible LP task D | `research/I05-W1-20260909-R2/continuation/CODEX_VERIFICATION_TASKS_v2.md:123-151` | Current G. This is the same fixed `C,V` LP/Farkas object, not a new computation. |
| Old strict entropy task E | `research/I05-W1-20260909-R2/continuation/CODEX_VERIFICATION_TASKS_v2.md:153-159` | Now the second paragraph of current G, conditional on LP feasibility. |
| Old counterexample search task F | `research/I05-W1-20260909-R2/continuation/CODEX_VERIFICATION_TASKS_v2.md:161-171` | Current H, search boundary. |
| Old delivery task G | `research/I05-W1-20260909-R2/continuation/CODEX_VERIFICATION_TASKS_v2.md:173-175` | Current I. |

## Interface issues fixed by v3.1 Markdown

1. The authoritative review list is now unambiguous: `HANDOFF.md:18-26` points
   to `CODEX_VERIFICATION_TASKS_v2.md` as the only review checklist and names
   the previously omitted proof files.

2. The handoff no longer asks for reversible conductances. It now says to use
   directed stationary flows and not reversible/symmetric conductances
   (`HANDOFF.md:28-39`).

3. The verifier-command mismatch is fixed in the task Markdown. Current F lists
   all three author script entries, including both continuation scripts
   (`CODEX_VERIFICATION_TASKS_v2.md:108-117`), and says their final lines should
   match the saved repository outputs (`CODEX_VERIFICATION_TASKS_v2.md:119-121`).

4. The missing-current-scope problem noted by the author-side consistency audit
   is fixed at the declaration level: `CONSISTENCY_AUDIT.md:25-35` says v3.1
   updates `RESULT_FINAL.md`, `frozen_statement_v3.md`, `proof_v3.md`,
   `README_v3.md`, `verification.md`, `CODEX_VERIFICATION_TASKS_v2.md`, and
   `HANDOFF.md`; `CONSISTENCY_AUDIT.md:37-43` says no substantive proof files,
   merge, or theorem expansion was added.

## Interface issues retained

1. The rational input JSON still carries the obsolete reversible LP field:
   `research/I05-W1-20260909-R2/continuation/inputs/rational_examples.json:34-45`
   still says
   `"reversible_conductance_variables": "w_xy=w_yx>=0 for unordered state pairs"`.
   Current G says the opposite: use directed stationary flows and do not impose
   `r_xy=r_yx` (`CODEX_VERIFICATION_TASKS_v2.md:137-151`). The task Markdown is
   now clear, but the machine-readable input remains stale.

2. The helper-generated LP payload is still stale because the code did not
   change. `continuation/code/verify_continuation.py:221-227` still writes
   `"conductances": "w_xy=w_yx>=0; ..."`, and
   `continuation/code/verify_continuation_v2.py:43-44` still calls that same
   writer. If C2 generates `inputs/generator_instance.json` from the helper and
   treats it as authoritative, it will solve the obsolete reversible LP. C2
   should follow current G's directed-flow equations instead.

3. The state-bit convention is still not frozen in the current task text.
   Current G gives fixed `C,V` but no state order or bit-to-coordinate mapping
   (`CODEX_VERIFICATION_TASKS_v2.md:123-151`). The unchanged JSON has state order
   `000,001,010,011,100,101,110,111`
   (`continuation/inputs/rational_examples.json:34-43`), while the helper labels
   rows with `reversed(bits(mask,3))`
   (`continuation/code/verify_continuation.py:18-19,208-214`). A C2 certificate
   should include its coordinate-to-bit convention so the author can check rows
   against the fixed `C,V`.

## Updated readiness note

The old-D/current-G LP remains actionable from the Markdown specification, but
only if C2 ignores the stale reversible JSON/helper field or documents that it
used current G as the source of truth. The task-letter rename does not change
the frozen numerical input, and it should not be treated as authorizing a new
solve or a different LP.
