# Frozen statement, formulas, and limits

The problem is the sign of H''(UAU^T;UVU^T) for the task's fixed rational 5 by 3 isometry U, 0<A<I_3 and any real symmetric V. H is the entropy of the entire random subset. Events of size at least four vanish identically along this fixed-support path and contribute zero; the other 26 probabilities are strictly positive. The target was not altered.

## Exact probability formulas

Let a=(1,2,3,4,5)^T, b=(2,-1,3,-2,1)^T and U be the first three columns of (I-2aa^T/(a^Ta))(I-2bb^T/(b^Tb)). Let r_i=U_i^T, w_ij=r_i cross r_j, d=det A, and q_S=det(U_S)^2 for |S|=3. Orthogonality gives U^TU=I. Cauchy--Binet gives sum q_S=1; this is also checked exactly in the script.

For B=A(I-A)^(-1), the L-ensemble expression p(S)=det(I-A)det((UBU^T)_S) follows from the probability generating determinant det(I-K+KZ) and expansion in principal minors. Consequently p(empty)=det(I-A). For one point, det(I-A)B=adj(I-A)A; the 3 by 3 Cayley--Hamilton identity expands this to A^2+(1-tr A)A+dI. For two points, the two-row Gram determinant is w^T adj(B)w, and det(I-A)adj(B)=d(A^(-1)-I)=adj A-dI. For three points, determinant multiplication gives p(S)=d q_S. These give all polynomial formulas used by the script and are valid for noncommuting A,V, because no simultaneous diagonalization is used.

Coordinates are x=(A11,A22,A33,A12,A13,A23). Their six symmetric basis matrices E_i have metric M=diag(1,1,1,2,2,2), so ||V||_F^2=v^T M v. Each p is a polynomial of degree at most three. The script differentiates each exact rational polynomial symbolically to obtain the full Jacobian J and Hessians B_S. Thus p'=Jv and p''=v^T B_S v.

For an independent numerical calibration, inclusion probabilities m(T)=det(K_T) are differentiated through each nonsingular principal minor. If Z_i=K_T^(-1)(UE_iU^T)_T, then m_i'=m tr Z_i and m_ij''=m[(tr Z_i)(tr Z_j)-tr(Z_i Z_j)]. Inclusion--exclusion supplies exact-event jets. The two implementations agree to about 5e-16 at the rational preflight fixture. Exact inclusion--exclusion probabilities at that fixture are additionally identical as rational numbers, and the polynomial identity sum p=1 is checked exactly.

## Entropy matrices and bounded design

For k=0,1,2,3 define F_k=sum_(|S|=k) J_S^T J_S/p_S and L_k=-sum_(|S|=k) log(p_S) B_S. The full curvature matrix is Q=sum_k(L_k-F_k). F_low=F_0+F_1+F_2. The geometry matrix is G=c Hess(det A), where c=-sum q log q. Selected directions are generalized eigenvectors for (F_low,M), (J_low^T J_low,M), (Q,M), (Q,F_low), and (G,F_low). No direction is chosen solely to maximize geometry/top Fisher.

Eight spectra are used: (0.2,0.4,0.6), (0.3,0.5,0.7), (0.4,0.6,0.8), (0.2,0.65,0.95), (0.35,0.75,0.9), (0.55,0.65,0.8), (0.58,0.67,0.75), and (0.65,0.65,0.65). Three orientations are I and the 3 by 3 Householder reflections of (1,2,3) and (2,-1,1). This gives 24 records but 22 distinct A. There are no random centers or adaptive retries. At the nine trace-two records, V=A(I-A) supplies an additional pair-null diagnostic, normalized after construction.

To see its mechanism directly, set T=A^(-1), s=tr(TV). Differentiating C=adj A-dI=d(T-I) yields DC[V]=d[s(T-I)-TVT]. With V=A(I-A), TVT=T-I and s=tr(I-A)=3-tr A=1 when tr A=2, hence DC[V]=0. This kills pair first derivatives; it does not kill D^2 C[V,V]. Furthermore p_empty'= -det(I-A)tr((I-A)^(-1)V)=-2det(I-A), so even this exact pair-null direction has an empty-event score cost.

## Legal domain and rational certificates

For positive A and I-A set X=A^(-1/2)VA^(-1/2) and Y=(I-A)^(-1/2)V(I-A)^(-1/2). Both A plus/minus hV are positive precisely when I plus/minus hX are positive, equivalent to h||X||_op<1. Their complements are positive precisely when h||Y||_op<1. Therefore the exact maximal open symmetric interval is |t|<1/max(||X||_op,||Y||_op), with infinity if V=0. A simpler sufficient condition is |t| ||V||_op < min(lambda_min(A),lambda_min(I-A)). The search records the first formula numerically; it is not used as an exact validity certificate.

The final rational fixtures instead use h=1/100 and exact positivity of all three leading principal minors of A+tV and I-A-tV at t=-h,0,h (Sylvester criterion). Convexity of the positive-definite cone proves the full intervening segment valid. Every probability and its first two derivatives is rational. The saved 70-decimal outward interval evaluations enclose -sum p log p, -sum p'^2/p -sum p'' log p, and the complete finite chord. These are computational certificates relying on mpmath's interval arithmetic, not formal proof-assistant certificates. No positive boundary chord was obtained, so no claim of an interior positive lift is made.

## Scope of result and sources

Polynomial formulas and calculus above are rebuilt from the supplied task; no external research theorem is used to conclude a curvature sign. Neither the 22 distinct negative center Hessians nor these two negative chords resolve the universal sign. No novelty claim or literature-absence claim is made. The parent unit handles broader prior-art audit. Author is the C2 directed-search child; no mechanism or review drafts were accessed.
