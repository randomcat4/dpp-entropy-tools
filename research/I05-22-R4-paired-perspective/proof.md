# I05-22 R4: one-sided perspective, complement compensation, and a two-dimensional core

Status: **PROVED (author proofs; not independently reviewed)** for the identities, positive blocks, reductions, and quadratic-perspective theorem below. **INCOMPLETE** for `G1'' >= 0` and for general missing-edge Shannon concavity. No entropy counterexample is asserted. Novelty is unassessed.

The starting main is `9dcb6e9079ca57f94e0e30d63161cda89ca61fae`. PR60 at `f869fd251c0d6fdad737b6d5efa287307795a87d` is an unreviewed author input, not an accepted theorem. Its public comments were checked at the start of this unit: the returned discussion contained the author's continuation but no nonauthor requested correction. None of the proofs here assumes its 1731-coefficient certificate, its Lambda-zero theorem, or the older r=0 candidate. Those certificates were not rerun.

## 1. Events, domain, and all six directions

For a real symmetric three-point matrix with diagonal x,y,z and off-diagonals a,b,c, set

    Q12=xy-a^2, Q13=xz-b^2, Q23=yz-c^2, R=det K.

In mask order 0,1,2,12,3,13,23,123 the COMPLETE atoms are

    (1-x-y-z+Q12+Q13+Q23-R,
     x-Q12-Q13+R, y-Q12-Q23+R, Q12-R,
     z-Q13-Q23+R, Q13-R, Q23-R, R).                 (1)

They are exactly inclusion-exclusion of the inclusion minors. The entropy uses all eight atoms, natural logarithms, and `0 log 0=0`. At a strict kernel all atoms are positive. Every directional derivative below is on the true line `K+tD` in the observation coordinates. In particular

    -H'' = sum p'^2/p + sum p'' log p.              (2)

At a connected missing-edge center take

    K=[[x,0,b],[0,y,c],[b,c,z]], b c != 0,
    v=x(1-x), w=y(1-y), A=b^2/v, B=c^2/w,
    q=z-A(1-x)-B(1-y), qbar=1-A-B-q.

The exact domain is

    0<x,y<1, A,B,q,qbar>0.                         (3)

Indeed q and qbar are the Schur complements in K and I-K. Diagonal sign conjugation restores either sign of b,c and bijects all physical directions; it does not rotate the observation basis.

Put `Pij=pij0+pij1`. At the center

    Pij=Bern_x(i) Bern_y(j),
    tij=pij1/Pij=q+A(1-i)+B(1-j).                  (4)

For any symmetric D let d=D11, e=D22, and write the conditional derivative as

    Tij=m+f(i-x)+g(j-y)+h(i-x)(j-y), U=(m,f,g,h)^T.

This is an invertible six-coordinate direction change, with inverse

    D33=m-Ad-Be,
    D13=b/2*((1-2x)d/v-f/A),
    D23=c/2*((1-2y)e/w-g/B),
    D12=bc h/(2AB).                               (5)

For direct checking, with `phi_i=(i-x)/v`, `psi_j=(j-y)/w`, (1) gives

    Tij=D33+b^2 d phi_i^2+c^2 e psi_j^2
        -2b D13 phi_i-2c D23 psi_j+2bc D12 phi_i psi_j.

No missing-edge, diagonal, or mixed direction has been removed. The independent product marginal does not remain independent off the center:

    Pij''=2 det(D12block) (-1)^(i+j).               (6)

This term must not be silently set to zero.

## 2. Re-derivation of the perspective formula and scale law

For a twice differentiable scalar function phi and positive P,r, put t=r/P, T=t'. Direct scalar differentiation gives

    [P phi(r/P)]''
      =P phi''(t) T^2+r'' phi'(t)+P''[phi(t)-t phi'(t)].  (7)

This includes the acceleration of both arguments of the perspective. Convexity of the perspective in affine (r,P) therefore does not by itself establish convexity on a kernel-affine path.

Let

    G1(K)=sum_ij pij1 log(pij1/Pij).

For phi(t)=t log t, (7) gives

    G1''=F1+sum pij1'' log tij-sum Pij'' tij,
    F1=sum Pij Tij^2/tij.

The omitted `+1` has coefficient `sum pij1''=K33''=0`. By (4) and (6), `sum Pij'' tij=0` EXACTLY: the double difference of the additive table is zero. This does not drop any of the four selected atoms.

Write

    ell0=log(t00/t10), k0=log(t00/t01),
    V1=log(t10*t01/(t00*t11))>0,
    N1=diag(k0,ell0,0)+V1 K.

The four selected masses in (1) are `(z-Q13-Q23+R,Q13-R,Q23-R,R)`. Pairing their second derivatives with the four log weights gives

    sum pij1'' log tij
      =-2 ell0 det(D13block)-2 k0 det(D23block)
       -2 V1 tr(K adj D).

Consequently

    G1''(K;D)=F1(D)-2 tr(N1 adj D).                 (8)

This confirms PR60 continuation (38) from complete events, rather than assuming its sign. Because `K>0`, `V1>0`, and k0,ell0>0, `N1>0`. That fact alone is insufficient for the sign of (8).

Define `G0(K)=sum pij0 log(pij0/Pij)`. Complementation of ALL three bits gives

    -H(X3|X1,X2)=G1(K)+G0(K)=G1(K)+G1(I-K).        (9)

The direction in the complemented kernel is -D; its adjugate equals adj D. Its four terms are retained, not declared independently nonnegative.

For lambda>0 let S=diag(1,1,sqrt(lambda)). Inclusion-exclusion shows, even off the arrow center,

    pij1(SKS)=lambda pij1(K),  Pij(SKS)=Pij(K).

Hence, wherever these positive masses define the perspectives,

    G1(SKS)=lambda G1(K)+lambda log(lambda) K33,
    G1''(SKS;SDS)=lambda G1''(K;D).                 (10)

The second added term is affine. The transformed direction is essential. This is not entropy invariance under a spectral rotation. Setting lambda=1/q normalizes q to 1, giving the auxiliary one-sided shape domain `0<x,y<1, A/q,B/q>0`. The resulting matrix need not be a contraction, but its four selected masses and four Pij remain positive. Conversely any such auxiliary arrow center can be scaled down to a strict contraction, for example by lambda=1/(1+q+A+B). Thus the one-sided sign question on this auxiliary domain is equivalent to the one-sided sign question on legal connected arrows. It is NOT equivalent to the full entropy sign question, which is weaker by (9).

## 3. Two positive blocks for each side

Use the two scalar functions

    phi1(t)=t log t, phi0(t)=(1-t) log(1-t).

For s=0,1 define all quantities in the ORIGINAL table (4):

    ell_s,j=phi_s'(t0j)-phi_s'(t1j)>0,
    k_s,i=phi_s'(ti0)-phi_s'(ti1)>0,
    ell_s=(1-y)ell_s,0+y ell_s,1,
    k_s=(1-x)k_s,0+x k_s,1,
    lambda_s=ell_s,0-ell_s,1,
    J_s=phi_s(t00)+phi_s(t11)-phi_s(t10)-phi_s(t01).

Explicitly `lambda_1=-V1`; put

    V0=log((1-t10)(1-t01)/((1-t00)(1-t11)))>0.

Then `lambda_0=V0`. Set `n1=V1 z`, `n0=V0(1-z)`. With `mu=2x-1, nu=2y-1`, define

    L_s=[[A ell_s/(2v), J_s],[J_s,B k_s/(2w)]],

    C_s=[[-ell_s, mu ell_s/2, w lambda_s, -w lambda_s mu/2],
         [-k_s, v lambda_s, nu k_s/2, -v lambda_s nu/2]],  (11)

and let R_s have first row/column zero and lower 3x3 block

    [[v ell_s/(2A), 0, -vw lambda_s/(2A)],
     [0, w k_s/(2B), -vw lambda_s/(2B)],
     [-vw lambda_s/(2A),-vw lambda_s/(2B),vw n_s/(2AB)]]. (12)

For `aij=(1,i-x,j-y,(i-x)(j-y))^T`, the complete side Fisher is

    F_s=sum Pij phi_s''(tij) aij aij^T,
    phi1''=1/t, phi0''=1/(1-t).

Then, with `delta=(d,e)^T`,

    G_s''=delta^T L_s delta+2 delta^T C_s U
                              +U^T Y_s U, Y_s=F_s+R_s. (13)

To verify (11)-(13), substitute (5) into (8) and the analogous complemented cofactor formula. In either case N_s in original coordinates is

    [[k_s,0,-lambda_s b],[0,ell_s,-lambda_s c],
     [-lambda_s b,-lambda_s c,n_s]].

Collecting coefficients uses the identity

    J_s=A k_s+B ell_s-n_s+lambda_s(A mu+B nu).

It follows either by collecting the four logarithms or integrating phi_s''. The attached exact checker verifies the coefficient collection for a GENERIC symmetric arrow N with this relation, hence includes all mixed terms.

**Lemma 1.** Both L_s are positive definite on the entire domain (3).

Proof. Here phi_s'' is strictly convex and positive. The fundamental theorem of calculus and the strict trapezoid inequality give

    J_s=int_0^A int_0^B phi_s''(q+a+b) db da>0,
    J_s < B(ell_s,0+ell_s,1)/2,
    J_s < A(k_s,0+k_s,1)/2.

Also

    ell_s-w(ell_s,0+ell_s,1)
      =(1-y)^2 ell_s,0+y^2 ell_s,1>0,

and the analogous k_s-v sum is positive. Multiplication gives
`J_s^2 < AB ell_s k_s/(4vw)`. The diagonal entries of L_s are positive, proving the lemma.

**Lemma 2.** R_s has precisely one zero direction (m), and its lower 3x3 block is positive definite. In particular, Y_s and Y=Y0+Y1 are positive definite on the entire domain (3).

Proof. We already have N1>0. Directly

    N0=diag(k_{side0,face1},ell_{side0,face1},0)+V0(I-K)>0.

Here the braces identify the side and the face, not matrix indices. The face-1 entries occur because k_{side0,face0}-V0=k_{side0,face1} and likewise for ell. The first checkpoint incorrectly printed face0 in this decomposition; that index is corrected here. The weighted N_s and the matrices (11)-(13) are unchanged.
In particular `(N_s)12=0` for each side. For a physical direction with d=e=0,

    -2 tr(N_s adj D)
      =2 (D23,D13,-D12) N_s (D23,D13,-D12)^T.

By (5) the map from (f,g,h) to (D23,D13,-D12) is invertible. This proves the stated congruence and strictness of the 3x3 block. Finally F_s>0 because all four weights are positive and the four evaluations of a bilinear polynomial determine it. This proves the lemma without a lower bound on rare-event probabilities.

## 4. Exact complement compensation: a genuinely weaker core

Define the individual side Schurs

    S_s=Y_s-C_s^T L_s^{-1} C_s,
    L=L0+L1, C=C0+C1, Y=Y0+Y1,
    Z=L1^{-1}C1-L0^{-1}C0,
    P=(L1^{-1}+L0^{-1})^{-1}>0.

Then the conditional-entropy Schur is EXACTLY

    S_cond=Y-C^T L^{-1}C=S1+S0+Z^T P Z.           (14)

No matrices are assumed to commute. To prove the identity, minimize
`(delta+a)^T L1(delta+a)+(delta+b)^T L0(delta+b)` over delta. Completing the square at the unique minimizer gives
`(a-b)^T(L1^{-1}+L0^{-1})^{-1}(a-b)`.
Set a=L1^{-1}C1 U, b=L0^{-1}C0 U and compare the constant terms. This proves (14) for every U.

At the arrow center the leaf marginal negative Hessian is exactly

    M=diag(1/v,1/w),

including the cancellation of its missing-edge acceleration. Therefore the full Shannon Schur is

    S_H=S1+S0+Z^T P Z
         +C^T[L^{-1}-(L+M)^{-1}]C.                (15)

Both added terms are positive semidefinite. They are the compensation LOST if the two sides are minimized independently, plus the retained marginal Fisher. Formula (15), not S0>=0 and S1>=0 separately, is the appropriate weaker core.

The logical difference is strict for general block matrices: L0=L1=1, C1=2, C0=-2, Y0=Y1=1 give S0=S1=-3 but S_cond=2. This artificial scalar illustration is not asserted to be a DPP example, and is not a counterexample to (8).

## 5. An explicit two-dimensional determinant target

Lemma 2 permits a different, globally justified elimination: eliminate all FOUR conditional score coordinates instead of the two leaf diagonal coordinates. Define

    E_s=L_s-C_s Y_s^{-1} C_s^T,
    E_cond=L-C Y^{-1} C^T,
    E_H=L+M-C Y^{-1} C^T.                          (16)

Each is only 2x2. They are pointwise equivalent, respectively, to the six-direction one-sided, conditional, and full entropy Hessian sign problems. This is not a proof of their signs.

There is a useful further exact sign fact. For any positive definite 3x3 N, the cofactor quadratic form

    Q_N(D)=-2 tr(N adj D)
          =det N [tr(E^2)-(tr E)^2],
    E=N^{-1/2} D N^{-1/2},

is strictly positive on a five-dimensional hyperplane. Adding the full relevant Fisher preserves at least five positive eigenvalues. Since Y_s,Y are positive 4x4 pivots, each 2x2 matrix in (16) has at least one strictly positive eigenvalue. Consequently

    all six-direction one-sided nonnegativity <=> det E_s>=0,
    all six-direction conditional nonnegativity <=> det E_cond>=0,
    all six-direction full entropy nonnegativity <=> det E_H>=0. (17)

Strict positivity is equivalent to a strictly positive determinant. This uses a proved positive pivot and inertia at each point; it does NOT use unproved global determinant nonvanishing or continuation from a seed.

An actual negative two-vector delta in E_H gives the full negative direction by

    U=-Y^{-1}C^T delta,

followed by (5). Thus the fastest targeted falsification is the 2x2 determinant and its minimizing vector, not an unrestricted six-direction scan. Floating output must be rationally reconstructed and certified using the original eight atoms. A negative E_s alone is only a single-side obstruction. A negative E_cond alone need not negate full entropy, because M is still positive.

## 6. Full Fisher inverses without rational expansion

Let Dv=diag(1,v,w,vw), and let E be the 4x4 matrix whose rows are aij^T, in order 00,10,01,11. With P=diag(Pij), independence gives

    E^T P E=Dv, E Dv^{-1}E^T=P^{-1}.

For any positive table weights w_ij this yields the COMPLETE inverse identity

    [E^T diag(Pij w_ij) E]^{-1}
       =Dv^{-1} E^T diag(Pij/w_ij) E Dv^{-1}.       (18)

Every event is used; there is no projection to fewer scores. Let Wt=E^T diag(Pij tij)E. Then

    F1^{-1}=Dv^{-1} Wt Dv^{-1},
    F0^{-1}=Dv^{-1}(Dv-Wt)Dv^{-1},
    (F0+F1)^{-1}
      =Dv^{-1}[Wt-Wt Dv^{-1}Wt]Dv^{-1}.            (19)

The last identity uses t(1-t), NOT a sum of the first two inverses. In particular

    (F0^{-1}+F1^{-1})^{-1}=Dv,

whereas F0+F1 is generally not Dv. Formula (19) is the useful complement-preserving identity.

Wt is a short polynomial matrix because t=z-A(i-x)-B(j-y). Explicitly

    Wt=z Dv-A Je-B Jf,

    Je=[[0,v,0,0],[v,-mu v,0,0],[0,0,0,vw],[0,0,vw,-mu vw]],
    Jf=[[0,0,w,0],[0,0,0,vw],[w,0,-nu w,0],[0,vw,0,-nu vw]].

Thus the remaining target (17) need not begin with a large determinant expansion. Inverting the positive Y=F+R can use (19) and a positive 3x3 update, since R has rank three. All log terms from q and qbar remain paired in C,L,R.

## 7. A full-six-direction quadratic-perspective theorem

This is a separate auxiliary theorem, not a Shannon theorem. Define locally

    J2(K)=sum pij1^2/Pij.

At every connected arrow with x,y in (0,1), A,B,q>0 (including the auxiliary non-contraction domain), its Hessian is strictly positive for every nonzero real symmetric D.

Proof. Apply (7) with phi=t^2. The selected atoms give

    J2''=2 E[T^2]-4A det(D13block)-4B det(D23block)
                              -4AB det(D12block). (20)

The last term comes from `-sum Pij'' tij^2` and must be retained. Substitution of (5), `E[T^2]=m^2+vf^2+wg^2+vw h^2`, and `mu^2=1-4v`, `nu^2=1-4w` gives the exact sum of squares

    J2''=2(m-Ad-Be)^2
       +3v[f+A mu d/(3v)]^2+3w[g+B nu e/(3w)]^2
       +2A^2(1-v)d^2/(3v)+2B^2(1-w)e^2/(3w)+3vw h^2. (21)

All displayed coefficients are positive. Vanishing of the sum forces d=e=h=f=g=m=0, and hence D=0 by (5). This proves the theorem.

For fixed x,y,A,B and fixed PHYSICAL D, let only the auxiliary q tend to infinity. From (8),

    q G1''(K(q);D) -> J2''(K(q);D)/2.              (22)

Indeed q/tij->1, q k0->B, q ell0->A, q^2 V1->AB, and the off-diagonal/first-two-diagonal parts of q V1 K tend to zero. The right side of (20) is independent of q. The finite-dimensional matrix convergence and (21) imply positivity for all sufficiently large q at each fixed shape (x,y,A,B). Neither the threshold nor the convergence is claimed uniform near leaf or coupling degenerations. This identifies a controlled asymptotic baseline, not a proof for intermediate q and not a finite-sample inference.

## 8. Literature bridges, chosen route, and exact remaining obligations

Two structurally different routes were compared before selecting the paired route.

* Scalar perspective / Phi-entropy route: Boyd--Vandenberghe, *Convex Optimization*, section 3.2.6, gives the perspective operation. Chafai, *Entropies, convexity, and functional inequalities*, arXiv:math/0211103, and his author exposition *About variance and entropy* (2025-01-25), relate Phi-entropy convexity to concavity of 1/phi''. Here phi=t log t and phi=t^2 satisfy that scalar condition. The PRECISE missing bridge is (7): P and r accelerate on a K-affine path. Fixed-measure Phi-entropy convexity cannot delete those terms. Formula (21) closes the quadratic member, but supplies no automatic limiting argument for Shannon.
* Complement/parallel-sum route: Anderson--Duffin, *Series and parallel addition of matrices*, J. Math. Anal. Appl. 26 (1969), 576--594, DOI 10.1016/0022-247X(69)90200-5, defines the positive parallel sum `(L1^{-1}+L0^{-1})^{-1}` for nonsingular positive matrices. Lemma 1 verifies precisely that hypothesis here. Equations (14)-(15) are the explicit DPP bridge, derived in full rather than borrowed as a global theorem.

The second route was selected because it preserves the q/qbar compensation and gives the smaller determinant target (17), regardless of the unresolved truth of the stronger single-side statement.

Source entry points: https://web.stanford.edu/~boyd/cvxbook/ ; https://arxiv.org/abs/math/0211103 ; https://djalil.chafai.net/blog/2025/01/25/about-variance-and-entropy/ ; https://doi.org/10.1016/0022-247X(69)90200-5 . The source-backed standard facts and the new DPP bridge are distinct. The Quarez matrix-polynomial existence result is not invoked to certify a logarithmic open-domain inequality.

Remaining: prove or disprove det E_1>=0 on its four-shape auxiliary domain; independently, and more importantly, prove or disprove det E_H>=0 on (3), with both sides and marginal Fisher present. No sign of these determinants is asserted. A longer global elimination belongs to a bounded independent computation contract, not an unbounded author expansion. The original fixed-three-diagonal radial Loewner route is not restarted. All displayed new identities have an actual short exact author check in `verify_bridges.py`; that run is not independent review, CI, or a proof-assistant certification.
