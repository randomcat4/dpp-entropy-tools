# D10-Prior audit: Yuzhou Gu rank-one and thinning results

STATUS: CORRECT

Scope: this audits the author-hosted report by Yuzhou Gu, *Entropy of Determinantal Point Processes*, specifically Corollary 6 and Theorem 7 as they are relevant to the R3 search. The source checked is the report PDF at <https://sevenkplus.com/data/dpp.pdf>. It is author material / course-report prior art, not a peer-reviewed certification of this repository.

## Items audited

1. Corollary 6: for a DPP with marginal kernel \(K\), the scalar thinning path \(tK\) satisfies
   \[
   H(tK)\ge tH(K),\qquad t\in[0,1].
   \]
2. Theorem 7: if two DPP marginal kernels \(K_1,K_2\) satisfy
   \[
   \operatorname{rank}(K_1-K_2)=1,
   \]
   then the full-configuration Shannon entropy is concave along the affine segment between them.

## Exact atom semantics

CORRECT. Theorem 7 is formulated for the entropy of the full DPP distribution, not for inclusion-event entropy. The proof introduces exact atom probabilities \(f_S(t)=\Pr(Y=S)\) and uses the relationship
\[
\det K_T(t)=\sum_{S\supseteq T}f_S(t)
\]
to move between inclusion probabilities and atom probabilities. Thus the report is not treating \(\det K_S\) itself as the exact atom probability.

For Corollary 6, the argument uses inclusion probabilities correctly: thinning a DPP sample by retaining each selected point independently with probability \(t\) gives
\[
\Pr(S\subseteq T_tY)=t^{|S|}\Pr(S\subseteq Y)=t^{|S|}\det K_S=\det((tK)_S).
\]
Since finite DPP laws are determined by their inclusion probabilities, the thinned process has marginal kernel \(tK\). This is inclusion-probability reasoning, not an exact-atom shortcut.

## Rank-one determinant affine argument

CORRECT. Along \(K(t)=K_0+tD\) with \(\operatorname{rank}D\le1\), every principal direction \(D_T\) also has rank at most one. Therefore
\[
\det(K_T(t))
\]
is an affine polynomial in \(t\): all determinant terms using two or more columns from \(D_T\) vanish because \(D_T\) has rank at most one.

Möbius inversion is linear, so each exact atom
\[
f_S(t)=\sum_{T\supseteq S}(-1)^{|T|-|S|}\det K_T(t)
\]
is affine in \(t\). Shannon entropy is concave as a function of the probability vector:
\[
-\sum_S f_S(t)\log f_S(t)
\]
is concave along affine probability paths. This proves the rank-one concavity statement on the strict interior.

This multilinear determinant-degree proof is slightly cleaner than differentiating through inverse matrices, because it does not require every \(K_T(t)\) to be invertible.

## Boundary and strict-interior issues

No critical gap for this project's strict-kernel use. The report states its DPP kernel space with closed inequalities. Some displayed differential formulas in the report use divisions by atom probabilities or inverse-like determinant derivatives, which are only automatically safe in the strict interior where all exact atoms are positive.

The boundary extension is nevertheless standard: along a closed feasible segment, each exact atom \(f_S(t)\) is affine and nonnegative, and the scalar function \(-x\log x\) is continuous and concave on \([0,\infty)\) with \(0\log0=0\). Therefore the entropy concavity statement extends to boundary points without needing the interior second-derivative formula.

For R3, all final kernels are required to be strict \(0<K<I\), so the strict-interior proof is already enough for the intended exclusion.

## Corollary 6 thinning

CORRECT, conditional on the thinning entropy theorem used earlier in Gu's report. DPP coordinate marginals are Bernoulli and hence satisfy the needed ultra-log-concavity condition. Taking one input random vector to be the zero process in the thinning entropy inequality yields
\[
H(T_tY)\ge tH(Y).
\]
The inclusion-probability computation above identifies \(T_tY\) with the DPP kernel \(tK\). The endpoints are consistent:

- \(t=0\): deterministic empty process, entropy \(0\);
- \(t=1\): equality \(H(K)=H(K)\).

## R3 implication

The rank-one \(K\)-affine route and the \(0\)-to-\(K\) scalar thinning route are occupied prior work for this project. They should not be reported as new R3 progress. Future candidate directions must explicitly avoid collapsing to rank-one \(K_+-K_-\), and a chord from \(0\) to \(K\) cannot be used as a new entropy-concavity finding.

## Verdict

Theorem 7 and Corollary 6 are usable as prior-art exclusions for R3, with the caveat that the source is a course/project report and the closed-boundary proof should be read with the affine-probability/continuity addendum above.
