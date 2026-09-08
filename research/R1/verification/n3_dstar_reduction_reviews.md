# Fixed-object reviews for the `D_*` reductions

## One-dimensional allocation dual

- fixed commit: `a628f3afb640b8f00c2c09356699e2ec17f55c6b`
- tree: `900a5351545d65e1793ccafa9dac8eb224534c0a`
- proof blob: `e65028b6c1169274f276c2d32c9958dd6bf02c7d`
- path: `research/R1/proofs/n3_hessian_log_odds_normal_form.md`

Two nonauthor reviewers read the proof from the fixed Git object.  Both
returned `STATUS: CORRECT`.  They checked the LP-dual sign, feasible `r`
interval, common DPP shift, four breakpoint values, zero-odds degeneracies,
and the signed convention for `N`.  An earlier commit used ambiguous wording
about which interval collapses and called the global expressions quadratic;
the fixed object above clarifies that the edge box collapses while the common
interval may only shorten, and that the expressions are piecewise quadratic,
ordinary quadratic only on a fixed `sigma` sign cone.

## Compound-symmetric specialization

- fixed commit: `6b34f86a167db9bcfcde20e54ab994f9dcb15b50`
- tree: `91c18f663643f2757dad6eddaee7018881cd524e`
- proof blob: `52e197f901fde82869bfa56b3fdfa390a5489dda`
- path: `research/R1/proofs/n3_equicorrelation_dstar_reduction.md`

Two nonauthor reviewers read this proof from the fixed Git object and both
returned `STATUS: CORRECT`.  They checked complementation, the four scalar
branches, complete-event Fisher formulas, the `tau<=0` log-determinant bound,
the full four-dimensional standard sector, the pure trivial sector, and the
reduction of mixed directions to the single-edge and double-edge `6 x 6`
matrix families.

Both reviews explicitly confirmed the scope boundary: these are exact
reductions and partial family results.  The two parameterized matrix signs,
the global sufficient inequality `F>=D_*`, and general connected `3 x 3`
entropy concavity remain open.

## Single-edge scalar reduction

- fixed commit: `6612bccb93389cbf403ec04e22ca19c221462488`
- tree: `bb2540c2eab6178458d2e66dda18cab179ab523d`
- proof blob: `31034eda6461efab6b912cff5ef4aeb6a1b094cd`
- formal-script blob: `27fa65ac22970f253e95a743e9886663210a1cde`
- paths: `research/R1/proofs/n3_equicorrelation_single_edge_reduction.md`
  and `research/R1/certificate/phase4/scripts/equicorrelation_single_edge_symbolic.py`

Two nonauthor reviewers read only the fixed Git objects and returned
`STATUS: CORRECT`.  Both replayed the fixed dependency-free script with exit
code `0`.  They checked the stabilizer odd/even decomposition, positivity of
the base trivial and standard blocks without circular use of the target,
the rank-one downdate equivalence, the cleared scalar `Phi`, the two Fisher
sufficient regions, and the separate treatment of the product line.

The reviewers confirmed that the script checks formal identities with zero
parameter evaluations.  The global sign `Phi>=0`, the double-edge matrix,
and general connected `3 x 3` concavity remain open.
