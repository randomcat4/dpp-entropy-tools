# Proof corresponding exactly to the public frozen theorem v1

Author status: PROVED, pending fresh-context verification. This proves only the four claims in `dpp-entropy-tools/research/R2/frozen_theorem_v1.md`, read on 2026-09-08. In particular the chord length here is exactly

    t_epsilon=tau sqrt(epsilon(1-epsilon)).

All parameters n,r,P,U,V,B,tau are fixed as in that statement. Write m=n-r, W=[U V], Q=I-P, F=||B||_F^2. All constants in asymptotic notation may depend on these fixed finite data. Natural logarithms are used.

## 1. Exact feasibility, including the zero direction

Conjugation by W gives

    W^T(M_epsilon+tD)W
      = [[(1-epsilon)I_r, tB], [tB^T, epsilon I_m]].

Since epsilon and 1-epsilon are positive, its Schur complement condition for positive semidefiniteness is

    epsilon I_m - t^2 B^TB/(1-epsilon) >=0,

which is equivalent to t^2||B||_op^2 <=epsilon(1-epsilon). The complementary matrix I-M_epsilon-tD has diagonal blocks epsilon I_r and (1-epsilon)I_m. Its Schur condition is the same inequality. This proves the exact interval, including equality, for a positive contraction. If B=0, the scalar inequality is always true and every real t gives the same strict contraction M_epsilon.

For the specified endpoints, the inequality is strict because

    t_epsilon^2 ||B||_op^2
       =tau^2||B||_op^2 epsilon(1-epsilon)
       <epsilon(1-epsilon).

Thus both K_epsilon,+ and K_epsilon,-, and their complements, are positive definite for every 0<epsilon<1/2. This proves claim 1 without a small-epsilon restriction. If tau B=0, the two endpoints equal the center, and Delta_epsilon=0 identically. The arguments below still allow this case.

## 2. Full exact-event law and its spectral mixture

The inclusion-exclusion definition in the frozen theorem is equivalent to saying that p_K(S) is the coefficient of z_S=product_(i in S) z_i in

    G_K(z)=det(I+K(diag(z)-I))=det(I-K+K diag(z)).       (1)

Indeed expanding a determinant of I+K diag(z-1) by its principal minors gives sum_A det(K_A) product_(i in A)(z_i-1); collecting z_S gives exactly the specified alternating superset sum. In particular every p_K(S) is a polynomial in matrix entries.

We record a spectral mixture directly from (1). Let K=R diag(lambda_1,...,lambda_n)R^T with R real orthogonal and 0<=lambda_i<=1. Conjugation and expansion by rows give

    G_K(z)=sum_{J subset E} w_J det((R^T diag(z)R)_J),
    w_J=product_(j in J) lambda_j product_(j notin J)(1-lambda_j).

The row expansion uses the diagonal entries of I-diag(lambda) on rows outside J; the surviving minor on J has no additional sign. Cauchy-Binet gives

    det((R^T diag(z)R)_J)
       =sum_{|S|=|J|} det(R_(S,J))^2 z_S.

Therefore the full law is

    p_K(S)=sum_{J: |J|=|S|} w_J det(R_(S,J))^2.          (2)

The weights w_J are nonnegative and sum to 1. For a fixed J the squared minors sum to 1 by Cauchy-Binet and orthonormality of R's columns. Formula (2) both verifies nonnegativity of all exact probabilities and justifies every eigenmode deletion/addition statement below. It is not a substitution of inclusion determinants for exact-event probabilities.

For K=P, only J consisting of all r columns in ran P survives. Hence p_P(S)=psi_S^2 for |S|=r and zero for all other cardinalities.

## 3. The zero-coordinate exterior coefficient

Let u_i and v_j be the columns of U and V. Define in the r-th exterior power

    omega=u_1 wedge ... wedge u_r,
    eta=sum_(i=1..r,j=1..m) B_ij
        u_1 wedge ... wedge v_j (in position i) wedge ... wedge u_r.

The r*m exterior basis vectors in this sum are mutually orthonormal up to their ordering signs: each uses a different subset of the fixed orthonormal basis [U V]. Consequently ||eta||^2=F. The coordinate of omega at an r-set S is psi_S. Multilinearity of the determinant shows that the coordinate of eta is exactly

    phi_S=(d/da) det((U+a V B^T)_S)|_(a=0),

with precisely the sign convention of the frozen statement. Summing eta's squared coordinates only over the zero psi coordinates gives

    0<=Z=sum_(|S|=r, psi_S=0) phi_S^2<=||eta||^2=F.     (3)

This proves claim 2.

## 4. A signed analytic parameter for both endpoints

Use the real signed parameter x, with |x|<1/sqrt(2), and define

    K(x)=P+x^2(-P+Q)+tau x sqrt(1-x^2) D,
    M(x)=P+x^2(-P+Q).

For x>0, K(x)=K_(x^2,+) and K(-x)=K_(x^2,-). By section 1 both are strict contractions for all nonzero x in this interval. The square root is its positive analytic branch at zero, so K(x) and each p_(K(x))(S) are real analytic in a two-sided neighborhood of zero. The probabilities are polynomial in matrix entries, but they need not be polynomial in x; analyticity is the property used here.

The new chord length gives the explicit Taylor expansion

    tau x sqrt(1-x^2)=tau x-(tau/2)x^3+O(x^5),
    K(x)=P+tau xD+x^2(-P+Q)-(tau/2)x^3D+O(x^5).        (4)

The difference from the old parametrization begins in degree three. We do not compare entropies by a generic matrix continuity bound; instead we derive the needed probability and entropy expansions for (4) itself.

Define the physical-coordinate skew-symmetric operator

    J=V B^T U^T-U B V^T,
    J U=V B^T,
    O(x)=exp(tau xJ),
    P_rot(x)=O(x)P O(x)^T.

Direct block multiplication yields

    [J,P]=D,
    (1/2)[J,[J,P]]=W diag(-BB^T,B^TB)W^T.

Therefore

    P_rot(x)=P+tau xD
               +tau^2 x^2 W diag(-BB^T,B^TB)W^T+O(|x|^3).  (5)

Its continuously oriented exterior state is

    wedge_(i=1..r)(O(x)u_i)=omega+tau x eta+O(x^2).       (6)

Set

    L_H=I_r-tau^2 BB^T,  L_L=I_m-tau^2 B^TB,
    N=W diag(-L_H,L_L)W^T.

Both L blocks are positive definite under tau||B||_op<1. Introduce the comparison kernel

    K_tilde(x)=O(x)(P+x^2 N)O(x)^T.                      (7)

Equations (5)–(7) show

    K_tilde(x)=P+tau xD+x^2(-P+Q)+O(|x|^3),
    K(x)-K_tilde(x)=O(|x|^3).                           (8)

Thus the normal response blocks L_H,L_L are unchanged by the corrected chord length. Because exact-event probabilities are polynomials in entries and there are finitely many events, (8) implies, separately for every event and for both signs of x,

    p_(K(x))(S)=p_(K_tilde(x))(S)+O(|x|^3).              (9)

## 5. All event scales from the full law

Diagonalize L_H and L_L independently inside ran P and ran Q. If their eigenvalues are l_1,...,l_r and h_1,...,h_m, the eigenvalues of K_tilde(x) are

    1-x^2 l_i (high modes), and x^2 h_j (low modes),

with corresponding fixed orthonormal frames rotated by O(x). For small |x| they lie in [0,1], and (2) applies exactly. Let C=tr L_H+tr L_L=n-2tau^2 F.

The weight for retaining every high mode and no low mode is 1-Cx^2+O(x^4). Deleting just high mode i has weight x^2 l_i+O(x^4). Adding just low mode j has weight x^2 h_j+O(x^4). The combined weight of selections requiring at least two flips is O(x^4), since there are finitely many selections and every flip brings a factor x^2. Each conditional projection probability in (2) lies in [0,1]. These statements cover r=1 and r=n-1, with rank-zero and rank-n conditional laws understood in the usual empty/full sense.

Partition the events as follows.

(a) Supported r-events: if |S|=r and psi_S!=0, analyticity gives

    p_(K(x))(S)=psi_S^2+a_S x+b_S x^2+O(|x|^3),
    p_(M(x))(S)=psi_S^2+O(x^2).                          (10)

(b) Zero r-events: if |S|=r and psi_S=0, the no-flip projection contribution has probability tau^2 x^2 phi_S^2+O(|x|^3), by (6). Single flips have the wrong cardinality. Selections with at least two flips have total weight O(x^4). Combining this with (9),

    p_(K(x))(S)=tau^2 phi_S^2 x^2+O(|x|^3).             (11)

At the center its no-flip projection term is exactly zero, and one deletion and one addition are needed to change the selected rank-r subspace, so

    p_(M(x))(S)=O(x^4).                                 (12)

(c) Cardinalities r-1 and r+1: single flips give nonnegative coefficients c_S at x=0. Their rotated projection probabilities are analytic in x, so (9) gives

    p_(K(x))(S)=c_S x^2+O(|x|^3),
    c_S>=0,
    sum_(|S|=r-1 or r+1)c_S=C=n-2tau^2F.                (13)

The coefficient sum follows because each single-flip conditional law sums to one on its cardinality. At the center the same reasoning with every rate equal to 1 gives

    p_(M(x))(S)=d_S x^2+O(x^4),
    d_S>=0,
    sum_(|S|=r-1 or r+1)d_S=n.                          (14)

(d) All other cardinalities: at least two flips are needed in (7), hence p_(K_tilde(x))(S)=O(x^4). Equation (9) initially gives p_(K(x))(S)=O(|x|^3). This estimate is already enough for the entropy calculation, separately at each endpoint. There is also a sharper conclusion: p_(K(x))(S) is analytic and nonnegative for both positive and negative x, with its coefficients of degrees 0,1,2 equal to zero. If its cubic coefficient were nonzero, its sign would be negative for one sign of x sufficiently close to zero. Therefore that coefficient must vanish, and

    p_(K(x))(S)=O(x^4),  p_(M(x))(S)=O(x^4).             (15)

Exactly the same argument upgrades (11) or (13) to O(x^4) whenever its displayed quadratic coefficient is zero. This uses individual-event nonnegativity for both endpoints, not cancellation of potentially signed probabilities by averaging. Cubic coefficients in (10)–(13) are allowed when a positive lower-order coefficient is present.

## 6. Entropy remainder and the coefficient

Put f(p)=-p log p for p>0 and f(0)=0. For fixed c>0 and a nonnegative function satisfying p(x)=c x^2+O(|x|^3), the elementary expansion is

    f(p(x))=c x^2 log(1/x^2)-c x^2 log c
              +O(|x|^3 |log|x||).                       (16)

For 0<=p(x)=O(x^4), monotonicity of f on a sufficiently small interval [0,e^-1] gives

    0<=f(p(x))=O(x^4 |log|x||)=o(x^2).                 (17)

Even the weaker 0<=p(x)=O(|x|^3) would give O(|x|^3 |log|x||)=o(x^2). In particular no positivity of the leading quadratic coefficient is tacitly assumed at a zero mode. Formula (16) holds separately at x and -x with the same c; its remainder uses absolute values and does not require the cubic terms to cancel.

For (a), f is smooth near each fixed psi_S^2>0. The average of f(p_(K(x))(S)) and f(p_(K(-x))(S)) cancels the linear term and differs from f(p_(M(x))(S)) by O(x^2).

For (b), (11), (12), (16), and (17) give total contribution to the averaged-endpoint minus center entropy of

    tau^2 Z x^2 log(1/x^2)+O(x^2).

For (c), (13), (14), (16), and (17) give total contribution

    (C-n)x^2 log(1/x^2)+O(x^2)
       =-2tau^2F x^2 log(1/x^2)+O(x^2).

For (d), (15) and (17) give o(x^2), both endpoint by endpoint and at the center. All sums are finite, so the aggregate remainder is O(x^2). Substitution epsilon=x^2 proves

    Delta_epsilon=tau^2(Z-2F)epsilon log(1/epsilon)
                     +O(epsilon),                      (18)

exactly as claim 3 states, for the corrected t_epsilon.

Finally, if tau B!=0, then tau^2F>0 and (3) implies tau^2(Z-2F)<=-tau^2F<0. Since log(1/epsilon) tends to infinity, the displayed leading term dominates the O(epsilon) remainder and Delta_epsilon<0 for sufficiently small epsilon. The zero case was established identically in section 1. This proves claim 4.

No uniform threshold over varying P,B,tau or n is asserted. No global concavity result, numerical certificate, or independent verification is claimed by the proof author.
