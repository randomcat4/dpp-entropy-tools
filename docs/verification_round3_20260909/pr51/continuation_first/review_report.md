# PR51 continuation first independent review

Verdict: `ACCEPTED_SCOPED_FOR_IDENTITIES_AND_OBSTRUCTIONS`; `INCOMPLETE` for the explicitly open global inequalities.

This review covers only the added public file `research/I05-22-missing-edge-20260909/continuation.md` at PR51 head `2e4b8754ad4af2fe055ebeeef1159877773372a3`. It does not re-open the already reviewed half-filled proof packet, does not use private author verifier scripts, and does not attempt issue52's heavy determinant/global certificate task.

## Source and scope

The continuation itself states that the identities, positive two-dimensional block, and two method obstructions are author-proved but unreviewed, while the remaining four-dimensional inequality and radial monotonicity conjecture are incomplete (`continuation.md:3`). I preserved that division.

Files/artifacts in this review directory:

- `frozen_scope.md`
- `COMPUTE_PLAN.md`
- `independent_continuation_checks.py`
- `independent_continuation_checks.json`

The bounded checker result is `PASS_BOUNDED_CONTINUATION_CHECKS`. It used Python `3.12.14`, SymPy `1.14.0`, and one arithmetic thread; elapsed time was `3.180152` seconds for the final run. One attempted full six-coordinate radial simplification was stopped because it was drifting into the issue52-style heavy symbolic work; the final checker keeps that item to the non-overlapping derivative/log-weight check.

## Per-claim verdict

| Continuation claim | Source lines | Verdict | Review notes |
|---|---|---|---|
| Product-domain parameterization of connected missing-edge centers | `continuation.md:5-29` | `ACCEPTED_SCOPED` | The Schur complements are exactly `q` for `K` and `1-q-A-B` for `I-K`. With `0<x,y<1`, `A,B>0`, `q>0`, and `q+A+B<1`, this is exactly the strict product domain, with signs of `b,c` restored by diagonal sign conjugation. |
| Full six-direction conditional direction map | `continuation.md:31-49` | `ACCEPTED_SCOPED` | I re-derived the inverse map (22) from the conditional derivative formula and checked all four `T_ij`. The double-contrast coordinate `h` maps to `D12`; it is not discarded. |
| Log identities, rectangle coefficient `J`, and `J>0` | `continuation.md:50-73` | `ACCEPTED_SCOPED` | The log identities `ell0-ell1=k0-k1=Lambda` and the collected formula for `J` checked symbolically. The integral formula has positive integrand on the product domain. |
| Positive `2 x 2` block `L` | `continuation.md:121-142` | `ACCEPTED_SCOPED` | The trapezoid argument is sound: `f0''` is strictly convex on `(0,1)`, so the rectangle integral is strictly below the endpoint trapezoid averages. The inequalities `ell>w(ell0+ell1)` and `k>v(k0+k1)` then give `J^2<L11 L22`. |
| Full six-direction `L,C,R` Hessian identity | `continuation.md:75-119` | `ACCEPTED_SCOPED` | Starting from the cofactor log part with signs `-2k0 det D23 -2ell0 det D13 -2v0 det D12 +2Lambda tr(K adj D)`, I substituted the inverse map and collected terms. The displayed `L,C,R` block form matches exactly. |
| Schur complement equivalence | `continuation.md:144-156` | `ACCEPTED_SCOPED` for equivalence; `INCOMPLETE` for PSD | Since `L` is positive definite and the marginal block `diag(1/v,1/w)` is positive, completing squares makes (29) equivalent to nonnegative curvature for the stated arrow-center reduction. But (29) and the stronger (30) are explicitly not proved here. |
| Face-acceleration coupling and failure of naive two-point iteration | `continuation.md:158-182` | `ACCEPTED_SCOPED` | Equation (31) checked by exact expansion. The leftover terms `2Jde` and `-vwJ h^2/(2AB)` are real coupling terms, so simply adding two face-wise two-point proofs would double-spend Fisher and omit coupling. |
| `Lambda=0` subfamily and fixed-coordinate radial derivative input | `continuation.md:184-250` | `ACCEPTED_SCOPED` for `Lambda=0`, coordinates, and log-weight derivatives; `INCOMPLETE` for `M>0` | `v0=v1` is equivalent to `(1-q-A-B)(1-q)=q(q+A+B)`, hence `q=(1-A-B)/2`. I checked the fixed-coordinate conditional Fisher form and the exact derivatives giving `n1,n2,n3`; I did not certify determinant positivity or `M>0`. The source also says those are open and handed off to issue52 (`continuation.md:248-250`). |
| Conditional-resolvent method obstruction `Phi''<0` | `continuation.md:252-299` | `ACCEPTED_SCOPED` | I recomputed the full eight-event definition of `Phi`, obtained the displayed exact rational negative second derivative, checked strict legality of `K_*`, `K_*±D_*/10000` and complements by Sylvester minors, and checked the entropy/Jensen log intervals. The actual entropy curvature has the opposite sign needed for a counterexample, so this is only an auxiliary-method obstruction. |
| Coefficientwise power-series obstruction | `continuation.md:300-317` | `ACCEPTED_SCOPED` | Direct substitution gives the displayed expression and the `s^4` coefficient `-1/18`. The direction `D_s` varies with the center parameter, so this does not refute the fixed-coordinate radial derivative conjecture in (35). |
| Final boundary | `continuation.md:318-322` | `ACCEPTED_SCOPED` | The continuation correctly leaves the arbitrary-diagonal missing-edge inequality (29), strict positive entropy Jensen candidates, the compute request, and novelty outside accepted mathematical results. |

## Targeted attacks

I attacked the specific fragile points requested:

- Trapezoid argument: accepted; strict convexity and positive rectangle side lengths give strict inequalities in the right direction.
- Cofactor signs: accepted; the signs in the log-acceleration part match exact substitution into the cofactor identity.
- Schur equivalence: accepted as an equivalence only; PSD of the `4 x 4` Schur complement remains open.
- Moving versus fixed direction in the power-series obstruction: accepted; the obstruction uses a direction depending on `s`, so it cannot refute the fixed-coordinate radial derivative statement.
- Legality and log-error in the `Phi` counterexample: accepted; all eight events are preserved, kernels and complements are strict on the checked segment, and the rational log enclosures give the declared signs.

No precise critical gap was found in the identity/reduction/obstruction claims actually asserted as proved in `continuation.md`.

## Limitations retained

This review does not certify:

- `S_full >= 0` in (29);
- `S_cond >= 0` in (30);
- global positivity of `M` in (35);
- issue52's determinant/global certificate target;
- general real three-point entropy concavity;
- a strict positive entropy Jensen counterexample;
- novelty or publication priority;
- private author scripts or private artifacts.

The continuation should merge, if at all, only as scoped identity/reduction/method-obstruction material with the open inequalities clearly preserved.
