# R1 lemma ledger

| Item | Status | Notes |
| --- | --- | --- |
| Event-probability formula | KNOWN | For a marginal kernel DPP, exact event probabilities are Mobius inversions of principal minors, equivalently `(-1)^|S^c| det(K-I[S^c])`. |
| First and second event derivatives | IMPLEMENTED | The scout uses determinant differentiation on `K+tV-I[S^c]`; independent finite differences are required before trusting search output. |
| Exact chord certificate | IMPLEMENTED | `certificate/certify_real_chord.py` uses rational determinants, Sylvester checks, and rational log intervals. |
| Diagonal-center Hessian exclusion | VERIFIED | If `K=diag(p_i)`, then `D^2H(K)[V,V] = -sum_i V_ii^2/(p_i(1-p_i)) <= 0` for every real symmetric V; commit-bound review: `verification/diagonal_hessian_commit_review.md`. |
| Diagonal-center finite-chord exclusion | VERIFIED | Every nontrivial feasible real-symmetric chord centered at a diagonal strict contraction has strictly negative midpoint gap; the failed `t=0` pre-freeze wording is retained. Commit-bound review: `verification/diagonal_midpoint_commit_review.md`. |
| Block-cross finite-chord exclusion | VERIFIED | At a block-diagonal strict midpoint, every nonzero pure cross-block feasible chord has strictly negative midpoint gap. Frozen commit `64c5bc0...`; non-author commit-bound review: `verification/block_cross_commit_review.md`. |
| Global real `2 x 2` concavity | VERIFIED | The complete-event entropy Hessian is negative semidefinite on every strict real `2 x 2` kernel; all nontrivial feasible chords are strict. Frozen commit `603300c...`; non-author review: `verification/n2_concavity_commit_review.md`. |
| Block-composition gap bound | VERIFIED | At a block-diagonal center, the global gap is at most the sum of principal-block gaps; cross-block coupling makes the bound strict. Frozen commit `603300c...`; non-author review: `verification/block_composition_commit_review.md`. |
| `1 x 1` / `2 x 2` block-center exclusion | VERIFIED | Combining the preceding two entries excludes every nontrivial real-symmetric chord centered at a block diagonal kernel whose blocks have size at most two. |
| Margin-stratified real search | FINITE_NO_HIT | Phase 2 completed 42,578 formal calls plus 823 validation calls with no value above `1e-6`. This is a denominator, not a theorem. |
| Connected `n=3` attack | FINITE_NO_HIT | Phase 4 completed 136,898 continuous successful calls; all 8,053 floating positives were reviewed at 90/140 digits and none survived. This is not a proof. |
| Equicorrelated `n=3` Hessian reduction | DERIVED / SIGN_OPEN | Exact `S_3` symmetry reduces six directions to a trivial `2 x 2` block and two copies of one standard `2 x 2` block. Both trivial diagonal signs are proved; its determinant and the standard block remain open. |
| General real-symmetric concavity for `n>=3` | OPEN_IN_R1 | No proof is claimed by finite computation; the next minimal obstacle is a connected `3 x 3` center. |
