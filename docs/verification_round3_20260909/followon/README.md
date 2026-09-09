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
