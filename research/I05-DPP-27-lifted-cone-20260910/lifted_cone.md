# Determinant lift, a strict entropy cone, and the unresolved physical response

Status: PROVED (AUTHOR PROOF), PENDING_REVIEW, except the explicitly open physical sign. The interval theorem is proved separately in interval_proof.md. This file does not substitute an affine squared parameter for an affine K path.

## 1. Correct complete-event lift

Put q=t/16>0, b=1/8 and s=q^2. Lift Q=[[x,z],[z,y]] to

    Z=(x,y,r,d), r=qz, d=xy-z^2.

The four signs (a,c) are the actual first and second cell occupations, respectively, encoded as +/-1. The complete-event weight is

    g_ac(s,Z)=1/4-a*x/2-c*y/2+ac(d+2r-s).                      (1)

The coefficients of x and y are IMPORTANT. A local preliminary draft interchanged a and c here. Direct rational determinant comparison rejected it; that failed draft and its invalid first witness are preserved. The final formula (1) follows by expanding ac det([[a/2-x,q-z],[q-z,c/2-y]]). The independently executed interval certificate always used this direct determinant, so was unaffected.

For the corrected lift, write g T=(Nx,Ny,Nr,Nd), where

    Nx=ac b^2(c/2-y),
    Ny=ac[b^2(a/2-x)+s(c/2-y)-2b(s-r)],
    Nr=ac[bs(c/2-y)-b^2(s-r)],
    Nd=ac b^4.                                                (2)

Thus the projective map is T=N/g. Its restriction to d=xy-r^2/s is exactly the original two-site Riccati map, including the transformed off-diagonal r. Every finite complete-word probability is the first coordinate of a product of five-by-five matrices acting on (1,Z); in particular it is AFFINE in the initial lifted state Z.

For fixed s, both g and N are affine in Z. For fixed Z they are affine in s. Joint dependence has the two bilinear terms -ac*s*y in Ny and -ac*b*s*y in Nr; one must not erase them when testing joint concavity.

The homogeneous matrix A_ac(s), with rows ordered1,x,y,r,d, is

    [1/4-ac*s,        -a/2,       -c/2,       2ac,    ac]
    [a*b^2/2,             0,    -ac*b^2,         0,     0]
    [c*b^2/2+a*s/2-2acbs,-ac*b^2,-ac*s,       2acb,     0]
    [a*b*s/2-ac*b^2*s,    0,     -ac*b*s,     ac*b^2,    0]
    [ac*b^4,              0,          0,          0,     0].

Summing the four matrices gives diag(1,0,0,0,0). Expanding a determinant first along its last row and then along the remaining last column gives

    det A_ac(s)=ac b^10=ac/2^30,                               (3)

for every s. Each labeled matrix has full rank5. The rank-one SUM therefore does not satisfy the rank-one LABELED-matrix hypothesis in Han--Marcus's Black-Hole stabilization theorem. This signed positive-on-a-cone realization is not declared a finite-state HMM. It does not exclude a different finite HMM presentation.

## 2. Exact convex hull, not a guessed reachable box

Let C_s be the convex hull of lifts of all real symmetric Q with ||Q||_2<=1/8. Introduce

    U=4(x+y), V=4(x-y), W=8r/q, D=64d.

Then the exact convex set is

    C_s = {2|U|-1 <= D <= 1-2sqrt(V^2+W^2)}.                   (4)

Proof. A physical lift satisfies |U|+sqrt(V^2+W^2)<=1 and D=U^2-V^2-W^2. Write R=sqrt(V^2+W^2). The graph lies between the convex function2|U|-1 and the concave function1-2R, because

    D-(2|U|-1)=(1-|U|)^2-R^2>=0,
    (1-2R)-D=(1-R)^2-U^2>=0.

For the reverse inclusion, at fixed U any (V,W) of radius<=1-|U| is a convex combination of two points on that circle, where the graph has D=2|U|-1. At fixed(V,W), any |U|<=1-R is a convex combination of U=+/- (1-R), where the graph has D=1-2R. Mixing these two representations, which have the same U,V,W, realizes every intermediate D. Degenerate zero-radius cases follow by continuity. This proves (4), with at most four graph points in a representation.

As an optional algebraic description, (4) says that the real block-diagonal matrix with blocks 1+D+2U, [[1-D+2V,2W],[2W,1-D-2V]], and1+D-2U is positive semidefinite. No quantum entropy, coordinate rotation of the DPP, or quantum channel theorem is used.

The original ball has positive complete-event weights, g>=81/1024, and all branch images have ||T_Q||_2<=17/144<1/8. Since (1) and (2) are affine in the initial lift, a convex mixture Z=sum lambda_j Z_j is updated to

    T(Z)=sum_j [lambda_j g(Z_j)/g(Z)] T(Z_j).                  (5)

Therefore g>=81/1024 extends to all C_s, sum g=1, and every branch preserves C_s. Its image is contained in a compact subset of the interior: each physical image has a strict operator-ball margin and hence strict inequalities in(4), and their convex hull retains that margin. Invariant-law integration is therefore supported away from the cone boundary.

For a nonphysical lift the defect has a particularly simple update:

    [d'-x'y'+(r')^2/s] = b^4[d-xy+r^2/s]/g^2.                 (6)

This confirms directly that the physical graph is invariant; the extension is a convex mathematical state domain, not a replacement family of DPP symbols.

## 3. The FULL probability operator preserves state concavity

Fix s. If A is concave on C_s, then

    L_s A(Z)=sum_ac g_ac(Z) A(N_ac(Z)/g_ac(Z))                 (7)

is concave on C_s. Indeed the perspective(p,v)->p A(v/p) is concave for p>0, and each(p,v)=(g,N) is affine in Z. Equation(5) is also a direct Jensen proof of(7). It retains the state-dependent probabilities; branch contraction alone would not prove this statement.

Let p_w(Z) be the complete probability of any output word of n cells. The product-matrix expression makes p_w affine in Z; sum_w p_w=1 and all p_w>0. Hence its Shannon entropy H_n(Z) is concave, with

    -D_Z^2 H_n(Z)[v,v] = sum_w (D_Z p_w[v])^2/p_w.             (8)

Equation(8) is the FULL initial-state Fisher information of this complete-word law. There is no omitted acceleration in (8), because affine dependence is proved for this initial-state variable. It says nothing by itself about the physical t derivative, for which probabilities are not affine.

## 4. The infinite entropy corrector is genuinely and uniformly strictly concave

Let h_cell(s)=2h(t). The original normalized Riccati law has the mixing/resolvent bounds proved in the preserved PR91 dependency. On the physical graph,

    H_n(Q)-n h_cell = sum_(j=0)^(n-1) L^j(B-h_cell)

converges uniformly to its entropy Poisson corrector U_s(Q).

For any Z in C_s choose a finite convex decomposition into physical graph points, with label J taking at most five values (the construction above even gives four). Affinity of every p_w gives an EXACT mixture of the physical initial-state word laws. Consequently

    H_n(Z)=sum_j lambda_j H_n(Z_j)+I(J;W_1,...,W_n).           (9)

The mutual information in (9) is nondecreasing in n and lies in[0,log5]. Thus H_n(Z)-n h_cell has a pointwise finite limit U_s(Z), uniformly bounded on C_s. The limit is concave, independent of the chosen decomposition, agrees with the physical corrector, and solves

    (I-L_s)U_s=B_s-h_cell.                                    (10)

Here B_s in (10) means the entropy observable at parameter s, NOT its derivative. In the derivative formulas below partial_s is written explicitly.

There is no unjustified differentiation of this limit. On a compact subset of int C_s, choose epsilon>0 so Z+/-epsilon*v lies in C_s for all Euclidean-unit v. Affinity and nonnegativity give |D p_w[v]|<=p_w/epsilon. The exact higher derivatives of -p log p therefore have uniform bounds (k-2)! epsilon^(-k) for k>=2 after summation over ALL words. The second and third derivative bounds, concavity and the uniform function bound give local compactness of derivatives. The pointwise limit is unique, so convergence is locally C2 (indeed smooth), and the monotone Fisher matrices in(8) converge to -D_Z^2 U_s. No rare word is discarded.

A two-cell observable calculation gives a uniform strictly positive lower bound. Write the first cell signs(a1,c1) and second(a2,c2). The four bounded observables

    a1, c1, a1*c1, a1*c1*c2

have expectations

    -2x, -2y, 4(d+2r-s),
    8b^2 x+8s y+16b(s-r).                                    (11)

The last expression follows by conditioning on the first branch and summing its weighted Ny numerator. For a state direction v=(vx,vy,vr,vd), denote the derivatives of these four expectations by m1,...,m4. Inverting their linear system gives

    vx=-m1/2, vy=-m2/2,
    vr=-m4/2-m1/32-2s*m2,
    vd=m3/4+m4+m1/16+4s*m2.                                  (12)

The inverse matrix has squared Frobenius norm1861/1024+20s^2, bounded by476821/262144<2 for s in[1/1024,9/1024]. Each observable has variance<=1. Applying Cauchy--Schwarz to its covariance with the full two-cell score gives mi^2<=I_2(v). Hence

    ||v||^2<=2 sum_i mi^2<=8 I_2(v).

Information only increases when more observed cells are retained. Combining this with(8) and the justified limit yields the global STATE theorem

    -D_Z^2 U_s(Z) >= I_4/8,  Z in int C_s,                    (13)

uniformly for every original t in[1/2,3/2]. The norm is the ordinary Euclidean norm of(x,y,r,d), explicitly not the physical K-direction norm.

## 5. Exact pure-parameter cancellations; the terms still not signed

Hold a test function A fixed and vary s at a fixed Z. Now g and N are affine in s, so T_s=N/g has T_ss=-2(g_s/g)T_s. Twice differentiating (7) cancels all first-gradient terms:

    partial_s^2 L_s A(Z)
       =sum_ac g_ac(Z) D_Z^2 A(T_ac(Z))[partial_s T,partial_s T]. (14)

In particular (13) proves the pure operator term

    partial_s^2 L_s U_s <= -(1/8)sum_ac g_ac||partial_s T||^2<=0, (15)

where U_s is held fixed at the reference parameter while differentiating the operator. Likewise

    partial_s^2 B=-sum_ac 1/g_ac<=-16.                        (16)

These are entropy-relevant signs, not merely unspecified norm bounds.

They do not sign the whole physical rate. At a reference s, hold U=U_s fixed and put A_s=partial_s B+(partial_s L)U. Differentiating stationarity twice, and using(10), gives the exact identities

    2 partial_s h = eta_s A_s,
    2 partial_s^2 h = eta_s[partial_s^2 B+(partial_s^2 L)U]
                         +2 (partial_s eta_s)(A_s).           (17)

The weak derivatives of eta are those of the actual Riccati law under the smooth coordinate change r=qz. All states in the support and their branch images lie in the cone interior, so the fixed test functions in (17) are defined on a common neighborhood. Equation(17) can equivalently be written using a Poisson solution for A_s, but no sign for that second solution is assumed.

The original physical parameter satisfies s=t^2/256, s'=t/128, s''=1/128. Therefore

    2h_tt = (s')^2 eta[ B_ss+L_ss U ]
              +2(s')^2 (partial_s eta)(A_s)+s'' eta A_s.      (18)

The first bracket is nonpositive by(15),(16). The mixed stationary-law response and acceleration contribution in (18) are precisely the remaining terms. They cannot be removed by declaring s an affine K parameter. Even partial_s B is not state-concave: at Z=0 its state Hessian along(vx,vy,vr,vd)=(1,-1,0,0) is2/(1/4+s)^2>0.

## 6. Rigorous counterexamples to two general cone shortcuts

These are METHOD counterexamples only, never entropy counterexamples.

First fix s0=1/128 and the concave observable

    A(Z)=-(r-(s0/b)x+(s0/b^2)d)^2.

At Z=0, direct substitution of(1),(2) gives

    L_s A(0)=-(17/256)(s-s0)^2/(1-16s^2).

Its derivative is

    -(17/128)(s-s0)(1-16s*s0)/(1-16s^2)^2,

strictly positive for0<s<s0 in the target range. Thus L_s' is not universally nonpositive on concave observables, even at the physical seed.

Second, joint concavity in(s,Z) is stronger than the fixed-s statement(7) and is false. Take A(Z)=-y^2, reference s*=1/160, Z*=(0,-1/12,0,0), and joint direction

    (ds,dx,dy,dr,dd)=(1,15,-20,1/2,14).

The exact second derivative of L_s A along this line is

    62133760927002633199475/123948511626037169227442>0.         (19)

At epsilon=1/65536 the two endpoints are in the interiors of their exact cones (4), all branch weights are positive, and

    [L_(s*+eps)A(Z*+eps*v)+L_(s*-eps)A(Z*-eps*v)]/2
          -L_(s*)A(Z*)
    =83227040581365279974557560989255720223314146025
      /1426167397794154630144461142089621826100832351402858643456
    >0.                                                       (20)

Both(19) and(20) are evaluated with exact Fraction arithmetic, not numerical eigenvalues. The preliminary wrong-label witness is NOT (19) or (20); it was rejected and is retained in the failure ledger. A corrected numerical scout found a candidate direction; the final evidence is the exact rational substitution and cone inequalities in exact_lift_check.py.

## 7. Scope after these results

We have an explicit invariant convex cone, full weighted perspective preservation, a strictly concave infinite entropy corrector with an explicit full-Fisher lower bound, and exact nonpositive pure-s response terms. We have also disproved two tempting sufficient shortcuts and isolated the remaining mixed/acceleration expression (18). This does not prove or refute physical h_tt on all of[1/2,3/2]. The genuine continuous-interval result obtained by a different, quantitative residual argument is in interval_proof.md.

The source comparison and exact small crosschecks are author work, not S3/S2 acceptance. Novelty is UNASSESSED. No claim about arbitrary non-even/complex symbols, another amplitude, or a general DPP theorem is made.
