# PR54 Section 5 repair delta frozen scope

Reviewer: original first-pass reviewer, repair follow-up only.

Reviewed source object:

- New immutable source directory: `source-snapshots/pr54_a1e7f72`
- File: `research/I05-23-20260909/RESULT.md`
- Commit: `a1e7f7208262565bb3db0509ff0cccffab757e98`
- Parent: `c8486bcdb18a85f93dd27930686cc1d4146804f5`
- Blob: `39032f0df6913b4e2f2a57cfc2fcb459ffeacf15`
- Saved compare: `section5_repair.patch (exact patch extracted from public compare)`

Scope restrictions:

- This is not a second review of the original PR54 packet.
- This reviews only the one-file Section 5 repair delta against my original Section 5 findings in `review_report.md`.
- No later addenda, appended units, PR51, issue 52, outer-wedge/flow/rate units, or novelty/priority claims are reviewed here.
- The original `frozen_scope.md` and `review_report.md` are preserved unchanged.

## Frozen delta

The saved compare reports one modified file, `research/I05-23-20260909/RESULT.md`, with 7 additions and 4 deletions. The patch contains two hunks.

### Delta D1: missing initial relative-entropy derivative

Original lines:

- Old `RESULT.md` lines 856-865 stated the setup for Proposition 5.2 and assumed only the derivative bounds.
- Old `RESULT.md` line 891 then used `J_n(0)=0`.

New lines:

- New `RESULT.md` lines 856-867 now state:
  `Assume I_n(0)=I_n'(0)=0, as holds for the full relative entropy from the decoupled complete law.`
- New `RESULT.md` lines 884-893 retain the same proof step using `J_n(0)=0`.

Frozen question:

- Does the new explicit `I_n(0)=I_n'(0)=0` hypothesis close the original gap that `J_n(0)=2I_n'(0)` was used without being supplied?

### Delta D2: division by L in the radius

Original lines:

- Old `RESULT.md` lines 861-868 assumed `L<infinity` and then defined `delta` using `3c/(10L)`.

New lines:

- New `RESULT.md` lines 861-870 assume `0<L<infinity` before defining `delta=min{delta0,3c/(10L)}`.

Frozen question:

- Does requiring `0<L<infinity` close the original division-by-zero/convention issue?

### Delta D3: boundary-remainder wording

Original lines:

- Old `RESULT.md` lines 931-939 stated the concave-approximant boundary-remainder variant and ended: `The matching construction in Theorem 2.4 realizes this principle directly with the explicit boundary loss |d|/n.`

New lines:

- New `RESULT.md` lines 933-942 state the same concave-approximant variant but replace the final sentence with:
  `Theorem 2.4 uses the same boundary-normalization logic for the quartic deficit, with the explicit loss |d|/n; it does not by itself supply concave approximants satisfying (5.8).`

Frozen question:

- Does this revised wording avoid claiming that the matching theorem constructs concave approximants, while preserving the valid boundary-normalized quartic deficit passage?

## Frozen non-delta limits

The following remain outside this repair closure:

- Whether the later appended units are correct.
- Whether the unproved uniform `I_n'''=O(n)` hypothesis can be established.
- Whether Section 5 yields a necessary condition. It is only a sufficient criterion.
- Whether the quartic deficit implies chord concavity. It does not.
- Broad novelty or priority.
