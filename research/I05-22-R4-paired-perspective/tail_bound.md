# Explicit one-sided tail bound after the calculation handoff

**PROVED (author proof, not independently reviewed).** This is a fixed-shape auxiliary-domain theorem. It does not close the one-sided intermediate-q problem or the general legal-arrow Shannon problem. It was derived after opening calculation issue73 and assumes no result from that request.

Fix x,y in (0,1) and A,B>0, and fix either sign of b,c with b^2=Av,c^2=Bw. Let v=x(1-x),w=y(1-y),s=A+B and

    K(q)=[[x,0,b],[0,y,c],[b,c,q+A(1-x)+B(1-y)]], q>0.

This positive matrix need not be a contraction. Its positive selected masses and marginals define G1 as in proof.md; its true entropy-direction Hessian is always taken with a fixed physical symmetric D. Define explicit positive constants

    kappa=min(1,3AB,
        A^2(1-v)/(A(1-3v)+3v),
        B^2(1-w)/(B(1-3w)+3w)),

    CT=1+2(A+B)+2AB+A^2(1-3v)/v+B^2(1-3w)/w,
    zstar=A(1-x)+B(1-y),
    CN=s^2+2ABs+AB(x+y+zstar),
    Cstar=s CT+2 CN,
    qstar=2 Cstar/kappa.                              (T1)

For every q>=qstar and every physical symmetric D,

    G1''(K(q);D)>=kappa/(2q) ||D||F^2.                (T2)

Thus all six nonzero directions have strict one-sided positivity on this explicit tail. The constants depend on the fixed shape and may degenerate; no uniform safe margin or fixed weak-coupling constant is asserted.

## Proof: explicit positive limit rather than compactness alone

Put Qinf=J2''/2 from proof.md (20)-(21). In Frobenius-orthonormal physical coordinates, Qinf decomposes into two scalar blocks and two 2x2 blocks. The scalar coordinates D33 and sqrt(2)D12 have coefficients 1 and 3AB. On (D11,sqrt(2)D13) the matrix is

    B_A=[[A^2(1-3v)/v, sqrt(2) A(2x-1)b/v],
         [sqrt(2) A(2x-1)b/v, 3A]].                   (T3)

The second block is the same expression with A,v,x,b replaced by B,w,y,c. To obtain (T3), use f=-A(2x-1)D11/v-2bD13/v in the exact squares (21); m-Ad-Be=D33 and h=2bcD12/(vw). This preserves every physical direction and mixed term.

Direct arithmetic gives

    det B_A=A^3(1-v)/v>0,
    det B_A/tr B_A=A^2(1-v)/(A(1-3v)+3v)>0.

The first diagonal and trace are positive because 0<v<=1/4. The least eigenvalue of a positive 2x2 matrix is at least its determinant divided by its trace. Therefore Qinf(D)>=kappa||D||F^2 with kappa in (T1).

For the full side Fisher, put c_ij=A(1-i)+B(1-j), so 0<=c_ij<=s and t_ij=q+c_ij. At the arrow center the complete conditional score is

    T_ij=v_ij^T D v_ij,
    v_ij=(-b(i-x)/v,-c(j-y)/w,1)^T.

Cauchy--Schwarz in the Frobenius inner product yields

    E[T^2]<=E[||v_ij||^4]||D||F^2=CT||D||F^2.

The exact CT formula follows from independent Bernoulli moments
`E(i-x)^2=v`, `E(i-x)^4=v(1-3v)` and their y analogues. Consequently

    |q F1(D)-E[T^2]|<=s CT ||D||F^2/q.               (T4)

For the cofactor term, let Kstar=K(q)-qE33, a positive semidefinite rank-two matrix. Write Ninf=diag(B,A,AB). The exact integrals

    k0=int_0^B dt/(q+A+t),
    ell0=int_0^A dt/(q+B+t),
    V1=int_0^A int_0^B da db/(q+a+b)^2

give

    |q k0-B|<=Bs/q, |q ell0-A|<=As/q,
    |q^2 V1-AB|<=2ABs/q, 0<qV1<=AB/q.

For the third inequality, use `1-(1+r)^(-2)<=2r` for r>=0. Since
`qN1=diag(q k0,q ell0,q^2V1)+qV1 Kstar` and
`||Kstar||op<=tr Kstar=x+y+zstar`, these inequalities imply

    ||qN1-Ninf||op<=CN/q.                            (T5)

For every real symmetric D, its three eigenvalues show
`||adj D||nuclear=sum_(i<j)|lambda_i lambda_j|<=sum_i lambda_i^2=||D||F^2`.
The trace duality bound therefore gives

    |2tr((qN1-Ninf)adjD)|<=2CN||D||F^2/q.           (T6)

Now Qinf=E[T^2]-2tr(Ninf adjD), an exact consequence of (20). Combine (8), (T4) and (T6):

    qG1'' >= Qinf-Cstar||D||F^2/q
           >= (kappa-Cstar/q)||D||F^2.

For q>=qstar this is (T2). No asymptotic exchange over an unbounded set of directions was used; all errors are operator-form bounds.

The determinant/trace algebra and CT moment identity were independently re-expanded within the author's session using exact symbolic arithmetic; the result is in outputs/tail_checks.json in the local package. This is not a new nonauthor review. The universal inequalities above, rather than a finite tail sample, establish the theorem.

## Exact scope and role

Scaling in proof.md (10) transfers this single-side result to the corresponding strict legal kernels, with the transformed D. It does not grant a uniform range covering all shapes, and it does not replace the paired core in issue73. In particular, for strong fixed legal shapes the explicit qstar can exceed the entire legal q interval, so the bound then adds no coverage to that filament. This limitation is not hidden.

The theorem makes the already established large-q positive limit quantitatively checkable. The main general-Lambda target remains the complement-paired determinant (P12), with its positive compensation and full marginal Fisher. The one-sided statement at intermediate q and the total general-arrow Shannon sign remain INCOMPLETE.
