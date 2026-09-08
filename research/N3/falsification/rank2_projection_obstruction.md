# Rank-two boundary obstruction to the pair-score Fisher bound

AUTHOR STATUS: PROVED_HERE / PENDING_NONAUTHOR_REVIEW.
This is a counterexample to a proposed sufficient inequality, not to entropy
concavity. It does not change the frozen N3 theorem or settle its remaining
optimal-direction version.

## Statement

Let u=(1,2,3)/sqrt(14), P=uu^T, a_i=u_i^2, and

    K_epsilon=(I-P)/2+epsilon P,  0<epsilon<1/2,  D=I.

For the eight DPP configuration probabilities p_S, put
v_S=d/dt p_S(K_epsilon+tI)|_(t=0) and F=sum v_S^2/p_S.
Let F_pair be the squared norm, in L^2(p), of the orthogonal projection of
the score v_S/p_S onto the span of the constant and all one- and two-site
occupancy statistics. Define ell_ij, Lambda and N as in the frozen theorem,
and C(D)=2 tr(N adj D). Then, as epsilon tends to zero,

    F_pair(I) = 577/18 + O(epsilon),
    C(I) = 2 log(1/epsilon)+2 log(325/1372)
           +O(epsilon log(1/epsilon)).

Consequently F_pair(I)<C(I) for all sufficiently small positive epsilon.
All kernels are strict, real, connected and nonexchangeable; I is an
admissible affine direction. Meanwhile

    F(I)-C(I)=1/(4epsilon)-2log(1/epsilon)+O(1)>0

eventually, so this obstruction is not an entropy-curvature counterexample.

## 1. Exact score projection identity

This paragraph applies to every strictly positive distribution on the cube.
Write s_S=(-1)^(3-|S|). In the eight-dimensional Hilbert space with inner
product <f,g>_p=sum p_S f_S g_S, the seven monomials of degree at most two
are linearly independent. Their orthogonal complement is spanned by
r_S=s_S/p_S, because the alternating sum of each such monomial is zero.
In particular r has mean zero. Its squared norm is Z=sum 1/p_S.

The score h_S=v_S/p_S has mean zero because sum v_S=0. Its pairing with r is

    <h,r>_p=sum s_S v_S/p_S=Lambda',

where Lambda=log(p_123 p_1 p_2 p_3/(p_empty p_12 p_13 p_23)). Thus

    F_pair=F-(Lambda')^2/Z
          =min_c sum_S (v_S-c s_S)^2/p_S,                 (1)
    c_* = Lambda'/Z.

The projection here is onto the whole score span of all first- and
second-order observables. It is not a sum of three pair marginal Fishers.

## 2. Exact events, derivatives, and admissibility

The eigenvalues of K_epsilon are (1/2,1/2,epsilon), so 0<K<I. The off-diagonal
entries are (epsilon-1/2)u_i u_j and are all nonzero. Unequal a_i make the
kernel nonexchangeable. Along D=I the eigenvalues become
(1/2+t,1/2+t,epsilon+t); in particular every |t|<epsilon is strictly feasible.

For a temporarily variable theta, the principal pair minor and determinant
of K=theta(I-P)+epsilon P are

    q_ij=theta^2 a_k+theta epsilon(1-a_k),
    p_123=theta^2 epsilon,

where {i,j,k}={1,2,3}. Mobius inversion, specialized to theta=1/2, gives

    p_empty=(1-epsilon)/4,
    p_i=[1-a_i+(2a_i-1)epsilon]/4,
    p_ij=[a_k+(1-2a_k)epsilon]/4,
    p_123=epsilon/4.                                      (2)

For every 0<epsilon<1/2, positivity of p_i follows because its bracket is
linear between 1-a_i>0 and 1/2; the p_ij bracket is linear between a_k>0
and 1/2. The empty and full atoms are also positive. At epsilon=0, in order
empty,1,2,3,12,13,23,123 the probabilities are

    (1/4,13/56,5/28,5/56,9/56,1/14,1/56,0).

The direction tI changes theta and epsilon simultaneously with derivative
one. Differentiating the general-theta formulas (or their inclusion minors)
therefore gives

    v_empty=-5/4+epsilon,
    v_i=(2a_i-1)/4-a_i epsilon,
    v_ij=(1+2a_k)/4-a_k epsilon,
    v_123=1/4+epsilon.                                    (3)

Equations (2)--(3) have sum p=1 and sum v=0. In particular the derivative is
not the derivative of K_epsilon with respect to epsilon alone.

## 3. Finite projection-Fisher limit

Only p_123 tends to zero. From (2)--(3),

    Z=4/epsilon+O(1),
    Lambda'=v_123/p_123+O(1)=1/epsilon+O(1).

All seven other atoms are analytic and positive near zero. Therefore their
reciprocals and score terms are analytic, and c_*=Lambda'/Z=1/4+O(epsilon).
More precisely c_*-v_123=O(epsilon). The full-atom summand in (1) is then
O(epsilon^2)/p_123=O(epsilon); it contributes zero to the finite limit.

For the remaining atoms, substitute c_*=1/4+O(epsilon) in (1). Their limiting
residual derivatives v_S-(1/4)s_S and contributions are

| Atom | Residual derivative at zero | Squared residual / limiting mass |
|---|---|---|
| empty | -1 | 4 |
| i | -(1-a_i)/2 | 1-a_i |
| ij, complementary k | (1+a_k)/2 | (1+a_k)^2/a_k |

Since sum a_i=1, the total is

    4+sum_i(1-a_i)+sum_i(1+a_i)^2/a_i
    =13+sum_i 1/a_i
    =13+14(1+1/4+1/9)=577/18.                              (4)

All omitted terms are O(epsilon), establishing the claimed expansion. This
argument proves the pole cancellation without subtracting two divergent
asymptotic series or assuming an exchange of limits and differentiation.

## 4. Logarithmic cofactor divergence and the actual Hessian

Set A0=product_i a_i and B0=product_i(1-a_i)=325/1372. At epsilon=0,

    ell_ij=log[a_k/((1-a_i)(1-a_j))]+O(epsilon),
    Lambda=log(epsilon)+log(B0/A0)+O(epsilon).

Consequently N=log(1/epsilon)K_0+O(1). For the precise trace constant use
tr K_epsilon=1+epsilon and

    sum_(i<j) ell_ij=log(A0/B0^2)+O(epsilon).

Since adj I=I,

    C(I)=2 tr N
        =-2 sum ell_ij-2 Lambda(1+epsilon)
        =2 log(1/epsilon)+2log B0+O(epsilon log(1/epsilon)). (5)

Equations (4)--(5) prove F_pair-C tends to minus infinity. On the other hand,
the full event alone contributes

    v_123^2/p_123=1/(4epsilon)+2+4epsilon

to F, and all remaining contributions are bounded. The exact frozen
identity B=F-C therefore proves eventual positive B on this direction.

## Scope and verification binding

The analytic proof is the counterexample mechanism. One deterministic point
epsilon=10^-12 is additionally checked by `rank2_projection_check.py`, which
uses exact rational events, derivatives, F, Lambda', Z and F_pair, and
rational upper/lower bounds for the logarithms in C. A separate covariance
projection calculation corroborates (1) at that same point. No parameter
scan is performed. The check is author verification and must not be relabeled
as a fresh nonauthor review. No conclusion is asserted about F_pair-C at
the frozen A-optimal direction.
