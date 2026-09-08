# Variational residual refinement for the selected phase candidate

Status: author proof and application, independent audit pending. The original B0 certificate is unchanged.

This unit only addresses the already selected phase candidate P0 in phase_candidate.json. Its margin is 1/50. The original M64 norm-residual bound was about 2.765e-7 for its slowest extreme-past kernel, too coarse for the probability error budget. The following energy identity squares the residual without extending the past truncation or selecting new symbols.

Use the notation T>=epsilon I, B, C, X, R=B-TX, Y=T^(-1)B of boundary_residual_proof.md. Define

    H_X=B*X+X*B-X*TX,
    A_X=C-H_X.

Expanding R*T^(-1)R gives the exact matrix identity

    B*T^(-1)B-H_X=R*T^(-1)R.

Consequently, if C_infinity=C-B*T^(-1)B is the true all-one conditioned kernel,

    0 <= A_X-C_infinity <= (||R||_F^2/epsilon) I.

The approximation and error remain confined to the first m future coordinates. No exact Galerkin solve is required. Every entry of X and R is rational and finitely supported; hence H_X is rational too. The implemented correction uses the identity

    A_X=[C-sym(B*X)]-sym(X*R).

This equals C-H_X because X*TX is Hermitian. The original rational sum-of-component-absolute-values bound r_bound>=||R||_F yields the rational error delta=r_bound^2/epsilon. The implementation recomputes R exactly and checks agreement with its original saved bound and corner before applying the correction. It records its own source hash and the complete input hash.

For f_P0,t=1/2+(3/10)cos(theta)+(3/25)cos(2theta)+(1/25)cos(3theta)
                    +t[(3/25)sin(2theta)-(1/25)sin(3theta)], t=+-1/8,

use these improved corners in the unchanged rational_rate_certificate.py. Its previously audited Schur probability error and finite extreme-past entropy inequalities apply whenever delta<epsilon. No other assumption or formula changes. Thus this is a concrete second fixed-pair application of the same rate argument, not a theorem for the family.

The executed refinement reduced the largest operator-error bound to less than 1.230e-14. At past length 8, 3,072 exact event determinants and interval logs then gave the rational rate-gap interval

    [-66526970206269242160979448724583101877021,
     -53940728164719571439402461532317703232197]
    /11417981541647679048466287755595961091061972992.

It is approximately [-5.82651e-6,-4.72419e-6] nats and is strictly negative. The recorded result is phase_rate_n8.json. Thus the first phase task's specific two-invariant-phase candidate is also excluded as a counterexample, conditional on independent audit of this refinement and its application. No window expansion was needed for the sign.
