# DPP32: explicit Neumann-tail bridge for the true curvature

Status: AUTHOR_PROOF / PENDING_REVIEW. Date: 2026-09-10.

This note replaces any use of the qualitative sentence "PR91 spectral gap implies a uniform second-parameter boundary constant" as a black box. PR91 actually proves, on the fixed correction-state ball B, C1/C2 state-seminorm contraction and fixed-observable first/second parameter response. The construction below stays inside those proved spaces. It does not use PR112's wide interval computation, the failed S3 production source, or any finite-HMM assumption.

All complete-event probabilities, all branches, state motion, Fisher terms, acceleration terms, and invariant-law response remain in the underlying PR91 second-response identity. The physical kernel path is affine in t. We do not infer an s-derivative estimate by differentiating a value bound.

## 1. Constants actually supplied by PR91

Use the sharpened PR91 constants

    beta = 2/3,
    gamma = 19/25,
    Cgrad = 17618609/99532800,

where, for a C2 observable A on the fixed state ball,

    |L A|_1 <= beta |A|_1,
    |L A|_2 <= gamma |A|_2,
    |L' A|_1 <= Cgrad |A|_2.

The second and third statements use the affine cancellation L_t Q=0 and are state-seminorm statements. They are not a spectral-gap assertion for arbitrary parameter-dependent observables.

Let epsilon=81/1024 be the uniform complete-branch probability lower bound. From the exact four-branch weight formulas and their PR91 state derivative bounds,

    sum_alpha |D g_alpha[U]| <= 2,
    sum_alpha |D^2 g_alpha[U,V]| <= 4,
    sum_alpha |D g_{alpha,t}[U]| <= 3/8,
    sum_alpha |g_{alpha,t}| <= 7/64,

for unit Frobenius state directions U,V. Put ell=log(1024/81). Since sum Dg=sum D2g=sum g_t=sum Dg_t=0, the complete-cell Shannon observable B=-sum g log g obeys

    |B|_1 <= 2 ell,                                      (1)
    |B|_2 <= 4/epsilon + 4 ell,                          (2)
    |B_t'|_1 <= (3/8)ell + (7/64)/epsilon.              (3)

For a purely rational verification one may use ell<127/50, hence

    b1 := 127/25,
    b2 := 4096/81 + 254/25,
    bt1:= 381/400 + 112/81                              (4)

as valid upper bounds for (1)-(3).

## 2. Canonical finite Neumann trials

For an integer m>=1 define the finite first Poisson trial

    u_m = sum_{j=0}^{m-1} L^j B.

Choose c0 arbitrarily. Then

    r0 = B-c0-(I-L)u_m = L^m B-c0.

Constants disappear from state seminorms, so PR91 gives the explicit tail estimates

    e01(m) := beta^m b1,
    e02(m) := gamma^m b2,                               (5)

with

    |r0|_1 <= e01(m),
    |r0|_2 <= e02(m).

Moreover

    |u_m|_2 <= b2 (1-gamma^m)/(1-gamma).               (6)

Now put

    F_m := B_t' + L_t' u_m,
    v_m := sum_{j=0}^{m-1} L^j F_m.

Choose c1 arbitrarily. Exactly as above,

    r1 = B_t' + L_t' u_m-c1-(I-L)v_m = L^m F_m-c1.

Using only the proved C2-to-C1 bound for L', not any C3 resolvent claim,

    |F_m|_1
      <= bt1 + Cgrad*b2*(1-gamma^m)/(1-gamma),

and therefore

    e11(m) := beta^m [bt1 + Cgrad*b2*(1-gamma^m)/(1-gamma)]             (7)

satisfies

    |r1|_1 <= e11(m).

Equations (5)-(7) are analytic, parameter-uniform, and require no state-space covering.

## 3. Quantitative size of the already-closed two response tails

Substituting (5)-(7) into the sharpened mixed PR91 true-curvature gate

    |h_tt-c2/2|
      <= 3 e01 + e02/15 + (11/20)e11 + e20/2           (8)

shows that the contribution of r0 and r1 alone is bounded by

    E12(m)=3e01(m)+e02(m)/15+(11/20)e11(m).             (9)

With the rational bounds (4), direct rational evaluation gives

    E12(32) < 0.000717,
    E12(36) < 0.000227,
    E12(40) < 0.000073.                                (10)

The decimal displays are not certificate inputs; each inequality follows from the exact rational expression in (9). In particular m=40 already makes the two nested response-tail budgets much smaller than the approximately 10^-3 physical-curvature scale seen in prior non-certifying scouts, without reusing any scout value as evidence.

## 4. The one remaining finite-dimensional gate

Define the finite second-response observable built from the canonical trials

    A_m = B_t'' + L_t'' u_m + 2 L_t' v_m.              (11)

At this point PR91 does NOT supply a theorem of the form |L''A|_1<=C|A|_2, so we do not invent one. Instead choose an integer r>=1 and the finite third Poisson trial

    w_{m,r}=sum_{j=0}^{r-1}L^j A_m,
    c2_{m,r}(t)=(L^r A_m)(0).                           (12)

Then the third residual is exactly

    r2 = A_m-c2_{m,r}-(I-L)w_{m,r}
       = L^r A_m-(L^r A_m)(0).                         (13)

Consequently it is enough to verify one finite-dimensional state-gradient enclosure

    G_m(J) >= sup_{t in J,Q in B} |D_Q A_m(t,Q)|.       (14)

The law-level C1 contraction gives

    e20(m,r;J)
      <= diam(B) beta^r G_m(J)
      <= (3/8) beta^r G_m(J).                          (15)

Combining (8)-(15) yields the explicit macro bridge:

    sup_{t in J} c2_{m,r}(t)/2
      + E12(m)
      + (3/16) beta^r G_m(J) < 0                       (16)

implies

    h_tt(t)<0  for every t in J.                        (17)

This is a sufficient true-rate statement, not a finite-window extrapolation. The quantity c2_{m,r} is a finite complete-event expectation generated by the exact four-branch operator, and G_m is a finite-dimensional supremum on the same three-dimensional state ball times one parameter interval. There is no invariant-law derivative to approximate numerically.

The bridge is intentionally asymmetric: all long-memory errors are already disposed of analytically by (10); only the local finite function A_m needs an interval enclosure. Thus a verifier need not solve three global Poisson residual problems. For m=40, the first two residual layers cost less than 7.3e-5 before the third-tail term.

## 5. Relation to the s=t^2/256 formulation

No s-second derivative is bounded here by converting a generic t-bound through factors 16384/t^2 and 16384/t^3. The bridge closes the physical affine-t curvature directly. If one instead needs parity-information convexity D''(s), a separate s-response certificate must be built; (16) by itself proves physical h_tt<0, which is the macroscopic target but is logically weaker than D''(s)>=0.

This distinction is important because a possibly negative D''(s) need not contradict physical concavity once the acceleration term involving D'(s) is retained.

## 6. Review and computation boundary

Everything in this note is AUTHOR_PROOF / PENDING_REVIEW. Equations (1)-(9) are deductions from the explicit PR91 complete-event operator bounds; (12)-(16) are algebraic finite-Neumann identities plus the stated C1 contraction. No PR112 wide-interval arithmetic result is used. No >60-minute computation is started or claimed here. A future interval execution longer than 60 minutes must receive its own explicit local contract and cannot reuse an older issue74 budget.
