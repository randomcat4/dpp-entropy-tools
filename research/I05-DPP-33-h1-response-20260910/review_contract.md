# Independent review contract

State: **PENDING_REVIEW / UNCLAIMED until an explicit issue claim appears.**

A review should freeze one exact PR head and audit the units below independently of the author verdict.

## U1 — one-dimensional event packing

Verify that all finite complete-event pairs `(I,x)` are countable and can be translated into pairwise disjoint finite blocks of one `Lambda subset Z` while preserving every internal displacement. Confirm that the block-direct-sum diagonal envelope is bounded by the Fourier coefficient sequence and that off-block zero entries create no density problem.

## U2 — external inverse theorem map

Using the primary DOI `10.5802/crmath.54`, verify the exact definition and theorem for `C^{p,r}` matrices. Check all parameters:

```text
d=1,
p_mtx=2,
r=1>d(1-1/p_mtx)=1/2,
Lambda relatively separated,
M direct sum invertible on ell^2.
```

Confirm that the theorem gives the inverse direct sum in the same algebra. Reject any argument that applies a nonuniform theorem separately to infinitely many events.

## U3 — common complex envelope

Reproduce the convolution-algebra estimate for weighted `ell^2_1`, the Neumann majorant

```text
d=sum_n r^n (d0*b)^{*n}*d0,
```

and the origin/future leg bounds. Verify the terminal-site effective coupling `a+a*d*a`, the scalar Schur inverse, and

```text
sum_j (1+j)^2 beta_j < infinity.
```

Check both emitted symbols and complex non-Hermitian parameters.

## U4 — differentiated memory

Use Cauchy's formula on a strictly smaller common disk to verify that parameter derivatives through order four retain the same single-coordinate majorant. Check the identity

```text
sum_n (n+1) sum_{j>n} beta_j
 = (1/2) sum_j j(j+1) beta_j.
```

Verify complete-event parity before factorization through `s=z^2`.

## U5 — BFG coupling in moment spaces

Check the primary BFG ratio condition, matched-suffix coupling, age chain, first-return formula, and arbitrary-observable variation inequality. Reproduce

```text
R:V0 -> C,
R:V1 -> V0
```

from the nonnegative sums in the proof. Do not replace this with the unsupported phrase “summable variation implies C2 response.”

Compare Fernandez--Maillard `math/0305026` only within its actual uniqueness/loss-of-memory scope.

## U6 — response identities

Starting from

```text
(nu_u-nu_s)(F)=nu_u(L_u-L_s)R_sF,
```

rederive the first and second response formulas, including moving-observable terms. Audit uniform tails and continuity in `V0` and `C`; no derivative of `R_s` may be assumed.

## U7 — true entropy bridge

Verify complete-event cylinder continuity, invariance, uniqueness, `h_s=-nu_s ell_s`, fixed parity marginals, and `nu_s ell_0=nu_0 ell_0`. Check normalization `D'(0)=0`, the exact imported PR53 matching coefficient, and the conversion

```text
D(s)=A s^2+o(s^2)
h''(t)=-12 A t^2+o(t^2).
```

All complete events and the physical affine kernel must remain present.

## U8 — explicit scope separation

Verify that the exponent `7/4` family belongs to `H^1_F`, lies in every `A_p` for `p<3/4`, lies outside `A_1`, has a nonconstant mean-`1/3` center, and is not covered by the repository's constant-center, mean-one-half Wiener-small, exponential, or `A_p,p>=1` results.

## Deliverable and stop conditions

At the earliest invalid load-bearing step, stop dependent conclusions and report whether the defect is locally repairable. If all units pass, issue an `ACCEPTED_SCOPED` verdict with the exact theorem class and excluded scopes.

Separate:

- author proof;
- independently accepted imports;
- external theorem assumptions;
- machine evidence (none expected);
- universal conclusion;
- novelty (NOT_ASSESSED).

This is a source/proof review and may exceed 60 minutes. A claimant should state a time budget, stop at a resumable equation anchor if exhausted, and must rebind if the PR head changes. Creating the issue is not a review start.