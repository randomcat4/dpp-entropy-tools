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

## Precise remaining obstruction

The macroscopic sign problem is thus reduced to two scalar entropy-specific questions, not to generic state concavity:

1. control partial_s h (the physical acceleration contribution in t);
2. control the bilinear information-response term

       J_s := eta_s(partial_s P_s)(partial_s Phi_s)

   against (1/2) eta_s(I_s+K_s).

Strong state concavity of Phi_s alone gives no sign for J_s, and the already-published concave-observable counterexample to monotonicity of partial_s P_s cannot be applied as an entropy counterexample. Conversely, any proof that

    J_s <= (1/2) eta_s(I_s+K_s)

throughout an interval would prove auxiliary s-concavity there; together with partial_s h<=0 it would prove physical t-concavity on the corresponding positive-t interval by (6).

This checkpoint makes no claim that either inequality has yet been proved. The next step is to seek a relative-entropy / complete-word Fisher representation of J_s that uses the special identity V_s=partial_s Phi_s rather than an arbitrary concave test observable.
