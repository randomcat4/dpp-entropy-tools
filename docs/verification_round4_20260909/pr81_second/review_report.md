# PR81 independent SECOND review report

Overall verdict: the analytic reductions in the PR81 packet are correctly scoped as author proofs and formula-source continuations, not a proof of the full missing-edge entropy theorem. The four-scalar compression, rectangle FTC identities, complement imbalance bounds, half-leaf Gram inequality, same-q secant constraints, and relaxed tuple nonrealizability argument are internally coherent at the static proof level. The full determinant sign `det E_H >= 0` remains `INCOMPLETE`. All fixed-shape large rational derivatives, relaxed Sylvester minors/determinant values, and diagnostic numerics remain `SOURCE_ONLY/PENDING` because this review did not execute checker code or arithmetic certification.

## 1. Binding and scope

Verdict: CORRECT.

All four input files match both the SHA256 and Git blob values in `input_binding.json`. The reviewed PR81 head is `92c1b3dfd85c4be4f0ce13b59ffb51e6e0869eac`.

The scope statements in `input/proof.md` lines 3-5 and 269-279 correctly say the author unit is `PENDING_REVIEW`, does not rerun PR60/issue73 arithmetic, and does not claim an entropy counterexample. The addendum in `input/coupled_gram_fixed_shape.md` lines 3-5 and 381-393 likewise leaves the actual fixed-shape and general determinant signs incomplete.

## 2. PR70 formula-source status

Verdict: SOURCE_ONLY.

The PR70 packet supplies the event-complete formula source: all eight atoms and the true entropy Hessian formula are in `pr70_source/proof.md` lines 13-22; the missing-edge domain and six-coordinate direction map are lines 23-60; the side matrices `L_s,C_s,R_s,F_s` are lines 117-168; the complement/marginal Schur formulas are lines 200-227; the `2x2` determinant target and equivalence are lines 231-259; and the Fisher inverse identity is lines 261-292.

For this review, those are accepted only as source formulas. I did not use PR70 as an independent C2 certificate and did not read any FIRST/public-comment material. Therefore PR81 statements that depend on "accepted PR70" should be read here as "using the frozen PR70 formula source."

## 3. Original scalar compression, Fisher, acceleration, and marginal Schur

Verdict: CORRECT as static formula reduction; SOURCE_ONLY for inherited PR70 core.

The paired scalar compression in `input/proof.md` lines 39-102 is consistent with the PR70 side definitions. Summing the two side potentials gives `psi(t)=t log t+(1-t)log(1-t)`, `g=psi'`, `f=psi''`; hence `ell,k,lambda,J` in lines 47-58 are the side sums listed in lines 60-67. The combined `L,C,R` formulas in lines 69-95 follow by summing PR70's side matrices and the identity `J_s=A k_s+B ell_s-n_s+lambda_s(A mu+B nu)` from `pr70_source/proof.md` lines 164-168.

The Fisher statement in `input/proof.md` lines 97-102 preserves the complete paired Fisher rather than projecting to fewer scores. It matches the source identity in `pr70_source/proof.md` lines 261-283: `(F0+F1)^(-1)` uses the complement-preserving `t(1-t)` identity, not a sum of side inverses.

Acceleration and marginal terms are not silently dropped. PR70 explicitly warns that `P_ij''` need not vanish in `pr70_source/proof.md` lines 56-60, and PR81 keeps the rational Fisher `F`, the update `R`, the marginal matrix `diag(1/v,1/w)`, and mixed directions in `input/proof.md` lines 27-35 and 265-267. The addendum repeats this retention in `input/coupled_gram_fixed_shape.md` lines 3-5.

## 4. Rectangle FTC and complement imbalance bounds

Verdict: CORRECT.

The rectangle FTC identities in `input/proof.md` lines 106-124 are consistent with the definitions `t_ij=q+A(1-i)+B(1-j)`: `ell_0,ell_1,k_0,k_1` are one-dimensional edge integrals of `f`, `J` is the rectangle integral of `f`, and `lambda=J'` is the rectangle integral of `f'`. This keeps all entropy terms inside the binary negative-entropy potential rather than dropping a sign-indefinite log remainder.

The complement symmetry and imbalance theorem in lines 126-201 are also structurally correct. The involution `q <-> qbar=r-q` uses `f(1-t)=f(t)`, giving `J(r-q)=J(q)` and `lambda(r-q)=-lambda(q)` in lines 138-149. The convexity formula `J''=int int f''` and the floor `f''>=32` in lines 151-174 imply the stated sign and growth inequalities in lines 175-201. The endpoint envelope in lines 203-219 preserves rare-event blow-up with explicit `q qbar` denominators rather than discarding it.

The rewritten bounds in lines 248-265 are consistent in form with the previous inequalities and are explicitly not claimed sufficient for the determinant sign.

## 5. Method scope and determinant sign

Verdict: CORRECT_SCOPE / INCOMPLETE_FOR_TARGET.

The method discussion in `input/proof.md` lines 221-247 correctly separates matrix-perspective/logarithmic-mean motivation from the actual DPP Hessian. It states that perspective convexity cannot replace the true Hessian because event accelerations remain, and that `lambda` and `J` bounds alone do not sign `det E_H`.

The exact remaining gap is accurately stated in lines 248-267: the determinant inequality must use `ell,k,lambda,J` jointly with the exact positive `Y=F+R`, and no claim is made that the displayed scalar bounds are enough.

## 6. Fixed actual shape derivative ledger

Verdict: PARTLY_CORRECT / SOURCE_ONLY_PENDING.

The symbolic derivative formulas in `input/coupled_gram_fixed_shape.md` lines 28-37 follow from the rectangle definitions when `x=y=1/2`: `ell'`, `k'`, `lambda'=J''`, and `J'=lambda` are the expected edge/rectangle derivatives.

The exact rational derivative values at `q*=11/144` in lines 39-54 are `SOURCE_ONLY/PENDING`. I did not recompute or certify these large rational values. The qualitative discussion of "wrong-sign channels" in lines 54 and 198-220 is diagnostic and not a global determinant proof.

## 7. Half-leaf Gram inequality

Verdict: CORRECT.

The one-dimensional Gram lemma in `input/coupled_gram_fixed_shape.md` lines 56-117 is a valid analytic proof on the stated domain. The identity for `f''`, the Cauchy-Schwarz estimate in the positive measure `f(t+a) da`, and the inequality `2 h h'' - 3 h'^2 > 0` imply strict concavity of `u_A=h_A^(-1/2)`.

The rectangle inequality in lines 118-183 correctly integrates the reciprocal square of the endpoint secant and yields

```text
J^2 < B^2(ell^2-lambda^2/4),
J^2 < A^2(k^2-lambda^2/4).
```

This is an actual analytic realizability constraint for the `x=y=1/2` half-leaf family. It is also correctly scoped: lines 173 and 182 say it does not assert entropy concavity and only constrains the relaxed determinant domain.

## 8. Relaxed tuple, minors, determinant, and nonrealizability

Verdict: SOURCE_ONLY_PENDING for large rational minors/determinant; CORRECT for the displayed nonrealizability mechanism.

The relaxed tuple and its exact Gram residuals in `input/coupled_gram_fixed_shape.md` lines 222-240 are source-only in this review. The positive Sylvester minors and negative determinant in lines 242-259 are also `SOURCE_ONLY/PENDING`; they are not an independent C2 certificate because no checker or arithmetic reconstruction was run here.

The nonrealizability proof in lines 261-294 is the important analytic point and is structurally correct. Actual realizability at the fixed `q` requires

```text
ell+lambda/2 = h_A(q+B).
```

For the relaxed tuple this left side is `6`, while the same-q interval placement forces the integral to lie below the displayed endpoint bound in lines 268-283. Thus the negative relaxed determinant point is outside the actual DPP one-parameter curve. This is not an entropy counterexample.

## 9. Same-q secant constraints and relaxed stress test

Verdict: CORRECT for the analytic secant inequalities; SOURCE_ONLY_PENDING for diagnostics.

The same-q secant inequalities in `input/coupled_gram_fixed_shape.md` lines 296-336 correctly follow from strict concavity of `u_A=h_A^(-1/2)` and its B-axis analogue. These constraints add edge placement relative to the same rational q-rectangle and are stronger than free scalar range or independent Gram ellipses.

The numerical secant display in lines 338-364 and the two-axis stress test in lines 366-379 are diagnostics only. The text correctly states that negative relaxed determinants can still occur under a free relaxation and that actual realizability requires the shared four-corner representation in lines 370-379. These diagnostic claims are `SOURCE_ONLY/PENDING`, not a new proof or disproof of `det E_H>=0`.

## 10. Thinning bridge

Verdict: SOURCE_ONLY formula bridge; scope correctly separated from full entropy.

The PR70 thinning bridge is not used as a PR81 determinant certificate. As a source note, `pr70_source/thinning_bridge.md` distinguishes universal conditional concavity from full entropy: lines 5-44 give the global equivalence of the one-sided and conditional statements, and lines 76-106 explain why a hypothetical negative side would not automatically be a full-entropy counterexample after thinning because the marginal Fisher remains. This supports PR81's insistence that side or conditional obstructions cannot be relabeled as full Shannon counterexamples.

## Final status table

| unit | verdict |
| --- | --- |
| input hashes and git blobs | CORRECT |
| PR70 files as formula source | SOURCE_ONLY |
| event-complete entropy / all six directions retained | CORRECT_SCOPE |
| paired scalar compression `ell,k,lambda,J` | CORRECT |
| paired Fisher and inherited inverse identity | CORRECT as formula use / SOURCE_ONLY for PR70 proof |
| acceleration and marginal Schur terms retained | CORRECT |
| rectangle FTC identities | CORRECT |
| complement symmetry and imbalance bounds | CORRECT |
| Method A/B determinant scope | CORRECT_SCOPE |
| fixed-shape symbolic derivative ledger | CORRECT |
| fixed-shape large rational derivative values | SOURCE_ONLY/PENDING |
| half-leaf Gram inequality and rectangle ellipses | CORRECT |
| relaxed tuple Gram residuals, minors, determinant | SOURCE_ONLY/PENDING |
| relaxed tuple nonrealizability mechanism | CORRECT |
| same-q secant constraints | CORRECT |
| numerical secant display and two-axis stress test | SOURCE_ONLY/PENDING |
| full fixed-shape `det E_H>=0` | INCOMPLETE |
| general missing-edge entropy theorem | INCOMPLETE |
| novelty | NOT_ASSESSED |
| formal/C2 verification | NOT_PERFORMED |

