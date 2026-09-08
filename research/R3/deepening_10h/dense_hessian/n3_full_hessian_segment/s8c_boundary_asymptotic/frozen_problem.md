# D10-S8c: positive feasibility boundary of the M8 line

Status: PROOF_CANDIDATE_PENDING_INDEPENDENT_REVIEW. Author work, not an independent certification.

Let u=(1,1,1), v=(1,2,-3), w=(5,-4,-1), and let U=uu^T/3, V=vv^T/14, W=ww^T/42. These are mutually orthogonal rank-one projections summing to I. Freeze

K(t)=(1/5+t/5)U+(1/2+t/3)V+(4/5+2t/3)W.

The question is whether the full real-symmetric Hessian of the full-subset Shannon entropy is strictly negative definite throughout 29/100 <= t < 3/10. Directions are arbitrary elements of Sym(3), not just commuting or positive-semidefinite directions. Exact probabilities mean P(Y=S), recovered by Mobius inversion of det(K_A), not det(K_S).

Candidate answer: yes, via six rational interval leaves on [29/100,299/1000] and one analytic singular Schur-complement majorant for [299/1000,3/10). The endpoint 3/10 itself is excluded. This proves no general global DPP entropy concavity assertion.

All arithmetic witnesses and all unsuccessful bound attempts are in boundary_probe_results.json. The numerical inverse-Cholesky operations only propose rational preconditioners; no floating-point sign determines a proof acceptance. The probe depends on the already independently checked S8 verification helper, not an author S8/S8b Hessian module. Dependency and source hashes are frozen in the result.
