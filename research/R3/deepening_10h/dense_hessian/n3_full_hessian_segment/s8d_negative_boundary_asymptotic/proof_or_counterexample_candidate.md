# S8d negative boundary: analytic proof candidate

Author candidate, pending independent review. The frozen JSON passes the continuous bridge. Combined with the analytic tail, the candidate proves B=-Hess H positive definite for every -1<t<=-29/100, not by extrapolating the finite eigenvalue scouts.

## 1. Independent left-boundary coordinates

Use the frozen M8 line and s=t+1. Write

K=cU+aV+bW,
a=1/6+s/3, b=2/15+2s/3, c=s/5.

Use the fixed rational full Sym(3) basis

F0=U,
F1=(uv^T+vu^T)/7,
F2=(uw^T+wu^T)/11,
F3=V,
F4=W,
F5=(vw^T+wv^T)/24,

where u=(1,1,1), v=(1,2,-3), w=(5,-4,-1). Its Frobenius Gram matrix is diagonal with entries (1,12/7,252/121,1,1,49/24), hence it is a basis. In particular the basis includes arbitrary noncommuting mixing directions. Let r1=6/7, r2=126/121, r3=49/48 denote the squared off-diagonal scales in the normalized eigenbasis.

At t=-9/10, the V and W eigenvalues coincide and all observation diagonals coincide. This does not invalidate the fixed basis, K-affinity, strict feasibility or the entropy Hessian. No distinct-spectrum or heterogeneous-diagonal assumption is used anywhere in this argument.

## 2. Exact singular summand

The full-set atom p=det K=abc is the only vanishing atom at s=0. Its gradient in the displayed basis is

g=(ab,0,0,bc,ac,0).

Its Hessian h has only these nonzero entries:

h03=h30=b; h04=h40=a; h34=h43=c;
h11=-2br1; h22=-2ar2; h55=-2cr3.

These formulas are independently checked as exact polynomial identities against the Mobius event jets. For every one of the eight events, its second derivative along F0=U is identically zero, since U is rank one; the polynomial jets also check this identity.

For B=-Hess H, cancellation of the total second atom mass gives

B_ij=sum_S(p_{S,i}p_{S,j}/p_S+p_{S,ij}log p_S).

Let G be the contribution of the seven events other than the full set. They have strictly positive endpoint atoms and hence G is analytic through s=0. The exact decomposition is

B=gg^T/(abc)+h log(abc)+G.

Moreover G00=sum_{S!=123}p_{S,0}^2/p_S>=0. Therefore

B00=ab/c+G00 >= (1/9)/s.

The only singular off-diagonal entries in row zero are

B03=G03+b(1+log p), B04=G04+a(1+log p).

The two mixing diagonal terms are 2br1(-log p) and 2ar2(-log p). In the remaining (V,W,VW) block the full-atom diagonal terms bc/a, ac/b and -2cr3 log p are nonnegative when p<1. Its only off-diagonal full-atom contribution is c(1+log p), in the (V,W) entry.

No positivity assumption is made about the full regular matrix G.

## 3. Endpoint asymptotic sign

For ell=log(1/s), let T(s)=diag(sqrt(s),ell^(-1/2),ell^(-1/2),1,1,1). Then

T(s)^T B(s)T(s) -> diag(1/9,8/35,42/121,C0),

where C0=G(0)[3:6,3:6]. All singular mixed terms vanish under this congruence: the pole/finite terms are O(sqrt(s)log s), while the remaining finite-block full-atom terms are O(s log s). Analyticity controls the regular terms.

Rational logarithm intervals certify positive Gershgorin row margins for C0, approximately (3.5841579630,4.2480247952,8.3742584400). Thus the limit is strictly positive definite, proving eventual positivity of the entire B, not just its restriction to the line. These margins and congruence-scaled constants are not raw eigenvalue bounds for B.

The full Hessian is not asserted at s=0 itself. Along the original line only, the leading scalar curvature is H''(t)=-(1/225)/s+O(|log s|); this is consistent with the full result but is not used to prove it.

## 4. Explicit analytic tail 0<s<=1/1000

The following bounds are proved directly for the left full-set atom. They do not assume that the right-end certificate transfers.

Set h=1/1000, a0=1/6, b0=2/15, kappa=1/5, c0=a0*b0*kappa=1/225, k0=a0*b0/kappa=1/9. Set amax=a0+h/3 and bmax=b0+2h/3. Enclose G(s) with rational entry intervals [G] over 0<=s<=h, using only the seven nonvanishing events. Their interval probability floors are all strictly positive.

Let w(s)=-log(c0*s). Compute a rational upper bound w0 for w(h), and a rational lower bound Lmin for -log(amax*bmax*kappa*h). The exact calculation gives Lmin>2. On this tail,

0<-log p(s)<=w(s), and -log p(s)>=Lmin.

Partition B into its scalar pole A=B00 and the five remaining coordinates:

B=[[A,bvec^T],[bvec,R]], with A>=k0/s>0.

In remaining-coordinate order (UV,UW,V,W,VW), define

v=(0,0,bmax,amax,0),
u_i=maxabs([G]_{0,i+1})+v_i.

The exact row-zero formulas imply |bvec_i(s)|<=u_i+v_i*w(s). All u_i,v_i are nonnegative. Because w(s)>2, the functions s, s*w(s), and s*w(s)^2 are increasing on (0,h]; for k=1,2 their derivatives are w(s)^(k-1)(w(s)-k). Expanding products with nonnegative coefficients therefore gives

|bvec_i*bvec_j/A| <= Cij := h/k0*(u_i+v_i*w0)*(u_j+v_j*w0).

This does NOT assert w(s)<=w0, which would be false. The vanishing factor s is essential. The diagonal Schur subtraction lies in [-Cii,0]; off-diagonal subtractions lie in [-Cij,Cij]. The remaining (V,W) full-atom term satisfies

|c(1+log p)|<=kappa*h*(1+w0)=e.

Retain the favorable diagonal lower bound

d=(2*b0*r1*Lmin,2*a0*r2*Lmin,0,0,0),

and discard the other favorable full-atom diagonal contributions. Construct an interval model [M] by

[M]ii=[G]_{i+1,i+1}+[d_i-Cii,d_i],
[M]ij=[G]_{i+1,j+1}+[-Cij,Cij] for i!=j,

additionally widening its (V,W) entries by [-e,e]. The true Schur complement R-bvec*bvec^T/A equals a symmetric matrix in [M] plus a nonnegative diagonal matrix. The interval model is a lower model, not an enclosure of the unbounded positive logarithmic diagonal terms themselves.

A fixed rational upper-triangular P5 with positive diagonal is frozen in the JSON. Exact signed interval congruence P5^T[M]P5 has all Gershgorin row margins positive, minimum approximately 0.20009961668. Hence every model matrix is positive definite, then the true Schur complement is positive definite, then B is positive definite. This proves the entire tail -1<t<=-999/1000.

The same coarse construction at h=1/100 failed to produce a positive model; its midpoint Cholesky proposal failed. This is recorded as a bound/proposal failure, not a curvature sign reversal. The narrower h=1/10000 construction also passed but is unnecessary once h=1/1000 passes.

## 5. Continuous bridge and exact arithmetic acceptance

The remaining bridge is 1/1000<=s<=71/100, equivalently -999/1000<=t<=-29/100. The script adaptively bisects this CLOSED interval, with depth cap 14 and processed-node cap 4095. For each leaf it rebuilds the full eight-event interval B. Its midpoint high-precision evaluation is used only to propose an upper-triangular rational 6x6 P, with each entry denominator at most 4096.

Every accepted leaf has (i) positive exact atom interval floors, (ii) positive diagonal entries of P and hence invertibility, and (iii) all six positive exact Gershgorin row margins of P^T[B]P. Interval multiplication uses the sign of each rational congruence coefficient when selecting endpoints. Thus acceptance certifies all points of that leaf. Midpoint floating-point values never decide a proof sign.

The JSON retains every accepted leaf and every rejected internal node, including full preconditioners, row-margin fractions and atom floors. Its bridge.passed flag is true only if there are no failed final leaves; additionally the code checks the first and last endpoints and every shared neighboring endpoint exactly. Only if this continuous cover passes may it be combined with section 4 to claim the entire target -1<t<=-29/100.

The completed run passes: 162 accepted leaves, 161 rejected internal nodes, 0 failed final leaves, and 323 processed nodes, with maximum leaf depth 8. The smallest accepted transformed row margin is approximately 0.009384781967274894; the smallest exact atom lower bound is 11189/2500000000. All intervals and full fractions are retained. The bridge has a spectral feasibility margin at least 1/5000, attained by the U eigenvalue at its left endpoint. There is no positive uniform spectral margin for the analytic tail approaching s=0.

Thus section 4 and the completed bridge certify the proposed entire half-open interval. The 161 failed internal bounds are retained method failures resolved by subdivision; none is a sign witness against the Hessian.

The rational logarithm enclosure uses N=24 terms of log y=2*sum_{k>=0}z^(2k+1)/(2k+1), z=(y-1)/(y+1), after range reduction to 1<=y<=2. The omitted positive tail is at most 2*z^(2N+1)/((2N+1)*(1-z^2)). Powers of two use signed rational bounds for log 2. No floating rounding is used in the final inequalities.

## 6. Scope and review priorities

The result concerns the full real Sym(3) Hessian, including indefinite and noncommuting directions. The interior spectral collision at t=-9/10 is included; the strict feasible boundary t=-1 is excluded. At each individually certified point, continuity gives some ambient strict-kernel neighborhood with the same full-Hessian sign. There is no uniform neighborhood reaching through t=-1.

Independent reviewers should prioritize the signs and normalization of the full-set atom jets; the rank-one identity used for G00>=0; the weighted-log monotonicity; the lower-model-plus-nonnegative-diagonal Schur decomposition; and the rational bridge congruence and coverage ledger. The script imports the previously independently checked S8 verification helper, not an author Hessian module; its dependency hash is frozen. A reviewer should inspect or replace that dependency rather than assume it from its name.

The author does not assign CORRECT. Finite eigenvalue scouts remain SCOUT; failed interval bounds are method failures unless independently converted into a reliable sign witness.
