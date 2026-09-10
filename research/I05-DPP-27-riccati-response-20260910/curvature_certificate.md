# A finite-data, three-Poisson certificate for the TRUE rate curvature

Status: PROVED (AUTHOR PROOF), PENDING_REVIEW. This is a sufficient certificate theorem, not a claim that its numerical hypotheses have been certified for the whole interval. All notation and all constants are independently proved in proof.md.

## 1. Certificate statement

Fix any t in [1/2,3/2]. On the real symmetric correction-state ball B={||Q||_2<=1/8}, choose C2 trial functions u,v, a continuous trial w, and real constants c0,c1,c2. Define

    r0 = B_t-c0-(I-L_t)u,
    r1 = B_t' + L_t' u-c1-(I-L_t)v,
    A  = B_t'' + L_t'' u+2 L_t' v,
    r2 = A-c2-(I-L_t)w.                             (C1)

Assume verified bounds

    |r0|_1<=e01,  |r0|_2<=e02,
    |r1|_1<=e11,  ||r2||_infinity<=e20.              (C2)

Then the complete-configuration Shannon entropy rate per ORIGINAL coordinate satisfies

    |h''(t)-c2/2|
      <=13 e01+(1/8)e02+(6/5)e11+(1/2)e20.           (C3)

All constants are parameter-uniform. Thus interval-enclosed trial functions and (C2) on B times a parameter cell J prove a negative true-curvature cell if

    sup_J(c2/2)+13 e01+(1/8)e02+(6/5)e11+(1/2)e20<0. (C4)

A finite union of such J covering [1/2,3/2] without gaps would prove the whole requested positive-parameter interval. No such completed covering is claimed in this manuscript.

There is no invariant-measure derivative to approximate numerically in (C1)-(C4), no requirement that a finite transition matrix represent the DPP exactly, and no unquantified C_r-to-h'' limit. The trial functions may be finite polynomials; only finite-dimensional function data and explicit residual enclosures are required. A sampled residual is NOT (C2).

## 2. Proof, including all response errors

Let Rcal denote the centered resolvent in proof.md. Write exact solutions

    u*=Rcal B_t,
    v*=Rcal(B_t'+L'u*).

Since constants vanish under L' and L'', the errors, modulo additive constants, obey

    u*-u=Rcal r0,
    v*-v=Rcal r1+Rcal L' Rcal r0.                  (C5)

The exact second-response formula therefore gives

    2h''-eta A
      =eta L''Rcal r0+2eta L'Rcal r1
       +2eta L'Rcal L'Rcal r0.                     (C6)

This is where the invariant-measure response enters; it has not been discarded.

Set k=34/81, beta=4363/5184, R1=5184/821, b2=16399/2916, a=1/6, Ct=575/3072, Ctt=257/1536, and

    Z=(e02+b2 R1 e01)/(1-k^2).

The C1/C2 resolvent and operator estimates from proof.md give

    |h''-(eta A)/2|
      <=(1/2)[(Ctt R1+2Ct R1^2)e01
              +(a^2+2Ct R1*k*a)Z
              +2Ct R1 e11].                        (C7)

The exact coefficients after expanding Z are

    e01: 30801807981/2534394160 <13,
    e02: 8322993/71000080 <1/8,
    e11: 15525/13136 <6/5.                          (C8)

All three strict comparisons are tested with exact Fraction arithmetic in exact_checks.py. Finally invariance gives eta A-c2=eta r2, so its absolute value is at most e20. Equations (C7)-(C8) prove (C3).

The role of w is substantive: it replaces an expensive approximation of eta A by a pointwise, uniformly checkable Poisson defect. The residuals r0 and r1 need derivative-seminorm bounds, not value bounds. Arbitrary additive errors in c0 or c1 do not affect (C3).

## 3. Optional finite-state stationary approximation, with its own error

Without w, let pi be any probability measure supported at finitely many points of B. A genuine stationary approximation error can be certified by

    zeta>=W1(pi,pi L).

The contraction in proof.md implies W1(pi,eta)<=zeta/(1-beta). Therefore

    |h''-(pi A)/2|
      <=13 e01+(1/8)e02+(6/5)e11
        +(16/5)|A|_1 zeta.                         (C9)

Here (1/2)/(1-beta)=2592/821<16/5. In particular, for a projected transition matrix P on the chosen points, with transition projection error at most delta in mean Frobenius distance and an explicitly bounded total-variation stationarity defect tau=TV(pi,pi P),

    zeta<=delta+(3/8)tau.                           (C10)

Proof: couple each exact image T_alpha(Q_i) to its projected point, then couple the two finite probability vectors. This is an ACTUAL error for the continuous operator. It is not a statement that the finite chain is the DPP or a finite hidden-state representation.

(C9) can be expensive if one insists on a fine covering of the whole ball. The third Poisson equation (C1) avoids that potentially prohibitive W1 discretization requirement; this is why the polynomial scout uses three solves instead of only computing C_r.

## 4. Strong differentiability justification for the Poisson solutions

Here is a direct supplement to the second-order stationary perturbation argument. Fix a smooth observable F and anchor its Poisson solution U_t at Q=0 rather than centering it under eta_t. The two choices differ only by a constant. The uniform C1/C2 series bounds imply strong continuity of this anchored resolvent on C1 and C2 observables.

Subtracting the two anchored Poisson equations gives, modulo constants,

    U_s-U_t=Rcal_s[(L_s-L_t)U_t].

The right side divided by s-t converges in C1 to Rcal_t L'_t U_t: U_t is C2, L_s-L_t has the required C2-to-C1 difference quotient, and the resolvents are uniformly bounded and strongly continuous in C1. Thus the anchored U_t is differentiable in C1. For a t-dependent F_t, add F_t' inside the resolvent.

Now differentiate eta_t L'_t U_t. The moving observable L'_t U_t lies in C1; its C0 derivative is L''_t U_t+L'_t U'_t. The first-response identity, with U'_t=Rcal_t L'_t U_t modulo constants, proves the usual second-response formula with its factor 2. This proves an actual second derivative, not only a second-order Peano expansion. The argument applies to B_t because every g is bounded away from zero on a strict compact neighborhood. No differentiability theorem for finite HMMs is invoked.

## 5. How a finite implementation must apply the operators

All L_t' and L_t'' are partial derivatives of the OPERATOR while holding the trial observable fixed. If polynomial trial coefficients themselves depend on t, do NOT differentiate those coefficients inside L_t'u or L_t''u. An implementation can use separate t_map and t_coeff variables, differentiate in t_map, then set them equal. The derivative of the local entropy B_t is the ordinary fixed-Q derivative. This distinction is essential for (C1).

State derivatives use the Frobenius metric. For raw coordinates (x,y,z)=(Q11,Q22,Q12),

    |Dr|_F^2 = r_x^2+r_y^2+(1/2)r_z^2.

A safe squared Frobenius bound on the state-Hessian operator is

    r_xx^2+r_yy^2+(1/4)r_zz^2
      +2r_xy^2+r_xz^2+r_yz^2.

Thus rational squared-norm comparisons avoid inserting approximate square roots into a certificate. The ball can be represented semialgebraically by (1/8)I-Q>=0 and (1/8)I+Q>=0. An interval cover may discard an outside box only with an explicit exclusion proof; otherwise it must enclose the intersection with this domain. The global proven determinant/weight bounds can be intersected with interval bounds on that intersection.

Freeze decimal trial coefficients as exact rationals before verification. Use directed interval logarithms and all four branches. Arithmetic error is included in (C2) and the interval evaluation of c2. A finite grid maximum or finite-difference Hessian does not enclose the necessary supremum.

## 6. Executed scout, explicitly separated from a certificate

poisson_scout.py uses ordinary binary floating least squares to construct degree 6,8,10 polynomial trials at t=5/4. It has 1800 fitting points and 600 diagnostic points, fixed seed 270074, and diagnostic finite differences of step 1/2048 in an orthonormal symmetric-matrix basis. These operations are NOT outward enclosures.

The respective candidate c2/2 values are approximately -0.00333007665, -0.00333007551, -0.00333007753. Substitution of SAMPLED derivative residuals in the right side of (C3) yields approximately 0.00166733, 0.000159902, 0.00000993160. These last numbers are deliberately marked invalid_as_certificate_sampled_budget in the raw outputs. They are not error bars for h'', and the apparent separation does not prove even the single point.

The improved degree-10 residuals motivate a rigorous polynomial certificate, but the remaining gap is now concrete: enclose the four quantities in (C2) uniformly over B and the parameter cells, with enough separation in (C4). Full continuum certification is requested separately in issue74; it is not assumed to be running or to have succeeded.
