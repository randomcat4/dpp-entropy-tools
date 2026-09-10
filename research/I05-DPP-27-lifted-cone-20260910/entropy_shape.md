# Entropy-specific sign beyond the abstract concavity cone

Status: PROVED (AUTHOR PROOF), PENDING_REVIEW. This was derived after the initial determinant-lift checkpoint. It does not assert that the remaining mixed response has a favorable sign. It keeps the original symbol, t in [1/2,3/2], s=t^2/256 and b=1/8. The full physical response is always restored from the auxiliary s parameter, including its acceleration.

## 1. A narrower invariant shape for actual states

Let Q be a real symmetric physical correction state, q=t/16, and consider

 ||Q||_2<=1/8,   |Q12|<=3q/4.                        (1)

The no-future seed Q=0 satisfies (1). The ball is invariant by the PR91 analytic construction. We now prove that the extra off-diagonal condition is invariant as well, without a box enumeration.

Set F=D_ac-Q and R=F^(-1). On the ball, the smallest singular value of F is at least 9/32, so ||R||_2<=32/9. Its diagonal entries have modulus at least 3/8, and (1) gives |F12|<=7q/4. Thus

 |det F| >=(3/8)^2-(7q/4)^2
           >=1863/16384,
 |R12| <= (7q/4)*(16384/1863).

The next correction has

 T12=b*q*R11+b^2*R12.

Consequently

 |T12|/q <=4/9+448/1863=1276/1863<3/4,               (2)

where the last exact positive cross-multiplication gap is 5589-5104=485. The estimate applies to every sign branch, not just a typical word. Induction and closure prove (1) for every finite complete-cell future and the true infinite reachable attractor.

The result is not asserted for every point of the larger lifted convex hull: convex mixtures of physical lifts need not themselves be physical lifts. The invariant probability law is supported on actual physical lifts, which is exactly where the following entropy sign is used.

## 2. The entropy derivative is a negative log odds ratio

Write Q=[[x,z],[z,y]], r=q*z, d=det Q. The four complete cell probabilities in lifted coordinates are

 g_ac=1/4-c*x/2-a*y/2+a*c*(d+2r-s).

At fixed lifted state Z=(x,y,r,d), partial_s g_ac=-a*c, and therefore the exact local entropy derivative is

 partial_s B_s(Z)
 =log[(g_++*g_--)/(g_+-*g_-+)].                       (3)

For a physical lift, the complete 2 by 2 probability table has determinant

 g_++*g_---g_+-*g_-+=-(q-z)^2.                        (4)

This is the complete table identity, not a substitution of an inclusion minor for a full event. Equation (1) gives q-z>=q/4>0.

We can make the sign uniform. Since d>=-1/64 and r>=-3s/4,

 g_+-+g_-+=1/2-2(d+2r-s)
             <=1/2+1/32+5s<=589/1024.

Thus

 g_+-*g_-+ <=(589/2048)^2<1/12,

because 12*589^2=4163052<4194304. Combining (3)-(4) with log(1-u)<=-u gives, on the actual reachable attractor,

 partial_s B_s(Z)<-12(q-z)^2<=-3s/4.                 (5)

This is an entropy-shape sign, stronger than saying a generic test function is concave. It holds simultaneously for every t in [1/2,3/2]. It is a PARTIAL derivative at fixed lifted state, not by itself the total derivative of the stationary entropy rate.

## 3. A second signed term and its fixed lower budget

Because g_ac is affine in s,

 -partial_s^2 B_s=sum_ac 1/g_ac>=16.                 (6)

All four probabilities occur in (6). This is the fixed-lift Fisher component of the full response, not a relabeling of it as the entire moving-state Fisher rate.

Let Phi_s be the strongly concave entropy-excess Poisson function proved in lifted_cone.md. Its state Hessian satisfies -D^2 Phi_s>=I/8. The fourth output coordinate of the lifted fractional map is

 (F_ac,s)_d=a*c*b^4/g_ac,s.

At fixed Z its derivative is b^4/g_ac,s^2. Thus, writing

 K_s(Z)=sum_ac g_ac[-D^2 Phi_s(F_ac)]
                         [partial_s F_ac,partial_s F_ac],

we obtain

 K_s >=(b^8/8)sum_ac g_ac^(-3)
      >=(b^8/8)*256=1/524288.                        (7)

The first inequality uses the determinant-output coordinate only to LOWER-bound a sum of nonnegative quadratic terms; the complete exact quadratic form is retained in the response formula. No positive acceleration term is removed.

## 4. Uniform true-rate inequality with the exact remaining term

Let P_s be the full lifted weighted operator and eta_s its true invariant law. Put

 C_s^obs=partial_s B_s+(partial_s P_s)Phi_s,
 V_s=R_s C_s^obs,
 Gamma(t)=[eta_s(partial_s P_s)Phi_s]/256
          +(t^2/16384)*eta_s(partial_s P_s)V_s.      (8)

The centered resolvent R_s and every operator derivative are understood in the full response sense explained in PR91 and lifted_cone.md: test functions are held fixed inside operator derivatives, while their state evaluations move. Both occurrences in Gamma are retained.

The exact physical response is

 h_tt=[eta_s partial_s B_s]/256
       -(t^2/32768)*eta_s(I_s+K_s)+Gamma(t),          (9)
 I_s=sum_ac 1/g_ac.

Here the coefficient 1/256 is one half of s''(t)=1/128, and the other coefficient is one half of s'(t)^2=t^2/16384. Applying (5)-(7) to (9) proves the explicit continuous-parameter inequality

 h''(t)<Gamma(t)-131*t^2/262144-t^2/17179869184,
                                  1/2<=t<=3/2.     (10)

The negative budget contains three separately justified pieces: the negative entropy log odds, the fixed-lift Fisher component, and the negative state-Hessian perspective term. This is a theorem about the full true-rate response, not a finite window or a branch-contraction implication.

Equation (10) does NOT close the full sign because Gamma(t) has not been signed or bounded sharply enough. Gamma is an explicit two-term stationary Poisson observable, not an unspecified constant or omitted remainder. The rational concave-observable counterexample in lifted_cone.md shows why abstract cone preservation alone cannot justify declaring its first-operator-derivative factors nonpositive. That counterexample does not settle the sign for the particular entropy corrector Phi_s or V_s.

## 5. Scope and next distinction

The state-cone theorem, the log-odds sign and (10) hold throughout the original target interval. A separate appendix explicit_rate_interval.md proves the much smaller but actual physical interval |t-1|<=2^(-27), with h''<-1/2000, using the accepted PR77 anchor and a fully explicit analytic third-derivative bound. The narrow interval is not claimed as a solution of the macroscopic problem.

For a materially wider interval, the original degree10 polynomials restored in PR98 remain possible trial functions, but their sampled residuals are still non-certifying. No new run, current executor claim, independent acceptance or novel-priority claim is inferred from this manuscript.
