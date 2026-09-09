# PR43 E-H rank-two second proof review

STATUS: CORRECT_WITH_MINOR_TEXT_FIX

Repository verdict: the mathematical concavity claims in E-H are correct under the frozen and inherited standing assumptions. I found no critical proof gap. Before certification or publication, the repository should fix the descriptive H sentence at `continuation/frozen_statement_v3.md:153` and `proof/06_correlated_3plus3_family.md:69`: because `eta=0` is allowed at `frozen_statement_v3.md:138-144` and `proof/06_correlated_3plus3_family.md:53-59`, `C=D_0` can be diagonal even when `alpha != beta` and `M_0` has nonzero off-diagonal entries. The correct wording is: if `alpha != beta`, `eta != 0`, and `M_0` has a nonzero off-diagonal entry, then both `A` and `C` are non-diagonal.

## Source locations

Source root: `source-snapshots/pr43_7bd5962`

Dependency root: `source-snapshots/dependency_c3`

- Clauses E-H: `continuation/frozen_statement_v3.md:20-169`.
- Standing finite DPP/block assumptions: `frozen_statement.md:23-45`.
- Conditional Schur/radial lift statement: `frozen_statement.md:49-86`; proof at `proof/01_conditioning.md:30-67` and `proof/03_lifting_and_exterior.md:7-51`.
- Rank-two exterior likelihood: `frozen_statement.md:112-162`; proof at `proof/03_lifting_and_exterior.md:89-144`.
- C3 imported diagonal-anchor theorem: `dependency_c3/frozen_statement_v2.md:8-15`; proof of entire finite rays at `dependency_c3/proof.md:81-141`.

## Dependency check

The inherited setup fixes strict real blocks `0<A<I`, `0<C<I`, the cross-block family `K(t)`, the strict legal interval `I^o={t:0<K(t)<I}`, and its closure `I` at `frozen_statement.md:23-45`. This supplies the strictness needed by the Schur event matrices and by all conditional complete-event laws.

Proof I gives the exact complete-event determinant formula and Schur factorization. For every left complete configuration `S`, `p_{K(t)}(S,T)=p_A(S)p_{C-sM_S}(T)` with `s=t^2`, and the conditional kernel is the true affine line `C-sM_S`, not a projection or rotated surrogate (`proof/01_conditioning.md:30-67`). Proof III then proves that if all conditional lines are concave in `s`, their weighted entropy sum `G(s)` is concave, is maximal at `s=0` by fixed marginals and mutual information, and gives concavity of `t -> G(t^2)` on the true legal interval (`proof/03_lifting_and_exterior.md:7-43`). Its strictness argument uses an actual cross-block covariance `-sB_ij^2` when `B != 0` (`proof/03_lifting_and_exterior.md:45-51`). Boundary extension is by continuity of finite entropy.

The imported C3 theorem matches every diagonal-anchor use. Its finite statement covers every strict diagonal Hermitian kernel and every fixed Hermitian direction on the entire feasible interval, without commutation or zero-diagonal restrictions (`dependency_c3/frozen_statement_v2.md:8-15`). The proof identifies the affine DPP family by an exact product-replacement channel (`dependency_c3/proof.md:81-112`) and extends from `[0,T]` and `[T,0]` to the entire feasible ray, including boundaries (`dependency_c3/proof.md:114-141`). Thus a shifted line `C-rM` that contains a strict diagonal kernel is a legal affine reparameterization of the C3 theorem.

## Clause E

Verdict: CORRECT.

The proof of the three-point indefinite rank-two theorem is complete. Since `rank(D)=2`, complete-event probabilities have no cubic term; the quadratic coefficient law `c` is determined by pair inclusion coefficients, the triple coefficient, total mass, and one-point moments (`proof/04_three_point_indefinite_rank2.md:23-57`). For a unit null vector `n`, `adj(D)=gamma nn^T` with `gamma<0`, and the pair coefficients are `delta_ij=gamma n_k^2<=0`.

The four-cycle decomposition is exact, not fitted: each fixed-`k` four-cycle has the right lower moments and triple contribution, and Boolean Mobius inversion makes the comparison unique (`proof/04_three_point_indefinite_rank2.md:61-87`). Conditional on `x_k=epsilon`, the remaining two coordinates form a strict two-point DPP, so the conditional odds log is nonpositive by the negative DPP covariance identity (`proof/04_three_point_indefinite_rank2.md:91-110`). Pairing these odds with the nonpositive `delta_ij` gives `<c,log p> >= 0` (`proof/04_three_point_indefinite_rank2.md:112-123`).

The full curvature formula retains the complete Fisher term and the full acceleration term (`proof/04_three_point_indefinite_rank2.md:126-136`). Re-centering at an arbitrary interior `z` is legitimate because `Dn=0`, so `kappa=n^T(K+zD)n` remains in `(0,1)`. Semidefinite rank-two directions are explicitly excluded (`proof/04_three_point_indefinite_rank2.md:138-140`), so the sign reversal in that case is not a counterexample.

Counterexample attempts checked: zero coordinates of `n` only make some `delta_ij` vanish and do not change the sign argument; boundary masses are handled by finite entropy continuity; semidefinite directions are outside the frozen theorem.

## Clause F

Verdict: CORRECT.

The exterior likelihood identity follows from Schur plus Sylvester: after a full rank factorization `B=UV^T`, the likelihood ratio is exactly `det(I_2-sG_A(S)G_C(T))` (`proof/03_lifting_and_exterior.md:89-112`). The linear and quadratic coefficients are exactly the trace and exterior-degree terms, and the zero-mean identities are obtained by normalization of determinant perturbations (`proof/03_lifting_and_exterior.md:115-142`).

The sufficient-statistic claim is also correct. Since the likelihood ratio is measurable with respect to `(G_A,G_C)`, the conditional law inside each feature fiber is the baseline product fiber law. The feature marginals remain the pushed-forward fixed block marginals, so KL to `p_A otimes p_C` and mutual information are exactly preserved under the pushforward (`proof/05_diagonal_and_feature_routes.md:48-73`). This is a true sufficiency statement, not a Fisher projection.

The Hessian formula is exact. For `p_{C+VZV^T}(T)=mu_T ell_T(Z)`, the two-by-two determinant expansion gives `ell_T'` and `ell_T''=2 det(H) det(G_T)` (`proof/05_diagonal_and_feature_routes.md:77-101`). Normalization cancels the `+1` entropy derivative term and leaves the full event Fisher term plus `2 det(H) Lambda_{C,V}(Z)` (`proof/05_diagonal_and_feature_routes.md:103-120`). For `ell=3`, the acceleration sign follows from clause E's stronger `<c,log p> >= 0` sign lemma applied to `D=VHV^T` with `det(H)<0`; the general higher-dimensional sign is correctly left open.

Counterexample attempts checked: non-injective feature fibers do not break KL/I preservation because the likelihood ratio is feature-measurable and the feature marginals are fixed; the Hessian formula does not drop the Fisher term; semidefinite and general high-dimensional rank-two directions are not claimed.

## Clause G

Verdict: CORRECT, with one harmless standalone-clarity note.

The three alternatives cover the needed conditional line concavity. If `rank(M_S)<=1`, every complete-event determinant along `C-rM_S` is affine in `r`, so Shannon entropy is concave. If `M_S` is indefinite rank two, clause E applies to the direction `-M_S`. If the line contains a strict diagonal kernel, the imported C3 diagonal-anchor theorem applies after an affine reparameterization. This is exactly the proof at `proof/06_correlated_3plus3_family.md:19-27`.

Once each conditional line is concave on the common legal `s` interval, Proof I and Proof III give the stated radial concavity and strictness for `B != 0`. Clause G's compact statement at `continuation/frozen_statement_v3.md:90-112` inherits strict block assumptions from `frozen_statement.md:23-45`; if the clause is later excerpted as a standalone theorem, it should explicitly say that the block family has nonempty strict legal interval, equivalently `A` and `C` are strict kernels. This is a clarity issue rather than a proof gap in the current frozen file.

Counterexample attempts checked: shifted diagonal anchors match C3; rank-one directions may be indefinite, positive, or negative, but determinant rank update still makes event probabilities affine; `rank(B)=0` gives the non-strict case as stated.

## Clause H

Verdict: CORRECT for the concavity theorem and explicit example; MINOR_TEXT_GAP for the descriptive non-diagonality sentence.

The structural family has strict `A` because its eigenvalues are `alpha` on `n^perp` and `beta` on `span(n)`, with `0<alpha<1` and `theta<beta<1-theta` (`proof/06_correlated_3plus3_family.md:31-44`). The condition `n^T B=0` and `rank(B)=2` allow `B=UR` with `U` spanning `n^perp` and `R` full row rank (`proof/06_correlated_3plus3_family.md:46-84`).

For `S={1,2,3}` and `S=emptyset`, the conditional matrices are scalar multiples of `M_0=B^T B`, so the conditional lines pass through the strict diagonal anchor `D_0` and satisfy G(3) (`proof/06_correlated_3plus3_family.md:87-105`). For the six configurations with `|S|=1` or `2`, the event matrix `X_S=A-E_{S^c}` has inertia `(|S|,3-|S|)`, and Jacobi's complementary minor identity gives the sign of the compressed determinant from `n^T X_S n / det X_S` (`proof/06_correlated_3plus3_family.md:107-126`). The inequalities `beta-(1-n_i^2)<0` and `beta-n_k^2>0` give `det G_S<0` in both cases (`proof/06_correlated_3plus3_family.md:128-145`). Since `R` is full row rank, `M_S=R^T G_S R` is indefinite rank two, satisfying G(2) (`proof/06_correlated_3plus3_family.md:147-149`). This covers all eight left configurations.

The explicit dense example satisfies the hypotheses: `n=(1,1,1)/sqrt(3)`, `alpha=2/5`, `beta=1/2`, `B` has rank two and column sums zero, and `C=2/5 I+(1/1000)B^T B` is strict (`proof/06_correlated_3plus3_family.md:151-215`). The exact legal radius is correct. The nonzero coupled singular values are controlled by `lambda_max=123+3 sqrt(1663)`. Positivity gives `t^2 < 4/(25 lambda_max)+1/2500`; positivity of `I-K(t)` gives `t^2 < 9/(25 lambda_max)-3/5000`. Since `lambda_max>200`, the second bound is smaller, and rationalizing it gives `4091/15000 - sqrt(1663)/150 > 0` (`proof/06_correlated_3plus3_family.md:217-236`).

The one flaw is descriptive. The allowed hypotheses include `eta=0`, and then `C=D_0` is diagonal. For example, using the displayed `n, alpha, beta, B`, taking any strict diagonal `D_0` and `eta=0` satisfies the structural theorem hypotheses and has `alpha != beta` and nonzero off-diagonal entries in `M_0`, but `C` is diagonal. This refutes only the sentence at `continuation/frozen_statement_v3.md:153` and `proof/06_correlated_3plus3_family.md:69`, not the theorem or the explicit example where `eta=1/1000`.

## Final per-claim status

- E: CORRECT.
- F: CORRECT.
- G: CORRECT under the inherited strict block/legal-interval setup; add strictness wording if excerpted standalone.
- H concavity theorem: CORRECT.
- H explicit dense example and legal radius: CORRECT.
- H descriptive claim "A,C both non-diagonal" under only `alpha != beta` and off-diagonal `M_0`: MINOR_TEXT_GAP; add `eta != 0`.

No CRITICAL_GAPS were found for the E-H concavity results. The repository should be treated as mathematically passable for these claims after the small wording fix above.
