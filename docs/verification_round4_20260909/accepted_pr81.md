# PR81 — fixed half-leaf family closed by shared-corner analysis

Status: **ACCEPTED_SCOPED**, frozen `1e2081d374edeca1533c05356afa38e052f9f78e`. Original,92c1,d995 and1e20 source/delta FIRST and isolated SECOND reports are complete and fully read. The three d995 source files are unchanged at the final head. This closes the specified fixed shape and strict sufficient families, not general real three-point entropy concavity.

## Accepted mathematical result

For every `0<q<11/36`, the real strict kernel

```text
K(q) = [[1/2, 0,   1/4],
        [0,   1/2, 1/3],
        [1/4, 1/3, q+25/72]]
```

has strictly negative complete-configuration Shannon Hessian in every nonzero real symmetric physical direction D: `-H''(K(q);D)>0`. The corresponding positive-pivot core satisfies `E_H>0` and `det E_H>0`. Diagonal sign conjugations of the two cross entries are covered. Endpoints are used only for continuous comparison; they are not included as strict legal kernels.

The proof retains all eight complete atoms, full Fisher information, every acceleration and marginal term, and all six physical directions. For general strict connected half-leaf arrows with `b²=A/4`, `c²=B/4`, `z=q+(A+B)/2`, the rectangle integral

`J = ∫₀ᴬ ∫₀ᴮ [ (q+s+t)(1-q-s-t) ]⁻¹ dt ds`

gives a sufficient condition `J<12AB`. The one-edge inverse-root lemma for `f-3`, where `f(t)=1/[t(1-t)]`, yields the shared-corner cell margin `3/8-J/(32AB)`. A positive marginal block and four completed edge squares then force strictness in every nonzero physical direction.

For the specified A=1/4,B=4/9, symmetry and strict convexity of J, followed by elementary exponential/logarithm bounds, give `J(q)<13/10<4/3=12AB` on the complete legal open interval. This is an analytic continuum proof, including nonzero-Lambda points; no finite scan is used. The displayed positive-square form Qstar proves qualitative uniform coordinate coercivity by its zero-space argument, without using its printed large-rational principal minors.

The final refinement uses the actual optimal edge coefficient

`κ(u,s) = [f(u)f(u+s)-(h/s)²] / [8(f(u)+f(u+s)-2h/s)]`,

where `h=logit(u+s)-logit(u)`. Combining opposite edges gives parallel coefficients K_A and K_B. The strict condition `K_A+K_B>J/(32AB)` also proves the full six-direction result and recovers the coarse condition above. The universal non-strict inequality and equality-surface closure remain open. The four coefficients and J must come from the same physical rectangle.

The original paired-logit/four-scalar compression, complete Fisher/Schur reductions, imbalance identities, Gram restrictions and actual common-corner constraints retain their scoped analytic status. Their earlier fixed-shape OPEN wording is historical and is superseded only by the d995 fixed-shape proof. Relaxed scalar negative determinants are not physical DPP counterexamples.

## Uncertified and open scope

Large-rational relaxed determinants, principal minors, derivative fractions, the printed alpha bound, author script assertions, direct fixed spot comparisons and PASS output remain **SOURCE_ONLY / PENDING**. They were neither executed nor independently reconstructed. The checker mainly tests the earlier shared-corner algebra and fixed-shape examples; it is not a machine certificate for the final optimal-edge refinement. Its internal “independent reconstruction” means same-author reconstruction only.

No new C2 contract, mathematical execution, determinant/log/entropy recomputation, precision change, interval subdivision or issue73 run was performed. General half-leaf cases outside the strict criteria, unequal leaf diagonals, general missing-edge determinants and general real three-point Shannon concavity remain open. Novelty is **NOT_ASSESSED**; formal verification is **NOT_PERFORMED**.

## Full source and review record

- [Original paired-logit source](../../research/I05-22-R5-logmean-imbalance/proof.md), [Gram/source checkpoint](../../research/I05-22-R5-logmean-imbalance/coupled_gram_fixed_shape.md), [fixed-shape proof](../../research/I05-22-R5-logmean-imbalance/shared_corner_cell_theorem.md), [parallel refinement](../../research/I05-22-R5-logmean-imbalance/shared_corner_parallel_refinement.md), and [preserved failure/edit-restoration ledger](../../research/I05-22-R5-logmean-imbalance/failure_ledger_shared_corner.md).
- [Immutable complete FIRST unit](https://github.com/randomcat4/dpp-entropy-tools/tree/d5c79ada01d949fe32beb277dae5614d8e154a2f/research/C1-verification-round8-20260910/units/pr81), including original and all three successor gates. The79-file archive is Git-bound; six d995/1e20 report lengths and hashes match its bindings.
- Predecessor isolated SECOND [report](pr81_second/review_report.md), [scope](pr81_second/frozen_scope.md), [code review](pr81_second/code_review.md), [binding](pr81_second/source_binding.json), [publication map](pr81_second/publication_mapping.json).
- Fresh d995 isolated SECOND [full report](pr81_d995_second/review_report.md), [scope](pr81_d995_second/frozen_scope.md), [code review](pr81_d995_second/code_review.md), [binding](pr81_d995_second/source_binding.json), [provenance note](pr81_d995_second/publication_scope_note.md).
- Final1e20 isolated SECOND [full report](pr81_d995_second/delta_1e20_review.md), [scope](pr81_d995_second/delta_1e20_scope.md), [code review](pr81_d995_second/delta_1e20_code.md), [binding](pr81_d995_second/delta_1e20_source_binding.json), [input map](pr81_d995_second/delta_1e20_input_binding.json), [publication map](pr81_d995_second/publication_mapping.json).

Four predecessor inputs, five d995 original/delivered files and four exact1e20 delta files are bound. Four nonmathematical review-history/status replacements in the fresh d995 packet preserve all mathematical content and line numbers; source links point to immutable original lines. Original and delivered hashes are not conflated. No independent reviewer opinion was provided to the fresh d995/final delta SECOND.

Source merged at `d1985b0bb6c52b2eb49d22d586579b69a3602c0f` with exact reviewed head `1e2081d374edeca1533c05356afa38e052f9f78e` as second parent.
