# PR58 Second Verification Report

Overall verdict: the scoped analytic compensation unit is accepted with one important wording exception. The complete-law Cauchy inequality, the conditional interval interface, and the conditional-centering addendum are mathematically correct under the accepted PR54 outer-wedge identity. The statement that the Cauchy criterion is "strictly weaker" than `W>=0` is not proved as a logical containment claim and should not be certified in that form.

## Claim Status Table

| claim | scope lines | status |
| --- | --- | --- |
| Complete-law identity may be used as prerequisite | accepted outer-wedge addendum lines 47-57; accepted scope record lines 45-51 | CORRECT as accepted input |
| Theorem 3.1 Cauchy compensation inequality | `RESULT.md` lines 72-104 | CORRECT |
| Theorem 3.1 sufficient strict-concavity criterion | `RESULT.md` lines 90-92, 98-104 | CORRECT |
| "Strictly weaker than `W>=0`" relation wording | `RESULT.md` lines 94 and 142 | CRITICAL GAPS |
| Corollary 3.2 interval envelope, conditional on its assumptions | `RESULT.md` lines 106-140 | CORRECT |
| Squared rational certificate interface | `RESULT.md` lines 130-136 | CORRECT with a narrow zero-case qualification |
| Fixed `3+3` corridor certificate | `RESULT.md` lines 146-225; code lines 85-108; output lines 5-25 | INCOMPLETE in this review |
| `s=10` negative `W` and direct curvature numbers | `RESULT.md` lines 230-258; code lines 110-173; output lines 26-30 | INCOMPLETE in this review |
| Fiberwise cancellations from fixed block marginals | `ADDENDUM_CONDITIONAL_CENTERING.md` lines 15-43 | CORRECT |
| True conditional centering and two-direction residual compensation | `ADDENDUM_CONDITIONAL_CENTERING.md` lines 45-123 | CORRECT |
| Failure of a compensation condition is not an entropy counterexample | `ADDENDUM_CONDITIONAL_CENTERING.md` lines 125-137; `RESULT.md` lines 252-258, 286 | CORRECT as a scope statement |

## Theorem 3.1

Status: CORRECT for the inequality and pointwise sufficient condition.

The accepted prerequisite gives, under the complete product law `mu=p_A tensor p_C`,

`t^2 I''(t)=E[Phi(u)+4y^2/q+y psi(u)]`

with `q=1+u>0` on a strict legal point. `RESULT.md` lines 78-82 define `P=E Phi(u)`, `A2=4E[y^2/q]`, and `Rpsi=E[q psi(u)^2]`. Weighted Cauchy gives

`|E[y psi]| <= sqrt(E[y^2/q] E[q psi^2]) = (1/2) sqrt(A2 Rpsi)`,

so the factor `1/2` at lines 100-102 is exactly accounted for by the definition of `A2`. Substituting the worst sign proves line 88. If line 92 holds and `t != 0`, then `I''(t)>0`, hence `H''(t)<0` because `I=H(A)+H(C)-H(K(t))`. At `t=0` the displayed strict condition is not triggered, so no zero-center claim is smuggled in.

Status: CRITICAL GAPS for the relation wording at lines 94 and 142.

The proof shows that the Cauchy criterion is a valid sufficient condition and that it can in principle compensate a negative signed term. It does not prove the logical implication `W>=0 => P+A2 > (1/2) sqrt(A2 Rpsi)`. Thus "strictly weaker than the sign condition" is not certified if "weaker" means logical containment. The safe certified wording is: the Cauchy criterion is a separate sufficient condition that can be checked without assuming `W>=0`, and it may apply in negative-`W` cases once those cases are independently certified.

## Corollary 3.2

Status: CORRECT as a conditional analytic interface.

Assume the interval hypotheses in lines 108-116: `0<q_-<=q_s<=q_+`, `|psi(u_s)|<=Psi`, `E[u_s^2]>=M2>0`, and `B2=E[b^2]`. Since `Phi(u)=4u^2/q+2u log(1+u)` and `u log(1+u)>=0` for `u>-1`, line 120 follows from `q<=q_+`. Since `y=s^2b` and `s<=R`, line 122 follows from `q>=q_-`. Line 124 follows from `q<=q_+`, the bound on `psi`, and `E_mu 1=1`.

Inserting these into Theorem 3.1 and discarding the positive `+A2` term gives line 128:

`t^2 I''(t) >= 4M2/q_+ - R^2 Psi sqrt(B2 q_+/q_-)`.

Thus line 132 is a valid sufficient strict-concavity condition. The square test at lines 134-136 is valid when the compared sides are nonnegative. The text's "positivity of both sides" is conservative; if `B2=0`, the right side is zero and the original inequality can still be certified directly. This is a narrow zero-degeneration qualification, not a failure of the corollary as used with positive `B2`.

Status: INCOMPLETE here for the fixed corridor.

The static checker interface matches the corollary: code lines 85-105 compute exact `q_-`, `q_+`, `Psi`, the lower moment bound, and the squared margin; output lines 5-25 report four positive-margin pieces covering `3<=s<=15`. Under this task's instructions, however, I did not run Python/SymPy, redo the rational reconstruction, or independently certify those values. Therefore `RESULT.md` Theorem 4.1 is only conditionally supported by the analytic interface in this review.

## Conditional Centering Addendum

Status: CORRECT.

Lemma 1.1 uses the fixed DPP block marginals correctly. For fixed `S`, the true left marginal equals `p_A(S)` for every legal radial parameter, so

`sum_T p_C(T) q_s(S,T)=1`.

Because the left side is the polynomial `1-s E_{p_C}a+s^2 E_{p_C}b`, equality on a nonempty legal interval forces both fiber coefficients to vanish. The same argument with `S` and `T` swapped gives the right-fiber cancellations. This proves lines 21, 25, and 29 without using a channel or reference-law independence as a centering substitute.

The centering in Section 2 is with respect to the true conditional law `P_s(T|S)=p_C(T)q_s(S,T)` from lines 47-53, not the reference independent law. The identity

`E_mu[y psi]=E_mu[y(psi-c(S))]`

uses only the reference-law fiber cancellation `E_{p_C}[y|S]=0`. Weighted Cauchy then gives the same `1/2` factor as in Theorem 3.1. Minimizing `E_{p_C}[q(psi-c)^2]` over `c(S)` selects the true conditional mean `m_S`, so line 73 follows. The right-fiber proof is identical, giving line 77.

The residual comparisons are also correct. Since `sum_T p_C q=1`,

`R_0-R_S=E_{p_A}[m_S^2]>=0`

and similarly `R_0-R_T=E_{p_C}[n_T^2]>=0`. Hence `R_S<=R_0`, `R_T<=R_0`, and the lower bound using `R_*=min(R_S,R_T,R_0)` is never weaker than the uncentered Cauchy lower bound. If `A2=0`, the Cauchy term vanishes and no division by `A2` is used.

## Machine Obligations For Root

No new machine obligation is needed to certify the scoped analytic inequalities above.

To upgrade the excluded fixed-corridor or `s=10` numerical claims, a separate finite exact check should independently reconstruct the 64 complete events, verify the DPP event probabilities and `G_A/G_C` definitions, recompute interval extrema from endpoints and rational vertices, verify the rational log enclosures, and compare the resulting exact inequalities with the frozen code/output blobs. That would be a numerical/certificate review, not part of this analytic second verification.
