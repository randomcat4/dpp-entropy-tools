# PR58 delta first review report

Role: fresh non-author FIRST delta reviewer for PR58 new head `a4f05cc962985015b71635bf633acce9dfe76866` against frozen prior head `1770ed29e8487b8f39aebb4c9466406c7493e580`.

Overall delta status: CRITICAL_GAPS.

Later wording-repair note: PR58 head `7d3dd405faea365e3ddcfd8c1b6f38ae47e34387` separately repairs the two original `RESULT.md` wording findings. See `wording_review.md`. That wording closure does not change this additive-delta report's INCOMPLETE finite-evidence findings.

Scoped verdicts:

- ACCEPTED_SCOPED: the joint-additive projection identity, the two-margin Cauchy sufficient criterion, the normal-equation framework up to the line-noted typo, the rank-at-most-four reduction, and the limited Erbar-Maas comparison.
- NEEDS_FIX: one literal formula/domain error in the normal-equation discussion: `source-snapshots/pr58_delta/ADDENDUM_JOINT_ADDITIVE.md:99` gives the operator norm as `||K_s||_{U\to U}<1`, while `K_s` was defined as mapping right zero-mean functions to left zero-mean functions at `source-snapshots/pr58_delta/ADDENDUM_JOINT_ADDITIVE.md:73`-`77`. The corrected text should say `||K_s||_{V\to U}<1`, or simply `||K_s||<1` after the domains have been fixed.
- INCOMPLETE: the finite strict witness at `s=9/10`, including the claimed failure of the joint-additive sufficient criterion, `W(9/10)<0`, and positive `t^2 I''` hence negative entropy `H''`, remains pending independent C2 exact reconstruction.
- NOT_ASSESSED: novelty. The author makes no priority claim in the delta packet, and this review performs no novelty certification.

For additive head `a4f05cc962985015b71635bf633acce9dfe76866`, the original four-file PR58 review findings were unchanged. The later wording-only repair at head `7d3dd405faea365e3ddcfd8c1b6f38ae47e34387` is closed separately in `wording_review.md`.

## Source binding

CORRECT / ACCEPTED_SCOPED. The delta packet binding identifies the new commit, file count, and review scope at `source-snapshots/pr58_delta/SOURCE_BINDING.json:2`-`4`. It binds exactly three added source artifacts with blobs and line counts at `source-snapshots/pr58_delta/SOURCE_BINDING.json:6`-`22`, and records the previous frozen base and repository prefix at `source-snapshots/pr58_delta/SOURCE_BINDING.json:26`-`28`. The compare metadata line confirms this is a three-addition delta against the prior frozen head. I treated the saved checker output as author evidence only, consistent with the binding scope statement at `source-snapshots/pr58_delta/SOURCE_BINDING.json:4`.

## Claim review

| Delta claim | Status | Scoped verdict | Source lines | First-review conclusion |
| --- | --- | --- | --- | --- |
| Exact two-margin projection and Cauchy criterion | CORRECT | ACCEPTED_SCOPED | `source-snapshots/pr58_delta/ADDENDUM_JOINT_ADDITIVE.md:19`-`63` | The derivation is formally coherent. With `h=y/q_s`, the fixed-marginal identities make `h` orthogonal to all additive functions under `P_s`; therefore `E_mu[y psi]=E_{P_s}[h(psi-f-g)]`. Cauchy gives the stated sufficient lower bound with the factor `1/2 sqrt(A2 R_add)`, since `A2=4 E_{P_s}h^2`. |
| Relationship to one-sided conditional centering | CORRECT | ACCEPTED_SCOPED | `source-snapshots/pr58_delta/ADDENDUM_JOINT_ADDITIVE.md:61`-`63` | The joint-additive residual cannot exceed a one-sided residual because the additive subspace contains the left-only and right-only subspaces. This supports only the stated sufficient-test comparison, not a necessity theorem. |
| Normal equations and residual value formula | CRITICAL_GAPS | NEEDS_FIX for one formula; ACCEPTED_SCOPED after correction | `source-snapshots/pr58_delta/ADDENDUM_JOINT_ADDITIVE.md:65`-`105` | The gauge choice, conditional-expectation equations, and residual formula are correct in structure. The strict-contraction argument is also sound under full Cartesian support. The line `||K_s||_{U\to U}<1` is a literal domain error because `K_s:V\to U`; fix line 99 before treating the addendum as polished. |
| Rank-at-most-four DPP reduction | CORRECT | ACCEPTED_SCOPED | `source-snapshots/pr58_delta/ADDENDUM_JOINT_ADDITIVE.md:107`-`132` | The displayed formula for `K_s g` follows from `q_s=1-sa+s^2b` and `E_{p_C}g=0`. Its image is contained in the span of the three entries of `G_A(S)` and `det G_A(S)`, so the claimed rank bound is valid; the adjoint statement follows symmetrically. |
| Standalone rational `3+3` witness at `s=9/10` | CRITICAL_GAPS | INCOMPLETE pending C2 | `source-snapshots/pr58_delta/ADDENDUM_JOINT_ADDITIVE.md:134`-`231`; `source-snapshots/pr58_delta/output/verify_joint_additive_failure.txt:1`-`11` | The packet gives a concrete matrix fixture, an integer additive-annihilating dual table, and author output claiming strict residual and curvature inequalities. I did not run arithmetic, SymPy, interval checks, or a fresh enumeration. These finite signs remain author evidence, not independently verified theorem evidence. This is an evidence-status gap, not a discovered mathematical refutation. If C2 confirms the witness, it shows failure and non-necessity of the joint-additive sufficient criterion despite favorable entropy curvature, namely positive `t^2 I''` and hence negative entropy `H''`. |
| `W<0` versus positive `t^2 I''` | CRITICAL_GAPS | INCOMPLETE pending C2 | `source-snapshots/pr58_delta/ADDENDUM_JOINT_ADDITIVE.md:213`-`231`; `source-snapshots/pr58_delta/output/verify_joint_additive_failure.txt:6`-`11` | The addendum explicitly distinguishes `W(9/10)<0` from the asserted positive `t^2 I''`, which corresponds to negative entropy `H''` under the paper's sign convention. I found no contradiction in that distinction at the source-proof level, but the strict numeric signs depend on the same finite exact reconstruction as the witness. |
| Erbar-Maas comparison | CORRECT | ACCEPTED_SCOPED | `source-snapshots/pr58_delta/ADDENDUM_JOINT_ADDITIVE.md:233`-`245` | The comparison is limited and negative: it says the Erbar-Maas framework is not a black-box substitute for the present radial hidden-state curvature proof. A primary-source spot check of Erbar-Maas, [arXiv:1111.2687v2](https://arxiv.org/html/1111.2687v2), confirms the paper works with finite Markov-chain entropy geometry under its own reversible/geodesic setup. The addendum makes no broader priority or novelty claim here. |
| Remaining whole-chord task | CORRECT | INCOMPLETE as explicitly scoped | `source-snapshots/pr58_delta/ADDENDUM_JOINT_ADDITIVE.md:247`-`251` | The addendum leaves the complete legal-chord computation to a separate long exact task. This reviewer does not promote that future target to a completed result. |

## C2 handoff contract for the finite witness

C2 should reconstruct the finite witness independently, without trusting `source-snapshots/pr58_delta/code/verify_joint_additive_failure.py` or its saved output as proof. The required deliverable is an exact, fresh enumeration with a mismatch report if any author value fails.

The independent reconstruction should:

1. Re-enter the matrices `A`, `C`, `U`, `V`, `B` from `source-snapshots/pr58_delta/ADDENDUM_JOINT_ADDITIVE.md:136`-`163`, with `s=9/10` from `source-snapshots/pr58_delta/ADDENDUM_JOINT_ADDITIVE.md:165`-`169`.
2. Verify strict legality: `0<A<I`, `0<C<I`, rank two, dense nonzero cross block, and strict validity of both `K_s` and `I-K_s` for the full six-point block kernel.
3. Enumerate all `64` complete events and independently derive `p_A`, `p_C`, `G_A`, `G_C`, `a`, `b`, `q_s`, `y`, `Phi`, `psi`, `A2`, `P0`, `W`, and true `t^2 I''` with exact rational or certified interval arithmetic.
4. Verify the integer dual table at `source-snapshots/pr58_delta/ADDENDUM_JOINT_ADDITIVE.md:171`-`182`, including the row and column zero-sum annihilation claims at `source-snapshots/pr58_delta/ADDENDUM_JOINT_ADDITIVE.md:184`-`188`.
5. Prove the dual residual lower bound from `source-snapshots/pr58_delta/ADDENDUM_JOINT_ADDITIVE.md:190`-`203`, then compare it to the independently computed criterion threshold from `source-snapshots/pr58_delta/ADDENDUM_JOINT_ADDITIVE.md:205`-`211`.
6. Separately certify the strict signs `W(9/10)<0` and true `t^2I''>0` asserted at `source-snapshots/pr58_delta/ADDENDUM_JOINT_ADDITIVE.md:213`-`223`.
7. Confirm that all complete events and all Fisher/entropy-acceleration terms are included; if any event, denominator, interval endpoint, or strict margin differs from the author packet, report the first mismatch and leave the finite claim unaccepted.

## Separation of review categories

General analytic proof: ACCEPTED_SCOPED, except for the line 99 domain typo.

Static code review: see the separate delta code review; no blocking implementation defect was found by static inspection.

Independent finite computation: INCOMPLETE. No independent finite reconstruction was performed in this C1 delta review.

Formal coverage: INCOMPLETE. The delta packet contains author script checks, not a formal proof artifact.

Novelty: NOT_ASSESSED. No priority claim is certified by this report.
