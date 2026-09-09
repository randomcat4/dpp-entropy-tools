# Restricted compensation results — proof v1

This proves the three restricted statements in frozen_statement.md. It does not prove the original full-face conjecture. Author: C2 main, with the exact logarithmic cancellation communicated independently by the mechanism child. Computational constants are rational certificates, not floating-point signs.

## 1. Support, probabilities, and legal paths

The displayed U satisfies U^T U=I. Every three-row determinant is nonzero; all ten squared determinants are computed exactly in main_check.py. Thus every subset of at most three rows is independent. Put d=det A, E=I-A and L=U A E^{-1} U^T. The generating determinant of the L-ensemble gives

    p_S = det(E) det(U_S A E^{-1} U_S^T).

For completeness, multiplying K-diag(1_{S^c}) on the left by I+L gives, with S first, blocks [L_S,0; L_{S^c,S},-I]. Its signed determinant therefore equals det(I+L)^{-1}det L_S. Expanding the determinant in the diagonal entries of diag(1_{S^c}) gives the stated inclusion-exclusion event law. det(I+L)=det(E)^{-1} follows from U^T U=I. The principal L blocks are positive definite for |S|<=3 and singular for larger S. This proves the asserted fixed support.

Write C(A)=adj A-d I and R(A)=A^2+(1-tr A)A+d I. Then

    p_empty=det E,
    p_i=r_i^T R(A)r_i,
    p_ij=w_ij^T C(A)w_ij,
    p_S=d det(U_S)^2  (|S|=3).

To derive the singleton formula, det(E) A E^{-1}=A adj(E). Expanding adj(E) as a quadratic in A and using the degree-three characteristic identity reduces it to R(A). For pairs, the cross-product minor identity det([x,y]^T M[x,y])=(x cross y)^T adj(M)(x cross y) for invertible symmetric M follows first for diagonal M and then by orthogonal conjugation. Here M=A E^{-1}, so det(E)adj(M)=d(A^{-1}-I)=C(A). The triple formula follows by taking determinants. These identities are also independently compared to all 32 inclusion-exclusion polynomials in the attached computation.

For V nonzero, define

    h_*^{-1}=max(||A^{-1/2} V A^{-1/2}||op,
                 ||E^{-1/2} V E^{-1/2}||op).

Both A+hV and A-hV are strict contractions exactly when 0<=h<h_*. Indeed conjugating each of the four positive-definiteness conditions by the respective inverse square root yields I plus or minus h times the indicated symmetric matrix. Its eigenvalues are positive for both signs exactly when h times its operator norm is less than one. A sufficient bound on the cone is h<min(1-2e,e)/||V||op. Consequently every direction considered has a nonempty legal interval, including noncommuting directions.

## 2. Entropy derivative and cancellation of the rare-event logarithm

The 26 positive probabilities are polynomials; H is analytic at every 0<A<I. Normalization and the one-point inclusion probabilities give

    sum p_S=1,   sum |S|p_S=tr A.

Along the affine path this implies sum p_S'=sum p_S''=0 and

    sum (3-|S|)p_S''=0.                                      (2.1)

Differentiating the finite entropy sum twice therefore gives exactly

    H''=-sum (p_S')^2/p_S -sum p_S''log p_S.                  (2.2)

At A=I-eB, with e fixed at the center, define g_S=p_S/e^(3-|S|). Equation (2.1), applied to the actual derivatives in V, implies the exact identity

    sum p_S''log p_S = sum p_S''log g_S.                     (2.3)

One does not differentiate an e-dependent parametrization here: e is a positive number used to split each logarithm at the chosen center. The coefficient of log e cancels because the expected deficit 3-|X| is affine in A. No rare event is discarded, and no limit is interchanged.

## 3. An exact frame inequality

For any symmetric 3 by 3 matrix X, set

    Q(X)=sum_{i<j}(w_ij^T X w_ij)^2/||w_ij||^2.

For the specified rational U,

    Q(X) >= (1/22)||X||_F^2.                                (3.1)

Here is a finite exact certificate and its interpretation. In coordinates x=(X11,X22,X33,X12,X13,X23), set D=diag(1,1,1,2,2,2) and a(w)=(w1^2,w2^2,w3^2,2w1w2,2w1w3,2w2w3)^T. The rational matrix G=sum a(w)a(w)^T/||w||^2 satisfies Q(X)=x^T Gx and ||X||F^2=x^T Dx. main_check.json contains every entry of G and the six leading principal minors of G-D/22; all numerators and denominators are positive. Sylvester's criterion proves G-D/22 positive definite, which implies (3.1). This computation uses exact rational operations only. The recipe with the displayed U is itself sufficient to reconstruct the certificate without that JSON. As a cross-check, 1/tr(D G^{-1}) equals

    14596961251947412891381898243211648288 /
    315011606151606360378912154946004466727 > 1/22.

The frame spans all six symmetric coordinates. It is not a restriction to commuting or diagonal matrices. Its use below is rotation invariant in the matrix X, with U kept fixed.

## 4. Uniform pair Fisher lower bound

Let A=I-eB, I<=B<=2I, and delta=2e<=1/8. All eigenvalues lambda_i of A lie in [1-delta,1). In an orthonormal eigenbasis C(A) has diagonal entries c_i=(1-lambda_i)lambda_j lambda_k. The differential DC[V] has off-diagonal entries

    (DC[V])_ij=-lambda_k V_ij,                              (4.1)

including repeated eigenvalues by the polynomial differential formula. Its diagonal entries are

    (DC[V])_ii=-lambda_j lambda_k V_ii
       +(1-lambda_i)(lambda_k V_jj+lambda_j V_kk).            (4.2)

The linear map DC+Id on diagonal matrices has diagonal coefficients bounded by 2delta and off-diagonal coefficients by delta. Both maximum row sum and maximum column sum are at most 4delta, so its Euclidean operator norm is at most 4delta (by ||M||2<=sqrt(||M||1||M||infinity)). On off-diagonal matrices, (4.1) gives norm at most delta. The two subspaces are orthogonal in Frobenius norm and preserved. Hence

    ||DC[V]+V||F<=4delta||V||F,
    ||DC[V]||F>=(1-4delta)||V||F>=(1/2)||V||F.              (4.3)

All c_i are positive and at most delta. Thus 0<p_ij<=delta||w_ij||^2. Combining (3.1) and (4.3),

    F_pair=sum(p_ij')^2/p_ij
       >=Q(DC[V])/delta >=||V||F^2/(88delta)
       =||V||F^2/(176e).                                   (4.4)

This bound proves precisely why making all pair events rare cannot simultaneously make their total Fisher penalty weak in this cone.

## 5. Bounding all logarithmic acceleration

The L formula in section 1 gives, for s=|S|<=3,

    g_S=det B det(U_S(B^{-1}-eI)U_S^T).

For e<=1/16 and I<=B<=2I, 1/4 I<=B^{-1}-eI<=I and 1<=det B<=8. Write gamma_S=det(U_SU_S^T), gamma_empty=1. Positive-definite order, conjugated by (U_SU_S^T)^(-1/2), gives

    4^{-s} gamma_S <= g_S <=8 gamma_S<=8.                   (5.1)

All gamma_S are positive, and gamma_S<=1 since UU^T is an orthogonal projection. Direct rational evaluation yields

    min_{s<=3} 4^{-s} gamma_S =441/1092025 > 2^{-14}.

Therefore |log g_S|<10. To justify this bound without floating-point logarithms, Euler's number exceeds 8/3 by its positive exponential series, and (8/3)^10>2^14 by integer arithmetic; hence exp(10)>2^14>8.

We now bound every p_S'' absolutely. For T of cardinality k<=3, multilinearity of det(K_T+t D_T), with D=UVU^T, gives k(k-1) terms in the second derivative. Each term has two columns of D_T and k-2 columns of K_T. Their norms are bounded by ||V||F, ||V||F, and 1, respectively, because K is a contraction and ||D_T||op<=||V||op<=||V||F. Hadamard's inequality bounds each determinant by ||V||F^2. Larger minors vanish identically along the fixed face. Inclusion-exclusion thus gives

    |p_S''| <= b_s ||V||F^2,
    b_0=80, b_1=44, b_2=20, b_3=6.

For example b_s=sum_{k=max(s,2)}^3 binom(5-s,k-s)k(k-1). Summing over all supported S gives 80+5*44+10*20+10*6=560. Using (2.3),

    |sum p_S''log p_S|<=5600||V||F^2.                       (5.2)

This includes all low, top, and empty events. It is deliberately conservative but uniform over the stated cone and every V.

## 6. Explicit compensation cone

From (2.2), nonnegativity of all omitted Fisher summands, (4.4), and (5.2),

    H'' <=[-1/(176e)+5600]||V||F^2.

When 0<e<=1/1971200, one has 5600<=1/(352e), and e<=1/16. Therefore

    H'' <=-||V||F^2/(352e).

This proves frozen statement 1 for every symmetric V, including V depending on e and B. It is not asserted to be an optimal radius. No positive boundary chord is available, so an interior counterexample lift is not triggered.

## 7. Global injectivity of the empty-and-pair derivative map

Fix arbitrary 0<A<I and d=det A. Let s=tr(A^{-1}V). Differentiating C=d(A^{-1}-I) gives

    DC[V]=d[s(A^{-1}-I)-A^{-1}VA^{-1}].                    (7.1)

If every pair derivative vanishes, (3.1) applied to DC[V] forces DC[V]=0. Multiplying (7.1) on the left and right by A yields

    V=s A(I-A).

Taking tr(A^{-1}V) gives s=s(3-tr A). Thus either s=0 and V=0, or tr A=2. Conversely, when tr A=2, any V=s A(I-A) has tr(A^{-1}V)=s and satisfies DC[V]=0. Finally,

    p_empty'=-det(I-A)tr((I-A)^{-1}V)
             =-s det(I-A)tr A =-2s det(I-A).

It is nonzero for s nonzero. This proves statement 2. In particular no exactly Fisher-null direction for all low events exists anywhere in the strict face. This is an injectivity theorem, not a quantitative comparison with the full log acceleration.

## 8. The exceptional pair-null direction still has negative pair curvature

Assume tr A=2 and V=s A(I-A), s nonzero. These commute, so choose one orthonormal eigenbasis. Write mu_i=1-lambda_i, with lambda_i in (0,1) and sum mu_i=1. Along the genuinely affine path lambda_i(t)=lambda_i+t s lambda_i mu_i, each eigenvalue of C(A+tV) is

    c_i(t)=(1-lambda_i(t))lambda_j(t)lambda_k(t).

Its three relative first derivatives at zero are -s lambda_i, s mu_j, s mu_k, whose sum is s(2-tr A)=0. Each factor is affine, so the product second derivative equals the product times the square of the sum of the relative derivatives minus their squared sum. Thus

    c_i'=0,
    c_i''=-s^2 c_i(lambda_i^2+mu_j^2+mu_k^2)<0.              (8.1)

For w expressed in this fixed eigenbasis, p_ij(t)=sum_i w_i^2 c_i(t). Since w is nonzero, (8.1) proves p_ij''<0. Also 0<p_ij<1 because all 26 supported probabilities are positive. Therefore -p_ij''log p_ij<0. Its Fisher term is zero but its full curvature contribution is strictly negative. This proves statement 3 and identifies the exact failure of the proposed pair-score cancellation mechanism. Other cardinality layers can have either sign; no sign for their total is inferred here.
