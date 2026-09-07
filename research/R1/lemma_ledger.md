# R1 lemma ledger

| Item | Status | Notes |
| --- | --- | --- |
| Event-probability formula | KNOWN | For a marginal kernel DPP, exact event probabilities are Mobius inversions of principal minors, equivalently `(-1)^|S^c| det(K-I[S^c])`. |
| First and second event derivatives | IMPLEMENTED | The scout uses determinant differentiation on `K+tV-I[S^c]`; independent finite differences are required before trusting search output. |
| Exact chord certificate | IMPLEMENTED | `certificate/certify_real_chord.py` uses rational determinants, Sylvester checks, and rational log intervals. |
| Diagonal-center Hessian exclusion | VERIFIED | If `K=diag(p_i)`, then `D^2H(K)[V,V] = -sum_i V_ii^2/(p_i(1-p_i)) <= 0` for every real symmetric V; commit-bound review: `verification/diagonal_hessian_commit_review.md`. |
| Diagonal-center finite-chord exclusion | VERIFIED | Every nontrivial feasible real-symmetric chord centered at a diagonal strict contraction has strictly negative midpoint gap; the failed `t=0` pre-freeze wording is retained. Commit-bound review: `verification/diagonal_midpoint_commit_review.md`. |
| General real-symmetric concavity | OPEN_IN_R1 | No proof is claimed by finite computation. |
