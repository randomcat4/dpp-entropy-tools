# Boundary singularity and a candidate certificate for the whole positive tail

Status: PROOF_CANDIDATE_PENDING_INDEPENDENT_REVIEW.

## 1. Probability semantics and strict feasibility

For S subset {1,2,3}, use p_S(K)=sum_{A superset S}(-1)^{|A|-|S|} det K_A. The independent S8 helper constructs these exact degree-three event polynomials and their first and second Sym(3) derivatives. The six observation coordinates are (11,22,33,12,13,23), with off-diagonal directions E_ij+E_ji; no Frobenius-gradient conversion is used here.

Because the three displayed eigenvalues in frozen_problem.md belong to (0,1) for -1<t<3/10, the entire proposed half-open interval is strictly feasible. The upper spectral margin is (2/3)(3/10-t), so there is no uniform positive spectral margin at the excluded endpoint.

Put s=3/10-t, a=37/50+s/5, b=2/5+s/3, c=(2/3)s. Then I-K=aU+bV+cW. The endpoint atoms in mask order 0,...,7 are

(0,37/210,296/2625,188/875,37/5250,311/1750,136/875,39/250).

Only the empty event vanishes, and it vanishes to first order:

p_empty=abc=(74/375)s+(49/225)s^2+(2/45)s^3.

The other seven atoms are analytic and strictly positive at s=0, with minimum 37/5250. These values and identities are checked in exact rational arithmetic.

## 2. A fixed full basis, and the exact singular summand

Use the six directions, in order,

F=(W,(uw^T+wu^T)/11,(vw^T+wv^T)/24,U,V,(uv^T+vu^T)/7).

Their Frobenius Gram matrix is diagonal with entries (1,252/121,49/24,1,1,12/7). Thus they are a basis of all Sym(3). Write r1=126/121, r2=49/48, r3=6/7 for the squared off-diagonal scales in the normalized eigenbasis.

In F coordinates the empty atom has gradient

g=(-ab,0,0,-bc,-ac,0),

and its Hessian h has only the following nonzero entries:

h03=h30=b; h04=h40=a; h34=h43=c;
h11=-2br1; h22=-2ar2; h55=-2cr3.

All these are polynomial identities, verified by the exact event jets, not fitted asymptotics. Moreover p_{S,00}=0 for EVERY S: each event determinant is affine along the rank-one direction W. The script checks this for all eight events.

For B=-Hess H, cancellation of sum_S p_{S,ij}=0 gives

B_ij=sum_S(p_{S,i}p_{S,j}/p_S+p_{S,ij} log p_S).

Consequently B=gg^T/(abc)+h log(abc)+G, where G is the sum over the seven nonempty atoms. G is analytic through s=0. In particular G00=sum_{S nonempty} p_{S,0}^2/p_S >=0. No positive-semidefiniteness of the entire G is assumed.

The pole entry and the only pole-to-finite singular off-diagonals are

B00=ab/c+G00 >= (111/250)/s,
B03=G03+b(1+log p_empty),
B04=G04+a(1+log p_empty).

Other B0j equal G0j. The mixing diagonal entries have positive contributions 2br1(-log p_empty), 2ar2(-log p_empty). In the remaining U,V,UV block the empty-event diagonal contributions are bc/a, ac/b, and -2cr3 log p_empty, all nonnegative whenever p_empty<1. Its only off-diagonal contribution is B34_empty=c(1+log p_empty).

## 3. Rigorous local asymptotic, independent of an explicit radius

For ell=log(1/s) and S(s)=diag(sqrt(s),ell^(-1/2),ell^(-1/2),1,1,1),

S(s)^T B(s) S(s) -> diag(111/250,504/605,1813/1200,C0),

where C0=G(0)[3:6,3:6]. The pole-finite cross terms are O(sqrt(s) log s); log-to-finite cross terms tend to zero; the empty contribution in the finite block is O(s log s). Analyticity handles the regular terms.

Exact rational log intervals give all three Gershgorin row margins of C0 positive, minimum approximately 0.9885840928424285. The exact endpoints and margins are stored in the JSON. Hence this limit is positive definite and B(s) is positive definite for all sufficiently small s>0. This is congruence, not similarity; the displayed margins are not raw eigenvalue bounds for B.

The full Hessian at s=0 is not asserted to exist: the empty event vanishes and the ambient entropy has a singular boundary. Along the original line, its leading scalar curvature is H''(t)=-(74/375)/s+O(|log s|), consistent with, but much weaker than, the full Hessian result.

## 4. An explicit analytic tail: 0<s<=1/1000

Freeze h=1/1000, a0=37/50, b0=2/5, kappa=2/3, c0=a0*b0*kappa=74/375, k0=a0*b0/kappa=111/250. Let amax=a0+h/5 and bmax=b0+h/3. Compute a rational interval enclosure [G] of G on t in [3/10-h,3/10], using only the seven nonempty atoms; all their interval probability floors are strictly positive.

Set w(s)=-log(c0*s). Let w0 be a rational upper bound for w(h), and Lmin a rational lower bound for -log(amax*bmax*kappa*h). The calculation certifies Lmin>2. Since c0*s<=p_empty<=amax*bmax*kappa*s, we have -log p_empty<=w(s) and -log p_empty>=Lmin throughout the tail.

Split coordinate 0 from the remaining five and write B=[[A,bvec^T],[bvec,R]]. We have A>=k0/s>0. In remaining-coordinate order (UW,VW,U,V,UV), define

vcoef=(0,0,bmax,amax,0),
ucoef_i=maxabs([G]_{0,i+1})+vcoef_i.

All these coefficients are nonnegative. The exact formulas in section 2 give |bvec_i|<=ucoef_i+vcoef_i*w(s). For k=0,1,2, differentiation gives

d(s*w(s)^k)/ds=w(s)^(k-1)(w(s)-k) >=0,

with k=0 interpreted directly as derivative 1. Because w(s)>2, expanding the product with nonnegative coefficients yields the uniform bound

|bvec_i*bvec_j/A| <= Cij := (h/k0)(ucoef_i+vcoef_i*w0)(ucoef_j+vcoef_j*w0).

This weighted-log monotonicity, NOT the false bound w(s)<=w0, is essential. The diagonal Schur subtraction belongs to [-Cii,0]; each off-diagonal subtraction belongs to [-Cij,Cij]. Also

|c(1+log p_empty)| <= kappa*h*(1+w0)=e,

using monotonicity of s and s*w(s).

Retain the fixed favorable diagonal d=(2*b0*r1*Lmin,2*a0*r2*Lmin,0,0,0), and discard the other favorable empty-atom diagonal terms. Form the symmetric interval matrix [M] by

[M]ii=[G]_{i+1,i+1}+[d_i-Cii,d_i],
[M]ij=[G]_{i+1,j+1}+[-Cij,Cij] for i!=j,

and widen its (U,V) and (V,U) entries by [-e,e]. For every s in (0,h], the true Schur complement R-bvec*bvec^T/A equals a symmetric matrix M_s in [M], plus a nonnegative diagonal matrix. In particular [M] need not enclose the unbounded positive logarithmic diagonals themselves. This lower-model formulation is what makes a compact uniform interval possible.

The JSON freezes a rational upper-triangular 5x5 matrix P with positive diagonal, obtained by rounding a floating-point proposal to denominators at most 4096. Therefore P is invertible. Exact interval arithmetic for P^T[M]P gives positive Gershgorin row margins, minimum approximately 0.6499154101790116. It follows that every M_s is positive definite, then the Schur complement is positive definite, then B is positive definite. This covers the entire half-open tail [299/1000,3/10), not only selected points.

## 5. Six exact leaves bridge [29/100,299/1000]

On each closed leaf below, compute the full eight-event interval B and certify a fixed rational 6x6 upper-triangular congruence. All atom floors and all six Gershgorin margins are strictly positive. The displayed decimals are explanatory only; all rational matrices, probability floors and row-margin fractions are in the JSON.

| Leaf | Minimum transformed row margin (approx.) |
| --- | ---: |
| [29/100,1169/4000] | 0.58346969849 |
| [1169/4000,589/2000] | 0.46706260452 |
| [589/2000,1187/4000] | 0.20663148369 |
| [1187/4000,2383/8000] | 0.44876638452 |
| [2383/8000,191/640] | 0.63752215500 |
| [191/640,299/1000] | 0.49451109150 |

There are 11 processed nodes: 6 accepted leaves and 5 rejected internal nodes. There are no failed final leaves. The sorted leaf endpoints coincide exactly and cover the bridge. The interval probability floors are positive; the smallest is approximately 0.00015643118056. Preconditioner diagonals are positive and each denominator is at most 4096. No midpoint numerical eigenvalue is used as an acceptance criterion.

Combining the six leaves and the analytic tail establishes the candidate claim for every t in [29/100,3/10) and every nonzero D in Sym(3): H''(K(t))[D,D]<0. At each such individual point, smoothness and strictness give some ambient open neighborhood of strictly feasible kernels with the same full-Hessian sign. No uniform-radius neighborhood extending through the excluded endpoint is claimed.

## 6. Rational logarithms, provenance, and review priorities

For 1<=y<=2, z=(y-1)/(y+1), bound log y between 2*sum_{k=0}^{N-1} z^(2k+1)/(2k+1) and that sum plus 2*z^(2N+1)/((2N+1)*(1-z^2)). Range reduction x=2^m*y uses the corresponding signed bounds for m log 2. Here N=24 and all arithmetic is rational. Interval products choose endpoints according to coefficient signs, including negative congruence coefficients.

The script imports only the pre-existing nonauthor S8 verifier fresh_s8_audit.py; source hash is in run_log.md and JSON. It rebuilds the exact event jets and checks the boundary formulas before issuing certificates. This dependency must be inspected or independently replaced by the reviewer. Numpy proposes rational P; it is not part of the proof arithmetic. The JSON retains the exact fractions without denominator truncation.

Most fragile review points: (i) off-diagonal basis normalization; (ii) exact rank-one identity p_{S,00}=0 used for the scalar pole lower bound; (iii) monotonicity of s*w^k, rather than w itself; (iv) the model-plus-nonnegative-diagonal Schur argument; (v) congruence interval signs and preconditioner invertibility. All must be independently checked before changing status.

The coarse h=1/100 majorant fails (minimum transformed margin approximately -4.18852725571); this is only failure of that bound. A h=1/10000 attempt passes but is not needed. No failed bound is interpreted as a positive-curvature example, and no finite search is promoted to a theorem.
