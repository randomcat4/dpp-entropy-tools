# Continuation: the actual reachable law, jet forgetting, and complete Fisher information

Status: PROVED (AUTHOR PROOF), PENDING_REVIEW. These results continue the analytic work after the initial PR91 checkpoint. All statements concern the same fixed symbol and t in [1/2,3/2]. Notation is from proof.md; none of this signs h''.

## 1. The four images are disjoint; the exact state law is not finite atomic

The correction maps are injective. Indeed E is invertible, so equality of E(D_alpha-Q)^{-1}E^T for two inputs implies equality of the inputs. More quantitatively, det E=1/64 and ||E||_2<=3/16 imply sigma_min(E)>=1/12. Also ||D_alpha-Q||_2<=23/32. Therefore the same inverse identity used for contraction gives the LOWER bound

    ||T_alpha(Q)-T_alpha(P)||_F
      >=ell ||Q-P||_F,
    ell=64/4761>0.                                  (S1)

For distinct alpha,beta,

    (D_beta-P)-(D_alpha-Q)=D_beta-D_alpha+Q-P.

The first difference is a nonzero diagonal matrix with spectral norm at least one; ||Q-P||_2<=1/4. Using the inverse identity with the two different matrices proves

    dist_F(T_alpha(B),T_beta(B))>=3ell/4=16/1587.      (S2)

Thus the four compact branch images are disjoint, not just contractive. Two different infinite words give different limits: remove their common prefix using injectivity and then apply (S2). The coding map from the four-symbol one-sided product space onto A_t is a continuous bijection, hence a homeomorphism. A_t is therefore an uncountable Cantor-type set in the three-dimensional real symmetric state space. At a common prefix of length m, the separation is bounded below by (16/1587)*ell^m and above by (3/8)*k^m.

The invariant law has full support on A_t and no atoms. For a cylinder T_w(A_t) of length m, injectivity and disjointness give a unique label word. Since every weight is between epsilon=81/1024 and 1-3epsilon=781/1024,

    epsilon^m<=eta_t(T_w(A_t))<=(781/1024)^m.         (S3)

The upper bound tends to zero, proving non-atomicity; the lower bound proves full support.

This proves that THIS exact correction-state presentation cannot be replaced by a finite set of its states. It does NOT rule out some different finite hidden-state HMM generating the same observed process, and it does not assert minimality of this sufficient statistic. In particular, the injective maps cannot have the exact finite-word reset property of a rank-one Black-Hole HMM filter.

## 2. Exact invariant moments and unconditional cell law

There are cancellations much stronger than normalization:

    L Q=0 (entry by entry),       L(det Q)=0.          (S4)

To prove the first, multiply each inverse in T_alpha by its determinant weight. One obtains a*beta*E adj(D_alpha-Q)E^T. Each entry of the 2x2 adjugate is affine in a,beta; summing against a*beta annihilates it. For the second,

    g_alpha(Q) det T_alpha(Q)=a*beta*(det E)^2,

whose sum is zero. Thus eta Q=0 and eta(det Q)=0 for every t. Their first and second invariant-functional responses are exactly zero, since these are fixed coordinate observables with identically zero stationary means.

Expanding g from proof.md now gives

    eta_t g_(a,beta)=1/4-a*beta*q^2.                 (S5)

This exactly recovers the unconditional complete two-site DPP law and its genuine t derivatives. It is a useful implementation check and an available exact control variate; it is not a curvature inequality. The exact checker verifies (S4), including both t-jet layers, on every tested finite parent state.

## 3. Explicit C2 forgetting along a fixed word

Here all norms on derivatives of maps are multilinear Frobenius norms. Put k=34/81, r=32/9, e=3/16, e2=17/512, c=1/16. The inverse differentiation formulas give

    ||T_QQ||<=2kr,
    ||T_QQQ||<=6kr^2,
    ||T_tQ||<=2cer^2+2e2*c*r^3=352/729,
    ||T_tQQ||<=4cer^3+6e2*c*r^4<5,
    ||T_ttQ||<=2c^2r^2+8c^2er^3+6e2*c^2r^4<1/2.

For two state/jet triples on the proved invariant jet bounds, subtracting the recurrences (8) in proof.md yields

    dQ_new<=k dQ,
    dJ_new<=k dJ+(3/2)dQ,
    dH_new<=k dH+3dJ+10dQ.                           (S6)

For example the coefficient of dQ in the last line is at most

    (2kr)*(9/8)+(6kr^2)*(9/100)
     +2*(4cer^3+6e2*c*r^4)*(3/10)
     +(2c^2r^2+8c^2er^3+6e2*c^2r^4)<10.

The coefficient of dJ is at most 2*(2kr)*(3/10)+2*(352/729)<3. These exact rational comparisons are checked in exact_checks.py.

Compare the infinite future state Q_infinity and the m-cell zero-terminal approximation Q_m for the same first m cells. The terminal discrepancies obey dQ_0<=3/16, dJ_0<=3/10, dH_0<=9/8. Solving (S6) gives

    ||Q_infinity-Q_m||_F <= (3/16) k^m,

    ||Q_infinity'-Q_m'||_F
      <=(3/10)k^m+(9/32)m k^(m-1),

    ||Q_infinity''-Q_m''||_F
      <=(9/8)k^m+(111/40)m k^(m-1)
        +(27/64)m(m-1)k^(m-2).                      (S7)

For m=0 or 1 the corresponding zero polynomial factors remove the terms, and k is nonzero. First apply these bounds to two finite truncations sharing a prefix. They prove uniform Cauchy convergence of both derivative layers. The uniform-limit differentiation theorem then proves that the limiting coding map is genuinely C2 and satisfies (S7); differentiability is not inferred from mere boundedness.

## 4. The complete conditional Fisher term, not its fixed-Q fragment

Let (Q,J,H) be the infinite coding state and its jets, and let alpha be the current cell label. Define the TOTAL conditional jets

    gamma_alpha = partial_t g_alpha + D_Q g_alpha[J],

    gamma2_alpha = partial_t^2 g_alpha
                  +2 D_Q partial_t g_alpha[J]
                  +D_Q^2 g_alpha[J,J]+D_Q g_alpha[H]. (S8)

Normalization gives sum gamma=sum gamma2=0. The conditional score is psi_alpha=gamma_alpha/g_alpha. Every branch, including rare ones, is present. The local total entropy second derivative is exactly

    -sum_alpha gamma_alpha^2/g_alpha
    -sum_alpha gamma2_alpha log g_alpha.              (S9)

Averaging only (S9) would still omit the response of the future-word law. Equation (15) of proof.md, or the three-Poisson identity in curvature_certificate.md, retains that response. The fixed-Q Fisher fragment in B_t'' is not relabeled as the complete Fisher rate.

Here is a direct bridge to the finite COMPLETE Fisher information. On B, ||D_Q g_alpha||<=1, ||D_Q^2g_alpha||<=1, |g_t|<=7/256 and ||D_Q g_t||<=3/32. Since ||J||_F<=3/10,

    |gamma_alpha|<=7/256+3/10<1/3.

For finite/infinite approximations sharing m future cells, (S7) gives

    |gamma_infinity-gamma_m|
      <=dJ_m+(63/160)dQ_m.

Thus the score difference is at most

    epsilon^(-1)dJ_m
     +[(63/160)epsilon^(-1)+(1/3)epsilon^(-2)]dQ_m.

Its sum over m>=0 is bounded by the explicit rational constant

    Cscore=32135398/894645.                           (S10)

For an n-cell COMPLETE event, its full score S_n=partial_t log p(word) is the sum of the finite future conditional scores. The corresponding sum Z_n of infinite conditional scores differs from it pointwise by at most Cscore. Under the true stationary DPP, each infinite score has mean zero conditional on its future, so different cells are reverse-martingale orthogonal. Therefore

    E Z_n^2=n E psi^2,
    |E S_n^2/n-E psi^2|
       <=2 Cscore sqrt(E psi^2/n)+Cscore^2/n ->0.

It follows that the Fisher information rate per ORIGINAL coordinate is exactly

    lim_(n->infinity) [sum_word (p_n')^2/p_n]/(2n)
      =(1/2) E sum_alpha gamma_alpha^2/g_alpha.        (S11)

This is the full Fisher limit. No event, acceleration, or invariant-measure response was dropped to obtain it.

## 5. A separate, explicit VALUE approximation bound

Let h_m=(1/2)H(Y_0|Y_1,...,Y_m)=(1/2)delta_0 L^m B_t. Conditional relative entropy gives

    h_m-h=(1/2) E KL(g_infinity || g_m).

By (S7) and the weight Lipschitz bound,

    ||g_infinity-g_m||_1 <=(27/64)k^m.

For a zero-sum vector delta, sum delta_i^2<=||delta||_1^2/2. Since each g_m>=epsilon, the elementary KL<=chi-square bound proves

    0<=h_m(t)-h(t)<=(9/16) k^(2m).                   (S12)

This controls the actual entropy RATE rather than a fitted finite-window trend. It is a value bound ONLY: differentiating the inequality does not produce a curvature bound. Curvature is certified by the explicit derivative residuals of curvature_certificate.md.

## Scope and novelty

Non-atomicity, quantitative C2 coding convergence, exact stationary moments, and (S11) are author proofs for this fixed family, pending independent review. They are not an entropy counterexample, a general non-HMM theorem, or a claim of literature novelty. (S12) and a negative sampled c2 do not prove whole-interval concavity.
