# Fixed-symbol value bridge (author proof)

All logarithms are natural. Fix one measurable E in T=R/Z, rho=|E|, Q_n=T_n(1_E), and K_n=a I+c Q_n, where 0<=c<=1 and 0<=a<=1-c. H_n is the Shannon entropy of the complete DPP law on [0,n-1]; h=lim H_n/n. Put b(x)=-x log x-(1-x)log(1-x), S_n=Tr b(K_n), and s=(1-rho)b(a)+rho b(a+c).

S_n is NOT H_n. It is the entropy of the gauge-invariant quasi-free state with one-particle covariance K_n.

## 1. Complete-event convention

For a word x, with zero coordinates Z_x, its probability is

    p_x=(-1)^|Z_x| det(K_n-I_Zx).

In the strict domain 0<a<a+c<1, all atoms are positive. If B_x=K_n-I_Zx, then

    p'_x=p_x Tr(B_x^-1),
    p''_x=p_x[(Tr B_x^-1)^2-Tr B_x^-2],
    H_n''=-sum_x (p'_x)^2/p_x -sum_x p''_x log p_x.

The derivatives here are with respect to a at fixed c,E. Storing the Taylor jet (p,p',p''/2) requires multiplying the third coefficient by two. For t=a/(1-c), H_tt=(1-c)^2 H_aa. The inclusion probability det(K_A) cannot replace p_x.

## 2. A difference of entropies is superadditive

The fixed occupation-number measurement of the finite quasi-free state has inclusion moments det(K_A), hence exactly the complete DPP law. On adjacent blocks A,B, apply the two local occupation measurements to the state and to the product of its marginals. Quantum relative-entropy data processing gives

    I_classical(A;B)<=I_quantum(A;B).

The tensor-product identification uses the Fock decomposition for contiguous mode blocks; the gauge-invariant states are even, so the reduced covariances are the indicated principal submatrices. No arbitrary nonlocal occupation measurement is substituted.

Consequently D_n=H_n-S_n obeys D_(m+n)>=D_m+D_n. Once S_n/n->s, Fekete's lemma gives D_n/n<=h-s. Subadditivity of H_n gives H_n/n>=h. Thus

    0<=H_n/n-h<=epsilon_n:=S_n/n-s.             (1)

Stationarity also gives q_n=H_n-H_(n-1) decreasing to h and q_n<=H_n/n, so

    0<=q_n-h<=epsilon_n.                       (2)

This is an averaged conditional-entropy value tail, not a per-history predictor bound or a derivative tail.

## 3. The spectral boundary error vanishes uniformly in a,c

For lambda in [0,1], let B be Ber(lambda) and, conditionally, Y be Ber(a+cB). Then

    g(lambda)=b(a+c lambda)-(1-lambda)b(a)-lambda b(a+c)=I(B;Y).

For c<1 the same channel is realized by an independent selector Z~Ber(c): output B if Z=1; otherwise output an independent Ber(a/(1-c)). Revealing Z proves 0<=g(lambda)<=c b(lambda). The c=1 and c=0 cases follow directly or by continuity. Since Tr Q_n=n rho,

    0<=epsilon_n<=c Tr b(Q_n)/n.               (3)

Let V_n=Tr Q_n(I-Q_n). Parseval gives the exact identity

    V_n=2 sum_(r>=1) min(r,n)|qhat(r)|^2,
    qhat(r)=integral_E exp(-2 pi i r theta)dtheta.

For every eigenvalue lambda_i of Q_n, w_i=min(lambda_i,1-lambda_i)<=2lambda_i(1-lambda_i). Concavity and monotonicity of b on [0,1/2] imply

    Tr b(Q_n)/n<=b(min(1/2,2V_n/n)).            (4)

By dominated convergence and Parseval, V_n/n->0 for every measurable E. Equations (3)-(4) therefore also prove S_n/n->s, completing Section 2 without assuming a differentiated Szego expansion. The convergence bound is uniform over the closed legal a,c domain for this fixed E, not uniform over all varying E.

If E is a union of J intervals, |qhat(r)|<=J/(pi |r|) for r!=0. Hence, for every n>=1,

    V_n<=(2J^2/pi^2)(harmonic(n)+1),
    epsilon_n<=c b(min(1/2,4J^2(harmonic(n)+1)/(pi^2 n))).    (5)

This is O_J((log n)^2/n) and does not blow up as a approaches a legal endpoint or c approaches 1. It does not imply convergence of second derivatives.

## 4. Correct-direction true-rate Jensen certificate

Freeze a,d,c,E with a-d>=0 and a+d+c<=1. Define

    J=h(a)-[h(a-d)+h(a+d)]/2,
    J_n=H_n(a)/n-[H_n(a-d)+H_n(a+d)]/(2n).

Applying (1) separately at these three points yields

    J_n-epsilon_n(a)<=J<=J_n+[epsilon_n(a-d)+epsilon_n(a+d)]/2.  (6)

A strictly negative upper bound proves a genuine fixed-process counterexample without needing existence of h''. A positive lower bound proves only this chord, not full local or global concavity.

One may strengthen the node intervals to

    L_n=max(s,H_n/n-epsilon_n), U_n=q_n,

then take the maximum of available lower bounds and the minimum of available upper bounds across n. Interval arithmetic must round each endpoint outward. It is invalid to divide a finite curvature error by d^2 without also dividing the value-tail budget.

## 5. Safe and unsafe symmetries

E->E+theta0 is a diagonal phase gauge; E->-E conjugates the kernel. Particle-hole symmetry is h_E(a,c)=h_(E^c)(1-c-a,c), so complement reduction must reflect a. For E^(q)={theta:q theta mod 1 in E}, the process decomposes into q independent interlaced copies and h_(E^(q))=h_E per original coordinate.

A fixed cycle mask S in Z_m may seed the fixed continuous set E_(m,S)=union_(s in S)[s/m,(s+1)/m). Its Fourier coefficient equals

    exp(-pi i r/m) sinc(pi r/m) (1/m)sum_(s in S)exp(-2 pi i r s/m).

The sinc factor cannot be discarded. Cycle modular multiplication can permute cycle coordinates but is not a general equivalence of these continuous lifts. The set E must remain fixed when n increases.

If 0<|E|<1, then 0<Q_n<I at every finite n: a nonzero trigonometric polynomial cannot vanish on a set of positive measure. Thus these finite blocks still have full support at a=0,c=1, unlike a finite cyclic projection with fixed-cardinality support. For E=[1/4,3/4], the test polynomial ((1+z)/2)^(n-1) proves lambda_min(Q_n)<=(2n-1)2^-n. A finite-dimensional endpoint argument therefore needs its own volume-uniform remainder.

## 6. Primary tools and scope

B. Dierckx, M. Fannes, M. Pogorzelska, Fermionic Quasi-free States and Maps in Information Theory, arXiv:0709.1061, J. Math. Phys. 49, 032109 (2008): the quasi-free entropy and covariance formalism. https://arxiv.org/abs/0709.1061

R. Lyons and J. E. Steif, Stationary Determinantal Processes: Phase Multiplicity, Bernoullicity, Entropy, and Domination, arXiv:math/0204324v5, Duke Math. J. 120 (2003), 515-575: stationary DPP framework and entropy-rate context. https://arxiv.org/abs/math/0204324

Quantum relative-entropy data processing is used as a standard theorem. The inequalities above are proved here from that theorem; neither source is represented as an independent review of this packet. Novelty is not established. The high-contrast universal sign and a true-rate counterexample remain INCOMPLETE.
