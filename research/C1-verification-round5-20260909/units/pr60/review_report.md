# PR60 C1 first mathematical review

Status: `CRITICAL_GAPS` in the review-gate sense only: the main theorem uses a load-bearing finite determinant/positive-chart certificate that C1 was forbidden to reconstruct or run. I found no source-level analytic defect in the Lambda-zero chain, but the theorem cannot be marked independently proved by this review alone.

Outcome: `INCOMPLETE` (`INCOMPLETE_PENDING_C2`) for the main Lambda-zero theorem and the conditional/nonzero-band consequences that depend on it. The one-sided perspective identities are `CORRECT` at source-review level and `ACCEPTED_SCOPED`; their remaining inequality is correctly left `INCOMPLETE`.

## Sources and binding

The packet binding records PR60 head `f869fd251c0d6fdad737b6d5efa287307795a87d`, base `9dcb6e9079ca57f94e0e30d63161cda89ca61fae`, public prefix `research/I05-22-R3-lambda-zero-global/`, and eight public files (`source-snapshots/pr60/SOURCE_BINDING.json:2-8`). The eight public file blob IDs in the binding (`source-snapshots/pr60/SOURCE_BINDING.json:10-65`) match the local snapshot by read-only `git hash-object`.

I used only two accepted main-side dependency summaries as scoped dependencies, not as fresh review opinions. They state that PR51 accepted the general arrow legality/product-coordinate identities, full Fisher/acceleration block form, two-dimensional positive eliminable block, Lambda-zero handoff identity `M=F'(u)+Q`, and conditional marginal-Hessian subtraction (`source-snapshots/accepted_main/docs/verification_round3_20260909/accepted_pr51.md:17-30`). They state that PR55 accepted all eight atom formulas, full Fisher/acceleration, `M=Fmat'+Q`, the fixed-direction congruence/Schur complement `Rstar`, determinant prefactor, and positive seed, while leaving both r=0 and full-r positivity unproved (`source-snapshots/accepted_main/docs/verification_round3_20260909/archived_pr55.md:5-13`, `:21-33`).

## Claim 1: full Lambda-zero M>0 and entropy Hessian strictness

Verdict: `CRITICAL_GAPS`.

Outcome: `INCOMPLETE` (`INCOMPLETE_PENDING_C2`).

The frozen statement has the right open-domain quantifiers: `|mu|,|nu|,|r|<1`, `0<u<1`, six real symmetric physical directions, and true affine entropy directions rather than differentiating along the nonlinear center curve (`source-snapshots/pr60/proof.md:7-29`). The general strict missing-edge Lambda-zero family is covered by setting `A=u^2 a`, `B=u^2 b`, `u^2=A+B`, and `r=(A-B)/(A+B)`; signs of the two nonzero edges are restored by diagonal sign conjugation (`source-snapshots/pr60/proof.md:31-42`, `:63`). This handles unequal diagonals and arbitrary nonzero edge ratio within the strict connected missing-edge family.

The event basis and complete Hessian formula retain all eight atoms, the full Fisher term, pair determinant accelerations, and the triple determinant acceleration (`source-snapshots/pr60/proof.md:44-78`). The Lambda-zero equivalence `q=(1-A-B)/2` follows from the displayed two conditional odds because `AB>0` (`source-snapshots/pr60/proof.md:80-90`). The fixed-direction derivative and 2+4 Schur reduction are within the accepted PR51/PR55 dependency scope and are restated in the packet (`source-snapshots/pr60/proof.md:94-165`).

The new analytic steps after the accepted dependencies are source-consistent: `t=u^4` leaves positive denominators `J=1-t`, `L=1-r^2 t`, `C=1-r^2 t^2`; `Rbar=(u/4)Rstar` is displayed as a symmetric four-dimensional matrix (`source-snapshots/pr60/proof.md:167-176`); actual leaf exchange sends `(mu,nu,r)` to `(nu,mu,-r)` and therefore justifies the fundamental domain `0<=r<1` without changing quantifiers (`source-snapshots/pr60/proof.md:178-178`).

The blocker is the finite certificate. The proof requires the determinant identity

```text
det Ahat = 8 t J^3 L^3 C^3 P
```

and the four-axis chart expansion with 1731 positive coefficients and constant 432 (`source-snapshots/pr60/proof.md:180-241`). Those are not derivable by ordinary source reading from the printed document; they require independent exact reconstruction of the determinant and coefficient array. The author verifier is described as exact and non-sampling (`source-snapshots/pr60/verification.md:5-38`), but author script success is not independent C1 evidence under the frozen instructions.

If C2 verifies the displayed `Rbar -> det/P -> Q` chain, then the remaining sign argument is correct: positive chart coefficients give `P>0`; (18) gives global nonvanishing; the positive seed and connectedness/inertia argument make `Rstar>0`; the accepted Schur equivalence gives `M>0`; integrating `M(s)` in a fixed physical direction from `u=0` gives the strict affine Hessian statement (`source-snapshots/pr60/proof.md:237-261`). Without that C2 result, Claim 1 remains incomplete rather than accepted.

## Claim 2: conditional entropy strictness on the Lambda-zero family

Verdict: `CRITICAL_GAPS`.

Outcome: `INCOMPLETE` (`INCOMPLETE_PENDING_C2`).

The deduction from Claim 1 is analytically correct. The leaf marginal remains diagonal/product along the `u` path, and the two-point negative Hessian is `D11^2/v + D22^2/w`, including cancellation of a possible `D12` contribution at the diagonal two-point center (`source-snapshots/pr60/continuation.md:7-17`; accepted dependency at `source-snapshots/accepted_main/docs/verification_round3_20260909/accepted_pr51.md:27-28`). Therefore the derivative of `-C''` is the same `M`, and at `u=0` the conditional negative Hessian starts as `diag(0,0,4,0,0,0)`.

This claim has no new finite certificate beyond Claim 1. It should be accepted if C2 closes the main Lambda-zero certificate; until then it inherits the same pending status.

## Claim 3: quantified nonzero-Lambda band

Verdict: `CRITICAL_GAPS`.

Outcome: `INCOMPLETE` (`INCOMPLETE_PENDING_C2`).

The band proof is a valid perturbation argument conditional on Claim 1. It defines a fixed strict Lambda-zero center, `pstar>0`, a Frobenius-orthonormal matrix `T0` for `-C''`, and `alpha=det(T0)/(tr(T0))^5` (`source-snapshots/pr60/continuation.md:23-33`). Once Claim 1 gives `T0>0`, the inequality `lambda_min(T0) >= det(T0)/(tr(T0))^5` is correct, and the `delta E33` shift keeps the two arrow Schur complements `q0+delta` and `q0-delta` positive for `|delta|<=q0/2` (`source-snapshots/pr60/continuation.md:35-43`).

The derivative bound is conservative but source-sound: the determinant representation of complete atoms, operator-norm bound on `K-Pi`, derivative bounds for `p_D`, `p_DD`, `p_E`, `p_DE`, `p_DDE`, the full derivative formula, and the eight-atom Lipschitz bound are all displayed (`source-snapshots/pr60/continuation.md:45-70`). This proves a center-dependent nonzero-Lambda interval, not a uniform margin. No additional finite sign computation is required for the analytic claim, but it cannot outrun the pending main theorem.

## Claim 4: fixed-diagonal radial monotonicity obstruction

Verdict: `CRITICAL_GAPS`.

Outcome: `INCOMPLETE` pending a separate exact obstruction check.

The continuation supplies an explicit rational `K*`, `D*`, and radial direction `C*`, then claims strict legality, `exp(Lambda)>1`, a negative derivative of the full negative Hessian along the radial scale, positive negative-Hessian quantity `-H''(K*;D*)`, hence concave actual entropy curvature, and a negative three-kernel Jensen difference (`source-snapshots/pr60/continuation.md:72-158`). This is not an entropy counterexample and is correctly scoped as an auxiliary-method refutation (`source-snapshots/pr60/README.md:13-15`).

The formulas are plausible and the source explains that all eight event polynomials and jets are used (`source-snapshots/pr60/continuation.md:122-140`). However, the sign of the interval in (33), the legal radius in (31), the curvature interval in (35), and the Jensen interval in (36) are finite exact computations. They are not covered by the current C2 full-r determinant contract. This claim needs an independent exact reconstruction of the eight atoms/jets for `K*+epsilon D*+delta C*`, rational Sylvester legality checks for the radial endpoints and Jensen segment, the `exp(Lambda)` ratio, the atanh/log2 interval enclosure, the negative `Mtilde(D*,D*)` interval, the positive `-H''(K*;D*)` interval, and the negative complete-entropy Jensen interval.

## Claim 5: one-sided perspective bridge

Verdict: `CORRECT`.

Outcome: `ACCEPTED_SCOPED`.

The bridge identities are source-checkable. The decomposition

```text
-H(X3|X1,X2) = G1(K) + G1(I-K)
```

keeps both leaf outcomes by complementing all three coordinates (`source-snapshots/pr60/continuation.md:160-172`). The perspective second derivative formula follows from `p=P t`, the cancellation of `sum p_ij1''`, and the checkerboard cancellation of `sum Pij'' t_ij` when `t_ij` is additive in the two leaf bits (`source-snapshots/pr60/continuation.md:177-186`). The positivity of `N1=diag(k0,ell0,0)+v1 K` is justified because `k0`, `ell0`, and `v1` are positive at strict arrow centers and `K>0` (`source-snapshots/pr60/continuation.md:172-188`).

The scale reduction by `S_l=diag(1,1,sqrt(l))` correctly scales the third-bit-one masses by `l`, leaves `Pij` unchanged, adds only the affine term `l log(l) K33`, and transforms the Hessian with the congruent direction (`source-snapshots/pr60/continuation.md:190-199`). The packet correctly leaves the real remaining obligation as the coupled inequality `F1(D) >= 2 tr(N1 adj D)` for every real symmetric direction (`source-snapshots/pr60/continuation.md:201-205`).

## Claim 6: remaining nonzero-Lambda and general real three-point scope

Verdict: `CORRECT`.

Outcome: `INCOMPLETE`.

The packet consistently states that the general Lambda-nonzero missing-edge Schur inequality outside the explicit band, the stronger one-sided inequality, and the general real three-point theorem remain open (`source-snapshots/pr60/README.md:15-17`; `source-snapshots/pr60/sources_routes.md:61-69`; `source-snapshots/pr60/continuation.md:207-211`; `source-snapshots/pr60/proof.md:263-263`). No novelty, CI, independent review, or proof-assistant formalization is claimed (`source-snapshots/pr60/verification.md:1-3`).

## Handoffs

The active C2 contract, as reported by the parent, is the right missing check for Claim 1: rebuild displayed `Rstar/Rbar -> exact det/P -> Q` independently at the same head, including all 1925 chart positions, the 1731 positive coefficients, 194 zeros, symmetries, and seed.

The C2 contract does not cover Claim 4. A separate exact obstruction review should rebuild `continuation_exact.py`'s target from the markdown formulas, not by importing the author script, and certify the legal interval, event jet table, log enclosures, radial derivative sign, positive negative-Hessian quantity `-H''(K*;D*)`, and Jensen sign.

Formal proof status: none.

Novelty status: not assessed.
