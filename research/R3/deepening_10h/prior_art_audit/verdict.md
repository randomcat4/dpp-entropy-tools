# D10-Prior verdict

STATUS: CORRECT

This work unit only audits prior-art scope. It does not verify my D10-A proof, does not certify a real R3 counterexample, and does not revise any shared branch files.

## Gu report

Source checked: Yuzhou Gu, *Entropy of Determinantal Point Processes*, author-hosted report, <https://sevenkplus.com/data/dpp.pdf>.

Verdict: CORRECT as R3 prior-art exclusion.

- Corollary 6 occupies the scalar \(0\)-to-\(K\) thinning path \(H(tK)\ge tH(K)\).
- Theorem 7 occupies rank-one marginal-\(K\) affine directions.
- Exact atom semantics are sound: the report works with exact atom probabilities \(f_S\) and uses inclusion probabilities through Möbius/inversion relationships.
- The rank-one determinant-affine step is valid because every principal perturbation has rank at most one, so each inclusion determinant is affine in the path parameter; exact atoms are affine by linear inversion.
- Boundary handling in the report is terse. The clean completion is to use concavity and continuity of \(-x\log x\) on \([0,\infty)\). For the project's strict-interior R3 kernels, this is not a blocking gap.

Conclusion: do not repackage rank-one \(K_+-K_-\) directions or \(0\)-to-\(K\) thinning as new R3 progress.

## Hino--Yano and T1 information geometry

Sources checked:

- T1 branch `origin/research/T1-curvature-structure:research/T1/prior_art.md`
- T1 branch `origin/research/T1-curvature-structure:research/T1/audits/prior_art_conditions.md`
- Hino--Yano, *Duality induced by an embedding structure of determinantal point process*, arXiv:2404.11024, <https://arxiv.org/abs/2404.11024>

Verdict: T1's caution is CORRECT.

Hino--Yano is directly relevant prior art for DPP information geometry, Fisher information, log-linear embedding, and \(e\)-curvature language. It does not directly control the sign of this project's finite-window Shannon entropy Hessian along marginal-kernel affine paths \(K(t)=K_0+tD\).

The implication direction is:

\[
\text{Hino--Yano}
\Rightarrow
\text{background/constraints for information-geometric DPP tools};
\]

not

\[
\text{Hino--Yano \(e\)-curvature}
\Rightarrow
\text{R3 Shannon \(H(K)\) \(K\)-affine Hessian sign}.
\]

The missing step is explicit: Shannon entropy curvature contains both the Fisher negative-square term and the atom-acceleration term
\[
-\sum_S p''_S(t)\log p_S(t).
\]
Hino--Yano's \(e\)-curvature does not automatically sign-control that term under a \(K\)-affine pullback.

## Overall prior-art conclusion

No critical gap was found in using Gu's report as a prior-art exclusion for rank-one/thinning routes, provided the boundary addendum is remembered. No direct Hino--Yano-to-R3 curvature implication was found; the T1 branch correctly labels that as a scope limitation rather than a solved sign theorem.

This means D10 follow-up routes should:

- exclude rank-one \(K\) directions and scalar thinning from novelty claims;
- cite Hino--Yano for information-geometry background only;
- prove any \(K\)-affine Shannon Hessian sign criterion directly, including the atom-acceleration term.

No server was used. No sub-agent was spawned. No `C:\canglan\` path was accessed. No shared files were modified.
