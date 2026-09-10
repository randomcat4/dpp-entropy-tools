# PR81 successor d995 delta FIRST review

Scoped verdict: CORRECT / ACCEPTED_SCOPED for the new shared-corner analytic proof. The d995 source proves a genuine sufficient condition, `J<12AB`, for strict full Shannon Hessian negativity on strict half-leaf arrows, and it proves that the requested fixed shape `x=y=1/2`, `A=1/4`, `B=4/9` satisfies that condition for every `0<q<11/36`. Therefore this delta closes that fixed half-leaf family in the source-only FIRST sense.

This is not a proof of all half-leaf arrows, all missing-edge arrows, or general real three-point entropy concavity. Large rational Gram-minor displays and same-author checker claims were not independently executed or arithmetically reconstructed.

## Source binding

Reviewed delta source:

- `source-snapshots/pr81_delta_d995/research/I05-22-R5-logmean-imbalance/shared_corner_cell_theorem.md`, 373 lines, blob `a45186d74f8ea9e512d46bc7ea30380149ec9a33`
- Immutable URL base: `https://github.com/randomcat4/dpp-entropy-tools/blob/d99550bfd9eee623ec80edbca1da17ff0ddbe4bf/`

Comparison:

- Base `92c1b3dfd85c4be4f0ce13b59ffb51e6e0869eac`
- Head `d99550bfd9eee623ec80edbca1da17ff0ddbe4bf`
- Compare URL `https://github.com/randomcat4/dpp-entropy-tools/compare/92c1b3dfd85c4be4f0ce13b59ffb51e6e0869eac...d99550bfd9eee623ec80edbca1da17ff0ddbe4bf`

The delta metadata lists one added file only. All source status lines and checker-pass statements were treated as author claims unless independently checked by static reasoning below.

## Accepted analytic points

ACCEPTED_SCOPED: the source keeps the complete DPP object. It restates the eight complete atoms and the exact negative entropy Hessian `Q_K(D)=-H''(K;D)=sum p'^2/p + sum p'' log p` at `source-snapshots/pr81_delta_d995/research/I05-22-R5-logmean-imbalance/shared_corner_cell_theorem.md:9-31`. The half-leaf coordinate map at `:33-70` is the `x=y=1/2` specialization of the accepted PR70 physical-direction map, and the matrix `E` is invertible, so `(d,e,T00,T10,T01,T11)` still represents all six real symmetric physical directions.

ACCEPTED_SCOPED: the shared-corner variables are actual PR81 variables, not relaxed scalar ranges. The four edge integrals and rectangle integral are defined at `source-snapshots/pr81_delta_d995/research/I05-22-R5-logmean-imbalance/shared_corner_cell_theorem.md:72-88`. Their relation to `ell,k,lambda,J` at `:90-107` follows from the original PR81 definitions with `x=y=1/2`: `a_minus=ell-lambda/2`, `a_plus=ell+lambda/2`, `b_minus=k-lambda/2`, `b_plus=k+lambda/2`, and `n=A k+B ell-J`. Thus the proof works with the same four corner logits on both axes.

ACCEPTED_SCOPED: Lemma 3.1 is correct. The source defines `h`, `m_edge`, and the claimed inequality at `source-snapshots/pr81_delta_d995/research/I05-22-R5-logmean-imbalance/shared_corner_cell_theorem.md:111-131`. With `r=f-3` and `w=r^(-1/2)`, the displayed derivative formula at `:133-146` gives concavity of `w`; since `w` is not affine on any nontrivial interval, the chord argument yields the strict endpoint/integral bound at `:148-155`. Completing the square leaves the two-endpoint matrix at `:157-168`, whose determinant is positive by that bound and whose diagonal entries are positive. This proves the one-edge Gram inequality with strict residual positivity.

ACCEPTED_SCOPED: the exact four-corner cell decomposition is consistent with the accepted PR70/PR81 full core. The identity at `source-snapshots/pr81_delta_d995/research/I05-22-R5-logmean-imbalance/shared_corner_cell_theorem.md:172-210` retains endpoint Fisher weights, the four edge acceleration terms, and the negative alternating cell term `-J Delta^2/(32AB)`. Static reconstruction from the half-leaf `L,C,F,R` formulas confirms the Fisher weights appear twice with coefficient `1/8`, giving the full `1/4 f(t_ij)T_ij^2` Fisher term, while the edge square terms reproduce the `R` block and the `-J` cell coefficient through `Delta=T00-T10-T01+T11`.

ACCEPTED_SCOPED: the shared-corner estimate is valid. Applying Lemma 3.1 to the four actual edges gives the nonnegative completed edge squares, and the two elementary difference inequalities at `source-snapshots/pr81_delta_d995/research/I05-22-R5-logmean-imbalance/shared_corner_cell_theorem.md:212-228` contribute at least `(3/8)Delta^2`. This leaves the load-bearing coefficient `3/8-J/(32AB)`.

ACCEPTED_SCOPED: Theorem 5.1 is correct in its stated scope. If `J<12AB`, then `3/8-J/(32AB)>0`. Since strict legality gives `A+B<1` and hence `AB<1/4`, the same condition gives `J<3<4`, so `4d^2+4e^2+2Jde >= (4-J)(d^2+e^2)` as used at `source-snapshots/pr81_delta_d995/research/I05-22-R5-logmean-imbalance/shared_corner_cell_theorem.md:230-260`. The equality analysis at `:262-268` is sound: `d=e=0`, `Delta=0`, and the four edge-square constraints force `T=0`; invertibility then forces `D=0`. Thus `Q_K(D)>0` for every nonzero physical direction, and the inherited positive-pivot representation gives `E_H>0` and `det E_H>0` at `:246-249`.

ACCEPTED_SCOPED: the q-uniform shape corollary is valid. The condition `h(A)+h(B)-h(A+B)<12AB` at `source-snapshots/pr81_delta_d995/research/I05-22-R5-logmean-imbalance/shared_corner_cell_theorem.md:272-278` follows from complement symmetry and strict convexity of `J(q)` after continuous endpoint extension. Endpoints are used only to bound the open interval; they are not treated as legal strict kernels.

ACCEPTED_SCOPED: the requested fixed shape is closed. For `A=1/4`, `B=4/9`, the source gives `12AB=4/3` and `0<q<11/36` at `source-snapshots/pr81_delta_d995/research/I05-22-R5-logmean-imbalance/shared_corner_cell_theorem.md:280-290`. Symmetry/strict convexity gives `J(q)<J(0)=h(1/4)+h(4/9)-h(25/36)` at `:292-303`. The elementary bounds `log 2<7/10`, `log(4/3)<1/3`, `h(1/4)<3/5`, and `h(4/9)<7/10` at `:305-319` imply `J(q)<13/10<4/3=12AB` at `:321-327`. Therefore Theorem 5.1 proves strict full six-direction negativity for the entire legal open interval of this fixed shape, including every nonzero-Lambda point.

ACCEPTED_SCOPED: the explicit coercivity statement is analytically supported without relying on the printed large minors. From `f>=4`, each edge has `h>=4s`; from `J<13/10`, the `d,e` and `Delta` coefficients have the lower bounds used in `Qstar` at `source-snapshots/pr81_delta_d995/research/I05-22-R5-logmean-imbalance/shared_corner_cell_theorem.md:329-351`. Even without independently checking the listed principal minors, `Qstar` is positive definite by the same constraint argument used in Theorem 5.1: if all displayed positive square terms and `Delta` vanish with `d=e=0`, then the four corner equations force an alternating `T`, and `Delta=0` forces `T=0`.

## Evidence not independently certified

SOURCE_ONLY_ARITHMETIC: the six printed leading principal minors at `source-snapshots/pr81_delta_d995/research/I05-22-R5-logmean-imbalance/shared_corner_cell_theorem.md:340-349` were not arithmetically reconstructed. They are not needed for the accepted qualitative positive-definiteness conclusion.

SOURCE_ONLY_CHECKER: the checker description and claimed Python/SymPy pass at `source-snapshots/pr81_delta_d995/research/I05-22-R5-logmean-imbalance/shared_corner_cell_theorem.md:353-364` were not run. They remain same-author supporting evidence only.

SOURCE_ONLY_PRIOR_DIAGNOSTIC: the references at `source-snapshots/pr81_delta_d995/research/I05-22-R5-logmean-imbalance/shared_corner_cell_theorem.md:355-362` to rebuilding previous relaxed determinants and derivative fractions were not used as proof evidence in this review.

## Boundaries

CLOSED_SCOPED: fixed half-leaf shape `x=y=1/2`, `A=1/4`, `B=4/9`, `0<q<11/36`: strict full Shannon Hessian negativity, equivalently `E_H>0` and `det E_H>0`, is accepted from the analytic source proof.

ACCEPTED_SCOPED: all strict half-leaf arrows satisfying the actual DPP condition `J<12AB` are covered by Theorem 5.1. This is a shape- and parameter-dependent sufficient family, not a universal half-leaf theorem.

OPEN: strict half-leaf arrows with `J>=12AB`, unequal leaf diagonals, general nonzero-Lambda missing-edge arrows, general `det E_H>=0`, and general real three-point concavity remain open, as stated at `source-snapshots/pr81_delta_d995/research/I05-22-R5-logmean-imbalance/shared_corner_cell_theorem.md:366-373`.

OUT_OF_SCOPE_PRIOR_FINITE_EVIDENCE: PR70's separate finite-evidence status is neither adjudicated nor advanced by this delta and is not a premise of the accepted shared-corner proof.

NOT_ASSESSED: novelty and publication priority.

NOT_PERFORMED: arithmetic execution, checker execution, interval certification, entropy finite job, and formal verification.

Final classification: CORRECT / ACCEPTED_SCOPED for Lemma 3.1, Theorem 5.1, the q-uniform shape condition, and the complete fixed-shape theorem. The fixed half-leaf shape is no longer OPEN under this source review; general determinant and general entropy concavity remain OPEN.
