# Unit 1 — uniform finite-law estimates and a transverse degeneration

Author status: **PROVED** for Lemmas 1–3 and Example 4 below, in the sense of a complete author proof awaiting independent review. The unrestricted A2 question remains **INCOMPLETE**. These are proposed auxiliary statements; they do not amend the main frozen scope. No novelty claim is made. No numerical search, external computation, or formal verification was used.

## 0. Scope and conventions

There are finitely many events, indexed by all subsets of a fixed ground set of size n. For a positive contraction K, use exactly

    p_K(S)=sum_{T superset S} (-1)^(|T|-|S|) det K_T,
    H(K)=sum_S h(p_K(S)),  h(z)=-z log z, h(0)=0.

All three laws below belong to two endpoints and their actual arithmetic midpoint. The midpoint law is calculated from the midpoint matrix; it is never replaced by the average endpoint law. Write weights w_-=w_+=1/2, w_0=-1, so Delta=sum_{j,S} w_j h(p_j(S)). All logarithms are natural.

The statements address two different uniformity requirements: uniform approximation of probabilities/entropy, and a negative coefficient large enough to dominate the uniform error. Neither requirement follows from a pointwise big-O statement.

## 1. A zero-safe finite-law truncation lemma

**Lemma 1.** Suppose p_j(S;t,z) are genuine probabilities, with j in {-,0,+}, 0<t<t0 and arbitrary auxiliary datum z in a stated domain. Let q_j(S;t,z) be any real approximants satisfying

    |p_j(S;t,z)-q_j(S;t,z)| <= R(t),   0<R(t)<=1,

uniformly in every index and datum. Set qbar=min(1,max(0,q)) and

    Dhat(t,z)=sum_{j,S} w_j h(qbar_j(S;t,z)),
    omega(d)=d(2+log(1/d)).

Then, with N=2^n,

    |Delta(t,z)-Dhat(t,z)| <= 2 N omega(R(t)).             (1.1)

In particular, if R(t)<=C t^k for fixed C,k>0, the right side is O(t^k log(1/t)), uniformly in z. No lower bound on any nonzero leading probability coefficient is needed. This remains true at exactly zero probabilities and at coefficient crossover scales. A checkable sign condition is Dhat+2N omega(R)<0.

**Proof.** For 0<=a<b<=1 and d=b-a, absolute continuity on [a,b] (interpreted as an improper integral if a=0) gives

    |h(b)-h(a)| <= integral_a^b (1-log s) ds
                  <= integral_0^d (1-log s) ds
                  =d(2-log d).

The second inequality follows because 1-log s decreases. The function omega is increasing on (0,1]. Clipping cannot increase the distance to a number in [0,1], hence every event entropy error is at most omega(R). The absolute weights sum to two, which proves (1.1). No normalization of the approximating arrays is needed. At R=0 the error is zero by continuity. This proves the lemma.

**Polynomial/analytic use and first nonzero orders.** If a uniform expansion is known,

    p_j(S;t,z)=sum_{k=0}^d a_{j,S,k}(z)t^k + O(t^(d+eta)),

use the full displayed polynomial as q. If all displayed coefficients vanish, that event is controlled by the same remainder, not silently discarded. If the probability is polynomial and every coefficient vanishes, it is identically zero. If the datum is frozen and the probability is analytic and nonnegative for t>0, its first nonzero Taylor coefficient is positive. If it is nonnegative for both signs of t, that first order is even. These assertions follow by dividing by the first nonzero power and taking one-sided limits. They do not provide a single valuation for moving coefficients a_k(z(t)): the whole q must be retained whenever two displayed terms compete.

For a fixed finite degree d and bounded matrix Taylor data, inclusion-exclusion and multilinearity of determinants give the required uniform remainder. For rational matrix paths with denominators uniformly bounded away from zero on a common neighborhood, expand those denominators first; the same conclusion follows. This is an extra quantitative hypothesis, not automatic for every moving path allowed by A2.

## 2. An optional matrix perturbation certificate

**Lemma 2.** Let K_j and L_j be two feasible triples, each with its own exact arithmetic midpoint, and suppose max_j ||K_j-L_j||op<=delta. Set L_n=n 2^n and suppose L_n delta<=1. Then

    |Delta(K)-Delta(L)| <= 2^(n+1) omega(L_n delta).       (2.1)

Consequently a reference bound Delta(L)<=-c t^q log(1/t), c,q>0, transfers to the moving triple if delta=o(t^q). This criterion is sufficient, not necessary, and can be much too restrictive for rotating frames.

**Proof.** For a k-subset T, telescope det(K_T)-det(L_T) one column at a time. Every unchanged column has Euclidean norm at most one because principal submatrices of contractions have operator norm at most one. A changed column has norm at most delta. Hadamard's determinant inequality therefore bounds the difference by k delta. Thus

    |p_K(S)-p_L(S)| <= delta sum_{T superset S}|T| <= L_n delta.

Apply Lemma 1 with q=p_L. For the stated transfer, put delta=t^q eta(t), eta->0. The ratio of omega(L_n delta) to t^q log(1/t) tends to zero: the term eta log(1/eta)/log(1/t) tends to zero, and the remaining terms are O(eta). This also treats arbitrarily fast decay of eta. Zero events are covered by the scalar estimate itself.

## 3. A quantitative moving-data version of the nonzero-transverse exclusion

This lemma concerns a particular family of moving data and is not a universal theorem about all A2 paths.

Fix n,r and a bound M>=1. For each epsilon, let W=[U,V] be orthogonal and let A,C,X,Y,B be real blocks of the old mixed two-term sizes. Their operator norms are at most M. For sigma=+1,-1 put

    H_sigma=A-sigma X, L_sigma=C+sigma Y,
    K_sigma=W [[I-epsilon H_sigma, sigma sqrt(epsilon)B],
               [sigma sqrt(epsilon)B^T, epsilon L_sigma]] W^T,
    K_0=W diag(I-epsilon A,epsilon C) W^T.

Assume the actual endpoints are feasible. In addition assume that each frozen datum has the old small-parameter feasibility conditions

    H_sigma-BB^T>=0, L_sigma-B^TB>=0,
    ker(H_sigma-BB^T) subset ker B^T,
    ker(L_sigma-B^TB) subset ker B.

These extra conditions allow one to freeze the datum and vary x=sqrt(epsilon) on a two-sided sufficiently small interval. They are not asserted to follow from feasibility at one isolated epsilon. A uniform Schur interval is not needed for the proof; actual endpoint feasibility at the evaluated epsilon is separately required.

Set

    psi_S=det U_S, phi_S=(d/da)det((U+aVB^T)_S)|a=0,
    F=||B||F^2, Z=sum_{|S|=r,psi_S=0}phi_S^2,
    m=min_{|S|=r,psi_S!=0}psi_S^2.

The minimum exists, since sum psi_S^2=1. Both the zero set and all these data may vary with epsilon.

**Lemma 3.** There are constants c,C>0 depending only on n,r,M such that, whenever 0<epsilon<c m and epsilon is sufficiently small by a constant depending only on n,r,M,

    |Delta-(Z-2F)epsilon log(1/epsilon)|
       <= C epsilon(1+log(1/m))
          +C epsilon^(3/2)(1+log(1/epsilon)).             (3.1)

Hence a moving family has Delta<0 eventually if

    F>=f_*>0,  log(1/m)=o(log(1/epsilon)).                (3.2)

A more general sufficient comparison is

    [1+log(1/m)+sqrt(epsilon)(1+log(1/epsilon))]
       /[F log(1/epsilon)] -> 0,                         (3.3)

together with epsilon<c m and the other assumptions. Formula (3.3) is only a sufficient criterion; it does not claim to cover all shrinking B.

**Proof, event coefficients and uniform bounds.** Put x=sqrt(epsilon). For a frozen datum each exact event probability is a polynomial in x of degree at most 2n. Its coefficients are continuous polynomial functions of W and the blocks, so all coefficients and the remainders after a fixed degree are bounded by a common constant on the stated bounded domain. Constants below depend only on n,r,M.

Let P=UU^T, D=UBV^T+VB^TU^T, and J=VB^TU^T-UBV^T. Expanding exp(sigma xJ) gives

    exp(sigma xJ) P exp(-sigma xJ)
      =P+sigma xD+x^2 W diag(-BB^T,B^TB)W^T+O(x^3).

The comparison kernel

    exp(sigma xJ)
      [P+x^2 W diag(-(H_sigma-BB^T),L_sigma-B^TB)W^T]
    exp(-sigma xJ)

agrees with K_sigma through order two, with a uniform O(x^3) matrix error. For a positive contraction T diag(lambda)T^T its full exact-event law is

    p(S)=sum_{|J0|=|S|} [prod_{j in J0}lambda_j
                       prod_{j notin J0}(1-lambda_j)]
                         det(T_{S,J0})^2.                (3.4)

To verify (3.4), expand det(I+K(diag(z)-I)) by principal minors and collect the coefficient of z_S; diagonalization followed by Cauchy–Binet yields the displayed expression. This is the same inclusion-exclusion law, not the inclusion-minor array.

In the comparison kernel a deletion from a high eigenmode or an addition to a low eigenmode costs x^2. Its rank-r no-flip exterior vector is omega+sigma x eta+O(x^2), where omega=u1 wedge ... wedge ur and eta has coordinates phi_S. Replacing one high vector by one low vector gives mutually orthonormal exterior vectors, so ||eta||^2=F and 0<=Z<=F. Formula (3.4) now gives every event through the relevant order:

* If |S|=r and a=psi_S^2>0, then
  p_sigma(S)=a+sigma b_S x+O(x^2), b_S=2 psi_S phi_S, while p_0(S)=a+O(x^2).
* If |S|=r and psi_S=0, then
  p_sigma(S)=phi_S^2 x^2+O(x^3), and p_0(S)=O(x^4).
* If |S|=r-1 or r+1, then
  p_j(S)=c_j(S)x^2+O(x^3), c_j(S)>=0.
* Every remaining cardinality has p_j(S)=O(x^4).

All errors are uniform. For the last assertion, the comparison first gives O(x^3); the actual polynomial has vanishing coefficients through degree two and is nonnegative for both signs of x. Indeed changing the sign of x only changes the transverse block and is orthogonal conjugation by W diag(I,-I)W^T, so feasibility holds on both sides for that frozen datum. Its cubic coefficient must vanish. The same argument applies when phi_S or c_j(S) is zero. Such an event either has a positive even first order at least four or is identically zero; a specific first order beyond four is immaterial because the uniform O(x^4) entropy bound controls it. This reasoning does not use entropy invariance under that conjugation; it uses only preservation of positive-contraction feasibility.

The c-coefficient sums can be obtained without choosing eigenvectors. For z!=0, expand the cardinality generating polynomial through x^2:

    det(I-K_sigma+zK_sigma)
      =z^r {1+x^2[(1-z)tr(H_sigma)/z
                         +(z-1)tr(L_sigma)
                         -(z-1)^2 F/z]}+O(x^4).

The determinant is even in x; expansion of the block determinant proves this identity. Taking coefficients z^(r-1) and z^(r+1) gives

    sum_{|S|=r-1,r+1} c_sigma(S)
       =tr H_sigma+tr L_sigma-2F.

For the midpoint the same sum is tr A+tr C. This identity is polynomial in z, so use of z!=0 in its derivation introduces no missing cardinality at r=1. Endpoint averaging subtracts 2F.

**Entropy estimate for active events.** We have |phi_S|<=sqrt(F)<=sqrt(r)M, hence

    |p_sigma-a| <= L sqrt(a)x+L x^2

for a uniform L; the midpoint satisfies the same inequality. Choosing c small enough in epsilon<c m puts every such probability in [a/2,3a/2] and gives (p-a)^2/a<=C epsilon. Since h''(u)=-1/u,

    h(p_sigma)=h(a)+h'(a) sigma b_S x
                 +O(epsilon[1+log(1/a)]).

For the midpoint the linear x term is absent. Averaging endpoints cancels that term exactly. Summing gives the first term on the right of (3.1).

**Entropy estimate for all zero-base events.** For p=c epsilon+O(epsilon^(3/2)), with 0<=c<=C, apply Lemma 1's scalar estimate to c epsilon (which lies in [0,1] for uniform small epsilon). It gives

    h(p)=c epsilon log(1/epsilon)-epsilon c log c
                +O(epsilon^(3/2)[1+log(1/epsilon)]),

where c log c=0 at c=0. The term |c log c| is uniformly bounded on [0,C], including vanishing coefficients. Events known to be O(epsilon^2) contribute O(epsilon^2[1+log(1/epsilon)]). This proves the uniform treatment of exact zeros, arbitrarily small nonzero c, and changes of the zero set.

The rank-r zero events contribute Z to the coefficient of epsilon log(1/epsilon), the adjacent cardinalities contribute -2F, and active events contribute only the displayed error. This proves (3.1). Since Z<=F, conditions (3.2) or (3.3) make the negative term dominate. In (3.2), log(1/m)=o(log(1/epsilon)) also implies epsilon/m->0, so its Taylor condition holds eventually. This proves the sign statement.

## 4. Explicit shrinking-direction crossover; fixed coordinate frame

This is an auxiliary degeneration of the already known two-coordinate family, not a proposed replacement for the constructor's moving-frame candidate. It shows precisely why fixed-data O(epsilon) cannot be read as O(F epsilon), even when the positive Pluecker mass m equals one.

Fix kappa>0 and let b=epsilon^kappa, 0<epsilon<1/2. Set

    K_sigma=[[1-epsilon, sigma b sqrt(epsilon(1-epsilon))],
             [sigma b sqrt(epsilon(1-epsilon)), epsilon]],
    K_0=diag(1-epsilon,epsilon).

Both endpoint determinants, and the determinants of their complements, equal epsilon(1-epsilon)(1-b^2)>0. Their traces equal one and their diagonal entries lie in (0,1), so both endpoints are strict positive contractions. The stated K_0 is exactly their arithmetic midpoint.

Put u=epsilon(1-epsilon), v=(1-epsilon)^2, w=epsilon^2, delta=b^2 u. The complete four-event laws, in the order empty,{1},{2},{1,2}, are

    endpoint: (u-delta, v+delta, w+delta, u-delta),
    midpoint: (u,       v,       w,       u).

Thus the endpoint laws agree, despite different kernels. Every first nonzero event scale is explicit:

* empty and {1,2}: epsilon with coefficient one at both endpoints and midpoint;
* {1}: order zero, coefficient one;
* midpoint {2}: epsilon^2, coefficient one;
* endpoint {2}: epsilon^(1+2kappa), coefficient one if kappa<1/2; epsilon^2, coefficient two if kappa=1/2; epsilon^2, coefficient one if kappa>1/2.

No zero event is omitted. The same formulas remain meaningful at b=1, when the empty and full endpoint events are exactly zero, although the asymptotic assertions below use kappa>0.

Let D(d)=2h(u-d)+h(v+d)+h(w+d)-2h(u)-h(v)-h(w). Direct differentiation, using u^2=vw, gives

    D'(d)=2log(1-d/u)-log(1+d/v)-log(1+d/w).

Integrating from 0 to delta shows

    Delta= -[(w+delta)log(1+delta/w)-delta]+E,
    |E|<=delta^2/[u(1-b^2)]+delta^2/(2v),  E<=0.          (4.1)

Indeed |log(1-d/u)|<=d/[u(1-b^2)] and log(1+d/v)<=d/v on this interval. This proves (4.1) with explicit denominators, rather than an unspecified shrinking-direction remainder.

The three regimes follow by putting delta=epsilon^(1+2kappa)(1-epsilon):

    0<kappa<1/2:
      Delta=-(1-2kappa)epsilon^(1+2kappa)log(1/epsilon)
                 +O(epsilon^(1+2kappa));

    kappa=1/2:
      Delta=-(2log 2-1)epsilon^2+o(epsilon^2);

    kappa>1/2:
      Delta=-(1/2)epsilon^(4kappa)(1+o(1)).               (4.2)

For the first line, delta/w->infinity and (w+delta)log(1+delta/w)-delta=delta log(delta/w)+O(delta), while E=O(delta^2/u)=o(delta). For the second, delta/w->1 and E=O(epsilon^3). For the third, the bracket is delta^2/(2w)(1+o(1)), and E divided by delta^2/w is O(w/u+w/v)=O(epsilon). All constants here may depend on the fixed kappa; no uniformity across kappa=1/2 is asserted.

For each frozen b the old coefficient has Z=F=b^2, hence leading form -b^2 epsilon log(1/epsilon)+O(epsilon). Substituting b=epsilon^kappa into its leading term produces the wrong leading coefficient for 0<kappa<1/2, the wrong logarithmic order at kappa=1/2, and the wrong power for kappa>1/2. This disproves that informal uniform extrapolation, without disproving the fixed-data theorem or producing a positive entropy gap. Equation (4.1) is a uniform crossover formula in the exact scalar parameter delta/w.

## 5. Separate failure mode: a positive event approaches zero

Even one-point DPP laws show why logarithms of small active probabilities enter (3.1). For h as above and a=epsilon^gamma, gamma>0,

    h(a+epsilon)-h(a)
      =min(gamma,1) epsilon log(1/epsilon)+O(epsilon)

when gamma>=1, and for 0<gamma<1 the same formula has remainder o(epsilon log(1/epsilon)) (indeed O(epsilon+epsilon^(2-gamma))). The fixed-a estimate is merely O(epsilon). These are genuine event probabilities of scalar kernels a and a+epsilon; the complementary event changes entropy by O(epsilon), so the total entropy has the same logarithmic leading term. This example concerns an entropy increment, not a positive chord gap.

An actual one-point chord shows a power crossover. For centers a=epsilon^gamma with 0<gamma<1 and endpoints a±epsilon,

    Delta=-(1/2)epsilon^(2-gamma)(1+o(1)).

Taylor's formula for the Bernoulli entropy gives this because H''(a)=-1/[a(1-a)] and epsilon/a->0. For center c epsilon, fixed c>=1, the leading order is instead epsilon times

    c log c -[(c+1)log(c+1)+(c-1)log(c-1)]/2<0,

with 0 log 0=0 when c=1. The complementary-event contribution is O(epsilon^2). Thus the endpoint-zero case is included, and no sign reversal is claimed.

## 6. Interface to the separately constructed four-coordinate family

The main agent supplied the interface W(t)=Q(t)W0 with c=(1-t^2)/(1+t^2), s=2t/(1+t^2), and a fixed scalar 0<x<1 in its high-block direction. The main candidate is not chosen or frozen here, and its coefficient is not independently recomputed in this unit.

For that interface, the matrix entries are rational/analytic in t with the common denominator 1+t^2. On a fixed small real interval this denominator stays uniformly away from zero. For x in a compact subinterval of (0,1), all matrix Taylor coefficients and full-event remainder constants through any fixed finite order are uniform. Lemma 1 therefore applies as soon as the constructor supplies every event's truncated probability polynomial, including the true midpoint. It does not require positive lower bounds on rare-event coefficients if the complete polynomial is retained and clipped.

For an ordinary entropy power/log series obtained by taking the logarithm of only each event's first term, require a common valuation and a positive uniform lower bound on that first coefficient, or treat its vanishing separately using Lemma 1. These are additional premises for the series manipulation, not automatic consequences of analytic matrix entries.

For fixed x, a proved negative coefficient -g(x)<0 and a proved uniform-in-t remainder close the sign after taking t sufficiently small depending on x. Uniform coefficient/remainder bounds in x alone do not make this threshold uniform as x->0 if g(x)->0. One would need an error bound relative to g(x), or a declared relation between x and t. At x=0 the endpoints coincide exactly and Delta=0; no strictly negative lower bound can extend through x=0. This unit makes no statement for a moving x(t).

## 7. Failure ledger, denominator, and status boundaries

One analytic work unit; no computations; no spawned agents. Four proposed reusable objects were pursued: the finite-law truncation bound, its matrix perturbation corollary, the bounded mixed-family estimate, and the shrinking-direction crossover. All four have complete author proofs above; none is independently audited in this unit.

Rejected inferences retained:

1. Fixed-data O(epsilon) implies a uniform relative error O(F epsilon): false as shown by (4.2).
2. Bounded matrix coefficients alone imply bounded active-event log derivatives: false as Section 5 shows.
3. Analytic matrix paths imply a uniform negative sign down to zero direction: unsupported; a negative coefficient can vanish.
4. Two-sided analytic nonnegativity makes a coefficientwise first nonzero order uniform under moving data: false; Example 4 has an explicit crossover.

The general finite-law approximation lemma is elementary and intended as a rigorous proof interface, not a claimed new mathematical contribution. Lemma 3 adds explicit sufficient conditions to the old scoped mixed-family theorem; those conditions do not solve arbitrary moving-frame A2 paths. The main decision scope remains INCOMPLETE. A fresh context must audit any of these objects before certification. This author will not perform that final audit.
