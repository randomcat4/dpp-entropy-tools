# PR58 fresh first review report

STATUS: CRITICAL_GAPS

SCOPED VERDICT: INCOMPLETE for PR58 as a whole. The general full-law Cauchy compensation theorem, its interval-envelope corollary as a conditional analytic criterion, and the conditional-centering addendum are ACCEPTED_SCOPED. The fixed-fixture compact corridor and the `s=10` negative-`W`/positive-curvature claims remain INCOMPLETE pending an independent C2 exact reconstruction. This is a missing independent-computation status, not a discovered mathematical counterexample or a refutation of the author formulas. One source wording item needs repair: the phrase "strictly weaker than the sign condition" is not established as a logical implication.

## Source Binding

CORRECT / ACCEPTED_SCOPED. `source-snapshots/pr58/SOURCE_BINDING.json:2-39` freezes the intended four-file PR58 packet at head `1770ed29e8487b8f39aebb4c9466406c7493e580`, base `9dcb6e9079ca57f94e0e30d63161cda89ca61fae`, and prefix `research/I05-23-middle-20260909/`. The four files and line counts in `SOURCE_BINDING.json:10-37` match the requested review scope.

The accepted-input cache `source-snapshots/accepted_main/SOURCE_BINDING.json:2-39` binds the PR54 summary and the two PR54 source documents used here. I also read the PR54 fixture checker and output copied into this child directory from public base blobs listed in `main/base_tree.json`; those copies were used only to compare matrix literals and not to rerun or certify arithmetic.

## Accepted Inputs

CORRECT / ACCEPTED_SCOPED. PR58 uses PR54 as an input rather than reclaims it: `RESULT.md:16` identifies the accepted local-center, simple-endpoint, global deficit, outer-wedge, and visible-state-obstruction results as inputs. The accepted PR54 summary supports those dependency boundaries at `accepted_main/docs/verification_round3_20260909/accepted_pr54.md:7-29`, `:31-43`, and `:45-63`.

The outer-wedge normal form used by PR58 is source-bound to PR54: `accepted_main/research/I05-23-20260909/ADDENDUM_OUTER_WEDGE_FLOW_RATE.md:47-75` states the formula, the definitions of `Phi`, `psi`, and `W`, and that `W>=0` is only sufficient. The derivation keeps the full relative-entropy law and Fisher term at `:79-95`.

## Claim Review

| Claim | Status | Verdict | Review |
| --- | --- | --- | --- |
| Full-law Cauchy compensation, Theorem 3.1 | CORRECT | ACCEPTED_SCOPED | From accepted (1.1), PR58 defines `P`, `A2`, and `Rpsi` at `RESULT.md:74-83`. The weighted Cauchy-Schwarz step at `:98-103` has the right weights: `y/sqrt(q)` paired with `sqrt(q) psi`, so the factor is exactly `(1/2) sqrt(A2 Rpsi)` because `A2=4E[y^2/q]`. Substituting the lower sign into `RESULT.md:36` proves `:88-92`, conditional on accepted PR54. |
| "Strictly weaker than `W>=0`" wording | CRITICAL_GAPS | NEEDS_FIX | `RESULT.md:94` and `:142` call the new criterion strictly weaker than the sign condition. The proof only establishes a different sufficient condition and, after C2 confirms the finite example, that it can certify a case with negative `E[y psi]`. It does not prove the logical implication `W>=0 => (3.2)`. Rephrase to "a different compensation criterion that can apply when `E[y psi]<0`." |
| Rational interval envelope, Corollary 3.2 | CORRECT | ACCEPTED_SCOPED | The analytic envelope at `RESULT.md:106-140` is valid under its displayed interval hypotheses. `Phi(u)>=4u^2/q`, `q<=q_+`, `q>=q_-`, `|y|<=R^2|b|`, and `|psi|<=Psi` give `RESULT.md:120-128`; squaring the positive sides gives `:134-136`. This is an analytic criterion, not by itself a verification that the PR58 fixture satisfies the inequalities. |
| PR54 fixture source binding | CORRECT | ACCEPTED_SCOPED | The PR58 fixture literals at `RESULT.md:148-158` and script lines `verify_middle_compensation.py:11-25` match the accepted PR54 fixture checker copied from base at `verify_local_and_matching.py:15-29`. PR54's accepted checker also asserts `rank(B)=2`, all dense entries, non-coordinate null vectors, strict blocks, and exclusion from the PR43 special family at `verify_local_and_matching.py:62-77`, with corresponding saved output at `verify_local_and_matching.txt:1-5`. |
| Compact middle corridor `3<=t^2<=15`, Theorem 4.1 | CRITICAL_GAPS | INCOMPLETE | The proof reduces the claim to four interval certificates at `RESULT.md:216-224`, and the intervals cover `[3,15]` as stated at `:218-222`. But the load-bearing facts are exact extrema, moment lower bounds, and strict squared margins printed by the author script at `verify_middle_compensation.txt:5-24`. C1 was explicitly barred from arithmetic execution and independent reconstruction, so these exact inequalities are pending C2. |
| Legality from positive complete atoms | CORRECT, conditional on C2 margins | ACCEPTED_SCOPED after C2 | The inference at `RESULT.md:222-224` is correct if C2 confirms `q_->0` on all four intervals: strict PR54 block atoms give `mu>0`; positive `q_s` gives all complete joint atoms positive; summing atoms over supersets and disjoint sets gives positive principal minors of `K(t)` and `I-K(t)`. The only pending part is the exact `q_->0` arithmetic. |
| `W(10)<0` disproof of universal sign and positive total curvature | CRITICAL_GAPS | INCOMPLETE | PR58 states the log enclosure method at `RESULT.md:232-250` and distinguishes it from entropy curvature at `:254-258`. The saved output gives the asserted `min q`, `W(10)` interval, and `t^2 I''` interval at `verify_middle_compensation.txt:26-30`. Those signs are author-computed finite evidence; C1 cannot promote them to an independent disproof or curvature certificate. |
| Distinction between `W<0` and entropy/Jensen failure | CORRECT | ACCEPTED_SCOPED | The text correctly limits the consequence: `RESULT.md:252-258` says negative `W` refutes only the universal sufficient sign law and is not an entropy counterexample; `RESULT.md:286-291` repeats that the finite corridor is not a whole-interval or global-deficit argument. This logic is sound, with the actual sign example pending C2. |
| Remaining-gap statement | CORRECT | ACCEPTED_SCOPED | PR58 does not silently close the full problem. `RESULT.md:295-309` keeps the whole legal chord incomplete for both the fixture and general dense correlated rank-two blocks, and names the next finite/analytic obligations. This matches accepted PR54's limits at `accepted_pr54.md:29`, `:43`, `:63`, and `:71`. |
| Conditional-centering addendum | CORRECT | ACCEPTED_SCOPED | Lemma 1.1 is valid: fixed block marginals imply `sum_T p_C(T)q_s(S,T)=1` and the polynomial coefficients vanish on every fiber (`ADDENDUM_CONDITIONAL_CENTERING.md:17-41`). Theorem 2.1 uses the right weighted Cauchy-Schwarz form and conditional means under the normalized law `p_C q_s` (`:47-63`, `:93-113`). The variance identities and inequalities `R_S<=R_0`, `R_T<=R_0` have the correct finite-law weights at `:115-123`. The appendix correctly remains a sufficient criterion only at `:125-137`. |

## C2 Contract

The compact corridor and `s=10` claims should go to C2 as a bounded independent reconstruction, not as a replay of the PR58 author script.

Inputs:

- Frozen PR58 head `1770ed29e8487b8f39aebb4c9466406c7493e580`.
- PR58 files `source-snapshots/pr58/RESULT.md`, `ADDENDUM_CONDITIONAL_CENTERING.md`, `code/verify_middle_compensation.py`, and `output/verify_middle_compensation.txt`.
- Accepted PR54 fixture source from base blob `fb10a0431efdc1eff5fbe293e90acd15b1ef0a3e` and output blob `aab9c442be9331ea3a791d36f173f6fa952dba91`.

Required C2 checks:

1. Reconstruct the PR54 fixture independently from the matrix literals in `RESULT.md:148-158` and PR54 checker lines `15-29`; confirm `rank(B)=2`, strict `A,C`, dense `B`, non-coordinate null planes, and the PR54-special-family exclusion without relying on PR58's script.
2. Enumerate all 64 complete pairs and independently derive `mu`, `a=tr(G_A G_C)`, `b=det(G_A)det(G_C)`, `q_s=1-sa+s^2b`, and the zero means needed by the formulas.
3. For `[3,9]`, `[8,12]`, `[11,14]`, and `[14,15]`, compute exact quadratic extrema by endpoints plus the rational vertex when inside the interval; verify `q_->0`, `q_+`, `Psi`, `Ea2`, `Eab`, `Eb2`, the lower bound (4.2), and the strict squared margin (3.5).
4. At `s=10`, independently enclose every log using the displayed atanh series and rational remainder, then verify `min q>0`, `Wup<0`, `Tlo>0` for the full normal-form quantity, and the stated interval widths.
5. Compare C2's exact rationals or outward intervals against `verify_middle_compensation.txt:5-30`. If any event, interval endpoint, vertex, sign, or margin disagrees, report the first failing event/interval and downgrade Theorem 4.1 and the `W(10)` disproof to NEEDS_FIX or REFUTED as appropriate.

## Coverage Separation

General analytic proof: ACCEPTED_SCOPED for Theorem 3.1, Corollary 3.2 as a conditional criterion, and the conditional-centering appendix.

Static code: see `units/pr58/code_review.md`; no static implementation bug was found that changes the intended formulas, but the code is still author code.

Independent finite computation: INCOMPLETE. C1 did not run scripts or reconstruct rational/log certificates.

Formal coverage: INCOMPLETE / not claimed. No Lean, Coq, or other kernel proof is present in PR58.

Novelty: NOT_ASSESSED; the author makes no priority claim and this review performs no novelty certification.
