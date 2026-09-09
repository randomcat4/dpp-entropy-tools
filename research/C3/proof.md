# Product replacement and radial scalar entropy-rate concavity

Author candidate for frozen_statement_v2.md. This proof concerns the stated
radial family; it does not settle general scalar entropy-rate concavity.

## 1. A finite product-channel lemma

Let Omega=product_{i=1}^n Omega_i be a finite product, let pi=product_i pi_i
have strictly positive masses, and let mu be any probability law on Omega.
For each i, define the linear replacement operator E_i on laws by

    (E_i mu)(x)=pi_i(x_i) sum_{z_i in Omega_i} mu(x_{-i},z_i).

Thus E_i^2=E_i, E_iE_j=E_jE_i, and E_i pi=pi. For 0<=r_i<=1 define

    Q_i(r_i)=r_i Id+(1-r_i)E_i,
    nu_r=product_i Q_i(r_i) mu,
    F(r)=D(nu_r || pi).

For r in (0,1)^n every nu_r(x)>0: the all-replaced term is
product_i(1-r_i) pi(x)>0. All derivatives below are ordinary derivatives of
finite positive sums. The law is affine in each coordinate separately.

The idempotence and commutation give

    r_i partial_i nu_r = nu_r-E_i nu_r.                         (1)

Indeed, Q_i(r_i)-E_i=r_i(Id-E_i), while E_i Q_i(r_i)=E_i.
Since sum_x partial_i nu_r(x)=0, differentiating relative entropy gives

    r_i partial_i F
      = sum_x (nu_r-E_i nu_r)(x) log(nu_r(x)/pi(x)).            (2)

Set eta=E_i nu_r. The function log(eta/pi) depends only on x_{-i}, and nu_r
and eta have identical (-i) marginals. Therefore its integral against
nu_r-eta is exactly zero. Subtracting it in (2) proves

    r_i partial_i F = J(nu_r,eta),
    J(u,v)=D(u||v)+D(v||u)
          =sum_x (u(x)-v(x)) log(u(x)/v(x)).                   (3)

No assertion that mu or nu_r has marginals pi_i has been used.

For j!=i and 0<a<b<1, keep every other coordinate fixed. By idempotence,
Q_j(a)=Q_j(a/b)Q_j(b). Commutation then gives

    nu_{r_j=a}=Q_j(a/b)nu_{r_j=b},
    E_i nu_{r_j=a}=Q_j(a/b)E_i nu_{r_j=b}.                    (4)

The same Markov channel is applied to both arguments. Relative entropy
contracts under a Markov channel, in each direction, hence J at a is at
most J at b. For completeness this contraction follows from log-sum:
for each output y, sum_x u(x)Q(y|x) log[u(x)/v(x)] is at least
(Qu)(y) log[(Qu)(y)/(Qv)(y)]; summing y proves D(Qu||Qv)<=D(u||v).
Zero channel entries are omitted by continuity.

Consequently J is nondecreasing in r_j. Its differentiability and (3) imply

    partial_j partial_i F >=0,       i!=j.                   (5)

For i=j, separate affinity of nu gives the exact formula

    partial_i^2 F = sum_x (partial_i nu_r(x))^2/nu_r(x)>=0.  (6)

Thus every entry of the Hessian of F is nonnegative. This does NOT assert
that the Hessian is positive semidefinite for arbitrary signed directions.
For the simultaneous retention path r_1=...=r_n=t, (5)-(6) imply

    d^2/dt^2 F(t,...,t)=sum_{i,j} partial_i partial_j F>=0.   (7)

Finally, Shannon entropy satisfies

    H(nu_r)=-F(r)-sum_x nu_r(x)log pi(x).                    (8)

The i-th marginal of nu_r is r_i mu_i+(1-r_i)pi_i. Since log pi is the sum
of log pi_i, the last term in (8) is affine in the whole vector r. Hence
t -> H(nu_{(t,...,t)}) is concave for 0<t<1. Finite entropy is continuous
on the probability simplex, so this concavity extends to [0,1], including
arbitrary zero masses of the input mu.

## 2. Exact DPP identification

Let K be any finite Hermitian contraction and B=diag(b_i), 0<b_i<1.
Sample X with DPP kernel K. Independently at every site, retain X_i with
probability t, and otherwise replace it by a fresh Bernoulli(b_i), all
coins and replacement bits mutually independent and independent of X.
Let the resulting configuration be Y.

For every subset S, conditioning on which sites were retained yields

    E product_{i in S}Y_i
     =sum_{T subset S} t^{|T|}(1-t)^{|S|-|T|}
                         det K_T product_{i in S\T} b_i.   (9)

The determinant expansion for a matrix plus a diagonal matrix gives

    det[t K_S+(1-t)B_S]
     =sum_{T subset S} det(tK_T) product_{i in S\T}(1-t)b_i,

which equals (9). One can see this expansion directly by determinant
multilinearity, choosing either the diagonal term or the K column at each
site; a selected diagonal column forces its own row and leaves the principal
minor on the other sites. The empty determinant is one. Inclusion moments
determine a law on {0,1}^n by inclusion-exclusion. Therefore Y is exactly
the DPP with kernel B+t(K-B).

Section 1 with pi=product Bernoulli(b_i) now proves concavity of

    t -> H(B+t(K-B)),           0<=t<=1.                    (10)

This is an affine path in K. No line in L=K(I-K)^{-1} or in eigenvalues is
being substituted. K may fail to commute with B.

## 3. Entire feasible rays, including both signs

Fix B and A as in T-finite, and J={s:0<=B+sA<=I}. J is a closed convex
interval containing an open neighbourhood of zero, since B is strictly
between zero and I. If A=0, entropy is constant and the claim is immediate.
Otherwise choose any positive T in J. Apply (10) to K=B+TA and set t=s/T.
This proves concavity in s on [0,T]. Since T is arbitrary, it proves
concavity on the nonnegative part of J. Using any negative T in J gives
the same conclusion on [T,0].

It remains to justify joining the two halves. Every exact DPP event mass
is a polynomial in s. At s=0 it is the positive product mass

    product_{i:x_i=1} b_i product_{i:x_i=0}(1-b_i).

All masses stay positive in a neighbourhood of zero, and H is differentiable
there. Its one-sided derivatives at zero agree. A continuous function
concave on both halves, with left derivative at the join at least the right
derivative, is concave on their union. Here they are equal. To verify this
criterion directly, for x<0<y the left secant slope on [x,0] is at least
H'(0), and the right secant slope on [0,y] is at most H'(0). Thus these two
secant slopes occur in decreasing order; subdivision at zero and weighted
averaging gives the same decreasing-secant criterion for any crossing
triple. This is exactly the three-point characterization of concavity.

The finite proof therefore covers all of J. Feasible end kernels with
zero event masses were already included by continuity in (10). No assertion
of a finite derivative at a boundary is needed.

## 4. Passage to the actual stationary entropy rate

Fix p in (0,1) and bounded measurable real g. For every s in I from the
frozen statement, the function f_s=p+s g takes values in [0,1] almost
everywhere. For a finite vector v, the Fourier integral identity gives

    v* K_{f_s,n} v=integral f_s(theta)|sum_j v_j exp(-2pi i j theta)|^2 dtheta.

It lies between zero and ||v||^2, so every finite compression is a legal
Hermitian contraction. Its dependence is exactly

    K_{f_s,n}=p I_n+s A_n,

where A_n is the fixed compression associated with g. Section 3 applies,
including when integral(g)!=0, A_n is complex, or f_s touches 0 or 1.

Consequently for any fixed s_1,s_2 in I and alpha in [0,1],

    H_n(alpha s_1+(1-alpha)s_2)
       >=alpha H_n(s_1)+(1-alpha)H_n(s_2).                  (11)

For each fixed s, stationarity and Shannon subadditivity give
H_{m+n}(s)<=H_m(s)+H_n(s). Since 0<=H_n(s)<=n log2, the subadditive lemma
gives h(f_s)=lim_n H_n(s)/n=inf_n H_n(s)/n. Divide (11) by n and take the
three pointwise limits. This proves T-rate for all specified parameters.
Only three limits of numbers in an already proved inequality are used.
There is no interchange of derivatives, integrals, limits, or infima.

## 5. What this leaves open

The endpoint symbols must be on a common affine line through a constant
symbol. General f_- and f_+ need not satisfy that restriction. Nor is the
entrywise nonnegative Hessian in (5)-(6) a positive-semidefinite Hessian.
Signed, nonuniform parameter directions cannot be covered by that step.
Thus the proof provides a scoped family theorem and no answer to the full
Lyons–Steif conjecture. Mathematical novelty requires a separate audit.
