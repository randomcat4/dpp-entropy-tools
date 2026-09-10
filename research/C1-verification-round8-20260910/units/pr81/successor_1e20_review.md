# PR81 successor 1e20 delta FIRST review

Scoped verdict: CORRECT / ACCEPTED_SCOPED for the new parallel-edge refinement as a strict sufficient theorem. The delta proves that a strict connected half-leaf arrow has strict full Shannon Hessian negativity when the actual shared-corner conductances satisfy `KA+KB > J/(32AB)`. This refines the lower bound and recovers the earlier coarse `J<12AB` sufficient condition, because each `kappa` is at least `3/8` and the two opposite-edge parallel sums give the old `3/8` cell margin as a corollary.

This delta does not close all half-leaf arrows or any general missing-edge theorem. The open target written with `KA+KB >= J/(32AB)` is not itself accepted as a closure condition unless strict inequality or a separate equality-surface argument is supplied. The added checker and checker output are same-author source evidence only.

## Source binding

Reviewed delta files:

- `source-snapshots/pr81_delta_1e20/research/I05-22-R5-logmean-imbalance/failure_ledger_shared_corner.md`, 44 lines, blob `2920df933887bd85fe0e449fb103002855bde9f2`
- `source-snapshots/pr81_delta_1e20/research/I05-22-R5-logmean-imbalance/shared_corner_cell_check.txt`, 18 lines, blob `f140e6320fe13950b9e25b96d4b7d17f946b118d`
- `source-snapshots/pr81_delta_1e20/research/I05-22-R5-logmean-imbalance/shared_corner_parallel_refinement.md`, 130 lines, blob `2c4a6d065caca66d9db43fd52a827c2f4ffbe1d6`
- `source-snapshots/pr81_delta_1e20/research/I05-22-R5-logmean-imbalance/verify_shared_corner_cell.py`, 419 lines, blob `95478434dc98d4b8beab2e3d1f801f1c64e7f758`

Comparison:

- Base `d99550bfd9eee623ec80edbca1da17ff0ddbe4bf`
- Head `1e2081d374edeca1533c05356afa38e052f9f78e`
- Compare URL `https://github.com/randomcat4/dpp-entropy-tools/compare/d99550bfd9eee623ec80edbca1da17ff0ddbe4bf...1e2081d374edeca1533c05356afa38e052f9f78e`
- Immutable URL base `https://github.com/randomcat4/dpp-entropy-tools/blob/1e2081d374edeca1533c05356afa38e052f9f78e/`

## Accepted analytic points

ACCEPTED_SCOPED: the failure ledger correctly preserves the boundary between failed sufficient methods and counterexamples. It says independent scalar bounds and separate one-axis placement constraints admit nonrealizable relaxed negatives, but not actual DPP points or entropy counterexamples, at `source-snapshots/pr81_delta_1e20/research/I05-22-R5-logmean-imbalance/failure_ledger_shared_corner.md:5-10`. It also states that no universal refined condition, general half-leaf theorem, or unequal-leaf theorem is claimed at `:10` and keeps resource/non-formal boundaries at `:36-44`. This is the right evidence posture.

ACCEPTED_SCOPED: the publication-error ledger is source-clean and nonmathematical. The ledger records that an overview commit mistakenly replaced detailed `proof.md` and that a later repair restored the exact prior blob at `source-snapshots/pr81_delta_1e20/research/I05-22-R5-logmean-imbalance/failure_ledger_shared_corner.md:24-34`. This review does not use that history as proof evidence; it only confirms the ledger does not hide the editing failure.

ACCEPTED_SCOPED: Lemma 1 in the refinement is correct. The refinement defines actual interval endpoint weights `f0=f(u)`, `f1=f(u+s)`, edge integral `h`, and average `m=h/s` at `source-snapshots/pr81_delta_1e20/research/I05-22-R5-logmean-imbalance/shared_corner_parallel_refinement.md:7-28`. The endpoint quadratic `M_edge=[f1 X^2+f0 Y^2-2mXY]/8` is positive definite because the earlier inverse-root edge bound gives `m^2<f0 f1`; minimizing it subject to `X-Y=1` gives the displayed optimal coefficient `kappa=(f0 f1-m^2)/(8(f0+f1-2m))` at `:30-48`. The statement that `kappa>=3/8` follows from the d995 one-edge `3/8` lemma.

ACCEPTED_SCOPED: the parallel-edge combination is valid and uses actual shared-corner data. The four `kappa` values in `source-snapshots/pr81_delta_1e20/research/I05-22-R5-logmean-imbalance/shared_corner_parallel_refinement.md:50-62` are evaluated at the real rectangle corners `q,q+A,q+B,q+A+B`. Weighted Cauchy gives `kA_plus r_plus^2+kA_minus r_minus^2 >= KA Delta^2` at `:64-75`, and the vertical pair gives `KB Delta^2`. Substituting into the d995 exact corner decomposition yields the refined lower bound at `:77-86` with coefficient `KA+KB-J/(32AB)`.

ACCEPTED_SCOPED: Theorem 2 is a correct strict sufficient theorem. Under `KA+KB > J/(32AB)` at `source-snapshots/pr81_delta_1e20/research/I05-22-R5-logmean-imbalance/shared_corner_parallel_refinement.md:88-99`, the alternating-cell coefficient in the refined lower bound is strictly positive. The bound `0<J<2 log 2<2<4` at `:100-106` makes the `(d,e)` block positive definite. The strictness argument at `:108` then matches d995: all completed edge squares, the positive `(d,e)` block, and the positive cell mode can vanish only for the zero physical direction. The inherited positive-pivot core therefore satisfies `E_H>0` and `det E_H>0`.

ACCEPTED_SCOPED: the refinement really extends the sufficient method but does not extend the closed fixed-shape theorem. Since each `kappa>=3/8`, each opposite-edge parallel pair is at least `3/16`, so `KA+KB>=3/8`; hence the old `J<12AB` condition is a corollary as stated at `source-snapshots/pr81_delta_1e20/research/I05-22-R5-logmean-imbalance/shared_corner_parallel_refinement.md:110-116`. The fixed shape `A=1/4,B=4/9` remains closed by the d995 coarse corollary, and the refinement explicitly says it is not needed for that proof at `:118-120`.

STRICTNESS_CAVEAT: the accepted sufficient condition is the strict inequality `KA+KB > J/(32AB)` at `source-snapshots/pr81_delta_1e20/research/I05-22-R5-logmean-imbalance/shared_corner_parallel_refinement.md:92-99`. The later universal target `KA+KB >= J/(32AB)` at `:122-128` is only an open target. A proof of non-strict `>=` would still need an equality-surface argument before it could be used to close all general half-leaf arrows through Theorem 2.

## Source-only evidence

SOURCE_ONLY_CHECK_OUTPUT: `source-snapshots/pr81_delta_1e20/research/I05-22-R5-logmean-imbalance/shared_corner_cell_check.txt:1-18` records a same-author checker command, environment, exit status, pass lines, and no retry. This review did not run it and does not inherit its PASS as independent evidence.

SOURCE_ONLY_CHECKER_CODE: `source-snapshots/pr81_delta_1e20/research/I05-22-R5-logmean-imbalance/verify_shared_corner_cell.py:1-419` is a same-author SymPy checker. Static reading shows it checks the half-leaf transform, `R` edge/cell decomposition, complete quadratic decomposition, one-edge completion, previous relaxed witness arithmetic, fixed-shape rational gates, three direct complete-event spot comparisons, and quantitative Gram minors. It has no external file reads or network effects, but none of its assertions were executed in this review.

SOURCE_ONLY_ARITHMETIC: large rational assertions in the checker, including previous relaxed determinant/minor checks at `source-snapshots/pr81_delta_1e20/research/I05-22-R5-logmean-imbalance/verify_shared_corner_cell.py:153-225` and `Qstar` minor/alpha checks at `:380-409`, were not independently reconstructed. They are not premises of the accepted refinement theorem.

SOURCE_ONLY_AUTHOR_RECONSTRUCTION: `source-snapshots/pr81_delta_1e20/research/I05-22-R5-logmean-imbalance/failure_ledger_shared_corner.md:12-22` describes author-side reconstruction work. It remains source evidence only and does not replace this source FIRST review.

## Boundaries

CLOSED_SCOPED_CARRIED_FORWARD: the fixed half-leaf shape `x=y=1/2`, `A=1/4`, `B=4/9`, `0<q<11/36` remains closed by the accepted d995 analytic proof. The 1e20 refinement is consistent with that closure and explicitly does not need to reprove it.

ACCEPTED_SCOPED_REFINEMENT: every strict connected half-leaf arrow satisfying the actual strict condition `KA+KB > J/(32AB)` is covered by the new refinement.

OPEN: universal `KA+KB >= J/(32AB)`, equality cases for the refined condition, strict half-leaf arrows not covered by the strict condition, unequal leaf diagonals, general nonzero-Lambda missing-edge arrows, general `det E_H>=0`, and general real three-point concavity remain open.

NOT_ASSESSED: novelty and publication priority.

NOT_PERFORMED: arithmetic execution, checker execution, import, compile, interval certification, entropy finite job, formal verification, and SECOND review.

Final classification: CORRECT / ACCEPTED_SCOPED for Lemma 1, the refined lower bound (7), and Theorem 2 under the strict condition `KA+KB > J/(32AB)`. The failure ledger is correctly scoped. The checker and output are SOURCE_ONLY. No general theorem is closed by this delta.
