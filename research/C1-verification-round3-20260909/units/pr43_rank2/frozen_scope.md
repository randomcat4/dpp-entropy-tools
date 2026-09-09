# PR43 rank-two verification frozen scope

Reviewer: `C1 rank-two first reviewer`

Date: 2026-09-09

## Source binding

- Current public source snapshot: `sources/pr43_7bd5962`
- Current frozen author commit: `7bd5962bbb2020ce47fbe286adda7dfe02f9645d`
- Current frozen entry: `sources/pr43_7bd5962/continuation/frozen_statement_v3.md`, clauses E--H
- Historical source snapshot read first: `sources/pr43`
- Historical author commit: `4e1369ef2a59ccfaba3ca8fce95d85e78857bf78`
- Historical entry: `sources/pr43/frozen_statement_continuation.md`
- Round freeze: `repo/research/C1-verification-round3-20260909/frozen_theorem_v1.md`
- Imported diagonal-anchor dependency: `sources/dependency_c3`, PR29 commit `648f1906468e3e548410f98a6b1a53a978f2ea11`

## In scope

1. Clause E: every strict real symmetric `3 x 3` DPP kernel and every real symmetric indefinite rank-two direction, on the full legal affine interval.
2. Clause F: exact rank-two exterior likelihood, KL/statistic compression, and fixed compressed-Hessian identity used by these claims.
3. Clause G: the three-point conditional direction criterion.
4. Clause H: the structured correlated non-coordinate `3+3` family with `A=alpha P+beta nn^T`, `rank(B)=2`, `n^T B=0`, and `C=D0+eta B^T B` strict, including the exact rational fixture.

## Out of scope

- General dense arbitrary rank-two cross-block concavity.
- PR43 nested v3 claims D--J.
- Clauses I--N of `frozen_statement_v3.md`.

## Review standard

I will treat finite or floating checks only as consistency evidence. A `CORRECT` status requires a proof-level argument under the frozen quantifiers or an exact computation for the finite fixture. A proof gap is separate from a theorem counterexample.
