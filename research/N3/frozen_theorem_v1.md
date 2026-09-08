# Frozen theorem v1

The route owner freezes this statement. Proof and review agents may not
alter, supplement, or reinterpret its premises.

## Objects and definitions

For every real symmetric 3 by 3 matrix K with 0<K<I, let p_S be the exact
configuration probabilities of its determinantal process, obtained by
Mobius inversion of inclusion minors. Let H(K)=-sum p_S log p_S (natural logs).
For every real symmetric D the target is -Hess H(K)[D,D]>=0.
All directions, including indefinite and noncommuting ones, are included.

At connected K use l_ij=log(p_empty p_ij/(p_i p_j)),
Lambda=log(p_123 p_1 p_2 p_3/(p_empty p_12 p_13 p_23)),
N=-diag(l_23,l_13,l_12)-Lambda K>0, and
F(D,E)=sum dp_S[D]dp_S[E]/p_S.
The inherited exact representation is B(D,D)=F(D,D)-2 tr(N adj D).
The first unit attacks the equivalent constrained inequality

    F(D,D)+det(N) tr(N^-1 D N^-1 D) >= det(N)
    whenever tr(N^-1 D)=1.

This equivalence is background, not a new result. A new lemma must exploit
the actual event map, especially
p_empty p_ij-p_i p_j=-[(1-K_kk)K_ij+K_ik K_jk]^2 and
p_k p_123-p_ik p_jk=-[K_kk K_ij-K_ik K_jk]^2.

## Success and excluded interpretations

A proof must cover arbitrary strict kernels; disconnected points may be
handled by smooth continuity from connected points, without using N^-1 at
singular N. A counterexample requires rationalized K,D,t, strict feasibility
of K+-tD, and rigorously positive Delta=(H(K-tD)+H(K+tD))/2-H(K).
Numerical rho>1 is only a candidate. rho approaching one is not a violation.
Artificial independent choices of F and N are not DPP counterexamples.
Counting entropy, complex kernels, nonlinear paths, and dimension >=4 are
outside this frozen target. No uniform rho<c<1 is assumed.

## Evidence and provenance

Source: issue #20 and the exact public baseline recorded in README.
The original problem remains unproved. A complete candidate must be frozen
and checked by two nonauthor independent contexts before claiming resolution.
First-unit finite probes use recorded seeds and actual executed coverage.
No novelty or Lean certification is implied by an analytic or numerical result.
