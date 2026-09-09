# PR43 rank-two continuation verification report v2

Reviewer: `C1 rank-two first reviewer`

Current source binding: PR43 commit `7bd5962bbb2020ce47fbe286adda7dfe02f9645d`, with historical source `4e1369ef2a59ccfaba3ca8fce95d85e78857bf78` read first.

This report preserves `review_report_v1.md` and adds one scoped literal-statement finding in clause H. No new computation was needed.

## Overall verdict

Clauses E, F, G: STATUS `CORRECT`; repository status `ACCEPTED_SCOPED`.

Clause H concavity theorem: STATUS `CORRECT`; repository status `ACCEPTED_SCOPED`.

Clause H universal descriptive correlation sentence: STATUS `CRITICAL_GAPS`; repository status `NEEDS_FIX`.

Clause H explicit rational fixture: STATUS `CORRECT`; repository status `ACCEPTED_SCOPED`.

The only new issue is a missing `eta != 0` condition in the prose claim that both internal blocks are correlated/non-diagonal. It does not affect the H concavity theorem or the explicit `eta=1/1000` fixture.

## Scoped finding H-descriptive-1

STATUS: `CRITICAL_GAPS`

Repository status: `NEEDS_FIX`

Locations:

- `sources/pr43_7bd5962/continuation/frozen_statement_v3.md:138-153`
- `sources/pr43_7bd5962/proof/06_correlated_3plus3_family.md:53-69`

Issue:

Clause H allows an arbitrary real `eta` such that `C=D0+eta M0` is strict. This includes `eta=0`. If `eta=0`, then `C=D0`, so `C` is diagonal even when `alpha != beta` and `M0` has a nonzero off-diagonal entry.

Therefore the sentence

`When alpha != beta and M0 has a nonzero off-diagonal entry, A,C are both correlated/non-diagonal`

is false as written. The minimal correction is to require `eta != 0` in that descriptive sentence:

`When alpha != beta, eta != 0, and M0 has a nonzero off-diagonal entry, A and C are both correlated/non-diagonal.`

This is a literal scope/description defect, not a counterexample to entropy concavity.

## Clause H revised status

### H1. Concavity theorem

STATUS: `CORRECT`

Repository status: `ACCEPTED_SCOPED`

The proof of whole-interval concavity does not require `eta != 0`. For empty/full left configurations, `M_S` is a scalar multiple of `M0`, so the conditional line still contains the strict diagonal anchor `D0`; see `sources/pr43_7bd5962/proof/06_correlated_3plus3_family.md:87-105`. For the six middle configurations, the Jacobi sign argument gives indefinite rank-two conditional directions; see `sources/pr43_7bd5962/proof/06_correlated_3plus3_family.md:113-149`.

### H2. Universal "both correlated/non-diagonal" descriptor

STATUS: `CRITICAL_GAPS`

Repository status: `NEEDS_FIX`

The descriptor needs `eta != 0`. Without it, `eta=0` is an immediate counterexample to the statement that `C` is non-diagonal.

### H3. Explicit rational fixture

STATUS: `CORRECT`

Repository status: `ACCEPTED_SCOPED`

The explicit fixture uses `eta=1/1000`; see `sources/pr43_7bd5962/proof/06_correlated_3plus3_family.md:205-208`. Thus `C=D0+(1/1000)M0` is genuinely dense/non-diagonal, and the previous exact computation remains valid.

## Unchanged findings from v1

### Clause E: three-point indefinite rank-two directions

STATUS: `CORRECT`

Repository status: `ACCEPTED_SCOPED`

Frozen claim: `sources/pr43_7bd5962/continuation/frozen_statement_v3.md:20-43`. Proof source: `sources/pr43_7bd5962/proof/04_three_point_indefinite_rank2.md`.

The proof correctly establishes the quadratic complete-event coefficient formula, `adj(D)=gamma nn^T`, the eight-atom conditional four-cycle decomposition, the conditional two-point odds sign, the complete Fisher-plus-acceleration Hessian formula, and the legal-boundary extension.

### Clause F: exterior sufficient statistics and compressed Hessian

STATUS: `CORRECT`

Repository status: `ACCEPTED_SCOPED`

Frozen claim: `sources/pr43_7bd5962/continuation/frozen_statement_v3.md:45-88`. Supporting proof locations: `sources/pr43_7bd5962/proof/03_lifting_and_exterior.md:89-142` and `sources/pr43_7bd5962/proof/05_diagonal_and_feature_routes.md:46-120`.

The KL and mutual-information compression is exact because the likelihood ratio is measurable with respect to `(G_A,G_C)`. The Hessian identity is valid on the strict interior where each denominator/log term is defined.

### Clause G: three-point conditional direction criterion

STATUS: `CORRECT`

Repository status: `ACCEPTED_SCOPED`

Frozen claim: `sources/pr43_7bd5962/continuation/frozen_statement_v3.md:90-112`. Proof source: `sources/pr43_7bd5962/proof/06_correlated_3plus3_family.md:3-27`, with Schur/radial dependencies in `sources/pr43_7bd5962/proof/01_conditioning.md:27-67` and `sources/pr43_7bd5962/proof/03_lifting_and_exterior.md:3-51`.

The criterion correctly combines rank-one affine entropy concavity, clause E, and the imported C3 diagonal-anchor theorem.

## Existing computation record

No new computation was run for v2. The previous independent check remains:

- Script: `children/pr43_rank2/independent_pr43_rank2_check.py`
- Input: `children/pr43_rank2/continuation_fixture.json`
- Output: `children/pr43_rank2/exact_check_output.txt`
- Verified exit: `children/pr43_rank2/exact_check_verified_exit.txt`
- Execution provenance: `children/pr43_rank2/execution_record.md`

It passed symbolic three-point identities, exact fixture/radius checks, exact exterior likelihood and KL compression checks, and 64-event positivity diagnostics for `t=1/100` and `t=1/50`.

## Limits

This review still does not cover clauses I--N, nested v3, arbitrary dense two-sided rank-two cross-block concavity, high-dimensional exterior scalar positivity, semidefinite rank-two directions, or novelty.
