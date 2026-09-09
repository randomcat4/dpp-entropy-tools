STATUS: CORRECT

Audited frozen author commit: 509ac053b49e61c4de8112a424578a5affa61f57

Input file SHA256:

- frozen_statement_v2.md: 21A913E9DCE7A11AD8E3ACF1E58ED7749766DE2756E40F010F00B8281DA63D81
- proof.md: 13059981CFD99C9A32D20B6E2DD0EF7D89C81E7E0215F8D7E30E6F1057BAC4FF
- hazards.md: 27B7708219C71F1EB754A7B40C89299C10246F32D097620013CD98BEA59DD58B

JUSTIFICATION:

1. Product replacement identity is valid at proof.md lines 24-40. The step from
   line 31 to lines 38-40 subtracts log(eta/pi), where eta=E_i nu_r. Since
   eta/pi depends only on x_{-i} and nu_r, eta have the same x_{-i} marginal,
   the subtracted integral is zero. This does not assume that the input law or
   nu_r has one-site marginals pi_i; it uses only the product form of pi and
   the definition of E_i.

2. The mixed derivative sign is justified at proof.md lines 44-59. For j != i,
   Q_j(a)=Q_j(a/b)Q_j(b), and E_i commutes with Q_j, so the same Markov channel
   acts on both nu_r and E_i nu_r. KL contracts in both directions under that
   same channel, so the Jeffreys divergence is nondecreasing in r_j. Together
   with r_i partial_i F=J and r_i>0, this gives partial_j partial_i F>=0.

3. The proof does not convert entrywise Hessian signs into a PSD claim. Lines
   61-69 use the diagonal second derivative formula and the nonnegative mixed
   entries only along the simultaneous positive direction r_1=...=r_n=t, where
   d^2 F/dt^2 is the sum of all entries. Lines 65-66 explicitly exclude the
   arbitrary signed-direction interpretation.

4. The passage from relative entropy convexity to Shannon entropy concavity is
   complete at proof.md lines 71-79. The correction term is affine because
   log pi is a sum of one-coordinate functions and the i-th marginal of nu_r is
   r_i mu_i+(1-r_i)pi_i. Continuity of finite entropy covers endpoint zero
   masses without differentiating them.

5. The DPP identification at proof.md lines 83-105 uses finite event laws.
   Independent retain-or-replace gives the inclusion moments in line 91-93,
   and the determinant expansion of tK_S+(1-t)B_S at lines 95-103 matches
   those moments. Inclusion-exclusion then determines the full binary law, so
   the product channel produces exactly B+t(K-B).

6. Entire finite feasible rays, including negative parameters and endpoints,
   are covered at proof.md lines 116-141. Each half-ray is obtained by choosing
   an arbitrary feasible T of the relevant sign and applying the [0,1] radial
   result to K=B+TA. At s=0 all event masses equal the strictly positive
   product mass in line 127, so H is differentiable near zero and the one-sided
   derivatives agree. The decreasing-secant argument in lines 131-137 correctly
   joins the two concave halves. Feasible boundary kernels are included by
   finite entropy continuity, not by boundary differentiation.

7. The scalar stationary entropy-rate argument at proof.md lines 145-169 proves
   the frozen T-rate statement. For each bounded measurable real g and feasible
   s, the finite Toeplitz compression is a Hermitian contraction by the Fourier
   quadratic form in lines 147-152, and depends affinely on s as pI_n+sA_n.
   Thus the finite Jensen inequality holds for every n. Stationarity and
   Shannon subadditivity give the pointwise limit H_n(s)/n -> h(f_s); dividing
   the finite Jensen inequality by n and taking the three fixed limits proves
   concavity of h without differentiating h, interchanging limits with
   derivatives, or assuming smoothness, zero mean, finite bandwidth, or a
   uniform boundary margin.

No critical gap was found relative to frozen_statement_v2.md. This audit does
not assess novelty, which the frozen statement itself marks as unconfirmed.
