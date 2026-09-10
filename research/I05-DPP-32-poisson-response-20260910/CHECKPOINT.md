# DPP32 checkpoint: parity information curvature and conditional affine-kernel reduction

Status: AUTHOR_PROOF / PENDING_REVIEW. Date: 2026-09-10. This checkpoint is a successor to PR112 and inherits its fixed family and notation only as explicitly stated below. It does not upgrade PR112's arithmetic interval certificate, does not use the old |t-1|<=2^-27 claim, and does not assert the full [1/2,3/2] sign.

We work with the original complete-configuration Shannon entropy rate per original coordinate for

    f_t(theta)=1/2+cos(4*pi*theta)/4+t*cos(2*pi*theta)/8,

with the physical affine kernel path kept in t. Put s=t^2/256 only as the auxiliary squared coupling parameter. Let P_s be the full four-branch probability operator, B_s its complete-cell entropy observable, eta_s its invariant law, and Phi_s a differentiable Poisson corrector solving

    (I-P_s) Phi_s = B_s - c_s,        c_s=2 h(s).

All derivatives hold the test observable fixed inside partial_s P_s, exactly as in PR91/PR112.

## 1. Previously isolated exact response identity

Differentiating the Poisson equation shows that the PR112 second Poisson observable is the centered class of partial_s Phi_s. Consequently the exact auxiliary curvature can be organized as

    partial_s^2 h
      = eta_s(partial_s P_s)(partial_s Phi_s)
        -(1/2) eta_s(I_s+K_s),                         (1)

and restoration of the genuine affine physical t path gives

    h_tt = (partial_s h)/128
           +(t^2/16384) partial_s^2 h.                 (2)

Equation (2) retains Fisher, state motion, invariant-law response and the t-to-s acceleration. This section is retained only to state the dependency used below; no generic sign for partial_s P_s is asserted.

## 2. Parity mutual information and corrected physical implication

Let mu_s be the stationary complete-configuration DPP law. At s=0 the nearest-neighbor Fourier mode vanishes, so the Toeplitz kernel splits into the even and odd coordinate blocks while each parity marginal is unchanged. The accepted cyclic block-decoupling identity therefore gives

    D(s):=D_rate(mu_s || mu_0)=h(0)-h(s),             (3)

which is the mutual-information rate between the even and odd subprocesses. Hence

    D''(s)
      = (1/2) eta_s(I_s+K_s)
        - eta_s(partial_s P_s)(partial_s Phi_s).       (4)

Thus convexity of D in squared coupling is exactly the remaining auxiliary-curvature inequality.

The physical implication must be stated carefully. Since

    h_tt = -D'(s)/128 -(t^2/16384)D''(s),             (5)

there are two valid sufficient routes on a target interval J:

1. prove D''>=0 on a connected interval [0,S] containing J. Then D(0)=0 and D>=0 imply D'(s)>=0 on [0,S], so (5) is nonpositive;
2. prove D''>=0 only on J AND independently prove D'>=0 on J.

In particular, convexity merely on J=[1/1024,9/1024], corresponding to t in [1/2,3/2], does NOT follow from D(0)=0 and D>=0 to give D'>=0 there. The earlier stronger sentence in this checkpoint was incorrect and is withdrawn.

The accepted cyclic theorem supplies only the value bound D(s)>=s^2 for this family. It cannot be differentiated into a derivative bound.

## 3. Finite complete-event likelihood: Fisher plus exact acceleration

The next theorem is stated for a general finite real DPP block family because the target parity split is a specialization. Let a finite coordinate set be partitioned as E union O and let

    K_s = [[A, sqrt(s) B],
           [sqrt(s) B^T, C]],                         (6)

on an interval of s>=0 for which 0<K_s<I. This notation is only for the squared-coupling analysis; in the original target family sqrt(s)=t/16 and the physical K path remains affine in t.

For complete configurations e on E and o on O put

    A_e=A-I_{E\e},   C_o=C-I_{O\o},
    eps_e=(-1)^|E\e|, eps_o=(-1)^|O\o|.

The exact complete-event probability is

    p_s(e,o)=eps_e eps_o det [[A_e,sqrt(s)B],
                              [sqrt(s)B^T,C_o]].       (7)

At s=0, p_0(e,o)=p_E(e)p_O(o). Schur complementation gives the complete-event likelihood ratio

    L_{e,o}(s):=p_s(e,o)/p_0(e,o)
      = det(I-s A_e^{-1} B C_o^{-1}B^T).              (8)

No inclusion minor has replaced a complete event. Therefore finite parity mutual information is

    D_{E,O}(s)=sum_{e,o} p_0(e,o)L_{e,o}(s)log L_{e,o}(s),

and ordinary differentiation, using sum p_0 L''=0, yields

    D_{E,O}''(s)
      =sum_{e,o} p_0(e,o)
         [ (L'_{e,o})^2/L_{e,o}
           +L''_{e,o} log L_{e,o} ].                  (9)

The first term is the full finite complete-event Fisher contribution. The second is the exact cross-event acceleration contribution. It first becomes nontrivial once the determinant in (8) has degree at least two; it may not be dropped or signed eventwise.

## 4. New theorem: all cross-event acceleration is an average of genuine affine-kernel DPP Hessians

For each complete E-configuration e define

    M_e=B^T A_e^{-1}B,
    C_e(s)=C-s M_e.                                   (10)

Then, conditional on E=e, the complete O-configuration law is exactly the DPP with correlation kernel C_e(s). Indeed (7) and the Schur determinant identity give

    p_s(o|e)=eps_o det(C_o-sM_e),                     (11)

while p_E(e)=eps_e det A_e is independent of s. Thus C_e(s) is a genuine correlation kernel of a conditional DPP and, crucially, is AFFINE in s.

Because the O marginal remains the DPP with kernel C and is independent of s,

    D_{E,O}(s)
      = H_DPP(C)-sum_e p_E(e) H_DPP(C_e(s)),           (12)

where every H_DPP is the full complete-configuration Shannon entropy, not spectral entropy. Twice differentiating the genuine affine kernel paths C_e(s) proves

    D_{E,O}''(s)
      = -sum_e p_E(e)
          D_K^2 H_DPP(C_e(s))[M_e,M_e].                (13)

Equation (13) is exactly equal to the Fisher-plus-acceleration expression (9). Hence the apparently unsigned cross-event acceleration is not an extra missing term: after conditioning on one fixed marginal it is absorbed into the ordinary complete-Shannon Hessian of conditional DPP kernels along true affine K directions. This is a structural identity, not a sign theorem for arbitrary dimension.

There is also an exact first-moment cancellation. Differentiating the normalization of the complete E-event probabilities in an arbitrary matrix direction X gives

    0=sum_e p_E(e) tr(A_e^{-1}X).

Therefore

    sum_e p_E(e) A_e^{-1}=0,
    sum_e p_E(e) M_e=0.                               (14)

This explains algebraically why the first variation of the conditional-kernel mixture cancels at s=0; it does not by itself sign the second variation.

## 5. Immediate verified-scope consequence and the first dimension obstruction

Whenever |O|<=2, the already accepted global concavity of the finite real two-coordinate DPP Shannon entropy applies to every affine conditional path C_e(s). Equation (13) therefore gives

    D_{E,O}''(s)>=0                                    (15)

throughout every legal squared-coupling interval. The same conclusion holds if |E|<=2 by conditioning in the opposite direction.

For the target consecutive-coordinate windows split by parity, the smaller parity block has size floor(n/2). Thus the complete finite-window parity mutual information is rigorously convex in s for n<=5. The first window not covered by this reduction is n=6, where both parity blocks have dimension three. At that point (13) lands exactly in the still-open three-dimensional complete-Shannon Hessian problem for the eight conditional affine kernels/directions; no finite-event acceleration has been omitted.

This is a precise obstruction rather than a counterexample. Failure to control the n=6 conditional Hessians would not imply D_6''<0, and a finite D_n''<0 would not by itself imply a negative entropy-rate curvature.

## 6. Exact finite-to-rate boundary identity

For the target process group original coordinates into two-site cells and let H_m(s) be the complete Shannon entropy of m cells (2m original sites). Let c_s=2h(s) be the cell entropy rate and choose any Poisson solution

    (I-P_s)Phi_s=B_s-c_s.

The exact chain rule and telescoping Poisson identity give

    H_m(s)=m c_s + Phi_s(0)-(P_s^m Phi_s)(0).          (16)

Define the boundary corrector

    Psi_m(s)=Phi_s(0)-(P_s^m Phi_s)(0).

Since the parity marginals equal the s=0 blocks,

    D_{2m}(s)=H_m(0)-H_m(s),                           (17)

and therefore, wherever the already-proved C2 response applies,

    D_{2m}''(s)/(2m)
      =D''(s)-Psi_m''(s)/(2m).                        (18)

This identity preserves the entire finite-event Fisher and acceleration response: all finite-volume boundary discrepancy is a single twice-differentiated Poisson boundary term.

The PR91 uniform contraction/smooth-resolvent machinery implies uniform C2 convergence of P_s^m Phi_s to its invariant value on compact parameter intervals. In particular there is a finite constant C_J, depending only on the already explicit common derivative/contraction bounds on a compact J, such that

    sup_{s in J,m>=1}|Psi_m''(s)| <= C_J,             (19)

and hence

    sup_{s in J}|D_{2m}''(s)/(2m)-D''(s)| <= C_J/(2m). (20)

For this checkpoint (19) is a qualitative uniform constant consequence of the proved smooth contraction bounds; no new numerical value for C_J is claimed. Producing a sharp explicit rational C_J is a separate arithmetic task and is not needed to justify the exact structural identity (18).

## 7. Current target

The squared-coupling convexity question is now reduced in two complementary ways:

- finite volume: prove the averaged conditional DPP Hessian in (13) is nonpositive for all window sizes, or exhibit an actual legal finite DPP with the average positive;
- rate: use (18)-(20) to pass any n-uniform strict finite curvature margin to the true parity-information curvature without confusing finite samples with the rate.

For the fixed Toeplitz family the first genuinely new local algebra begins at the n=6, 3-by-3 conditional kernels. The next theoretical step is to exploit their special tridiagonal signed-event inverses and the averaging identity (14), rather than invoke generic operator contraction or Gaussian I-MMSE analogies.

All new statements in this file are AUTHOR_PROOF / PENDING_REVIEW. No S2 result concerning a previous r1 differentiation convention is used here; that superseded computation is not an obstacle or dependency. PR112's newer [49/40,51/40] physical interval remains pending independent review and is not upgraded by this checkpoint.
