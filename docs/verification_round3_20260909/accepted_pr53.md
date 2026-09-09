# PR53: accepted local entropy-rate concavity beyond small Wiener centers

Final source head: `ebecc412467939591e018a295a18c49a0a341ce9`. Merge: `717cdb1c6acc3f51de9e04c77ec4dc6d8baa3419`. All eleven author files are under `research/I05-DPP-21-20260909/`. The C1 first-review and final-closure packet at`02417b25a5202485386ff069b93af7a7f9cc1e6e` merged as`40d17f5c650a6259c54c9447e580b70f788c5714`. [Final source binding](../../research/C1-verification-round4-20260909/FINAL_PR53_SOURCE_BINDING.json), [complete review map](followon/README.md).

This page gives current acceptance. Historical author self-audit labels and earlier review handoff states remain in their frozen records; they do not override these final version-bound dispositions. Original bridges, Theorem FR and Theorem EW have separate independent first/second pairs. Source-clarification follow-ups do not count as extra reviewers.

## Exponentially weighted Fourier class: precise theorem

Let beta>0, and let c,g be real functions on the unit torus satisfying

`sum_j exp(beta abs(j)) (abs(c_hat(j))+abs(g_hat(j))) < infinity`,

`c(theta+1/2)=c(theta)`, `g(theta+1/2)=-g(theta)`, `g!=0`,

and a strict pointwise center margin `delta<=c<=1-delta` for some delta>0. No mean-one-half, reflection-evenness or small-Wiener-norm condition is imposed. Put `mu=integral c`. For any odd k>=1 with `g_hat(k)!=0`, define

`gamma_k=abs(g_hat(k))^2`,

`alpha_k=gamma_k^2/[8 mu^2(1-mu^2)] > 0`.

There exists epsilon>0 such that c+t g is legal and the **true entropy rate per single lattice coordinate** satisfies

`t -> h(c+t g)+alpha_k t^4` is concave on `[-epsilon,epsilon]`.

Thus h(c+t g) is strictly concave on every nontrivial subchord there. The proof gives an existing positive local interval, not an explicit numerical epsilon or a whole-legal-interval curvature theorem. [Theorem EW and proof](../../research/I05-DPP-21-20260909/exponential_wiener_extension.md).

Theorem FR is the finite-trigonometric-polynomial special case, with the same arbitrary-mean and no-smallness conclusions. It was separately frozen and double reviewed before the infinite-range extension; it is not counted as a separate generality gain from EW. [Finite-range proof](../../research/I05-DPP-21-20260909/finite_range_local_theorem.md).

## Why this is a rate theorem

The proof retains every complete configuration. Signed accretivity bounds every event inverse, including rare words. Banded inverse decay, then exponential Fourier truncation with a weighted Neumann series, gives a common complex inverse neighborhood independent of volume and configuration. The far-boundary Schur identity supplies exponentially local conditionals, converging holomorphically in one fixed weaker Hölder space.

The normalized full-shift RPF theorem is used in its Hölder setting. With the uniform binary prior and potential log(2G_s), the cited integral operator is exactly the proof's sum operator. Its simple isolated eigenvalue and Riesz projection provide analytic eigendata. The right-to-left finite chain rule has an O(1) boundary replacement error, so the entropy-rate formulas are established before differentiation. No derivative of H_n/n is exchanged with the volume limit.

Independently of analyticity, a disjoint odd-step matching and determinantal negative association give, for each fixed legal t,

`h(c)-h(c+t g) >= (1/2) d(mu^2-gamma_k t^2 || mu^2)`,

where d is binary relative entropy. This is an entropy-deficit bound on legal t. The analytic rate expansion and normalization eliminate the s-linear term for s=t^2; its quartic coefficient is at least `gamma_k^2/[4 mu^2(1-mu^2)]`. The local curvature conclusion then follows. The deficit inequality itself is not a whole-interval concavity proof.

## Exact example and scope comparison

The displayed Rudin-Shapiro example has mean1/2, strict margin `(7-4sqrt(2))/16`, `2||c-1/2||_W=15/8>1`, `g_hat(1)=1/128`, and `alpha=1/(3*2^27)`. It lies outside PR39's small-Wiener hypothesis. The exact integer/rational checker and recorded output were statically inspected by independent reviewers; no C1/C3 checker execution is claimed. The checker verifies Fourier constants and autocorrelation cancellation only, not entropy or rate curvature. [Checker](../../research/I05-DPP-21-20260909/code/check_rudin_shapiro_example.py), [author output](../../research/I05-DPP-21-20260909/output/rudin_shapiro_exact.json).

## Final reviews and corrections

- FR: [C1 first](../../research/C1-verification-round4-20260909/units/pr53_fr/review_report.md), [C3 second](followon/pr53_fr_second/review_report.md), [first clarification closure](../../research/C1-verification-round4-20260909/units/pr53_fr/clarification_ebecc412_review.md), [second clarification closure](followon/pr53_fr_second/source_delta_review.md).
- EW and all seven companions: [C1 first](../../research/C1-verification-round4-20260909/units/pr53_ew/review_report.md), [C3 second](followon/pr53_ew_second/review_report.md), [first clarification closure](../../research/C1-verification-round4-20260909/units/pr53_ew/clarification_ebecc412_review.md), [second clarification closure](followon/pr53_ew_second/source_delta_review.md).
- Original bridges: [C1 first](../../research/C1-verification-round4-20260909/units/pr53/review_report.md), [C3 second](followon/pr53_second/review_report.md). These accept the parity/likelihood/inverse and fermionic beam-splitter reduction only. The occupation-Shannon beam-splitter inequality is still unproved; a quantum von-Neumann inequality does not supply it.

The final three-file delta specifies weaker Hölder norms/interpolation, the exact far Schur inverse and primary RPF normalization, and fixes the s-linear heading. Theorem quantifiers, conclusions, constants and all code/output remain unchanged. Original reviewers separately closed each delta. The EW second's source-line count175 is a metadata typo explicitly corrected to268 in its closure; its mathematical verdict and line anchors are unchanged.

## Still outside acceptance

Whole-legal-interval concavity, the earlier PR39 example on its full `[-384,384]` interval, arbitrary measurable half-period symbols, arbitrary fixed scalar-symbol chords, and a true entropy-rate counterexample remain OPEN. Broader novelty/priority and new formal verification are unassessed. This result does not settle general finite real-symmetric DPP entropy concavity.
