# Round 2 frozen beta-zero slice

Status: OPEN_SUBPROBLEM. Proof agents must not change premises or replace an
exact zero by a tolerance. This supplements, and does not rewrite, round 1.
Baseline e476db1bb056af57e883a47f470ea0f4443c1837; dispatch PR #25.

For every connected real symmetric K of size three with 0<K<I, take the eight
exact DPP configuration probabilities p (Mobius inversion of inclusion
minors), their full score Fisher F, and all real symmetric directions in the
observation basis (11,22,33,12+21,13+31,23+32). All logarithms are natural.
Use the inherited conditional odds ell_ij and Lambda, N>0, d=det(N),
G(D,E)=tr(N^-1 D N^-1 E), and c(D)=tr(N^-1 D).
Put Z=sum 1/p, v_score=grad Lambda/sqrt(Z), F_pair=F-v_score v_score^T,
H=F_pair+dG, alpha=c^T H^-1 c, beta=v_score^T H^-1 c,
gamma=v_score^T H^-1 v_score. H is positive definite on this domain.

The precise new candidate is:

    beta(K)=0 implies d(K)*alpha(K)<=1.                    (B0)

This is a slice of the original global question. The full score is retained:
A=H+v_score v_score^T. At an exact beta zero, rho=d alpha; approximate zeros
do not authorize dropping beta^2/(1+gamma).

Realizability must remain exact. If K=[[x,a,b],[a,y,c],[b,c,z]], define
u=xy-q12=a^2, v=xz-q13=b^2, w=yz-q23=c^2, and
T=r-xyz+xw+yv+zu=2abc. Keep T^2=4uvw and its first and second derivatives
along genuinely affine K+tD. Keep the entire Rayleigh square polynomial,
not just evaluations at two conditioning endpoints. At zero edges use the
polynomial equations, with no division by T,u,v,w.

Success: a proof of B0 on its full frozen domain; a strict actual beta-zero
counterexample with d alpha>1 and a certified positive entropy chord; or a
new exact partial lemma / obstruction with a precise remaining obligation.
Zeros established by symmetry or interval-certified sign changes are valid
when feasibility and all claimed inequalities are controlled on the bracket.
Numerical smallness, an optimization non-hit, or a reformulation of rho is
not a proof. No Lambda=0 assumption, symmetry family, spectral gap, sign of
abc, or direction restriction is added to B0.

No novelty or main-theorem resolution is presumed. Proof authors and the
independent reviewer own separate files and contexts. Two different units
that return to the same unclosed gap trigger substantive stop, not expansion
of the same scan.
