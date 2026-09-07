# Controlled finite-block Shannon entropy-gap transfer

Status: **PROVED (author's mathematical claim; independent verification pending)**.
This is a proof of the frozen T2 v1 candidate, not an independent validation report.
Author role: CONSTRUCTION. All quantities concern finite-dimensional complex
Hermitian kernels and natural-log Shannon entropy. No entropy-rate,
stationarity, scalar-process, or realification conclusion is asserted.

## 1. Statement and conventions

Let n >= 1, let (I_1,...,I_m) be a partition of {1,...,n} into nonempty
coordinate blocks, and let K be Hermitian with 0 <= K <= I. Write

    B = blockdiag(K[I_1],...,K[I_m]),    E = K-B.

The finite DPP P_K is characterized by P(S subset X)=det K[S]. Its Shannon
entropy is H(K)=-sum_X P_K(X) log P_K(X), with 0 log 0=0. Define
h(x)=-x log x-(1-x)log(1-x) on [0,1], and interpret tr h(K) spectrally.
The squared Frobenius norm is ||E||_F^2=tr(E*E)=tr(E^2).

The candidate consists of the following assertions:

    0 <= L(K) := H(B)-H(K) <= Q(K) := tr h(B)-tr h(K).       (1)

If, explicitly, eta I <= B <= (1-eta) I for 0 < eta <= 1/2, then

    Q(K) <= R(K) := tr[E^2 (B(I-B))^(-1)]
         <= ||E||_F^2 / [eta(1-eta)].                       (2)

No spectral gap is assumed on K. In particular K can have eigenvalues 0
or 1 in (2). The buffer hypothesis is needed only for the indicated
inverse and quantitative bound; (1) has no buffer hypothesis.

For two contractions K_0,K_1 and t in [0,1], put
K_t=(1-t)K_0+tK_1 and use the same partition for B_0,B_1,B_t. Define

    J_K = H(K_t)-(1-t)H(K_0)-tH(K_1),
    J_B = H(B_t)-(1-t)H(B_0)-tH(B_1).

Whenever L(K_r) <= C_r for r=0,1,t, the transfer interval is

    J_B-C_t <= J_K <= J_B+(1-t)C_0+t C_1.                  (3)

Here each C_r can be Q(K_r), or R(K_r), or the coarse final bound of (2),
provided that bound's hypotheses hold at that index. Thus J_B>C_t
certifies J_K>0; J_B<-(1-t)C_0-tC_1 certifies J_K<0.

## 2. Block marginals and the classical entropy identity

The marginal on I_a is the DPP with kernel K[I_a], because its inclusion
probabilities are the corresponding principal minors. Inclusion
probabilities determine a finite subset law by inclusion-exclusion.
The product of these block marginals has inclusion probabilities
product_a det K[S intersect I_a]=det B[S], so it is P_B.

If P_K(X)>0, each block marginal at X intersect I_a is positive, so
P_B(X)>0. Consequently the classical relative entropy below is finite.
Expanding log P_B as a sum over blocks gives exactly

    D(P_K || P_B)
       = -H(K) + sum_a H(K[I_a])
       = H(B)-H(K).                                       (4)

Classical relative entropy is nonnegative: for positive P on its
support, Jensen's inequality for -log gives
sum P log(P/Q) >= -log(sum_{P>0} Q) >= 0.
Thus (4) already proves L(K)>=0.

## 3. A self-contained measurement relative-entropy inequality

This section proves the only quantum information inequality used below.
Let rho,sigma be positive definite density matrices on a finite Hilbert
space, and fix an orthonormal basis e_i. Set p_i=<e_i,rho e_i>,
q_i=<e_i,sigma e_i>, and E_i=|e_i><e_i|. Then

    sum_i p_i log(p_i/q_i)
       <= tr rho(log rho-log sigma).                      (5)

Here is a proof using elementary finite-dimensional functional calculus.
For a positive definite operator A and an isometry V, one has

    (V* A V)^(-1) <= V* A^(-1) V.                         (6)

Indeed set T=A^(1/2)V and S=A^(-1/2)V. Then T*S=I, and the orthogonal
projection P=T(T*T)^(-1)T* satisfies S*(I-P)S>=0. Expanding gives (6).
Apply (6) to A+sI and use

    -log x = integral_0^infinity [(x+s)^(-1)-(1+s)^(-1)] ds.

The scalar formula extends by spectral calculus; in finite dimension the
integrals converge in operator norm after the displayed subtraction.
Integrating the compressed inverse inequality gives

    -log(V* A V) <= V*(-log A)V.                          (7)

On the Hilbert space of matrices with inner product <X,Y>=tr X*Y,
let Delta(X)=sigma X rho^(-1). Left multiplication by sigma and right
multiplication by rho^(-1) are commuting positive definite operators,
so Delta is positive definite and

    log Delta(X) = (log sigma)X-X log rho.

Define the isometry V by V e_i=E_i sqrt(rho)/sqrt(p_i).
Its isometry property follows from E_i E_j=delta_ij E_i and
tr sqrt(rho)E_i sqrt(rho)=p_i. Directly,

    <V e_i, Delta V e_j>
      = tr[sqrt(rho) E_i sigma E_j sqrt(rho) rho^(-1)]
          /sqrt(p_i p_j)
      = delta_ij q_i/p_i.

For v=(sqrt(p_i))_i, Vv=sqrt(rho). Take its quadratic form in (7),
with A=Delta. The left side is sum_i p_i log(p_i/q_i). The right side is

    <sqrt(rho), -log Delta sqrt(rho)>
       = tr rho log rho-tr rho log sigma.

This proves (5), with no external data-processing lemma imported.

## 4. Finite exterior-algebra realization of the DPP

First suppose 0<K<I. Let F=direct_sum_{r=0}^n wedge^r C^n. For an
operator A define Gamma(A)=direct_sum_r wedge^r A, and put

    M=K(I-K)^(-1),    rho_K=det(I-K) Gamma(M).

Gamma(A C)=Gamma(A)Gamma(C); and tr Gamma(A)=det(I+A).
For the latter identity, both sides are the sum of principal minors of
A, by the definition of the exterior power in the coordinate wedge basis.
Since M>0, rho_K>0 and
tr rho_K=det(I-K)det(I+M)=1.

The coordinate wedge basis is indexed by subsets X. Its diagonal entry is

    <X,rho_K X> = det(I-K) det M[X].                       (8)

To check that this is precisely P_K, let Z=diag(z_1,...,z_n). The
probability generating polynomial of (8) is

    det(I-K) det(I+M Z) = det(I-K+K Z).                   (9)

In (9) the equality follows by multiplying I+MZ on the left by I-K.
Substitute Z=I+W, W=diag(w_i). The result is det(I+KW), whose coefficient
of product_{i in S} w_i is det K[S]. The same coefficient in
E product_{i in X}(1+w_i) is P(S subset X). This proves the claim.

Diagonalize K with eigenvalues lambda_i. In the corresponding exterior
basis rho_K has eigenvalues

    product_{i in X} lambda_i product_{i not in X}(1-lambda_i).

Therefore its von Neumann entropy is

    -tr rho_K log rho_K = sum_i h(lambda_i)=tr h(K).       (10)

For a Hermitian one-particle operator A, let dGamma(A) act on wedge^r
by summing A over the r tensor factors (and by zero on wedge^0). Then

    tr rho_K dGamma(A)=tr K A.                            (11)

To see this without a commutation assumption on A, use the eigenbasis
of K. The diagonal matrix element of dGamma(A) at subset X is
sum_{i in X} A_ii. Averaging over the product eigenvalue weights above
gives sum_i lambda_i A_ii=tr KA. Off-diagonal entries have zero trace.

For any strict contraction C, functional calculus in its eigenbasis gives

    log rho_C = tr log(I-C) I_F
              +dGamma(log C-log(I-C)).                   (12)

Use (10)-(12) with C=B. The strict-contraction property of K implies the
same property for each compression, and hence for B. We obtain

    D(rho_K || rho_B)
       = tr[K log K+(I-K)log(I-K)
            -K log B-(I-K)log(I-B)].                     (13)

For every function f(B) used here, f(B) is block diagonal. Since E has
zero diagonal blocks, tr E f(B)=0. In (13) this replaces K by B in both
cross terms, and hence

    D(rho_K || rho_B)=tr h(B)-tr h(K)=Q(K).               (14)

Occupation measurement in the coordinate wedge basis yields P_K,P_B
by (8)-(9). Apply (5), then (4) and (14), to get L(K)<=Q(K)
for strict contractions.

## 5. Boundary kernels and the universal inequality

For an arbitrary contraction K, take 0<epsilon<1/2 and set

    K_epsilon=(1-2epsilon)K+epsilon I,
    B_epsilon=(1-2epsilon)B+epsilon I.

These are strict contractions, and B_epsilon is the prescribed block
diagonal of K_epsilon. The law P_K(X) is continuous in K: explicitly,
inclusion-exclusion gives

    P_K(X)=sum_{T subset X^c} (-1)^|T| det K[X union T].

There are finitely many X, and -p log p is continuous on [0,1]. Thus
H(K_epsilon)->H(K) and H(B_epsilon)->H(B). Eigenvalues and h are
continuous, so the two spectral entropies also converge. Passing to the
limit in 0<=L(K_epsilon)<=Q(K_epsilon) proves (1) on its full domain.
This limiting step does not assume that rho_B is invertible at the limit.

## 6. The B-only spectral buffer and the quadratic bound

Now assume eta I<=B<=(1-eta)I. Formula (13), expressed purely with
one-particle matrices and 0 log 0=0, still equals Q(K): its cross terms
remain well-defined because B is strict. Let a_i in [0,1] and
b_j in [eta,1-eta] be the eigenvalues of K and B, with orthonormal
eigenvectors u_i,v_j; let w_ij=|<u_i,v_j>|^2. The rows and columns of w
sum to one. Expanding the trace yields

    Q(K)=sum_ij w_ij d(a_i || b_j),
    d(a||b)=a log(a/b)+(1-a)log((1-a)/(1-b)).              (15)

The scalar inequality log x<=x-1 gives, for 0<a<1 and 0<b<1,

    d(a||b)
      <= a(a/b-1)+(1-a)((1-a)/(1-b)-1)
      = (a-b)^2/[b(1-b)].                                (16)

Continuity extends (16) to a=0,1. Thus no buffer on K is introduced.
For each j, expanding E^2=(K-B)^2 in the B eigenvector v_j gives

    <v_j,E^2 v_j>=sum_i w_ij (a_i-b_j)^2.

Combine this with (15)-(16) to obtain Q(K)<=R(K). Finally
(B(I-B))^(-1)<=I/[eta(1-eta)] by scalar functional calculus.
Since E^2>=0, taking its trace pairing with this operator inequality
gives the final bound in (2). Although E^2 need not commute with that
inverse, the trace inequality is valid: tr U V>=0 whenever U,V>=0,
because tr U V=tr U^(1/2)V U^(1/2).

## 7. Jensen-gap transfer, with its asymmetric error

Block extraction is linear, so B_t=(1-t)B_0+tB_1. Substitute
H(K_r)=H(B_r)-L(K_r) directly into the definition of J_K:

    J_K=J_B-L(K_t)+(1-t)L(K_0)+tL(K_1).                  (17)

All three losses are nonnegative by (1). Their upper bounds C_r now
give both sides of (3). This includes t=0,1 and K_0=K_1, and requires
neither an entropy-concavity assertion nor a sign for the seed gap.
The loss at the mixture appears only in the lower error bound;
endpoint losses appear only in the upper error bound.

## 8. Explicit finite graph gluing: a dimension-accounted application

Take two genuine 2-by-2 seed kernels

    A_0=[[3/10,1/10],[1/10,3/10]],
    A_1=[[7/10,1/10],[1/10,7/10]],
    C  =[[0,1],[1,0]].

Their eigenvalues are (1/5,2/5) and (3/5,4/5). Every A_s on their
line segment has spectrum in [1/5,4/5]. Let G be any finite simple
undirected graph on m vertices with adjacency matrix T_G, e edges,
and maximum degree d. Put

    B_s=I_m tensor A_s,
    E=alpha T_G tensor C,
    K_s=B_s+E,                                          (18)

where alpha is real and |alpha| d<=1/5. Coordinates are partitioned
into the m vertex blocks of size 2. Since T_G has zero diagonal,
blockdiag(K_s)=B_s. The adjacency norm satisfies ||T_G||_op<=d:
for complex x, |x*T_G x|<=sum_{edges{u,v}}2|x_u||x_v|
<=sum_u deg(u)|x_u|^2<=d||x||^2. Therefore
||E||_op<=|alpha|d and 0<=K_s<=I. Equality in the feasibility bound
is allowed. The B-only buffer is eta=1/5, even if K_s hits a boundary.

Exact dimension/error accounting gives

    n=2m,  ||E||_F^2=alpha^2(2e)(2)=4e alpha^2,
    L(K_s)<=25e alpha^2.                                (19)

At s=0,1,1/2 the four seed probabilities, ordered as empty, first
singleton, second singleton, full, are respectively

    p=(12/25,11/50,11/50,2/25),
    p_reversed=(2/25,11/50,11/50,12/25),
    q=(6/25,13/50,13/50,6/25).

Hence the exact seed gap g=H(q)-H(p) has a short rational lower bound.
On the segment between p and q every coordinate is at most 12/25.
The Hessian of vector Shannon entropy is diag(-1/x_i), so Taylor's
formula with integral remainder gives

    H(q)-H(p)
      >= grad H(q) dot(q-p)+(25/24)||p-q||_2^2
      = -(2/25)log(13/12)+9/100
      >= -(2/25)(1/12)+9/100=1/12.                       (20)

The second inequality uses log(1+x)<=x. All probabilities here are
strictly positive, so the Hessian use introduces no endpoint problem.
Block additivity gives J_B=m g. Equations (3), (19), and (20) imply

    H(K_1/2)-(H(K_0)+H(K_1))/2
       >= m/12-25e alpha^2.                             (21)

For a path graph and alpha=3/100, e=m-1 and d<=2. Feasibility is
automatic, and (21) gives the strictly positive bound

    J_K >= m/12-9(m-1)/400=(73m+27)/1200 >0.             (22)

This family has nonzero off-block coupling for m>=2. More generally
(21) covers nonperiodic bounded-degree graphs whenever its right side
is positive and the stated feasibility bound holds. It computes only
the four-outcome seed law and graph parameters; enumerating the full
law would require 2^(2m) subsets. The Frobenius error is proportional
to the number of graph edges, and the positive seed gap is proportional
to m. No limiting or scalar-stationary interpretation is needed.

## 9. A boundary example explaining the buffer's role

For 0<epsilon<1, let K be the rank-one projection

    [[epsilon, sqrt(epsilon(1-epsilon))],
     [sqrt(epsilon(1-epsilon)), 1-epsilon]],

and use two singleton blocks. P_K is supported on the two singleton
subsets with probabilities epsilon,1-epsilon. Its block product is the
independent Bernoulli law with those two parameters. Thus

    L(K)=h(epsilon),    ||E||_F^2=2epsilon(1-epsilon).

Their ratio diverges as epsilon decreases to zero. Consequently no
constant independent of the buffer can replace 1/[eta(1-eta)] by a
universal constant in a Frobenius-squared bound over all contractions.
At epsilon=0, E=0 and (1) remains exact; the inverse expression (2)
is simply outside its stated domain. The example explains a quantitative
boundary limitation and does not contradict the unrestricted bound (1).

## 10. Dependencies, cost, and remaining certification

PROVED_HERE: block-product identity; measurement relative-entropy bound
via inverse compression; finite exterior-algebra DPP representation;
quasifree entropy and cross-entropy formulas; B-only quadratic estimate;
Jensen transfer; graph family and rational seed-gap lower certificate.

Elementary background used: the finite spectral theorem, determinants
and exterior powers, scalar log inequality, and finite-dimensional
calculus. All nontrivial interfaces between them are derived above.
No unproved DPP coupling lemma or entropy Hessian claim is used.

The exterior-algebra space has dimension 2^n only as a proof device.
Evaluating Q uses n-by-n Hermitian spectra; evaluating R uses n-by-n
matrix operations; the coarse bound uses a supplied buffer and a
Frobenius norm. H(B) is the sum of block entropies, so exact subset
enumeration, if used for its blocks, costs sum_a 2^|I_a| rather than 2^n.
Floating-point evaluations of these formulas are not automatically
rigorous numerical certificates. The rational example (20)-(22) does
not rely on a floating-point run.

These entropy and relative-entropy constructions belong to standard
finite quasifree-state theory. The reusable finite-block transfer
interface and demonstration are the intended output; no novelty claim
for a new information-theoretic inequality is made. Prior-art audit
and independent verification are separate responsibilities.

The author has supplied a complete candidate proof. The author has not
independently validated it. A fresh verifier must check this exact file
against the frozen statement, including sections 3, 5, 6, and 8.
