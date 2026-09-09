# W4 frozen verification scope

Verifier: W4 independent non-author check for C1 verification, 2026-09-09.

## Fixed public inputs

- Author archive: `verification_20260909/sources/pr33/result/I05-W4-20260909_result/`.
- Frozen author commit: `0f06eef1dc723058b46596ff9b704d7e97d3522f`.
- Later PR33 head `a0869b44bdce75acb8c2438806b21d3cf013e508` is treated only as a no-math-change wrapper update, per the task statement.
- Author files read for this check: `frozen_statement.md`, `proof.md`, `inputs/exact_inputs.json`, `code/*.py`, and `outputs/*`.
- Existing `sources/pr33/review/` material is intentionally excluded before the independent verdict.

## Claim under review

Let

\[
K=\begin{pmatrix}x&a&b\\a&y&c\\b&c&z\end{pmatrix},\qquad
D=\begin{pmatrix}d_1&h_{12}&h_{13}\\h_{12}&d_2&h_{23}\\h_{13}&h_{23}&d_3\end{pmatrix}.
\]

The reviewed domain is

\[
0<x_i<1,\qquad |K_{ij}|\le {1\over4}\sqrt{x_i(1-x_i)x_j(1-x_j)}.
\]

The reviewed coercive Hessian claim is

\[
-H''(K;D)\ge {7\over10}(\mathcal S+\mathcal U+\mathcal V)
\]

for every real symmetric direction \(D\) along the true \(K+tD\) affine path, with \(\mathcal S,\mathcal U,\mathcal V\) exactly as stated in the author's `frozen_statement.md`.

The reviewed corollaries are:

- the domain condition itself implies \(0<K<I\), so all eight event probabilities are strictly positive at every interior center;
- all six coordinate directions are covered, including mixed diagonal-edge directions and edge-edge directions;
- \(\Omega\) is convex and the finite entropy chord inequality extends to the declared closure by continuity;
- if the nonzero edge graph is connected, then the full six-dimensional Hessian is negative definite at that center.

## Certification targets

This review attempts to certify only the following objects.

1. The eight event probabilities, their first derivatives, and their second derivatives from the determinant inclusion formula.
2. The product-density formula \(R=p/P_0\), the full first-density derivative \(g=p'/P_0\), and the full second-density derivative \(p''/P_0\), reconstructed directly from the eight probabilities.
3. The strict interior proof \(0<K<I\) and event positivity, including domain-boundary centers with \(|e_{ij}|=1/4\) and diagonal coordinates close to 0 or 1.
4. The normalized Fisher lower bound that retains the three-point coefficient.
5. The conditional Rayleigh square identity and the averaged two-point log-ratio bound.
6. The three-point log-ratio derivative bound and its rational constants.
7. The acceleration identity
   \[
   A_K(D)=2\sum_{i<j}\bar\theta_{ij}(d_id_j-h_{ij}^2)+4\Lambda W(D).
   \]
8. The two-edge and edge-diagonal coupling estimates used to combine Fisher and acceleration terms.
9. The final rational coefficient comparison with \(7/10\).
10. The strictness and degeneracy statements for connected two-edge centers, one-edge disconnected centers, and all-zero-edge centers.

## Exclusions

This review does not certify the unresolved general three-dimensional real kernel claim outside \(\Omega\), any \(n>3\) claim, complex Hermitian claims, scalar stationary entropy-rate claims, novelty, or the excluded PR30 author line. The second-round PR33 checkpoint is outside the accepted mathematical scope because the task statement says it adds plans but no new theorem or proof text.

## Verdict scale

- `ACCEPTED_SCOPED`: the submitted proof establishes the frozen T1--T3 claims in the stated scope, with any residual work only outside that scope.
- `NEEDS_FIX`: the frozen claims may be true, but the submitted proof has a repairable gap or inaccurate statement.
- `REFUTED`: a counterexample satisfies the frozen assumptions and violates a frozen conclusion.
- `INCOMPLETE`: the review cannot certify or refute within the assigned resources.
