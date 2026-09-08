# Review: general `3 x 3` log-odds normal form

Two complementary private reductions were independently reviewed.

For the four-interaction Hessian normal form, a nonauthor reviewer returned
`CORRECT` after checking the triple determinant second derivative, the full
four-dimensional Mobius acceleration basis, the dual theta vectors, edge
aggregation, Fisher data processing, and the exact/sufficient distinction in
the residual decomposition.  Its dependency-free script exited `0` with
`P4-10A exact identity check: PASS`.

For the L-ensemble six-odds representation, a different nonauthor reviewer
returned `CORRECT` after checking all normalized-correlation formulas, the six
nonpositive conditional odds, their two linear relations, the beta gauge, the
exact sign cone, and the direction of the optimized danger bound.  Its
dependency-free script exited `0` with
`P4-10D L-ensemble theta identity check: PASS`.

The public consolidation is
`proofs/n3_hessian_log_odds_normal_form.md`.  A commit-bound review is recorded
below.  The result is an exact reduction and sufficient condition, not a proof
of general `3 x 3` concavity.

## Commit-bound public review

The public consolidation was frozen in:

```text
commit ce023af28b1a46ef559a4dc0d43f430b564f2824
tree   2c5a7e84a7e1f7e8273e58a86f924606adf4d086
blob   3594a73915b164a24dc43ff5e463ce8a534243b1
```

Two independent contexts used only `git show` on the fixed blob.  Both
returned `STATUS: CORRECT`.  They checked the four-dimensional normal form,
edge/Fisher decomposition, the exact rigid-route obstruction, all six
conditional odds, the beta gauge, the direction of `Lambda>=-D_*`, and the
fact that `F>=D_*` is only sufficient.  Both confirmed that the document keeps
the general residual open and does not revive the retired mutual-information
route.  Neither reviewer modified files.
