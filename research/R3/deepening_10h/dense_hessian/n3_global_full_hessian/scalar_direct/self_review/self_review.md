# U10a clean replay and internal self-review

ROLE: **SAME AUTHOR INTERNAL SELF-REVIEW**, not a fresh/non-author audit.

RESULT: **CLEAN REPLAY PASS; NO CORE GAP FOUND IN THE REQUESTED CHECKS**.
The global inequality remains **INCOMPLETE** and new proof candidates still
require non-author review. This document does not self-award CORRECT.

## Reproducibility and untouched source

The author main routine was loaded in a fresh runpy namespace. Only its
runtime output-directory binding was redirected into self_review before
execution. It was not run as a writer in scalar_direct. The 29 full rows and
the exact obstruction object match the previously frozen JSON exactly;
only timing is naturally different. All seven author files' hashes were
checked before and after and were unchanged.

Bound author hashes:

- derivation: `b67520243b4b42443c6748c864c19f45e56138d8af42d3d9d53e402e6788acf1`;
- script: `8c09195c217c0981b0da80279529844745708f2e59a84f4b6b065e9d906a51c4`;
- original JSON: `5d4dea1e297c646cad26d9868b099c4284fbea990f891b7042c6d5171ba5e881`.

Command from the assigned repository root:

```powershell
& 'C:/Users/UIO/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe' research/R3/deepening_10h/dense_hessian/n3_global_full_hessian/scalar_direct/self_review/clean_replay.py
```

Exit code 0. `self_review.json` contains the hash binding, exact replay
comparisons and the extra witness calculation. `sanity.json` here is the
redirected clean replay, not an overwritten author output. No subagent,
external write, shared-index change, or forbidden-path access was used.

## 1. Fisher splitting: exact identity, not just a lower bound

For disjoint groups A,B with masses a,b>0 and differential column vectors
u=dp_A, v=dp_B, direct common-denominator expansion gives

u u^T/a+v v^T/b-(u+v)(u+v)^T/(a+b)
 = (b u-a v)(b u-a v)^T/[ab(a+b)].

This checks both the numerator and the weight. With h=b u-a v and
w=1/[ab(a+b)], the added information is exactly w h h^T and is positive
semidefinite. The nested three splits of {1,2,3,123} telescope from the
five-category Fisher to the eight-event Fisher. Hence

F=F_T+sum_(i=1)^3 wi hi hi^T

holds for arbitrary strict atoms and their derivatives, including the DPP
case; no connectedness or sign assumption is required for this identity.
Connectedness is used later only for N>0/inverses. The script checks all
36 matrix entries in exact Fraction arithmetic at each of 29 kernels.

The probabilistic orthogonality wording is also valid: a contrast is
constant on each of its two children and has mean zero within its parent;
it is orthogonal to every ancestor contrast, which is constant on that
parent. This does NOT imply orthogonality of the six-dimensional hi under
an arbitrary matrix inverse; the updates must still be sequential.

## 2. Sherman–Morrison: sequential denominators are correct

Let A0=F_T+delta G_N and Ai=Ai-1+wi hi hi^T. Strict connected K gives
delta>0 and G_N>0, so every Ai is positive definite even if F_T is singular.
The inverse update is

Ai^-1=Ai-1^-1 - Ai-1^-1 hi hi^T Ai-1^-1 /
                       (wi^-1+hi^T Ai-1^-1 hi).

Multiplication by delta eta^T and eta therefore subtracts

ci=delta(eta^T Ai-1^-1 hi)^2 /
              (wi^-1+hi^T Ai-1^-1 hi)>=0.

The code updates `acur` after each split and uses that updated matrix for
the next solve. It does not mistakenly use A0 for all three corrections.
The final identity rho=R_T-c1-c2-c3 agrees with a separate full 6 by 6 solve
at the prescribed 140/220-digit tolerances on all 29 points.

The code computes an unused `aeta` solve before each update; this is harmless
extra work, not a sign or formula error. It was not edited during self-review.

## 3. Proxy blocker: exact feasibility and actual entropy sign

The frozen K is the centered path with edge weights 3/10. The frozen D has
diagonal (1,5/6,1), path entries -3/5 and closing entry 1/3. A separate
implementation in the replay file computes direct signed 3 by 3 event
determinants, rather than using the author's inclusion-gradient routine.

Because each event is cubic in t, values at t=0,±h,±2h recover p',p''
exactly by symmetric interpolation, with h=1/1000. This separately verifies
all eight atoms, p', normalization, and the second derivatives. It then
reconstructs actual B directly as

B(D)=sum (p')²/p + sum p'' log p.

Logs use a fresh rational range-reduced atanh-series implementation with
120 terms and an explicit geometric remainder. The resulting exact B
interval overlaps the author's cofactor-expression interval and lies
strictly above zero. It does not depend on trusting the N formula to obtain
the actual entropy-curvature sign.

Separately, recomputing the cofactors of D gives precisely the log
coefficients 142/75 and 16/9 in the proxy. The proxy's rigorous upper bound
is negative. Rounded displays:

| form | value |
|---|---:|
| proxy B_T(D) | -1.0482033815378993 |
| actual B(D)=-H''(D) | 28.68078384622142 |
| first-contrast-restored B6(D) | 28.573703565040017 |

The sign of actual H'' is negative, not positive. The proxy is a hybrid form
using coarse Fisher and the original cofactor correction, not the entropy
Hessian of a separately defined coarse probability model.

The replay also uses exact Sylvester leading minors, independently of the
author's LDL implementation, for D and all four endpoint matrices
K±D/100-I/1000 and I-K∓D/100-I/1000. All are strictly positive. Convexity
then certifies every real |t|<=1/100 with the same 1/1000 margin. Thus D is
positive definite, rank three, and the exact real-symmetric K-affine chord
is legitimate. No float spectrum substitutes for these checks.

For S=diag(1,-1,1), I-K=SKS. Complementation and sign conjugation transfer
the negative proxy witness to B_T'(SDS); since SDS is also positive
definite, both orientations fail on the same strict K. This establishes
only failure of that sufficient proxy route, not failure of entropy
concavity or of the exact scalar inequality.

## 4. Denominators and scope of numerical checks

The clean output contains exactly 29 distinct rational matrices:

| family | count |
|---|---:|
| exchangeable centers | 4 |
| centered paths | 6 |
| fixed dense rank-one boundary points | 15 |
| complementary boundary points | 4 |

The full rho is below one at 29/29 points. The fixed five-category test
passes 23/29; the trace-capacity test passes 15/29; the six-category test
passes 29/29. The exact proxy gate is a second computation of the existing
3/10 path row, not a thirtieth distinct kernel.

All these scalar tests are finite high-precision sanity results. Only the
explicit witness interval/Sylvester computations are exact arithmetic
certificates. The script's one-parameter estimator formula is executed at
the 23 dense points; it is skipped at six path points to avoid division by
a missing edge. The separate affine-constraint recipe for paths is a
paper argument, not an executed path-estimator test. This scope limitation
does not affect the full Fisher/correction tests, which run at all 29.

## 5. Logical classification of the formulas

| Claim | Classification |
|---|---|
| F=F_T+sum wi hi hi^T | exact identity |
| rho=R_T-sum ci | exact identity, sequential positive-definite solves |
| rho=min_g Q(g) | exact regularized least-squares identity |
| V=minimum unbiased-statistic variance; one-dimensional affine formula | exact identity under connected-Jacobian full rank |
| S=(2delta/3)V<=1 implies rho<=1 | sufficient only; not necessary |
| R_T<=1 or R_T'<=1 implies rho<=1 | sufficient only; both can fail |
| R6=R_T-c1<=1 implies rho<=1 | sufficient only; 29/29 passes do not prove universality |
| if R_T>1, sum ci>=R_T-1 | equivalent to rho<=1 on that region |
| no test required when R_T<=1 | follows from ci>=0 |
| the preceding two cases for every connected strict K | exactly the original global inequality, still INCOMPLETE |

Equality must not be lost: non-strict correction inequality gives rho<=1;
strictness where rho=1 is excluded would be required to prove full-Hessian
strict negativity everywhere. The original S=1 equality analysis additionally
requires E scalar and Fisher Cauchy–Schwarz equality; this was not replaced
with an unjustified blanket strict conclusion.

The reviewed boundary input has rho approaching one from below. The
trace-capacity failure and fixed-orientation failure do not create a uniform
gap and do not imply that the exact correction inequality fails there.

## Final internal assessment

No correction to the requested core identities, exact proxy gate, or
29-point accounting was necessary. Two reporting cautions are explicit:
same-author checking is not independent certification, and the path version
of the estimator formula has no numerical replay in this script. The
six-category all-domain condition and the exact three-correction bound
remain unresolved; outside non-author review is still required.
