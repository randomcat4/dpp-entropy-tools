# U7: a graph-distance diagonal limit for every connected support

AUTHOR STATUS: GENERAL_CONNECTED_PROOF_CANDIDATE_PENDING_INDEPENDENT_REVIEW.

This is a complete proposed analytic proof, not a certification by its author. No finite scout is used to infer a universal identity. The critical new ingredient is the residual-support locality lemma in section 3.

## 1. Statement of the proposed distance-limit theorem

Fix finite n>=2, x in (0,1)^n, X=diag(x), and a real symmetric zero-diagonal A with connected support graph G. Write E for the set of all unordered vertex pairs, not just the support edges. For e={i,j}, let d_e=d_G(i,j). Define w_i=1/[x_i(1-x_i)] and

    b_e = 6 sum_{P shortest i-to-j path in G}
               (product_{v in P} w_v) (product_{a in P} A_a^2).       (1)

Every b_e is strictly positive. In coordinates consisting of x_1,...,x_n and all z_e, where z_ij denotes the symmetric direction E_ij+E_ji, put

    S_epsilon=diag(I_n, (|epsilon|^(-d_e))_{e in E}).

The proposed limit is

    S_epsilon^T Hess H(X+epsilon A) S_epsilon
       -> -diag(w_1,...,w_n,(b_e)_{e in E})                          (2)

as epsilon tends to zero from either side. Consequently the full Hessian is strictly negative definite for every sufficiently small nonzero epsilon. This proves primary target A and, as a corollary, all tree supports. Together with the disconnected obstruction proved below, it gives a connected iff classification for this small-puncture property in every fixed finite dimension.

## 2. Exact likelihood and the minimum-degree coefficient lemma

Let F(x,z)=H(diag(x)+Z), with Z symmetric and zero diagonal. For S subset [n] define

    a_S=product_{i in S}x_i product_{i notin S}(1-x_i),
    zeta_i(S)=1/x_i if i in S, and -1/(1-x_i) otherwise.

Expanding selected diagonal -1 entries gives, directly from Mobius inversion,

    p_S(X+Z)=(-1)^{|S^c|}det(X+Z-I_{S^c}).

Expanding instead in the diagonal entries x_i or x_i-1 yields

    D_S(Z):=p_S/a_S
        =1+sum_{|T|>=2} det(Z_T) product_{i in T}zeta_i(S)
        =det(I+diag(zeta(S))Z).                                    (3)

Thus these are exact event probabilities, not inclusion minors.

Under the reference product law a_S, the zeta_i are independent. Their moments satisfy mu_i(0)=1, mu_i(1)=0 and mu_i(2)=w_i; all moments are analytic functions of strict x. Because each singleton marginal is unchanged by Z, and log a_S is a sum of one-coordinate functions, sum_S a_S(D_S-1)log a_S=0. Hence exactly near Z=0,

    F(x,z)-F(x,0) = E_a[-D_S(Z)log D_S(Z)].                         (4)

All exact atoms at Z=0 are positive. Therefore F is jointly real analytic in (x,z) on some neighborhood of each fixed strict x. Every subsequent Taylor-coefficient argument is within that neighborhood.

For an edge-exponent vector alpha, let z^alpha=product_e z_e^alpha_e and let

    delta_i(alpha)=sum_{e incident to i} alpha_e

be its multigraph vertex degrees. In each determinant monomial on T, every active vertex has degree two, counting a transposition edge twice. The attached zeta exponent at that vertex is one. It follows that in every product of determinant monomials contributing to z^alpha, delta_i is even and the common attached zeta exponent is delta_i/2. Consequently the entropy coefficient has the form

    [z^alpha](F(x,z)-F(x,0))
      = c_alpha product_i mu_i(delta_i(alpha)/2),                    (5)

when all delta_i are even, and is zero otherwise. Here

    c_alpha=[z^alpha] {-det(I+Z)log det(I+Z)}

is a universal scalar independent of x. This follows term by term from the analytic expansion of -D log D about D=1; the common moment factor can be taken outside the coefficient sum.

In particular, if an entropy coefficient is nonzero, every active vertex has EVEN degree at least FOUR: degree two would contribute the zero factor mu_i(1). Thus, writing v(alpha) for its number of active vertices,

    |alpha| >= 2 v(alpha).                                        (6)

This also gives F(x,z)=sum_i h(x_i)+O(||z||^4), with all coefficients of degrees one, two and three identically zero in x. Minimum degree alone is not enough for the desired distance result; section 3 is indispensable.

## 3. Full block-diagonal Hessian locality

### Lemma 3.1: the full cross-block subspace is Hessian-flat

Let K be any strictly feasible block-diagonal kernel with vertex blocks C_1,...,C_r. Its exact law factors as p_S=product_b p_b(S intersect C_b), because inclusion determinants factor and Mobius inversion preserves this product structure.

Let D have zero entries within every diagonal block, with arbitrary real symmetric entries crossing blocks. For each inclusion minor K_T, the first determinant derivative is zero: K_T is positive definite and block diagonal, and tr(K_T^(-1)D_T)=0. Mobius inversion gives p'_S=0 for every event. Also every block marginal remains exactly unchanged along K+tD, since each within-block kernel submatrix is unchanged. Thus for every block event R subset C_b,

    sum_{S: S intersect C_b=R} p''_S = 0.

Using factorization of log p_S and sum_S p''_S=0 gives

    H''_K[D,D] = -sum_S (p'_S)^2/p_S -sum_S p''_S log p_S = 0.      (7)

Polarization proves that the Hessian bilinear form vanishes between any two cross-block directions. Furthermore, the first derivative in any fixed cross-block direction is zero at every strictly feasible block-diagonal K. Differentiating this identity along any block-internal direction proves zero mixed cross/internal Hessian entries. Finally, two internal directions in different blocks have zero mixed Hessian by entropy additivity.

Therefore a coordinate Hessian entry H_{ef} at block-diagonal K can be nonzero only if both coordinate pairs e,f are internal to the SAME block. Likewise H_e can be nonzero only if e is internal to a block. This concerns the entire cross-block subspace, not just one isolated bridging edge.

### Lemma 3.2: locality of residual Taylor support

Let beta be an exponent vector of a Taylor monomial in H_{ef}(X+Z), and let F_beta be the graph of its residual support {a:beta_a>0}. If the coefficient is nonzero, both endpoints of e, and both endpoints of f, must lie in the same connected component of F_beta.

Proof: restrict all kernel coordinates outside F_beta to zero. The resulting K is block diagonal over the components of F_beta for all sufficiently small retained coordinates. By Lemma 3.1 the relevant Hessian entry is identically zero unless the stated condition holds. An identically zero analytic function has zero coefficients, including the coefficient of z^beta. This restriction is performed AFTER taking the full-coordinate Hessian, so no cross-block direction has silently been removed from the direction space.

The analogous first-derivative statement says that a nonzero coefficient of z^beta in H_e requires the endpoints of e to be connected in F_beta.

These statements hold identically for every strict x, on a local x-neighborhood. No finite-parameter test is needed. They also show that if the fixed support G is disconnected, every strictly feasible X+epsilon A has a nonzero exact-flat cross-component direction, and hence cannot have a strictly negative full Hessian.

## 4. Filtration: every same-scale mixed term vanishes

Consider a residual Taylor monomial z^beta in H_{ef} that survives substitution Z=epsilon A. Its support is contained in G, and its epsilon degree is r=|beta|. It comes from the unique entropy monomial

    alpha=beta+1_e+1_f,

with the appropriate positive differentiation multiplier (and 2*1_e when e=f). If this coefficient is nonzero, Lemma 3.2 supplies in F_beta a path joining the endpoints of e and a path joining the endpoints of f. Therefore alpha has at least max(d_e,d_f)+1 active vertices. Applying (6),

    r+2=|alpha| >= 2v(alpha) >= 2(max(d_e,d_f)+1),
    hence r >= 2 max(d_e,d_f).                                    (8)

If d_e!=d_f this is strictly greater than d_e+d_f. Suppose instead r<=d_e+d_f when the distances are equal to d. Every inequality is then an equality:

    r=2d, v(alpha)=d+1, and every active vertex degree is exactly four.

A path in F_beta joining the endpoints of e must have length at least d. There are only d+1 active vertices, so it has length exactly d and uses all of them. Denote it P. It is a shortest path in G. The graph induced by these vertices in G is exactly P: an edge between nonconsecutive path vertices would shorten the path between its endpoints e.

The endpoints of f lie among these same vertices and have G-distance d. Their distance along P is an upper bound for their G-distance and is at most d. The only pair of vertices of a length-d path at path-distance d is its endpoint pair. Thus f=e.

We have proved, for every distinct pair of coordinates e!=f,

    H_{ef}(X+epsilon A) = O(|epsilon|^(d_e+d_f+1)).                 (9)

This includes all unequal-distance blocks and every same-distance block. It rules out a nontrivial leading mixed operator rather than merely asserting that the diagonal looks negative.

## 5. The diagonal equality case is a doubled shortest cycle

Now e=f={i,j}, with distance d. By (8), no diagonal-curvature term occurs below r=2d. In the equality case, the preceding argument shows that the residual support is exactly a shortest path P in G, with no extra vertex or extra edge among its vertices. Every active entropy-monomial vertex has degree four.

If d>=2, e is absent from G and has exponent exactly two in alpha. At either endpoint of P, degree four forces the incident path edge to have exponent two. Propagating along the path forces exponent two on every path edge. Thus alpha is precisely the monomial in which every edge of the cycle P plus e is squared. Different shortest paths give different monomials: a shortest path is the unique path on its induced vertex set.

If d=1, the only active vertices are i,j and the unique monomial is z_e^4. Its entropy coefficient is -w_i*w_j/2, so its second derivative gives -6 w_i*w_j z_e^2.

For d>=2, the next section proves that the doubled-cycle entropy coefficient is -3 product_{v in P}w_v. Two derivatives in the missing coordinate e therefore give -6 product_{v in P}w_v times the product of all path-edge squares. Summing the distinct shortest-path monomials proves

    H_{ee}(X+epsilon A)=-b_e epsilon^(2d_e)
                         +O(|epsilon|^(2d_e+1)),                  (10)

with b_e exactly as in (1). This is a sum of squared path-weight PRODUCTS, not the square of a signed sum. Arbitrary edge signs cannot cancel it.

## 6. Universal doubled-cycle coefficient via a finite coloring identity

Fix a simple cycle of length m>=3, with edge variables z_1,...,z_m. Put q=product z_i and X_i=z_i^2. Its scalar determinant is

    D=det(I+Z_cycle)=M(X)+c q,
    M(X)=sum_{matching J of the cycle} (-1)^|J| product_{i in J}X_i,
    c=2(-1)^(m-1).                                                (11)

Indeed a determinant permutation either consists of disjoint edge transpositions and fixed points, or traverses the entire cycle in one of its two orientations. This accounts for every term, also when m=3.

Let f(u)=-u log u. We want the coefficient of q^2=product z_i^2 in f(D). The expansion in cq gives

    f(M+cq)=f(M)+cq f'(M)+(c^2 q^2/2)f''(M)+higher q powers.

The linear-q contribution is zero at this coefficient, since f'(M) is even in each z_i. Terms of q degree >=3 cannot contribute. The quadratic-q contribution is c^2 f''(1)/2=-2. It remains to prove

    [X_1...X_m] f(M) = -1.                                       (12)

For every positive integer r, selecting a squarefree full-product term from M^r assigns each cycle edge to exactly one of r matching factors. This is precisely a proper r-coloring of the cycle's edges. The line graph of a simple cycle is the same cycle. Hence

    [X_1...X_m] M^r = (-1)^m chi_Cm(r),
    chi_Cm(r)=(r-1)^m+(-1)^m(r-1).                                (13)

For completeness, the latter count equals tr((J_r-I_r)^m), whose eigenvalues are r-1 once and -1 with multiplicity r-1. This counts cyclic color sequences with unequal neighboring colors, including the last/first pair.

The coefficient on the left of (13), defined by the formal binomial expansion (1+(M-1))^r, is a polynomial in r of degree at most m: a full squarefree monomial can use at most m positive-degree factors. Thus equality for all positive integers proves the polynomial identity for formal real r. Differentiating it at r=1 is legitimate and gives

    [X_1...X_m] M log M = (-1)^m chi'_Cm(1)=1.

This proves (12). The total scalar coefficient of q^2 in -D log D is -1-2=-3. Each cycle vertex has monomial degree four, so formula (5) multiplies this by its second moment w_i. The entropy coefficient is therefore exactly

    -3 product_{cycle vertices} w_i.                             (14)

The special one-edge coefficient used in section 5 follows separately from f(1-z^2): its z^4 coefficient is -1/2. The different derivative multiplicities are why both cases give a -6 Hessian factor.

## 7. Diagonal variables, analytic remainders and the full limit

The degree-four start of the entropy offset gives

    H_xx=-diag(w_i)+O(|epsilon|^4).                               (15)

For a residual coefficient of H_e of degree r, its source entropy monomial has degree r+1. The first-derivative locality in Lemma 3.2 forces at least d_e+1 active vertices. Therefore (6) gives r+1>=2(d_e+1), or r>=2d_e+1. These lower coefficients vanish identically on an open set of strict x. Differentiating in any x_i preserves their vanishing, proving

    H_{x_i,e}=O(|epsilon|^(2d_e+1)).                              (16)

These are not finite Taylor guesses: analyticity and the coefficient lemmas give each stated order for the actual function along the fixed ray. One can, equivalently, truncate at total entropy degree 2*diam(G)+2; the remaining zz derivatives have order at least 2*diam(G)+1 and cannot affect any of the finitely many scaled limits.

After applying S_epsilon, equation (9) gives mixed off-diagonal blocks O(|epsilon|); (10) gives diagonal limits -b_e; (16) gives x/e blocks O(|epsilon|^(d_e+1)); (15) gives the diagonal-variable block. This proves (2) in finite-dimensional operator norm. The use of absolute powers in S makes the same negative diagonal limit hold for both signs of epsilon.

Let gamma=min({w_i}_i union {b_e}_e)>0 for the fixed parameters. For all sufficiently small nonzero epsilon the scaled Hessian differs in operator norm from its negative diagonal limit by less than gamma/2, so it is strictly negative definite. S_epsilon is invertible and congruence preserves inertia, proving strict negativity of the original full Hessian.

Finally shrink epsilon_0 until

    |epsilon| ||A||_op < min_i{x_i,1-x_i}.

This guarantees 0<K_epsilon<I. Every point covered is an interior strict kernel, and every real symmetric direction admits a local feasible line there. The conclusion is thus about the full Sym(n) Hessian, including noncommuting and indefinite directions. At each fixed allowed epsilon, continuity also supplies some ambient open neighborhood with the same strict Hessian sign. No uniform unscaled curvature bound or neighborhood through epsilon=0 is asserted.

## 8. What remains for review

The proposed general connected theorem is analytically closed within this manuscript; it has not yet passed independent review. The three most fragile steps are:

1. Full cross-block Hessian flatness, polarization, and the analytic residual-support extraction in Lemma 3.2.
2. Equality in the vertex-count bound, especially why a geodesic on the entire active vertex set forces both marked pairs to coincide and excludes cross terms from multiple shortest paths.
3. The polynomial-in-r justification for differentiating the matching/coloring identity at r=1, followed by restoring the exact-event vertex-moment factors.

The bounded script verifies selected cycle identities, exact-likelihood semantics, long-distance tree and multiple-geodesic mixed coefficients, but is labelled SCOUT and is not any of these proofs. No novelty claim is made here. Independent correctness and prior-art review remain separate obligations.
