# Frozen round-two face target v1

Proof and review agents must not modify these premises.

## Object and exact target
Fix U in R^(4x3), U^T U=I3. The unit null vector z of U^T has z_i!=0 for
all four observed coordinates. Fix real symmetric A,V in Sym(3) and t>0 with
0<A-tV,A+tV<I3. Set K_j=U(A+j tV)U^T for j=-1,0,+1.
This is a fixed-U affine chord in the original four observed coordinates.
A and V need not commute. There are no sign/diagonal/equal-scale restrictions.

The exact event law is
p_K(S)=(-1)^(4-|S|)det(K-diag(1_{i notin S})).
The full event p_K([4]) is identically zero on the entire face; its derivatives
are zero. For every proper S the probability is strictly positive under the
stated assumptions (support proof is an explicit child obligation).
H_face(A;U)=-sum_(S proper) p_K(S)log p_K(S).

Investigate the universal inequality
Delta_face=(H_face(A-tV;U)+H_face(A+tV;U))/2-H_face(A;U)<=0.
An equivalent interior-of-face differential target is Hess H_face(A)[V,V]<=0.
There are six independent symmetric V coordinates. Floating non-hits cannot
prove either universal statement. A positive differential signal is a candidate
requiring a fixed finite positive chord.

## Strict-kernel transfer obligation
For a fixed boundary chord with strict positive gap, define for all three j
K_j(e)=(1-2e)K_j+e I4 with the same rational 0<e<1/2.
The required proof is strict feasibility, preserved midpoint and finite entropy
continuity giving existence of a positive-gap interior chord for small e.
A numerical or existential lift is not itself a strict finite certificate:
freeze rational U,A,V,t,e and certify the final gap with exact events and
rigorous log enclosures. No exchange of Hessians and boundary limits is assumed.

## Success and nonclaims
A disproof requires exact rational support/face feasibility and positive finite
gap, plus a strictly internal lifted rational certificate for the original
target. A scoped structural theorem needs complete proof and non-author review.
The original open conclusion requires two fresh non-author reviewers.
Support and lifting lemmas alone do not resolve face concavity. The coordinator
preflight and finite class searches are diagnostics only; novelty is unconfirmed.
No five-point expansion without a concrete support-mechanism reason.
