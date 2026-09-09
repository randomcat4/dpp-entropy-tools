# All unequal-diagonal Lambda-zero missing-edge centers

Status: **PROVED (author complete computer-assisted proof), not independently reviewed.** Novelty is not assessed. The general Lambda-nonzero missing-edge problem remains INCOMPLETE. The coefficient identities in sections 5–6 are part of the proof, with the complete exact input and verifier in `certificate.py`; they are not numerical sampling.

## 1. Frozen statements

Let |mu|,|nu|,|r|<1 and 0<u<1. Set

    a=(1+r)/2, b=(1-r)/2,
    x=(1+mu)/2, y=(1+nu)/2,
    v=(1-mu^2)/4, w=(1-nu^2)/4,
    z=1/2-u^2(a mu+b nu)/2,
    K(u)=[[x,0,u sqrt(a v)],
          [0,y,u sqrt(b w)],
          [u sqrt(a v),u sqrt(b w),z]].                       (1)

In all statements H is the natural-log Shannon entropy of all eight complete configurations. An entropy directional derivative means the true observation-coordinate affine line K+epsilon D, not the nonlinear path (1).

For a six-vector zeta=(alpha,beta,gamma,eta,xi,omega), use the physical direction

    D11=v alpha, D22=w beta, D33=gamma,
    D12=sqrt(a b v w) eta, D13=sqrt(a v) xi,
    D23=sqrt(b w) omega.                                   (2)

This direction coordinate map is invertible and independent of u at fixed mu,nu,r. Let B(u) be the matrix of -H''(K(u);D) in (2), and let M=dB/du, with zeta fixed.

**Theorem 1.** M(mu,nu,r,u) is positive definite on the entire stated open domain.

**Theorem 2.** At every center (1), -H''(K(u);D)>0 for every nonzero real symmetric D. In particular this includes arbitrary semidefinite rank-two and full-rank directions and the missing-edge direction.

Equivalently, write a general connected missing-edge center as

    K=[[x,0,b0],[0,y,c0],[b0,c0,z]], b0 c0 != 0,
    A=b0^2/[x(1-x)], B=c0^2/[y(1-y)],
    q=z-A(1-x)-B(1-y).

Theorem 2 covers the whole strict family with Lambda=0, equivalently

    q=(1-A-B)/2,
    z=1/2-[A(2x-1)+B(2y-1)]/2.                            (3)

It is not restricted to x=y=z=1/2, to r=0, to bounded edge ratios, or to a compact set separated from the boundary. Negative edge signs are restored by diagonal sign conjugation, preserving every principal minor and every exact event. No spectral rotation is used. Arbitrary long chords leaving this family are not claimed.

## 2. Legality, complete events and the full Hessian

For a general real symmetric three-point matrix with diagonal x,y,z and edges k12,k13,k23 put

    q12=xy-k12^2, q13=xz-k13^2, q23=yz-k23^2, R=det K.

In bit-mask order (0,1,2,12,3,13,23,123), inclusion-exclusion gives

    p0=1-x-y-z+q12+q13+q23-R,
    p1=x-q12-q13+R, p2=y-q12-q23+R,
    p12=q12-R, p3=z-q13-q23+R,
    p13=q13-R, p23=q23-R, p123=R.                          (4)

For (1) the leaf marginal is the product law

    Pij=(1+(2i-1)mu)(1+(2j-1)nu)/4,
    tij=P(X3=1|X1=i,X2=j)
       =[1-u^2(a(2i-1)+b(2j-1))]/2.                     (5)

All eight atoms are Pij tij and Pij(1-tij), strictly positive. More generally the arrow's exact legality domain is 0<x,y<1, A,B>0, q>0, q+A+B<1: the Schur complements in K and I-K are q and 1-q-A-B. For (1), A=u^2 a, B=u^2 b and both complements equal (1-u^2)/2>0.

Differentiating the complete entropy along K+epsilon D yields

    -H'' = sum_S (p'_S)^2/p_S + sum_S p''_S log p_S.        (6)

With lij=log(p0 pij/(pi pj)) and
Lambda=log(p123 p1 p2 p3/(p0 p12 p13 p23)), grouping derivatives of (4) gives

    -H'' = F + 2 sum_(i<j) lij det(Dij)
                 + 2 Lambda tr(K adj D).                 (7)

Here F has all eight terms in (6). The triple determinant identity is
 det(K+epsilon D)=det K+epsilon tr(adj K D)
                 +epsilon^2 tr(K adj D)+epsilon^3 det D.
Thus every acceleration and every mixed direction is retained.

On (1), Lambda=0. To check equivalence with (3), the two conditional leaf odds have magnitudes

    v1=log(1+AB/[q(q+A+B)]),
    v0=log(1+AB/[(1-q-A-B)(1-q)]),
    Lambda=v0-v1.

Since AB>0, equality is equivalent to q=(1-A-B)/2. Set g(s)=log((1+s)/(1-s)). Then (7) is

    B=F-2 tr(N adj D),
    N=diag(g(u^2)-g(r u^2), g(u^2)+g(r u^2),
           log((1-r^2 u^4)/(1-u^4))).                    (8)

These identities were accepted in PR51/55; (4)–(8) also display their complete event basis here.

## 3. Rational derivative and exact elimination

Let J=1-u^4, L=1-r^2 u^4, ei=i-x, fj=j-y. Define the six-vector

    qij=(u^2 a ei^2, u^2 b fj^2, 1,
         2u^2 ab ei fj, -2u a ei, -2u b fj)^T,
    denij=J when i=j, L otherwise.

The full Fisher is diag(v,w,0,0,0,0)+Fmat, where

    Fmat=sum_(i,j) 4Pij qij qij^T/denij.                  (9)

The constant marginal Fisher remains in B. Differentiating (8), put

    n1=4u(1/J-r/L), n2=4u(1/J+r/L),
    n3=4u^3(1-r^2)/(JL).

Directly, M=Fmat'+Q, where the only nonzero upper-triangle entries of Q are

    Q12=-n3 v w, Q13=-n2 v, Q23=-n1 w,
    Q44=2n3 abvw, Q55=2n2 av, Q66=2n1 bw.                 (10)

No logarithm derivative is assumed: g'=2/(1-s^2) gives n1,n2, while differentiating the last entry in (8) gives n3.

For the already formed quadratic form M, make the pointwise invertible change

    m=gamma+u^2 av alpha+u^2 bw beta,
    p=-u^2 a mu alpha-2ua xi,
    q=-u^2 b nu beta-2ub omega,
    h=2u^2 ab eta, Y=(m,p,q,h)^T.                         (11)

In particular qij dot zeta=m+p ei+q fj+h ei fj, because ei^2=v-mu ei and fj^2=w-nu fj. The derivative was taken BEFORE (11); no moving direction is substituted into a derivative.

Write Delta=diag(1,v,w,vw), d0=(1/J+1/L)/2, d1=(1/J-1/L)/2, and

    S=[[mu nu, 2v nu, 2w mu, 4vw],
       [2v nu,-mu nu v,4vw,-2mu vw],
       [2w mu,4vw,-mu nu w,-2nu vw],
       [4vw,-2mu vw,-2nu vw,mu nu vw]],
    G=d0 Delta+d1 S.                                    (12)

Then zeta^T Fmat zeta=4Y^T GY. For example S Delta^(-1) S=Delta, reflecting the two parity eigenvalues in the denominator; this is a product-Bernoulli moment calculation, not an observation-basis rotation.

The two directions invisible to Y give the positive diagonal block

    d_alpha=n2 a u^2 v/2,
    d_beta=n1 b u^2 w/2.                                (13)

The mixed alpha beta term vanishes by u^2(n2 b+n1 a)=n3. All n1,n2,n3 are positive: L +/- rJ=(1 +/- r)(1 -/+ r u^4)>0.

Put theta=a nu+b mu, la=(-2b,theta,0,2aw)^T and lb=(-2a,0,theta,2bv)^T. The couplings with Y are

    L_alpha(Y)=8uvd1 la^T Y,
    L_beta(Y)=8uwd1 lb^T Y.

The lower block before elimination is

    R0=4(R^T G+GR+G')
       +diag(0,n2 v/(2u^2 a),n1 w/(2u^2 b),n3 vw/(2u^4 ab)),
    R=diag(0,1/u,1/u,2/u).

Completing both squares gives

    M>0 iff Rstar>0,
    Rstar=R0-ell_alpha ell_alpha^T/(4d_alpha)
             -ell_beta ell_beta^T/(4d_beta),              (14)

where ell_alpha and ell_beta are the coefficient columns of the displayed couplings. The full change (11) has determinant 8u^4a^2b^2, so

    det M=16 n1 n2 u^12 a^5 b^5 v w det Rstar.             (15)

This is the previously accepted Schur structure, not a new inference from a single positive seed.

## 4. The new degree reduction and symmetry domain

Set t=u^4 and, from now on, J=1-t, L=1-r^2 t, C=1-r^2 t^2. All are positive. Define Rbar=(u/4)Rstar and E=diag(0,1,1,2). Substituting (12)–(14) gives the following entire matrix, depending on u only through t:

    Rbar=EG+GE+4t G_t
       +diag(0, v(1-rt)/(JL), w(1+rt)/(JL),2vw/(JL))
       -4v b^2 t^2/[JL(1-rt)] la la^T
       -4w a^2 t^2/[JL(1+rt)] lb lb^T.                  (16)

For example d1=2ab t/(JL) and rho+r lambda=(1+r)(1-rt)/(JL); these reduce the first Schur coefficient exactly. The second is analogous. Formula (16), not a raw six-dimensional determinant expansion, is the certificate input.

Exchanging the two actual leaf coordinates sends (mu,nu,r) to (nu,mu,-r). It permutes all complete events and all six physical directions, hence preserves inertia of M. Consequently it suffices to certify 0<=r<1. This symmetry restriction changes no quantifier and is not a finite cover approximation.

## 5. Exact determinant identity

Let P(mu,nu,r,t) be the explicitly specified integer polynomial returned by `residual_polynomial()` in the accompanying source. Its representation has six bivariate coefficient polynomials:

    P=c40(r,t)mu^4+c31(r,t)mu^3 nu+c22(r,t)mu^2 nu^2
       +c31(-r,t)mu nu^3+c40(-r,t)nu^4
       +c20(r,t)mu^2+c11(r,t)mu nu+c20(-r,t)nu^2+c00(r,t).

The complete six coefficient polynomials are literals in that file, with no external data dependency. P has 279 nonzero monomials and coordinate degrees (4,4,10,6). The two algebraic symmetries P(-mu,-nu,r,t)=P(mu,nu,r,t) and P(nu,mu,-r,t)=P(mu,nu,r,t) are checked as coefficient identities.

Define the polynomial matrix

    Ahat=2J^2L^2 C Delta^(-1) Rbar.

Although Delta^(-1)Rbar need not be symmetric, this matrix is used ONLY to evaluate the determinant. All its entries are polynomials with rational coefficients. Expanding the 24 determinant products gives the exact identity

    det Ahat=8 t J^3 L^3 C^3 P.                           (17)

It follows that

    det(Delta^(-1)Rbar)=tP/(2J^5L^5C),
    det Rstar=(1-mu^2)^2(1-nu^2)^2 P/(2J^5L^5C).          (18)

The verifier constructs (16) independently from its short defining formula, clears the indicated denominators entry by entry, expands the 24 products in a rational polynomial ring, and checks that every residual coefficient in (17) is zero. It does not load a saved determinant, fit sample values, or inherit the archived r=0 chain. The proposed P was initially transcribed from the public full-r archive; the exact zero residual binds it to the accepted matrix and removes transcription or archive correctness as an unverified premise of this author proof.

## 6. A finite positive-chart certificate on the whole domain

On 0<=r<1 use

    mu=(X-1)/(X+1), nu=(Y-1)/(Y+1),
    r=R/(1+R), t=T/(1+T),
    X,Y,T>0, R>=0.

Define

    Q=(1+X)^4(1+Y)^4(1+R)^10(1+T)^6 P(substitutions).     (19)

All multipliers are positive. Exact expansion gives 1731 nonzero coefficients, all positive integers; the minimum is 192 and the constant coefficient is 432. All absent coefficients in degrees (4,4,10,6) are zero.

Here is a compact audit of the entire coefficient array, grouped by the X,Y exponents. All groups have 71 positive entries except (0,0),(4,4), which have 63, and (0,4),(4,0), which have 57. The minimum positive coefficients in each group are

    [[432, 256, 448, 192, 256],
     [256,1664,2624,1408, 192],
     [448,2624,4352,2624, 448],
     [192,1408,2624,1664, 256],
     [256, 192, 448, 256, 432]].                          (20)

For completeness, the finite arithmetic rule proving (19)–(20) is as follows. To transform one variable of degree d, replace each coefficient on its k-th power by multiplication by the coefficient array of

    (lo+hi Z)^k(1+Z)^(d-k).

Its j-th entry is

    sum_(i+h=j) binom(k,i) lo^(k-i) hi^i binom(d-k,h).      (21)

Apply (21) on the four axes with (d,lo,hi) equal to (4,-1,1), (4,-1,1), (10,0,1), (6,0,1), respectively. The source implements exactly these bounded integer loops, asserts every nonzero coefficient is positive, asserts the counts/minimum/constant, and can emit the full P.json and Q.json arrays. Thus (20) summarizes a reproducible finite certificate, not a sampled sign assertion or an unspecified SDP.

Since Q>=432>0 on the whole chart, P>0 there. In fact

    P >= (27/16)(1-mu)^4(1-nu)^4(1-r)^10(1-t)^6>0         (22)

for the strict parameters in this chart. The bound is allowed to vanish on limiting faces; no uniform positive safety margin is asserted. Leaf exchange covers r<0. Hence P is positive on the entire required domain and (18) proves global nonvanishing.

## 7. Inertia, integration and scope

At mu=nu=r=0 and t=1/16 (u=1/2), the four leading principal minors of Rbar, in the order (m,p,q,h), are

    1009/7200, 743633/6480000,
    1137143/12150000, 9016/253125.                        (23)

The verifier reconstructs this seed from (16); no r=0 positivity theorem is used. Thus Rbar is positive definite at this one point. The parameter domain (-1,1)^3 x (0,1) is connected, the matrix is continuous and, by (18)–(22), nonsingular EVERYWHERE. The ordered eigenvalues are continuous; any change of inertia along a path would force a zero eigenvalue. This proves Rstar>0 globally. Equations (13)–(14) now prove Theorem 1.

At u=0, the center is diagonal and the complete negative Hessian in fixed coordinates (2) is

    B(0)=diag(v,w,4,0,0,0)>=0.

The events stay positive near u=0 for fixed mu,nu,r, so B is differentiable there. For every nonzero fixed zeta and every u>0,

    zeta^T B(u) zeta=zeta^T B(0) zeta
                    +integral_0^u zeta^T M(s) zeta ds>0. (24)

This integrates a field of TRUE AFFINE entropy Hessians in a fixed physical direction; it does not identify u with that affine direction. Theorem 2 follows. This proof neither requires nor asserts strict positivity at u=0, zero-edge axes, deterministic leaves, or singular spectral endpoints.

For a compact interval of an actual affine line all of whose strict centers satisfy (3), (24) gives the usual strict chord inequality. Arbitrary lines leaving that family still require the Lambda-nonzero analysis. No finite or infinite-volume entropy-rate claim, general real three-point theorem, strict positive Jensen counterexample, independent review, CI run or novelty certification is implied.
