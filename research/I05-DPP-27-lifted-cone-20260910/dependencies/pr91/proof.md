# Fixed two-harmonic DPP: a contractive correction-state operator and its second response

Status: PROVED (AUTHOR PROOF); PENDING_REVIEW. This manuscript does not assert a curvature sign. It starts from main 65e59a46b49cd2dbb5c779a4cfae8cef26441984, continues issues 65/74 and PR79, and does not change PR77/79. No unreviewed author theorem or numerical output is a premise. Natural logarithms throughout.

## 1. Frozen physical object and complete events

For every t in I=[1/2,3/2], fix

    f_t(theta)=1/2+cos(4*pi*theta)/4+t*cos(2*pi*theta)/8.

Writing x=cos(2*pi*theta) gives f_t=1/4+x^2/2+t*x/8. Thus 119/512<=f_t<=15/16 on I. Its correlation kernel is genuinely affine: diagonal 1/2, first off-diagonal q=t/16, second off-diagonal b=1/8, all others zero. No observation coordinates are rotated.

For a finite occupied set S in N, with absent set Z=N\S, multilinearity in the diagonal gives

    p(S)=(-1)^|Z| det(K_N-I_Z)
        =sum_{T superset S}(-1)^(|T|-|S|)det K_T.

The empty determinant is one. This is a complete-event identity, not an inclusion-probability substitution.

Group successive original coordinates into ordered two-site cells. For alpha=(a,beta) in {-1,+1}^2 define

    D_alpha=[[a/2,q],[q,beta/2]],
    E=[[1/8,0],[q,1/8]].

The upper off-diagonal cell block of the signed event matrix is E. Eliminate cells from the far end. If S is the leading Schur block of the already observed future, the correction to the next cell is Q=E S^{-1}E^T. In Q coordinates define

    M_alpha(Q)=D_alpha-Q,
    g_alpha(Q)=a*beta*det M_alpha(Q),
    T_alpha(Q)=E M_alpha(Q)^{-1} E^T.                 (1)

The no-future seed is Q=0. At every finite future word, the block determinant identity proves

    g_alpha(Q(word))=P(cell_0=alpha, future word)/P(future word).

Iterating T from the farthest cell towards the nearest, with these four weights, reconstructs EVERY complete finite event. The original S-map is equivalent; Q is a conditional sufficient statistic, not a spectral basis change or an L-kernel parameterization.

## 2. An analytic invariant domain; no box computation is needed

Use the fixed convex compact set

    B={Q real symmetric 2x2: ||Q||_2<=1/8}.

Frobenius norm is the metric on B. Spectral norm is used only for matrix estimates. Its Frobenius diameter is at most D=3/8.

For q<=3/32, entrywise domination by the nonnegative endpoint E_max implies ||E||_2^2<=17/512. This bound is verified without an eigenvalue approximation: the matrix (17/512)I-E_max E_max^T has diagonal entries 9/512,9/1024 and determinant 9/524288>0. Also ||E||_2<=3/16.

Every D_alpha has smallest singular value at least 13/32. Hence for every Q in B,

    sigma_min(M_alpha)>=9/32,   ||M_alpha^{-1}||_2<=r=32/9.

Along the segment from 0 to Q no determinant vanishes. Its sign is therefore the sign at D_alpha, namely a*beta. It follows that

    g_alpha(Q)>=epsilon=81/1024.                    (2)

Write Q=[[x,z],[z,y]]. The four weights are exactly

    g_(a,beta)=1/4-beta*x/2-a*y/2
               +a*beta*(x*y-(q-z)^2).

Their sum is identically one for ANY symmetric Q. Positivity and probability semantics require a domain, whereas normalization does not. Outside it positivity can fail: at t=1,Q=I, g_(+,-)=-191/256 despite the sum being one.

Finally,

    ||T_alpha(Q)||_2<= (17/512)*(32/9)=17/144<1/8.    (3)

Thus all four branches define a positive normalized Markov operator on the entire convex B, not merely on unspecified reachable states.

For Q,P in B, the inverse identity gives

    T_alpha(Q)-T_alpha(P)
      =E M_alpha(Q)^{-1}(Q-P)M_alpha(P)^{-1}E^T.

Consequently

    ||T_alpha(Q)-T_alpha(P)||_F<=k||Q-P||_F,
    k=34/81<1.                                     (4)

This proof replaces dependence on the previous comment-only 4096-box assertion. It does not assert that an unarchived computation was independently reproduced.

## 3. The entire probability kernel contracts, including changing weights

Let L A(Q)=sum_alpha g_alpha(Q) A(T_alpha(Q)). Branch contraction alone would NOT bound L because the branch probabilities change with Q.

For a Frobenius-unit symmetric direction U=[[u,w],[w,v]], put

    c=y*u+x*v+2(q-z)*w.

The four-sign identity gives exactly

    (1/2)sum_alpha |Dg_alpha[U]|
     =max(|u|,|v|,2|c|,(|u|+|v|)/2+|c|).

On B, |x|,|y|<=1/8 and |q-z|<=7/32. Cauchy-Schwarz in the Frobenius metric gives |c|<=sqrt(130)/32<3/8, while (|u|+|v|)/2<=3/4. Hence

    TV(g(Q),g(P))<=9/8 ||Q-P||_F.                   (5)

Maximally couple the four labels. Matching labels cost at most k||Q-P||_F; mismatches cost at most D. Therefore the 1-Wasserstein distance obeys

    W1(delta_Q L,delta_P L)<=beta||Q-P||_F,
    beta=k+D*(9/8)=4363/5184<1.                     (6)

Integrating couplings proves this for arbitrary probability measures. Completeness of probability measures on compact B in W1 and the contraction argument give a unique invariant probability eta_t, with

    W1(mu L^m,eta_t)<=beta^m W1(mu,eta_t).

This is a quantitative law-level contraction, not an assumed finite HMM theorem.

The genuinely infinite reachable set is

    A_t=intersection_{m>=0} union_{|w|=m} T_w(B).

Contraction identifies it with the limits T_(alpha_1)...T_(alpha_m)(0) for all infinite words, and A_t=union_alpha T_alpha(A_t). A closure of all finite seed states can also contain transient states; it must not be identified with this attractor without qualification. Positivity (2) implies supp eta_t=A_t.

## 4. Exact true entropy-rate normalization

Let B_t(Q)=-sum_alpha g_alpha(Q) log g_alpha(Q). Here B_t is an observable, not the domain B. The finite law mu_m=delta_0 L_t^m is exactly the law of the correction state for m future cells, by Section 1. Consequently

    mu_m(B_t)=H(Y_0 | Y_1,...,Y_m),
    Y_j=(X_(2j),X_(2j+1)).

Stationary conditional entropy convergence and Section 3 yield

    h(f_t)=(1/2) eta_t(B_t).                         (7)

The factor 1/2 is per ORIGINAL coordinate. This derivation does not differentiate H_n/n or substitute a quantum entropy.

## 5. Parameter jets on every finite and infinite coding trajectory

All dots in this section are total t derivatives along a fixed observed word. Put C=E'=[[0,0],[1/16,0]], V=D_alpha'=[[0,1/16],[1/16,0]], R=M_alpha^{-1}, J=Q', H=Q'', and A=V-J. Direct differentiation gives

    J_new=C R E^T+E R C^T-E R A R E^T,

    H_new=E R H R E^T+2 C R C^T
          -2 C R A R E^T-2 E R A R C^T
          +2 E R A R A R E^T.                       (8)

With c=1/16, e=3/16, e2=17/512 and r=32/9, the source bound for J_new is 71/648. Thus

    (1-k)/5-71/648=7/1080>0.

When ||J||_2<=1/5, the non-H source bound for H_new is 3151/8100 and

    (1-k)*(3/4)-3151/8100=187/4050>0.

Starting from the zero seed, induction proves, uniformly in parameter, word and depth,

    ||Q'||_2<=1/5,     ||Q''||_2<=3/4.               (9)

Uniform convergence of the jets, not merely their boundedness, is established by the explicit forgetting estimates in the continuation supplement. Alternatively it follows from the derivative recurrences and the uniform contraction with bounded higher derivatives on this strict compact domain. All needed inverses remain uniformly nonsingular.

## 6. Quantitative smooth resolvent

For a C2 observable A on B use seminorms

    |A|_1=sup ||DA||,   |A|_2=sup ||D2 A||,

where derivatives are multilinear operator norms in Frobenius coordinates. Define the centered resolvent

    Rcal A=sum_(n>=0) L^n(A-eta A).

Do not confuse Rcal with the 2x2 inverse R in Section 5. Constants are annihilated by all operator derivatives.

Besides (6), direct twice differentiation in Q gives

    |L A|_1<=beta |A|_1,
    |L A|_2<=k^2 |A|_2+b2 |A|_1,
    b2=16399/2916.                                  (10)

Here sum|Dg[U]|<=9/4, sum|D2g[U,W]|<=4 for unit directions, and ||D2 T||<=2kr. In the term sum D2g*A(T), subtract the midpoint of the four observable values, since sum D2g=0. Its bound is 2D|A|_1. Thus b2=2D+(9/2)k+2kr, proving (10) without a spectral-gap citation.

Let

    R1=1/(1-beta)=5184/821,
    R2(a,b)=(b+b2*R1*a)/(1-k^2).

Summing the resulting triangular recurrences proves convergence in C2 and

    |Rcal A|_1<=R1 |A|_1,
    |Rcal A|_2<=R2(|A|_1,|A|_2),
    ||Rcal A||_infinity<=D R1 |A|_1.                (11)

Partial t derivatives below keep Q fixed. With a0=1/6 and b0=1/8, elementary matrix bounds give

    ||T_t||_F<=a0,  ||T_tt||_F<=b0,
    ||D_Q T_t||<=1/2.

The bounds before rounding up are (3/2)*(71/648), (3/2)*(223/2916), and 352/729. For the weights,

    sum|g_t|<=7/64, sum|g_tt|<=1/32,
    sum|D_Q g_t[U]|<=3/8  (||U||_F=1).

Using normalization to center the value terms yields

    ||L' A||_infinity<=Ct |A|_1, Ct=575/3072,
    ||L'' A||_infinity<=Ctt |A|_1+(1/36)|A|_2,
    Ctt=257/1536,
    |L' A|_1<=|A|_1+(k/6)|A|_2.                    (12)

The unrounded coefficient of |A|_1 in the last inequality is 10277/10368<1. Formulas used are

    L'A=sum[g_t A(T)+g DA(T)T_t],
    L''A=sum[g_tt A(T)+2g_t DA(T)T_t
             +g D2A(T)[T_t,T_t]+g DA(T)T_tt].        (13)

Thus state movement is retained in both derivatives.

## 7. Invariant-measure response and the true second derivative

For any smooth fixed observable A, differentiate the stationary identity via the exact perturbation identity

    (eta_s-eta_t)A=eta_s(L_s-L_t)Rcal_t A.

The C1/C2 estimates (11)-(12) control the first and second difference quotients. Expanding once more gives

    eta'_t A=eta_t L'_t Rcal_t A,
    eta''_t A=eta_t L''_t Rcal_t A
              +2 eta_t L'_t Rcal_t L'_t Rcal_t A.   (14)

For clarity, applying the perturbation identity again to (L_s-L_t)Rcal_t A gives the second-order remainder eta_s(L_s-L_t)Rcal_t[(L_s-L_t)Rcal_t A]. Its divided limit is the second term in (14). Operator Taylor expansions hold in C0/C1 as needed, and the uniform bounds imply continuity. One can first take C3 observables and pass by C2 approximation; the entropy observable here is smooth on a strict neighborhood by (2). Endpoint derivatives extend from a neighborhood because all required strict inequalities have slack.

Set

    u=Rcal B_t,
    v=Rcal(B_t' + L' u).

Here B_t',B_t'' mean partial t derivatives at fixed Q, and the displayed u,v are centered Poisson solutions, not assumptions on eta'. Equations (7) and (14) give the exact true-rate identity

    h''(t)=(1/2) eta_t[ B_t'' + L_t'' u + 2 L_t' v ]. (15)

All invariant-law response terms are present. At fixed Q,

    B_t''=-sum (g_t)^2/g - sum g_tt log g.

This fixed-Q Fisher piece alone is NOT the full coding Fisher rate, because the conditional state moves. Formula (13) retains that movement. The continuation supplement identifies the complete conditional Fisher using the total jets (8), and the code checks complete-event values and both genuine t derivatives against an independent inclusion-minor/Mobius construction.

## Scope

Equations (1)-(15) are author proofs for exactly the fixed symbol and I. They establish a positive compressed rate operator, its true invariant law, uniform state derivatives and full second response, but do not sign (15). The complete interval h''<0 remains INCOMPLETE. No finite-HMM representation or novelty claim is made. The forthcoming residual certificate converts approximate Poisson solutions into an explicit true-curvature error without assuming that a finite discretization equals the DPP.
