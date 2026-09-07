# Frozen v2: exact component-pair decomposition and nonpositive C2

Author status: PROVED for the frozen decision problem, pending independent fresh-context verification. The proof uses the actual full tomography assumptions and allows all the singular and non-paired cases in ../frozen_theorem_v2.md. It does not assert global entropy concavity away from this boundary scale.

This file provides an exact alternative to a generic information-loss argument: after resolving the complete tomography kernel, every remaining contribution is a scalar two-point Jensen gap, summed over observable local cofactor pairs. No unproved data-processing inequality is used.

## 1. Objects and component structure

Use the frozen U,V,A,C,X,Y with A+/-X>=0 and C+/-Y>=0. Let E_1,...,E_k be the connected components of the graph of nonzero off-diagonal entries of P=UU^T. After internal orthogonal basis changes and coordinate reordering, the high and low frames are block diagonal:

    U=direct_sum_a U_a, V=direct_sum_a V_a,
    rank U_a=r_a, rank V_a=s_a, r_a+s_a=|E_a|.

The complete tomography identities imply

    X_aa=0 on R^(r_a), Y_aa=0 on R^(s_a), for every a. (1)

For completeness, the structural implication is proved by the following exact coefficient argument, with all details recorded in tomography_components_v3.md. If u_i^T is row i of U, the cofactor identity is

    tr[X adj(sum_i z_i u_i u_i^T)]
       =sum_(|R|=r-1)z_R alpha_R^T X alpha_R.

It vanishes by tomography. Since sum_i u_i u_i^T=I, this implies the analytic identity tr[X(I-sum_i t_i u_i u_i^T)^(-1)]=0 near t=0. A shortest nonorthogonality path i_0,...,i_l has no chord. In the coefficient of its squarefree monomial, the only nonzero products are its forward and reverse orders; the coefficient is twice the product of its nonzero adjacent inner products times u_(i_l)^T X u_(i_0). Thus X vanishes bilinearly on every connected row span. Zero rows are isolated zero high spans and cause no constraint problem. Conversely, an off-block X has zero trace against every such block-diagonal inverse, giving the exact kernel characterization.

The low graph is the same because (I-P)_ij=-P_ij off the diagonal. Complementary minors of [U V] identify the one-particle cofactor vector on T with, up to a common sign, the one-hole cofactor vector of V on E\T. Applying the same argument gives (1) for Y. This reduction neither assumes nor forces each component to have rank or corank one.

## 2. Local projection probabilities and cofactor frames

Let the local active projection law on component a be

    p_a(S_a)=psi_a(S_a)^2,
    psi_a(S_a)=det((U_a)_(S_a)), |S_a|=r_a,
    H_a=-sum_(active S_a)p_a(S_a)log p_a(S_a).

The global active law is its product, so H_P=sum_a H_a. Rank-zero components have the sole empty event of mass 1. Let

    D_a={R_a subset E_a: |R_a|=r_a-1},
    alpha_(a,R_a) in R^(r_a)

be the signed local one-hole cofactor vectors. If r_a=0 there are no such vectors. Cauchy-Binet gives the Parseval identity

    sum_(R_a in D_a)alpha_(a,R_a)alpha_(a,R_a)^T=I_(r_a). (2)

This includes r_a=1: the empty cofactor vector is the scalar 1. Zero vectors from rank-deficient minors can be retained harmlessly.

Likewise, let

    I_a={T_a subset E_a: |T_a|=r_a+1},
    beta_(a,T_a) in R^(s_a)

be the local one-particle cofactor vectors, with an empty family if s_a=0. Exterior orthogonality gives

    sum_(T_a in I_a)beta_(a,T_a)beta_(a,T_a)^T=I_(s_a).  (3)

Neither family is assumed orthogonal or uniformly weighted. Their actual scaled minors enter every expression below.

## 3. The exact finite coefficient being evaluated

The frozen full-event expansion gives

    Delta_e=C2 e^2+O(e^3 log(1/e)).

It comes from inclusion-exclusion, equivalently the exact spectral mixture

    p_K(S)=sum_(J:|J|=|S|)
        [product_(j in J)lambda_j product_(j notin J)(1-lambda_j)]
        det(T_(S,J))^2.

This counts exact events, not inclusion minors as full probabilities. The local argument below evaluates the frozen active, one-flip, two-flip, and zero-support terms individually.

All simultaneous cross terms vanish. On active product configurations, T_S is block diagonal, with block a equal to T_(a,S_a) product_(c!=a)psi_c. Since X_aa=Y_aa=0, an ordered pair a!=b contributes

    (product_(c!=a,b)p_c)psi_a psi_b
       tr(X_ab T_(b,S_b)Y_ba T_(a,S_a)^T).

For each component sum_active psi_a T_(a,S_a)=0 by exterior orthogonality. Multiplication by log p_S=sum_c log p_c does not change the zero: a log factor on a leaves the b sum zero, a factor on b leaves the a sum zero, and a factor elsewhere leaves both zero. Thus the complete active cross sum is zero, without a uniform-support assumption.

For a zero global r-event, T_S=adj(U_S)V_S is zero or rank one. In the rank-one case write T_S=u v^T. The high cofactor of r-1 independent rows in S is a nonzero multiple of u. A bordered addition cofactor on S plus one suitable row is a nonzero multiple of v. The two full tomography equalities force u^T X u=v^T Y v=0. Therefore each of q_S(X,C), q_S(A,Y), q_S(X,Y) is zero, and

    q_S(A-X,C+Y)=q_S(A+X,C-Y)=q_S(A,C).                (4)

If a factor vector is zero, all these claims are immediate. Thus zero-support entropy contributes exactly zero to C2, including singular zero rates.

Consequently the coefficient splits exactly into a high-side and a low-side expression:

    C2=C_U+C_V.                                       (5)

For the high side, writing f(z)=z log z with f(0)=0,

    C_U=(tr X^2/2)(1-H_P)
       -sum_(global one-hole R, m_R(A)>0)
            [1+log m_R(A)]m_R(X^2)
       +sum_(global two-hole S)
            [f(m_S^(2)(A))
                -(f(m_S^(2)(A-X))+f(m_S^(2)(A+X)))/2]. (6)

The low expression is the same insertion expression with C,Y and the beta cofactor frames. Equation (6) retains the non-affine probability drift; it is not replaced by a generic entropy-concavity claim.

## 4. Exact high-side pair formula

For each unordered pair of distinct components a<b, choose local cofactors alpha in D_a and beta in D_b, and set

    g=alpha^T A_aa alpha,
    h=beta^T A_bb beta,
    u=alpha^T A_ab beta,
    x=alpha^T X_ab beta,
    D=g h.                                           (7)

When D>0 define

    G_D(z)=z+(D-z)log(1-z/D), 0<=z<=D,
    G_D(D)=D,
    Phi_D(v)=G_D(v^2), |v|<=sqrt(D),
    gamma_D(u,x)=Phi_D(u)
                   -[Phi_D(u+x)+Phi_D(u-x)]/2.        (8)

When D=0 the contribution is defined as zero; section 7 proves that u=x=0 is then forced by PSD, so this convention omits no variation.

The high-side identity is

    C_U=sum_(a<b) sum_(alpha in D_a, beta in D_b)
                            gamma_(g h)(u,x).         (9)

Here the sum means one vector for every local event, retaining its actual scale. It is not a sum over normalized directions or a quotient of equal cofactor vectors.

## 5. Derivation of (9): active drift and one-hole correction

Because X_aa=0,

    tr X^2/2=sum_(a<b)||X_ab||_F^2.

By (2), for each pair a,b,

    sum_(alpha,beta)(alpha^T X_ab beta)^2=||X_ab||_F^2,
    sum_beta(alpha^T X_ab beta)^2
                    =alpha^T X_ab X_ba alpha.        (10)

Thus the active-drift term in (6) allocates (1-H_P)x^2 to each cofactor pair in (7).

A nonzero global one-hole cofactor comes from exactly one deficient component a: its local event has size r_a-1, every other component is on its active projection support, and the global cofactor is, up to a sign,

    alpha_global=(product_(c!=a)psi_c)alpha,

embedded in the high subspace of a. If a nominal configuration has a rank-deficient local minor elsewhere, its global cofactor is zero and contributes nothing. Hence, with w=product_(c!=a)p_c,

    m_R(A)=w g,
    m_R(X^2)=w alpha^T(sum_(b!=a)X_ab X_ba)alpha.

Summing the exact one-hole correction over the other active local configurations uses

    sum w=1, sum w log w=-sum_(c!=a)H_c.

The resulting coefficient for the a-end of a fixed component pair is

    [H_P-H_a-1-log g]sum_beta x^2.

The b-end gives [H_P-H_b-1-log h]sum_alpha x^2. Using (10) to distribute the active term, all active-plus-one-hole terms associated to one alpha,beta are exactly

    [H_P-H_a-H_b-1-log(g h)]x^2.                      (11)

If g or h is zero, the corresponding squared terms are zero by section 7, so no undefined log is used. This establishes the cofactor scaling and the constant -1 before the two-hole entropy is added.

## 6. Derivation of (9): every two-hole event

The leading two-hole law uses only high-frame columns. A nonzero event therefore cannot exceed r_c rows in any component. Its total deficit is two, leaving exactly two possibilities.

### Both holes in one component

The two-deletion cofactor vector lies in Lambda^2(R^(r_a)), multiplied by the other active projection amplitudes. Its rate is the contraction of Lambda^2(A_aa) with that vector. Although A can have nonzero off-component blocks, those blocks do not enter this principal compound compression. Since X_aa=0, the two endpoint rates equal the center rate. This class contributes zero to (6).

### One hole in component a and one in component b

The global two-deletion vector is, up to a common sign,

    (product_(c!=a,b)psi_c)(alpha wedge beta).

The spaces containing alpha and beta are orthogonal. The compound-matrix identity is

    <alpha wedge beta, Lambda^2(A-sigma X)(alpha wedge beta)>
       =g h-(u-sigma x)^2.                            (12)

There is no factor of 2: the ordered basis e_i wedge e_j for i<j is orthonormal, and (12) is its usual two-by-two determinant contraction. Thus the exact event coefficients are w d_sigma, where

    w=product_(c!=a,b)p_c,
    d_0=D-u^2,
    d_+=D-(u+x)^2,
    d_-=D-(u-x)^2.

Configurations with a deficient remaining local base have zero cofactor, so restricting the remaining factors to their active supports loses no nonzero event.

Since f(wd)=w f(d)+wd log w and d_0-(d_++d_-)/2=x^2, summing the two-hole finite contribution over the remaining active factors gives

    f(d_0)-[f(d_+)+f(d_-)]/2
                  -(H_P-H_a-H_b)x^2.                 (13)

Adding (11) and (13) cancels every component-entropy constant and leaves

    f(D-u^2)-[f(D-(u+x)^2)+f(D-(u-x)^2)]/2
                         -(1+log D)x^2.              (14)

The identity

    f(D-v^2)+(1+log D)v^2=D log D+Phi_D(v)

shows that (14) is exactly gamma_D(u,x). Equations (11)–(14) prove (9). The logarithmic flip-layer cancellation is already part of the frozen expansion; this calculation evaluates the entire finite residual, including its drift rather than dropping it.

## 7. PSD and singular boundaries

Embed alpha and beta in their two orthogonal high component spaces. Compressing A+/-X to their span in the quadratic-form sense gives

    [[g,u+x],[u+x,h]]>=0,
    [[g,u-x],[u-x,h]]>=0.                              (15)

This remains true without normalizing alpha or beta. Thus g,h>=0 and |u+/-x|<=sqrt(g h). If g=0, positivity forces (A+X)alpha=(A-X)alpha=0, because their quadratic form at alpha is g and X_aa=0. Hence A alpha=X alpha=0, so u=x=0; similarly for h=0. This also proves that all formerly omitted zero one-hole logarithms multiply zero corrections. Zero cofactor vectors are a special case of the same argument.

If D>0 but one of d_+,d_- vanishes, f(0)=0 and Phi_D is evaluated at its continuous boundary value. If d_0=0, feasibility (15) forces x=0, so that term has no variation. No interior-rate assumption has been added.

The exact-event asymptotic remainder in the frozen decomposition remains valid for these cases. In particular a zero first-event rate has zero one-flip contribution term by term in the nonnegative spectral mixture, so its next possible same-cardinality selection requires at least three flips. A vanishing second-order rare-event coefficient contributes only O(e^3 log(1/e)) or smaller. No log of a zero number is introduced by (9).

## 8. Low-side formula and the simultaneous case

For each unordered component pair a<b and local one-particle cofactors eta in I_a, theta in I_b, define

    g_V=eta^T C_aa eta,
    h_V=theta^T C_bb theta,
    u_V=eta^T C_ab theta,
    y=eta^T Y_ab theta.

Using (3), the one-particle correction, and the two-particle compound law gives exactly

    C_V=sum_(a<b) sum_(eta in I_a,theta in I_b)
                       gamma_(g_V h_V)(u_V,y).        (16)

The local projection entropy in this calculation is still H_a: complementary projection configurations have the same masses, so deletion of a low complementary mode and addition of a low mode have the same local entropy normalization. More directly, the global addition cofactor is the local beta multiplied by the other high projection amplitudes, exactly as in section 5. Same-component two-particle rates are unchanged because Y_aa=0. PSD of C+/-Y handles every zero boundary as in (15).

Equations (5), (9), and (16) are the required exact simultaneous decomposition. The high and low sides need not commute, need not have paired rank-one components, and need not be diagonal in any observation basis. All their cross contributions were handled in section 3 and are zero.

## 9. Nonpositive sign, then strict strengthening

For D>0 and |v|<sqrt(D),

    Phi_D''(v)=-2log(1-v^2/D)+4v^2/(D-v^2)>=0,

strictly except at v=0. Its continuous extension is strictly convex on the entire interval [-sqrt(D),sqrt(D)]: every nondegenerate interval contains an open subinterval where the second derivative is positive. Therefore every gamma_D(u,x) in (9) and (16) is nonpositive, including boundary endpoints. D=0 terms are zero. This proves the frozen claim

    C2<=0

for every datum satisfying ../frozen_theorem_v2.md.

Only after establishing that claim, a strict strengthening follows. If X!=0, (1) implies some off-block X_ab!=0. Equation (10) then provides at least one cofactor pair with x!=0. PSD forces g h>0 for that pair, and strict convexity makes its gamma strictly negative. All other terms are nonpositive. The same reasoning applies if Y!=0, using (3). Thus

    (X,Y)!=(0,0) implies C2<0,
    (X,Y)=(0,0) implies C2=0 and Delta_e=0 identically.

This is a strengthening of the frozen decision result, not an assumption used to prove it.

## 10. Interpretation and remaining certification scope

The proposed latent-channel intuition is resolved here by exact cofactor bookkeeping. The complete tomography gate first forces all invisible perturbations between orthogonal coordinate components. Parseval cofactor identities then pair the non-affine active drift with both one-flip corrections and the actual two-flip determinant entropies. Their residual is a sum of scalar small-kernel pair gaps. There is no unsigned information-loss remainder and no appeal to a blanket data-processing principle.

This completes an author-level proof of the frozen boundary C2 problem. It does not imply entropy concavity at arbitrary interior kernels or along unrelated scale families. Independent fresh-context verification has not been performed in this route, and no formal gate is claimed.
