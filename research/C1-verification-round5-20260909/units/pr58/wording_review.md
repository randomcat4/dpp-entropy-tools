# PR58 wording-repair first review

Role: bounded non-author FIRST review of PR58 wording-only repair head `7d3dd405faea365e3ddcfd8c1b6f38ae47e34387` against additive parent `a4f05cc962985015b71635bf633acce9dfe76866`.

Overall wording-repair status: CORRECT.

Scoped verdict: ACCEPTED_SCOPED for the two repaired `RESULT.md` sentences. The repair closes the prior wording-specific NEEDS_FIX finding, without changing any additive, code, output, finite-evidence, formal-coverage, or novelty status.

## Source binding

CORRECT / ACCEPTED_SCOPED. The repair binding identifies commit `7d3dd405faea365e3ddcfd8c1b6f38ae47e34387` at `source-snapshots/pr58_wording_repair/SOURCE_BINDING.json:2`, binds exactly one changed file at `source-snapshots/pr58_wording_repair/SOURCE_BINDING.json:3`-`10`, and states the scope as "Two wording replacements only; formulas, code, output and additive delta unchanged" at `source-snapshots/pr58_wording_repair/SOURCE_BINDING.json:12`. The parent head is `a4f05cc962985015b71635bf633acce9dfe76866` at `source-snapshots/pr58_wording_repair/SOURCE_BINDING.json:13`.

## Repaired sentence 1: old line 94

Status: CORRECT.

Scoped verdict: ACCEPTED_SCOPED.

The old sentence in the compare hunk beginning `@@ -91,7 +91,7 @@` said: `This criterion is strictly weaker than the sign condition W>=0: it can hold with E[y psi]<0.`

The new bound source at `source-snapshots/pr58_wording_repair/RESULT.md:90`-`94` now says that (3.2) is a sufficient condition and that it is a different sufficient criterion which can hold with `E[y psi]<0`; it explicitly says no logical implication from `W>=0` to (3.2) is claimed.

This directly fixes the original wording defect. The proof supports a Cauchy compensation sufficient condition, not the logical statement that `W>=0` implies (3.2) or that the criterion is strictly weaker in that order.

## Repaired sentence 2: old line 142

Status: CORRECT.

Scoped verdict: ACCEPTED_SCOPED.

The original report grouped this with the same comparison issue, but the old line 142 was textually distinct. It did not repeat the exact "strictly weaker" phrase; the compare hunk beginning `@@ -139,7 +139,7 @@` shows it said: `This is a genuine compensation criterion: unlike W>=0, it pays for a negative signed term using the retained full Fisher/quadratic contribution.`

The new bound source at `source-snapshots/pr58_wording_repair/RESULT.md:138`-`142` keeps the valid compensation interpretation while adding the missing limitation: the displayed sufficient inequality must still be verified.

This fixes the overstatement without changing the formula. The corrected sentence no longer suggests that the compensation bound is automatically certified by contrast with `W>=0`; it says the bound controls the negative signed term and leaves the displayed inequality as a separate condition.

## Remaining scope

This wording repair does not close any finite-evidence obligation. The original compact-corridor verification and the additive-delta `s=9/10` finite witness still require independent C2 exact reconstruction before their strict finite signs can be promoted from author evidence to independently verified theorem evidence.

Formal coverage remains INCOMPLETE for finite computations. Novelty remains NOT_ASSESSED.
