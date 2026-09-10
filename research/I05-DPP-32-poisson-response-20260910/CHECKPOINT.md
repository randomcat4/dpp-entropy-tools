# DPP32 checkpoint: the unresolved response is the parameter derivative of the entropy corrector

Status: AUTHOR_PROOF / PENDING_REVIEW. Date: 2026-09-10. This checkpoint is a successor to PR112 and inherits its fixed family and notation only as explicitly stated below. It does not upgrade PR112's arithmetic interval certificate, does not use the old |t-1|<=2^-27 claim, and does not assert the full [1/2,3/2] sign.

We work with the original complete-configuration Shannon entropy rate per original coordinate for

    f_t(theta)=1/2+cos(4*pi*theta)/4+t*cos(2*pi*theta)/8,

with the physical affine kernel path kept in t. Put s=t^2/256 only as the auxiliary lifted parameter. Let P_s be the full four-branch probability operator, B_s its complete-cell entropy observable, eta_s its invariant law, and Phi_s any C^1 Poisson corrector solving

    (I-P_s) Phi_s = B_s - c_s,        c_s=2 h(s).

All derivatives below hold the test observable fixed inside partial_s P_s, exactly as in PR91/PR112.

## Theorem 1: exact identification of the second unresolved Poisson observable

Define

    C_s := partial_s B_s + (partial_s P_s) Phi_s.

Differentiating the Poisson equation gives

    (I-P_s) partial_s Phi_s = C_s - partial_s c_s.      (1)

Applying eta_s to the definition and using eta_s(I-P_s)=0 gives

    eta_s C_s = partial_s c_s = 2 partial_s h.          (2)

Therefore, for the centered resolvent R_s=(I-P_s)^(-1) on zero-mean observables,

    V_s := R_s C_s

as used in PR112 is exactly the centered class of partial_s Phi_s:

    V_s = partial_s Phi_s  modulo constants.            (3)

Since partial_s P_s annihilates constants, the remaining response scalar is normalization-independent:

    eta_s (partial_s P_s) V_s
      = eta_s (partial_s P_s)(partial_s Phi_s).          (4)

Proof: (1) is ordinary differentiation of (I-P_s)Phi_s=B_s-c_s. Equation (2) follows by eta_s. The centered inverse applied to (1) yields (3), and partial_s P_s 1=partial_s(P_s1)=0 yields (4).

This is entropy-specific because Phi_s is the entropy-excess Poisson corrector; it is not a generic contraction statement.

## Theorem 2: exact collapse of PR112's two-term Gamma decomposition

PR112 writes

    Gamma(t)= eta_s(partial_s P_s)Phi_s/256
              +(t^2/16384) eta_s(partial_s P_s)V_s.

Its displayed curvature identity is

    h_tt = eta_s partial_s B_s/256
           -(t^2/32768) eta_s(I_s+K_s)
           +Gamma(t).

Using (2), the acceleration piece and the first Gamma term combine exactly:

    [eta_s partial_s B_s + eta_s(partial_s P_s)Phi_s]/256
      = (partial_s c_s)/256
      = (partial_s h)/128.                              (5)

Using (3)-(4), the full physical curvature becomes

    h_tt = (partial_s h)/128
           +(t^2/16384) [ eta_s(partial_s P_s)(partial_s Phi_s)
                           -(1/2) eta_s(I_s+K_s) ].       (6)

Equivalently the auxiliary curvature is exactly

    partial_s^2 h
      = eta_s(partial_s P_s)(partial_s Phi_s)
        -(1/2) eta_s(I_s+K_s).                           (7)

No Fisher, state-motion, invariant-law response, or t-to-s acceleration term is dropped: (6) is just a reorganization of PR112's full formula.

## Theorem 3: the unresolved scalar is exactly parity mutual-information curvature

Let mu_s be the stationary complete-configuration DPP law for the same symbol, with s=t^2/256. At s=0 the nearest-neighbor Fourier mode vanishes, so the Toeplitz kernel splits into the even and odd coordinate blocks while each block marginal is unchanged from mu_s. The already accepted cyclic block-decoupling identity (q=2) therefore gives, first on every finite coordinate window and then per original coordinate,

    D_rate(mu_s || mu_0) = h(0)-h(s).                  (8)

Equivalently this is the mutual-information rate between the even and odd coordinate sub-processes. Define

    D(s):=D_rate(mu_s || mu_0)=h(0)-h(s).

Combining (7) with D''=-h_ss gives the exact identity

    D''(s)
      = (1/2) eta_s(I_s+K_s)
        - eta_s(partial_s P_s)(partial_s Phi_s).        (9)

Thus the remaining PR112 response inequality

    eta_s(partial_s P_s)(partial_s Phi_s)
      <= (1/2) eta_s(I_s+K_s)                           (10)

is neither a generic cone-monotonicity assertion nor an arbitrary Poisson estimate: it is EXACTLY convexity of the parity mutual-information rate in the squared coupling s.

Moreover D(0)=0 and D(s)>=0 by relative entropy. Hence if D is convex on [0,S], then 0 is a global minimum on that interval and D'(s)>=0 for every s>0. With h_s=-D' and h_ss=-D'', equation (6) becomes

    h_tt = -D'(s)/128 - (t^2/16384) D''(s).            (11)

Therefore convexity of D(s) alone on [0,S] implies physical affine-t concavity for every positive t with t^2/256 in [0,S]. A strict positive lower bound on either D' or D'' gives strict physical curvature. In particular, proving mutual-information convexity on s in [1/1024,9/1024] would close the entire requested t in [1/2,3/2] interval without any sign claim for a generic concave observable.

Proof of (8): for a finite window, deleting all odd-even kernel entries leaves exactly the product of the true parity-block marginals, and for this family that deleted kernel is the t=0 compression. The standard block-decoupling identity gives H(mu_0,n)-H(mu_s,n)=D(mu_s,n||mu_0,n). Divide by n and use the stationary entropy-rate limit. Equations (9)-(11) are algebraic consequences of (7) and s=t^2/256.

## Precise remaining obstruction

The macroscopic sign problem has therefore collapsed to one entropy-specific global question:

    Is the parity mutual-information rate D(s) convex in squared nearest-neighbor coupling s?

Strong state concavity of Phi_s alone gives no sign for the equivalent bilinear term in (9), and the already-published concave-observable counterexample to monotonicity of partial_s P_s cannot be applied as an entropy counterexample. Conversely, a proof of D''>=0 would simultaneously control the formerly separate acceleration sign, because D>=0 and D(0)=0 force D'>=0 under convexity.

The accepted cyclic theorem also supplies the value bound D(s)>=s^2 for this family (the removed Fourier coefficient has magnitude |hat f_t(1)|=|t|/16, so |hat f_t(1)|^4=s^2). This certifies a nontrivial mutual-information gap but, by itself, does not imply D''(s)>=0 away from zero; differentiating a value inequality is invalid.

No finite sample, generic operator contraction, or old narrow-interval claim is used here. The next theoretical target is a complete-word relative-entropy/Fisher representation that can prove or disprove convexity of D(s) itself.
