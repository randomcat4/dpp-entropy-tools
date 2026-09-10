# I05-29: exact local-channel decomposition and genuine higher-dimensional whole chords

Status: PROVED (author proof), PENDING_REVIEW; novelty NOT_ASSESSED. Successor to PR80 and issue93, from main c6618e37640c5d019d9bbdc6fbffdc7fe31241f1. This file does not advance an earlier review freeze. All kernels below are real, and all entropies are complete-configuration Shannon entropy with natural logarithms and 0 log 0 = 0.

The construction is not an assertion that rotating an observed kernel preserves entropy. It proves an explicit classical law in the actual expanded coordinates, followed by an exact entropy identity. Spectral decompositions are used only to establish legality.

## 1. A finite binary-input channel has an entropy-preserving refinement up to an affine term

Let Q_x(y), x in {0,1}, be a fixed channel with finite output alphabet. Remove output symbols whose probability is zero for both inputs. Set d_y=Q_1(y)-Q_0(y), and partition outputs into P={d>0}, N={d<0}, Z={d=0}.

If the channel is informative, M=sum_P d_p=sum_N(-d_n)>0. Choose any coupling gamma_{pn}>=0 with row sums d_p and column sums -d_n; one explicit choice is gamma_{pn}=d_p(-d_n)/M. For each positive gamma introduce a selector j=(p,n) and define

    alpha_j(p)=gamma_{pn}/d_p,
    alpha_j(n)=gamma_{pn}/(-d_n),

with alpha_j(y)=0 elsewhere. Each z in Z has its own selector j=z with alpha_z(z)=1. For every output y, sum_j alpha_j(y)=1.

Refine the output by drawing J conditionally on Y using alpha, independently of the input given Y. For j=(p,n),

    c_j = gamma_{pn}[Q_0(p)/d_p + Q_0(n)/(-d_n)] > 0,
    a_j = gamma_{pn} Q_0(p)/(d_p c_j),
    theta_j = gamma_{pn}/c_j.

Then P(J=j|X=x)=c_j is independent of x. Label the two outputs in this selector by Z_j=1 for p, Z_j=0 for n. Its conditional binary channel is

    P(Z_j=1|X=x,J=j)=a_j+theta_j x,
    0<=a_j, 0<theta_j, a_j+theta_j<=1.

A zero-difference symbol has c_z=Q_0(z) and a_z=theta_z=0, with deterministic binary output 0. If the original channel is uninformative, all selectors can be of this last kind.

These statements follow by substitution: the difference between the two selector probabilities is gamma-gamma=0, while the difference between the binary success probabilities is gamma/c. Thus the selector is a genuine input-independent random variable, not a parameter-dependent reweighting.

For n independently applied local channels Q_i and any input law X, the selectors are mutually independent and independent of the entire X. Conversely, conditional on the original output Y, their law is the product of the alpha_i. Define

    chi_i(x)=sum_y Q_i(y|x) H(alpha_i(.|y)).

The two chain-rule evaluations of H(Y,J) therefore give exactly

    H(Y) = sum_i H(c_i)
           - sum_i [(1-m_i) chi_i(0)+m_i chi_i(1)]
           + sum_j (product_i c_{i,j_i}) H(Z|J=j),             (1)

where m_i=P(X_i=1). No data-processing inequality has been substituted for equality. In particular, the correction preceding the sum is affine in the input one-coordinate marginals, even when they move.

## 2. For DPP input, every refined binary law remains truly K-affine

Let X have real DPP kernel K. For a selector tuple j, set

    D_j=diag(sqrt(theta_{i,j_i})), A_j=diag(a_{i,j_i}),
    K_j=A_j+D_j K D_j.

Independent binary channels with success probability a_i+theta_i X_i give exactly the DPP with kernel K_j. Indeed, for every S,

    E product_{i in S} Z_i
      = E product_{i in S} (a_i+theta_i X_i)
      = det((A_j+D_j K D_j)_S)

by determinant multilinearity and the defining inclusion probabilities. This identifies the entire law, including all zero and rare events. Also

    K_j>=0,
    I-K_j=(I-A_j-D_j^2)+D_j(I-K)D_j>=0.

Combining this with (1) proves the exact identity

    H(Y_K)=C(K)+sum_j w_j H(K_j),                            (2)

where w_j=product_i c_{i,j_i} are fixed nonnegative weights summing to one, and C(K) is affine in diag K. Consequently, for every true affine path K(t)=K_0+tE,

    d^2/dt^2 H(Y_{K(t)}) = sum_j w_j d^2/dt^2 H(K_j(t)).    (3)

The same statement holds for mixed affine derivatives wherever derivatives exist. Deterministic coordinates cause only identically zero events and may be treated by continuity. This is an identity for the full Fisher plus acceleration expression, not a projection of the Fisher term. The transformed path is A_j+D_j K_0 D_j+tD_j E D_j, not an L-affine or spectral path.

## 3. Actual coordinate expansions that realize these local channels

Partition N observed coordinates into n disjoint, nonempty groups G_i. On G_i choose a real unit vector v_i. Embed these vectors as the columns of W, so W^T W=I_n and each observed row belongs to exactly one column support. Choose block diagonal R=direct_sum R_i such that

    R_i v_i=0,
    0<R_i|_{v_i^perp}<I|_{v_i^perp}.

For a one-coordinate group the condition on the zero-dimensional complement is empty. Set

    K_tilde=R+W K W^T.                                     (4)

It is strictly legal exactly when K is strictly legal: on Ran W it is K and on its orthogonal complement it is R. This fact concerns eigenvalues only.

The full observed configuration law of (4) is the product-channel output from X~DPP(K) with the local channels

    Q_i(T_i|x)=p_{R_i+x v_i v_i^T}(T_i), x in {0,1}.         (5)

Here both local kernels are legal, including their deterministic eigenvalue 0 or 1. To prove (5), fix every T_i and put E_i=R_i-diag(1_{G_i\T_i}). For invertible E_i, the determinant lemma gives

    det(E+W K W^T)=product_i det(E_i) det(I+K diag(g_i)),
    g_i=v_i^T E_i^{-1}v_i.

Expansion in principal minors of K equals the expectation over X of product_i det(E_i)(1+X_i g_i). The rank-one determinant lemma identifies det(E_i)(1+xg_i)=det(E_i+xv_iv_i^T). Multiplying the complete-event signs gives (5). The identity is polynomial in all matrix entries, so extends to singular E_i without dividing by a zero event probability. Thus this derivation is in the actual observed basis; it does not use entropy invariance under W.

For every group the empty and full configurations distinguish the input:

    Q_i(empty|1)=0, Q_i(full|0)=0,
    Q_i(empty|0)>0, Q_i(full|1)>0.

The product coupling in Section1 therefore gives a positive-probability selector with a=0, theta=1. This supplies a strictness witness, rather than assuming strictness survives arbitrary marginalization.

## 4. Whole-chord theorem beyond two observed coordinates per side

Accepted input: the real m-by-2 radial theorem on main, reviewed in

    research/C1-verification-20260909/children/w1/W1_ROUND2_INDEPENDENT_REVIEW.md

at blob b7804d6c9267cc7d2428765cf344e72470444b56. It states that for strict A,C with C of size two and arbitrary real B, the full entropy of K(t)=[[A,tB],[tB^T,C]] is concave on its whole closed legal interval, strictly Jensen-concave if B!=0. Its proof also proves G(s)=H(K(sqrt(s))) concave for s>=0. This is a previously accepted premise, not a new m-by-2 claim here.

### Theorem 4.1

Apply any expansions (4) separately within the two blocks of such a base path. Then the expanded real path

    K_tilde(t) = [[R_L+W_L A W_L^T, t W_L B W_R^T],
                 [t W_R B^T W_L^T, R_R+W_R C W_R^T]]

has concave complete Shannon entropy on its entire maximal closed legal interval. This interval is exactly the base interval. If B!=0, strict Jensen concavity holds. The observed dimensions on both sides may be arbitrarily large; cross rank is preserved exactly. There is no small-perturbation restriction.

Proof. By (2), the expanded entropy is an affine diagonal correction plus a finite nonnegative weighted sum of entropies of paths A_j+D_j K(t)D_j. They still have two base coordinates on the right and a fixed real cross block multiplied by t. The correction is constant here because the base diagonals are fixed. The accepted m-by-2 theorem applies to each summand; any deterministic coordinates follow by continuous regularization. The positive all-revealing selector gives the unchanged base path with positive weight, proving strictness, including at the legal boundary. Legality equivalence was proved in Section3. The same argument shows the expanded entropy is concave as a function of s=t^2. QED.

This produces correlated, dense cross-rank-two examples with more than two active observed coordinates on both sides. For example, start with arbitrary correlated 2-by-2 A,C and a rank-two B having no zero entry, choose nonzero entries in every v_i, and choose scalar complement backgrounds eta_i avoiding the associated diagonal entry of A or C. All within-group, between-group, and cross-block entries can then be nonzero. The conditions are coordinate constructions, not arbitrary rotations.

### Quantitative curvature

For any nonzero base cross entry B_ij, the accepted s-concavity also implies

    -H_base''(t)>=4 B_ij^4 t^2.                             (6)

A short proof avoids an additional imported inequality: the joint event {X_i=X_j=1} differs from its decoupled probability by -s B_ij^2. Log-sum reduction to that binary event and binary relative entropy's second derivative 1/[p(1-p)]>=4 give I(s)>=2s^2 B_ij^4. Since G is concave, G'(s)<=(G(s)-G(0))/s=-I(s)/s. Thus H''=2G'+4sG''<=-4sB_ij^4. At zero, H''(0)=0 by analyticity.

For arbitrary local channels, let kappa_i=sum_j c_{ij} theta_{ij}^2. Applying (6) inside the exact identity gives

    -H_output''(t)>=4 B_ij^4 kappa_i kappa_j t^2.            (7)

The mode channels (5) have kappa_i>0 because of their revealing selector. Hence (7) is a uniform, positive normalized-curvature margin on the whole strict chord, not just strict Jensen concavity.

## 5. Half-filled complement: a particularly explicit exact formula

If R_i=(I-v_i v_i^T)/2 and d_i=|G_i|, then

    Q_i(T|x)=2^{-d_i}[1+(2x-1) h_i(T)],
    h_i(T)=2 sum_{a in T} v_{ia}^2-1.

The selector is simply the unordered complement pair {T,T^c}. It is uniform and input-independent. Orient the pair so h_i(T)>=0 and put theta_i=|h_i(T)|. Then a_i=(1-theta_i)/2 and

    H(K_tilde)=(N-n)log2
        +2^{n-N} sum_{complement-pair tuples}
             H(I/2+D_theta(K-I/2)D_theta).                  (8)

Moreover kappa_i=sum_{a in G_i} v_{ia}^4, by expanding the second moment of the independent fair-sign sum h_i(T). Thus (7) has fully explicit constants. In a two-coordinate group v=(3/5,4/5), the two selectors have theta=1 and theta=7/25, each with probability 1/2, and kappa=337/625.

## 6. Limits, failed shortcut, and sources

Complement-pair selectors need not be input-independent for a background eta different from 1/2. That naive extension of (8) is false. The general refinement in Sections1-2 repairs this by splitting outputs and retaining the resulting affine entropy correction; one must not simply use uniform pair weights away from half filling.

The construction does not cover every rank-two cross block. With three observed right coordinates obtained from two base coordinates, two observed columns of B_tilde must be proportional. The analogous row condition holds on the left. The original PR58 s=.9 fixture has no proportional row pair in either U or V, so this exact grouped-channel representation does not apply to it. Separate complete-curvature work is required there.

Two methods are genuinely distinct. The PR80 signed-fiber/window method lower-bounds the original full curvature and must allow negative fibers. This method instead proves the exact full-law channel and the affine-correction identity (2), so no unproved sign of a fiber, additive residual, or Markov dissipation is needed. A fixed nonreversible semigroup route still needs a parameter-curvature bridge; a first-order data-processing contraction alone cannot replace (3).

Primary-source checks: Kulesza and Taskar, arXiv:1207.6083v4, Section2.1 and Section2.4.3, provide the DPP inclusion definition and conditioning background. Neither their L-ensemble coordinates nor spectral sampling are used as an affine-entropy theorem. Caputo, Dai Pra and Posta, Ann. IHP Probab. Stat.45 (2009), DOI 10.1214/08-AIHP183, address convex entropy decay through a Bochner method; this is a different second-order route, not a theorem supplying (2) or (3). All new bridge steps are proved above. No literature-priority claim is made.
