# PR41 second independent mathematical review

Exact verdict: CORRECT.

Scoped repository status: PR41 source was reviewed at immutable commit `6fd61dcd299417fc3a4eab3af682c03dd816b670` from the local frozen source bundle. I created only this child review directory and did not modify author/source files, publish to GitHub, merge, or consult C2 evidence. The status certified here is limited to R2-T1, R2-T2, and the missing-edge exact identities described in `frozen_scope.md`.

## Version and line ranges

Source files and claim ranges:

- `frozen_statement.md` lines 5-25: complete-configuration DPP entropy conventions, affine directions, and symmetric off-diagonal coordinate convention.
- `frozen_statement.md` lines 27-67: R2-T1 strong-coupling connected center family and strict full-direction claim.
- `frozen_statement.md` lines 69-96: R2-T2 block-plus-singleton identity and two-point conditional entropy lemma.
- `frozen_statement.md` lines 108-119: explicit exclusions for general missing-edge and general three-dimensional claims.
- `proof.md` lines 3-50: event formulas and complete second-variation formula.
- `proof.md` lines 52-283: R2-T1 proof.
- `proof.md` lines 316-517: R2-T2 proof.
- `proof.md` lines 519-612: missing-edge exact identities.
- `HANDOFF.md` lines 5-26 and 28-49: requested audit checklist.

## Assumptions used

The review uses the frozen convention that `K` is a real symmetric strict contraction, `0<K<I`, and the entropy is complete configuration Shannon entropy from the exact event probabilities given by Mobius inversion. Since strict contraction is an open condition, every real symmetric affine direction has a small two-sided interval on which the event probabilities are positive, so the Hessian formula in `proof.md` lines 41-47 is valid.

For R2-T1, the off-diagonal directions are the symmetric basis directions `E_ij+E_ji`, and the direction `D` is arbitrary in all six real symmetric coordinates. For R2-T2, after an allowed permutation I take the two-point block to be indices `{1,2}` and the singleton to be index `3`. The review does not assume the connecting directions vanish.

## Claim-by-claim review

### R2-T1 strong-coupling center

Conclusion: CORRECT.

The proof first reduces to `sigma=+1` in `proof.md` lines 54-76 and correctly obtains the eigenvalues `1/2, 1/2 +/- sqrt(2) kappa`; hence `0<K<I` is exactly `8 kappa^2<1`, with the frozen theorem taking the strict nonzero range. The event probabilities in lines 78-91 follow directly from the three principal two-minors and the determinant `r=1/8-kappa^2`, giving two rare events `(1-s)/8` and no endpoint claim.

The six-coordinate change in lines 95-106 is invertible. Rebuilding representative event derivatives from the Mobius formulas gives the table in lines 108-119; the signs are consistent, including the `H` and `N` combinations. The grouped second derivatives in lines 124-137 are legitimate because only equal log weights are grouped, and the three grouped sums add to zero as required by mass conservation.

The decomposition in lines 152-213 proves that the full Fisher term and the acceleration term split as a `3x3` block in `(P,Z,R)` plus scalar blocks in `H`, `Delta`, and `N`. The scalar coefficients in lines 207-209 are strictly positive for `0<s<1`.

For the remaining `G_s` block, the derivative formula in lines 230-244 is consistent with differentiating `m=log(1-s^2)` and `g=log((1+s)/(1-s))`. The Sylvester minors in lines 247-261 are strictly positive on `0<s<1`, so `G_s'` is positive definite. Although `G_0=diag(2,4,0)` is singular in line 266, the integral argument in lines 269-272 is sufficient: for every nonzero vector, the integral of the strictly positive quadratic form `x^T G_r' x` over `0<r<s` is positive. Thus `G_s` is positive definite for every strict center.

The sign-conjugation step in lines 281-283 does not weaken the direction quantifier. Diagonal sign conjugation preserves every principal minor and therefore every complete event probability, while `D -> S D S` is a bijection of the real symmetric direction space. This covers `sigma=-1` and both signs of `kappa`.

Counterexample attempts checked: the endpoint `s=1` is excluded; rare event weights are retained rather than bounded away uniformly; pure directions in the kernel of `G_0` are made positive by the integral of `G_r'`; and no symmetric direction is lost under sign conjugation.

### R2-T2 two-point block plus singleton

Conclusion: CORRECT.

The block-plus-singleton identity in `proof.md` lines 465-517 is exact. At the block center, the eight event probabilities factor as `p_{S,k}=u_S w_k`, and the first derivatives factor as in line 484 because connecting entries appear at least quadratically in the relevant principal minors. Summing the full eight Fisher terms gives line 490-492: the mixed first-order terms vanish by `sum_S u'_S=0` and `sum_k w'_k=0`.

The second derivatives from connecting directions need not vanish event-by-event, but lines 495-507 use the correct marginal cancellations: `sum_k p''_{S,k}=u''_S` and `sum_S p''_{S,k}=w''_k=0`. Since `log p_{S,k}=log u_S+log w_k`, all singleton-log acceleration and connecting cross-acceleration contributions cancel in the complete event sum. This proves the full six-direction equality

`-H_3''(A direct-sum [z];D) = -H_2''(A;D_{12}) + d_3^2/(z(1-z))`.

The two-point conditional entropy lemma in lines 316-463 is also correct. For `a != 0`, the variables `u`, `v`, `w=v-u`, `U`, and `V` are well-defined with `0<u<v<1`. The conditional Fisher formula in lines 371-375 is the standard conditional Fisher decomposition. The log-acceleration term is `-2 delta L` because the four second derivatives are `+2delta,-2delta,-2delta,+2delta` and the probability ratio is the inverse of the displayed log-odds ratio.

The identity for `delta` in lines 383-388 follows by differentiating `x=yu+(1-y)v` and `a^2=y(1-y)(v-u)`, then eliminating `h`. Substitution gives the square-plus-matrix form in lines 390-401. The determinant certificate in lines 404-437 is valid: the inequality `log t <= (t-1)/sqrt(t)` gives `L <= w sqrt(A_u A_v)`, and the resulting determinant lower bound is positive because `0<y(1-y)<=1/4`. The matrix is positive definite, and the square term forces the remaining direction component when `U=V=0`, so strictness holds for `a != 0`.

The `a=0` case in lines 439-449 is handled separately and correctly. At independence, the `a^2` first-order contributions to `C=H(X_1 | X_2)` cancel, leaving `-C''=d^2/[x(1-x)]`. This is only semidefinite, which is exactly what R2-T2 needs. Combining with `H_2(A)=h(y)+C(A)` yields line 460 and the required nonnegativity of `-H_2''`.

Counterexample attempts checked: pure connecting directions `D_13` or `D_23` give zero second variation at the block center, which is allowed because R2-T2 claims semidefiniteness, not strictness. At `a=0`, pure off-diagonal two-point directions also give zero second variation, again compatible with the frozen claim. Boundary denominators are protected by `0<A<I_2` and `0<z<1`.

### Missing-edge exact identities

Conclusion: CORRECT as exact identities only.

For the general missing-edge center in `proof.md` lines 519-612, the conditional probability identity

`t_ij = z - b^2 phi_i - c^2 psi_j`

is correct. It follows by dividing the exact event probability with `X_3=1` by the independent Bernoulli marginal of `(X_1,X_2)`, using `K_12=0`.

The derivative formula for `T_ij` in lines 541-548 is also correct. Direct quotient differentiation at `a=0` gives the displayed terms: diagonal changes produce `b^2 d_1 phi_i^2` and `c^2 d_2 psi_j^2`; edge changes produce `-2b h_13 phi_i` and `-2c h_23 psi_j`; and the missing-edge direction produces the mixed term `+2bc h_12 phi_i psi_j`.

The Jacobian in lines 551-567 is correct when `bc != 0`. The four rows are a Cartesian two-by-two design in `1, phi, psi, phi psi`, with determinant `(phi_1-phi_0)^2(psi_1-psi_0)^2=1/(v_1^2 v_2^2)`, multiplied by the column scalings `2bc`, `-2b`, and `-2c`, giving `8b^2c^2/(v_1^2 v_2^2)`.

The Fisher identity in lines 603-609 is correct. At the center, the score splits into an independent base score for `(X_1,X_2)` plus a conditional Bernoulli score for `X_3`; the conditional score has mean zero in each cell, so the cross term vanishes. This yields the base Fisher `d_1^2/v_1+d_2^2/v_2` plus the event-adaptive conditional Fisher sum.

These identities do not prove the unresolved global sign of the general connected missing-edge `6x6` Hessian. The proof itself keeps that limitation explicit in lines 612 and 614-619, and this review accepts only the exact reductions.

## Vulnerabilities considered

- Quantifiers: R2-T1 and R2-T2 both keep all six real symmetric directions. No proof step imposes preservation of missing edges, equal diagonals, equal couplings, or sign symmetry.
- Strictness: R2-T1 is strict because the coordinate map is invertible, scalar blocks are positive, and `G_s` is positive definite. R2-T2 is only semidefinite, matching the statement.
- Boundary behavior: all denominators are protected by strict hypotheses. No endpoint `s=1`, `a`-boundary, or `z`-boundary claim is made.
- Sign handling: diagonal sign conjugation preserves principal minors and maps the full direction space bijectively.
- Singleton cross-acceleration: connecting directions are present in second derivatives, but their complete-event log-weighted sums cancel by marginalization at the product center.
- Conditional entropy at `a=0`: the separate calculation gives semidefinite behavior and prevents division by `w=0`.
- Missing-edge identities: accepted only as exact coordinate and Fisher identities, not as a Hessian positivity theorem.

## Limits of this review

I did not perform a Lean or proof-assistant formalization. I did not run the author symbolic script or duplicate C2's all-event replay. I did not review novelty, priority, conference strength, or any general three-dimensional entropy concavity claim beyond the exact missing-edge identities stated above.

Final scoped status: CORRECT for PR41 R2-T1, CORRECT for PR41 R2-T2, and CORRECT for the missing-edge exact identities. All broader claims remain outside this verdict.
