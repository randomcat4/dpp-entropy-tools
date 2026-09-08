STATUS: CORRECT

Reviewed commit: `a49051d2f768ec2b926a2e4d68d5286b054f9656`.

- Frozen statement: `research/R1/frozen_diagonal_midpoint_v1.md`; Git blob ID `5deb1c8f8d11628904f6da37d9d1e259644f9a88`.
- Candidate proof: `research/R1/proofs/diagonal_midpoint_candidate.md`; Git blob ID `ed7607aca2aa4384a4d8a467b038c0ece388889d`.

Both mathematical documents were read exclusively through `git show <reviewed-commit>:<path>`. The blob IDs were resolved from the same commit. This report reviews those committed objects, not their working-tree versions or any later revision. The reviewer did not participate in writing this D1 proof and did not modify the proof or frozen statement.

## Verdict and premise audit

The proof establishes the frozen strict inequality for every n>=1, every diagonal D with 0<d_i<1, every nonzero real symmetric V, and every t>0 for which D-tV and D+tV are strict positive contractions. No additional assumption on normalization, sign pattern, rank, or dimension is used.

The candidate's opening discussion of a pre-freeze t=0 failure is not a counterexample to the reviewed frozen statement. The actual frozen statement and the subsequent candidate theorem both explicitly assume t>0 and V!=0. Every invocation of strictness below uses these assumptions correctly.

## Full-event entropy and inclusion semantics

The map from a random subset S of [n] to its binary indicator vector is a bijection. Consequently, the Shannon entropy of the full event distribution in the frozen statement is exactly H(X_1,...,X_n), with no marginal-entropy substitution or loss of outcomes.

For a diagonal D, the candidate explicitly applies the required Mobius inversion and obtains

`P_D(X=S)=product_{i in S} d_i product_{j not in S}(1-d_j)`.

This proves that H(D)=sum_i h(d_i). Elsewhere, K_ii is used only for a one-point marginal, and det K_{i,j} only for the valid two-point inclusion event {X_i=X_j=1}. No principal minor is mistaken for the exact event probability of an arbitrary subset.

## Subadditivity and its strict equality condition

For finite binary variables, H(X_1,...,X_n)<=sum_i H(X_i), with equality exactly when the full joint law is the product of its marginals. The chain-rule justification in the candidate is valid: equality in every conditioning inequality makes X_i independent of its full preceding vector; iterating these factorizations gives mutual independence. Conversely, mutual independence gives equality. Pairwise non-independence therefore suffices to force a strict entropy deficit.

Strict endpoint feasibility implies 0<(K_+)_ii,(K_-)_ii<1 by the Rayleigh quotient on each coordinate vector. Binary entropy has h''(x)=-1/[x(1-x)]<0 on this interval. Its midpoint inequality is strict precisely when the two marginal parameters differ, equivalently when t V_ii!=0. Thus one nonzero diagonal entry of V makes the sum of marginal midpoint inequalities strict, and the endpoint subadditivity bounds preserve the desired strict inequality.

## Purely off-diagonal directions

If all V_ii vanish but V!=0, real symmetry ensures an off-diagonal pair i<j with V_ij!=0. At both endpoints the one-point marginals are d_i and d_j, while the exact inclusion probability is

`P(X_i=X_j=1)=d_i d_j-t^2 V_ij^2<d_i d_j`.

The determinant sign and square are correct for either endpoint. Strictness follows from t>0 and V_ij!=0. This contradicts independence of that pair, hence also mutual independence of all indicators. Therefore each endpoint separately has entropy strictly less than sum_i h(d_i)=H(D); their average is strictly smaller as well.

For n=1 a nonzero purely off-diagonal direction does not exist; every allowed nonzero V is covered by the nonzero-diagonal case. No degenerate case is left uncovered.

## Equality audit

In the weak midpoint inequality, the total deficit is the sum of nonnegative endpoint subadditivity deficits and nonnegative binary-entropy midpoint deficits. Equality thus requires every t V_ii=0 and independence at both endpoints. Under endpoint independence, each two-point inclusion determinant forces the corresponding real off-diagonal entry to be zero. Since the midpoint is diagonal, this means every t V_ij=0. Together these conditions give tV=0. Conversely, tV=0 makes both endpoints equal D and gives equality.

The candidate therefore states the exact equality condition. The frozen assumptions t>0 and V!=0 exclude it. There is no hidden reliance on infinitesimal curvature, a small step size, or a numerical tolerance.

## Scope

No critical gap was found. This verifies only the frozen diagonal-midpoint chord theorem at the recorded commit. It does not establish global real-symmetric entropy concavity, numerical-search coverage, or novelty. No finite-search outcome or previous Hessian verification is used as evidence for this proof.
