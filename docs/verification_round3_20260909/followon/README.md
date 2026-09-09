# Follow-on independent reviews: exact unit boundaries

These are completed reviews of specified source units, not acceptance of later additions to a rolling PR. Public copies replace only private source-directory/prohibited-workspace strings with repository-relative/general descriptions. Frozen status and historical findings remain unchanged; final reports and repair closures give the current verdict.

## PR53 original five files

The original five files at `e0688fbb713e55f93acf791b83437ddf2cc06b7f` have two independent scoped acceptances: [C1 first review](https://github.com/randomcat4/dpp-entropy-tools/blob/169696aba938424310a0dca781f90fb12ec1d8b2/research/C1-verification-round4-20260909/units/pr53/review_report.md), [C3 fresh second review](pr53_second/review_report.md) and [its frozen scope](pr53_second/frozen_scope.md).

Accepted in that unit: parity mutual-information identities with factor-two rate normalization, full-event determinant/Fisher/acceleration identities, strict-margin configuration-uniform inverse and finite-range exponential decay, and the fermionic beam-splitter reduction. The missing global signed curvature and occupation-Shannon inequality remain open; finite floating diagnostics are not proof.

An exact-head merge attempt did not merge because the author added `finite_range_local_theorem.md` at `abdd660a6c7761c7a8a53cb8671b4d2543530a5c` during the request. The original five files are unchanged. C1 is first-reviewing that new 473-line entropy-rate theorem; C3 reserves a fresh second. The original reviews do not certify the new theorem.

## PR54 three local/endpoint addenda

Frozen first/second source: `c3b9e968c0b4557546c7b10137ef4fff295338b4`. This unit includes the arbitrary-rank near-zero curvature appendix, simple-endpoint rare-event appendix, rank-two endpoint spectral appendix, and only the added endpoint-discriminant/root-separation part of the fixture.

- [First review](pr54_addenda_first/first_review_report.md) and [frozen scope](pr54_addenda_first/frozen_scope.md).
- [Independent exact endpoint plan](pr54_addenda_first/fixture_arithmetic_plan.md), [rational checker](pr54_addenda_first/check_endpoint_roots.py), and [actual output](pr54_addenda_first/fixture_endpoint_root_check.txt). It confirms the two exact discriminants and `rho_K<1/25<1/20<rho_I-K`.
- [Fresh second review](pr54_addenda_second/review_report.md), [frozen scope](pr54_addenda_second/frozen_scope.md), and [two wording repairs explicitly closed](pr54_addenda_second/correction_review.md) at `d5c55447a0f7377dae085b8074f557e4f673b5a4`.

The second required endpoint analytic extension through `b` for the abstract lemma and rational spectral-margin/norm substitutes for a rational radius. C3 implemented precisely those two paragraphs; the independent second reviewer closed both. DPP atom polynomials were sound throughout. Displayed formulas, the endpoint spectral appendix and code/output are unchanged. Whole-chord concavity, the compact middle interval and multiple/isotropic endpoints remain open.

## PR54 outer-wedge, visible-flow and rate appendix

Frozen source: `c8486bcdb18a85f93dd27930686cc1d4146804f5`, only `ADDENDUM_OUTER_WEDGE_FLOW_RATE.md` and its own checker/output. [First review](pr54_outer_wedge_first/review_report.md), [first frozen scope](pr54_outer_wedge_first/frozen_scope.md), [fresh second review](pr54_outer_wedge_second/review_report.md), and [second frozen scope](pr54_outer_wedge_second/frozen_scope.md) all preserve this separate unit. Neither reviewer ran a new LP, scout or symbolic job.

Accepted: full-event outer-wedge normal form, `W(s)>=0` as sufficient only, four-sign tilted-law identity and stochastic-order interface, any-visible-linear-operator obstruction for strict correlated two-point blocks with invertible feature frame, the exact Farkas witness, and the subextensive negative-W finite-Jensen rate criterion. The potentially signed expected contribution is `s^2 W(s)`; `W` itself is an expectation. Universal W positivity, hidden-state mechanisms and whole-chord concavity remain open. The two-point obstruction does not contradict the accepted fixed three-point nonreversible flow.

## PR54 original RESULT and source corrections

C1's original first review found three localized Section5 issues. C3's `a1e7f7208262565bb3db0509ff0cccffab757e98` fixes exactly those: explicit `I_n(0)=I_n'(0)=0`, `0<L<infinity`, and matching deficit distinguished from concave approximants. The [original first report](https://github.com/randomcat4/dpp-entropy-tools/blob/ca49694f4319059636fc5e2a2424bcf101cb8332/research/C1-verification-round4-20260909/units/pr54/review_report.md) is preserved next to [its exact repair closure](https://github.com/randomcat4/dpp-entropy-tools/blob/ca49694f4319059636fc5e2a2424bcf101cb8332/research/C1-verification-round4-20260909/units/pr54/section5_delta_review.md). The corrected original unit has now passed a separate [C3 fresh second review](pr54_original_second/review_report.md), with [its frozen scope](pr54_original_second/frozen_scope.md). PR54 final `d5c55447` is merged as `24ae88bf14b540b66490e3266a75849e6e258bad`; [complete accepted scope](../accepted_pr54.md). The addendum reviews above are not counted as that original-unit review.

Current queue: [third-round integration](../../verification_round3_20260909.md). C2 issue52 and its separately reviewed algebraic reduction remain a distinct computation lane; no general sign certificate is assumed here.

## C2 issue52 structural reduction: independent second audit

The C2 authored reduction at PR55 `de802933899b6a02e7c4fb8afc79e0b15564caba` has a separate [fresh C3 second analytic review](pr55_structure_second/review_report.md) and [frozen scope](pr55_structure_second/frozen_scope.md), following C2's first nonauthor review. The second used only the literal issue input and structural note, not either earlier review. It ran no arithmetic and did not duplicate the C2 machine job.

Accepted conditionally on the literal matrix `M=Fmat'+Q`: the polynomial/reflection Gram representation, fixed-physical-direction derivative followed by pointwise congruence, positive two-dimensional eliminated block, exact four-dimensional Schur form and negative-vector back-map. It also independently derives `det T=8u^4a^2b^2` and `det M=16 n1 n2 u^12 a^5 b^5 v w det Rstar`, with orientation `M_red=T^{-T} M T^{-1}`. The reviewer recommends including that orientation in the source note. These are algebraic identities, not a global sign certificate. The all-event machine gate and sign computation remain with C2; global Rstar/M positivity remains open.

The determinant/orientation recommendation is now implemented in source at `4bd0d615f6cfc44aea537ccfdc62cd8420b2d3ea`; the same independent second reviewer [closed the exact source delta](pr55_structure_second/source_delta_review.md). This closure is not a new reviewer and changes no global-sign status.

## PR53 Theorem FR: separate true entropy-rate theorem

The unchanged 473-line finite-range theorem at `abdd660a6c7761c7a8a53cb8671b4d2543530a5c` now has [C1 independent FIRST](https://github.com/randomcat4/dpp-entropy-tools/blob/a136a57316ce5e866588881b43ce561c0e25657c/research/C1-verification-round4-20260909/units/pr53_fr/review_report.md) and [C3 independent SECOND](pr53_fr_second/review_report.md), both ACCEPTED_SCOPED. [Second frozen scope](pr53_fr_second/frozen_scope.md). Neither review used finite-volume derivative extrapolation or new arithmetic. The first recommends a fixed weaker Hölder-norm clarification, direct RPF gap citation, and an s-linear heading correction; the second records a nonblocking source-list citation note. These findings remain visible.

Accepted: for real trigonometric polynomials c,g, with strict pointwise margin on c, c half-period invariant, g half-period anti-invariant and nonzero, there is a positive local interval on which the true rate `h(c+t g)+alpha_k t^4` is concave. The mean mu is arbitrary; for any nonzero odd Fourier coefficient, `alpha_k=|g_hat(k)|^4/[8 mu^2(1-mu^2)]`. This implies strict local concavity of h itself, with no explicit numerical interval promised. The Rudin-Shapiro example lies outside the earlier small-Wiener condition.

PR53 itself awaits separate first/second review of the exponential Wiener extension and its six companion changes. FR acceptance does not cover that extension, arbitrary measurable symbols or the whole legal interval. Broader novelty and formal verification remain unassessed.

FR source clarification at`ebecc412467939591e018a295a18c49a0a341ce9` has an explicit [closure by the same independent second](pr53_fr_second/source_delta_review.md). The historical comments above are preserved; this closure fixes the weaker-Hölder/RPF exposition and s-linear heading without changing theorem scope. C1 first-review delta closures and the separate EW second are tracked in the current queue.

PR55 has now merged as a [partial archive](../archived_pr55.md). Its new r=0 first remains INCOMPLETE; no certificate second or extra arithmetic was started after that unmet gate.

## PR53 Theorem EW: independent second and source-delta closure

The seven-file exponential-Wiener successor at`73cdbd09ad9aa975354a116a01f1e0f4955a8c27` has [C1 FIRST](https://github.com/randomcat4/dpp-entropy-tools/blob/aaac8a064cc72e513a97bb0f25736edab122bb6d/research/C1-verification-round4-20260909/units/pr53_ew/review_report.md) and [independent C3 SECOND](pr53_ew_second/review_report.md), both ACCEPTED_SCOPED. [Second frozen scope](pr53_ew_second/frozen_scope.md). It accepts arbitrary-mean strict exponential-Wiener half-period centers and nonzero half-period odd directions, with true local quartic strict entropy-rate concavity and no small-Wiener hypothesis. It does not establish the whole legal interval, arbitrary measurable symbols or arbitrary scalar chords.

The same independent second has [closed the precise three-file exposition delta](pr53_ew_second/source_delta_review.md) at`ebecc412467939591e018a295a18c49a0a341ce9`: exact far Schur inverse, fixed weaker Hölder norm/interpolation, primary RPF Hölder theorem and operator normalization, plus the inherited s-linear heading. No theorem quantifier, numerical constant, checker or output changed. C1's original first reviewers are separately closing their portions before final integration.

The second report's opening line count175 is a metadata typo, explicitly corrected to268 in its closure; its mathematical review and line anchors are unchanged. The closure directly checks primary Cioletti-Silva Theorem2.1 and its uniform-prior/log(2G_s) normalization. No arithmetic or first-review artifact was used by this second. The exact example script/output were statically reviewed only.
