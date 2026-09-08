# Mixed blow-up theorem, including feasible singular Schur limits

Author status: PROVED for the results stated below, pending independent verification. The global real-kernel question and the final zero-coefficient branch remain INCOMPLETE. No positive gap is claimed.

Fix orthonormal frames `U in R^(n x r)` and `V in R^(n x s)` with
`W=[U,V]` orthogonal. Let `A,X` be symmetric `r x r` matrices, `C,Y`
symmetric `s x s` matrices, and `B` a real `r x s` matrix. Put, for
`sigma in {+1,-1}`,

    H_sigma=A-sigma X,       L_sigma=C+sigma Y,
    R_Hsigma=H_sigma-BB^T,  R_Lsigma=L_sigma-B^TB,
    F=||B||_F^2.

The endpoint and center are

    K_(e,sigma)=W[[I-eH_sigma,sigma sqrt(e)B],
                    [sigma sqrt(e)B^T,eL_sigma]]W^T,
    M_e=W diag(I-eA,eC) W^T.

## Theorem A: exact small-parameter feasibility

For fixed sigma and every sufficiently small positive e so that I-eH_sigma and I-eL_sigma are positive definite, K_(e,sigma) is a positive contraction if and only if

    S_Lsigma(e)=L_sigma-B^T(I-eH_sigma)^(-1)B >=0,
    S_Hsigma(e)=H_sigma-B(I-eL_sigma)^(-1)B^T >=0.       (1)

Replacing both inequalities by strict inequalities is equivalent to a strict contraction. In particular, strict contractions exist for all sufficiently small e if and only if both R_Hsigma and R_Lsigma are positive definite.

Allowing singular endpoints, contractions exist for all sufficiently small positive e if and only if

    R_Hsigma>=0, R_Lsigma>=0,
    ker R_Hsigma subset ker B^T,
    ker R_Lsigma subset ker B.                          (2)

The conditions must hold for both sigma to obtain a feasible chord. They imply A,C>=0, so the center is also a contraction for small e. No strictness assumption on the R blocks is hidden in (2).

### Proof

Schur complements of K and I-K give (1), since

    W^T K W=[[I-eH,sigma sqrt(e)B],[sigma sqrt(e)B^T,eL]].

The signs square out. If K is a contraction, its principal blocks imply H,L>=0. With e small, inverse monotonicity yields S_H(e)<=R_H and S_L(e)<=R_L. Thus the two R blocks must be positive semidefinite; a strict S implies a strict R.

For v in ker R_H, write

    v^T S_H(e)v
      =-e (B^Tv)^T L(I-eL)^(-1)(B^Tv).                 (3)

The matrix L(I-eL)^(-1) is positive semidefinite, so S_H(e)>=0 forces L^(1/2)B^Tv=0. Since R_L>=0 implies L>=B^TB, this gives

    0=(B^Tv)^T L(B^Tv)>=||BB^Tv||^2.

Therefore BB^Tv=0 and then ||B^Tv||^2=v^TBB^Tv=0. This is the first kernel condition in (2). Interchanging H,L and B,B^T proves the second. In fact, if either kernel condition fails while the R blocks are nonnegative, (3) is strictly negative for a corresponding vector at every e for which the inverse is positive. There is no smaller-e rescue of that frozen family.

Conversely assume (2). The correction

    R_H-S_H(e)=e B L(I-eL)^(-1)B^T

annihilates ker R_H, because B^T does. On the orthogonal complement of that kernel, R_H is positive definite with a fixed smallest eigenvalue mu_H>0, unless the complement is empty. The correction has norm tending to zero as e tends to zero, so S_H(e) is nonnegative, positive definite on that complement, for all sufficiently small e. If the complement is empty then R_H=0 and the kernel condition gives B=0, so the correction is zero exactly. The same argument applies to S_L. This proves sufficiency and the strict statement.

An explicit sufficient small-e bound on a nonempty support is obtained from

    ||R_H-S_H(e)|| <= e ||B||_op^2 ||L||_op/(1-e||L||_op),

and its H/L counterpart: require the denominators positive and these bounds smaller than the respective positive support eigenvalues mu_H,mu_L. Terms with zero numerator impose no restriction. This also provides a checkable feasible interval without assuming uniformity in the data.

Finally H_++H_-=2A and L_++L_-=2C, so (2) implies A,C>=0. The average of two contractions is also a contraction. This proves Theorem A.

## Theorem B: entropy coefficient with longitudinal directions

Assume the conditions (2) for both signs. Define

    psi_S=det(U_S),
    phi_S=(d/da) det((U+aVB^T)_S)|_(a=0),
    Z=sum_(|S|=r,psi_S=0) phi_S^2.

Then 0<=Z<=F and

    Delta_e=(Z-2F)e log(1/e)+O(e).                       (4)

If B!=0, Delta_e<0 for all sufficiently small positive e. The coefficient is independent of X and Y, including every singular limit actually feasible in the fixed family.

### Full-law preparation

The generating polynomial of the exact-event law is

    det(I+K(diag(z)-I))
       =sum_T det(K_T) product_(i in T)(z_i-1).

Its coefficient at z_S is precisely the required inclusion-exclusion sum. If K=T diag(lambda)T^T with T orthogonal and 0<=lambda_i<=1, row expansion followed by Cauchy-Binet gives the exact spectral mixture

    p_K(S)=sum_(J:|J|=|S|)
        [product_(j in J)lambda_j product_(j notin J)(1-lambda_j)]
        det(T_(S,J))^2.                                 (5)

Each conditional squared-minor law has the indicated fixed cardinality and sums to one. Formula (5) proves positivity and all flip-count estimates below. Principal minors alone are not used as event probabilities.

In exterior-power coordinates, omega=u_1 wedge ... wedge u_r has coordinates psi_S. Its derivative eta obtained by replacing u_i by sum_j B_ij v_j has coordinates phi_S. These r(n-r) replacement exterior vectors are mutually orthonormal up to signs, so ||eta||^2=F. Summing only over the original zero coordinates gives 0<=Z<=F.

### Endpoint traces, rotations and zero modes

Put x=sqrt(e), J=VB^TU^T-UBV^T and, for each fixed sigma, O_sigma(x)=exp(sigma xJ). Define the analytic path

    K_sigma(x)=P+sigma x(UBV^T+VB^TU^T)
                     +x^2 W diag(-H_sigma,L_sigma)W^T.

For positive x this is the actual sigma endpoint. For negative x it reverses only that endpoint's off-diagonal block, not its longitudinal block. Those negative-x matrices are also contractions: conjugation by W diag(I,-I)W^T flips the off-diagonal block without changing the diagonal blocks. This ensures two-sided nonnegativity event by event. It must not be confused with identifying K_+(negative x) with K_-(positive x), which is generally false when X or Y is nonzero.

The rotation expansion is

    O_sigma(x)P O_sigma(x)^T
       =P+sigma x(UBV^T+VB^TU^T)
          +x^2 W diag(-BB^T,B^TB)W^T+O(|x|^3).

The comparison contraction

    K_tilde_sigma(x)=O_sigma(x)
        [P+x^2 W diag(-R_Hsigma,R_Lsigma)W^T]
        O_sigma(x)^T

therefore agrees with K_sigma(x) through degree two. Its high-mode hole rates are the nonnegative eigenvalues of R_Hsigma, and its low-mode particle rates are those of R_Lsigma. Zero rates are allowed. The actual high eigenvalue deficits and low eigenvalues have corresponding summed first coefficients

    high-hole trace: e[tr A-sigma tr X-F]+O(e^(3/2)),
    low-particle trace: e[tr C+sigma tr Y-F]+O(e^(3/2)). (6)

For example these trace statements follow from the comparison kernel and the eigenvalue perturbation bound for real symmetric matrices; one can also obtain them from its two separated spectral groups by taking traces. Only their first coefficients are used below.

The full law (5) says that the no-flip weight is 1-e T_sigma+O(e^2), one-flip weights are e times their rates plus O(e^2), and all multiple-flip weights are O(e^2), where

    T_sigma=tr R_Hsigma+tr R_Lsigma
       =tr A+tr C+sigma(-tr X+tr Y)-2F.                 (7)

Because exact probabilities are polynomials in entries, comparison errors are O(|x|^3) for every event. The following four disjoint classes exhaust all events.

1. For |S|=r and psi_S!=0,

       p_(K_sigma(x))(S)=psi_S^2+sigma a_S x+O(x^2).

   The coefficient a_S arises solely from the common transverse rotation; longitudinal blocks first appear at degree two. Thus the average of the two actual positive-x endpoint entropies cancels its linear term and differs from the center contribution by O(x^2).

2. For |S|=r and psi_S=0, the rotated exterior vector omega+sigma x eta+O(x^2) and the flip counts yield

       p_(K_sigma(x))(S)=phi_S^2 x^2+O(|x|^3).

   At the center such an event requires a deletion and an addition, and has probability O(x^4). No one-flip longitudinal contribution has cardinality r.

3. For |S|=r-1 or r+1, the endpoint probabilities are c_(sigma,S)x^2+O(|x|^3), where c_(sigma,S)>=0 and their sum is T_sigma. The center has coefficients c_(0,S)>=0 whose sum is T_0=tr A+tr C.

4. For all other cardinalities, the comparison probabilities are O(x^4), giving initially O(|x|^3) for the actual probabilities. These are analytic and nonnegative for both signs of x by the above conjugation argument. Their first three coefficients vanish, and a nonzero cubic leading coefficient would change sign. Hence they are actually O(x^4). A zero coefficient in class 2 or 3 is handled by the same argument.

For a positive coefficient c, -[cx^2+O(|x|^3)] log[cx^2+O(|x|^3)] equals cx^2 log(1/x^2)+O(x^2). For a zero coefficient the just-established O(x^4) probability gives O(x^4|log|x||)=o(x^2). There are finitely many events, so all remainders sum to O(x^2).

Class 2 contributes Z e log(1/e). Class 3 contributes

    [(T_++T_-)/2-T_0]e log(1/e)=-2F e log(1/e).

The other classes contribute O(e). This proves (4), including singular feasible rates. Its coefficient is at most -F, strictly negative when B!=0.

## Singular limits and genuinely uncovered next scales

Theorem A prevents a false boundary inference: R_H,R_L>=0 alone is not sufficient. In the scalar example H=L=B=1, both residuals vanish but

    det [[1-e,sqrt(e)],[sqrt(e),e]]=-e^2<0,

and S_H(e)=S_L(e)=-e/(1-e)<0. Both signs of the off-diagonal block fail for every e in (0,1). There is no second-order feasible escape in the stated fixed family.

Compatible singular residuals behave differently. For example r=n-r=2, B=diag(b,0), H_sigma=diag(h_sigma,0), L_sigma=diag(l_sigma,0), with h_sigma>b^2 and l_sigma>b^2, satisfy (2). The uncoupled null directions give exact eigenvalues 1 and 0; the remaining two-dimensional block is feasible for small e. Theorem B includes this case without strict endpoint assumptions.

A higher-order repair changes the frozen object and must be named. In the scalar failed example, replacing sqrt(e) by sqrt(e(1-e))=sqrt(e)-(1/2)e^(3/2)+O(e^(5/2)) makes both endpoints rank-one projections. More generally the Schur expansion starts

    S_H(e)=R_H-e B L B^T+O(e^2),
    S_L(e)=R_L-e B^T H B+O(e^2).                         (8)

On residual kernels, an added e^2 diagonal slack or an e^(3/2) transverse correction can compete with the negative terms in (8). Such corrections can repair feasibility. For analytic feasible extensions that keep exactly the same constant, x, and x^2 Taylor coefficients, however, the event-scale proof of Theorem B is unchanged: the leading entropy coefficient remains Z-2F, still negative when B!=0. Feasibility repair by those higher terms is therefore not a positive-leading-coefficient escape.

## The zero-transverse branch B=0

When B=0, coefficient (4) vanishes and it is incorrect to infer Delta=0 or a sign from that formula. There is a further rigorous first-order exclusion. Let c_(sigma,S) be the one-flip exact-event rate vector on cardinalities r-1 and r+1 for H_sigma,L_sigma, and c_(0,S) the rate vector for A,C. The first derivative of the generating polynomial at P is linear in the perturbation, hence

    c_(0,S)=(c_(+,S)+c_(-,S))/2.

Expanding the full law, supported r-events have a first-order contribution linear in tr H_sigma+tr L_sigma, which cancels in the chord average. All other zero events outside the one-flip classes are O(e^2). Thus, writing f(z)=-z log z with f(0)=0,

    Delta_e=e J+O(e^2 log(1/e)),
    J=sum_S [(f(c_(+,S))+f(c_(-,S)))/2-f(c_(0,S))]<=0.  (9)

Strict concavity of f on the nonnegative half-line gives J<0 unless the two complete rate vectors coincide coordinate by coordinate. Formula (9) requires no strictly positive rates. It strictly excludes every B=0 family with unequal visible one-flip rates for small e.

If B=0 and all these rate vectors coincide, both the e log(1/e) and e coefficients vanish. The remaining e^2 log(1/e) and e^2 terms are not signed by this proof. This is the precise remaining branch; it is not covered by either strict-residual or singular-residual first-order arguments. Likewise data varying with e may invalidate the fixed-parameter remainder and require their own frozen hierarchy.

This finishes the analytic working unit. The expanded theorem is a candidate for independent review because it covers longitudinal directions and all feasible singular residuals of the fixed blow-up family. No novelty or global-concavity claim is made.

