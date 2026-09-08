# U8/M10 conclusion and remaining blocker

GLOBAL STATUS: INCOMPLETE.

No positive-curvature DPP counterexample has been found or certified in this unit. Neither global B>=0 nor connected-global B>0 has been proved.

Two analytic candidates have been produced:

1. At every connected strict n=3 kernel, the exact full Hessian is a positive definite form minus one rank-one form. Its only possible failure is the explicit scalar rho(K)>1. There is a five-dimensional weighted-trace-zero direction hyperplane with a strict negative entropy-curvature bound. The Lambda=0 connected case is proved using the simultaneous vanishing conditions of the two conditional covariance squares.
2. Near each dense rank-one boundary kernel theta uu^T, with fixed theta in (0,1) and every ui nonzero, the equal-soft-eigenvalue family epsilon I+(theta-epsilon)uu^T has full-Hessian negativity for all sufficiently small positive epsilon. Its scalar satisfies rho=1-1/(theta log(1/epsilon))+O(log(1/epsilon)^(-2)); the complement family has the same property.

Both remain AUTHOR PROOF CANDIDATES pending independent review. Full derivations are in derivation.md and boundary_asymptotic.md.

The exact remaining global inequality is

det(N)*eta^T [Fisher+det(N)G_N]^(-1) eta <= 1,

where N=-diag(l23,l13,l12)-Lambda K, eta_i=tr(N^(-1)E_i), and (G_N)ij=tr(N^(-1)E_i N^(-1)E_j). Strict connected negativity needs the strict version. This is a six-coordinate positive-definite solve followed by one scalar comparison; all variables are explicit functions of the eight exact atoms.

N>0 and Fisher>=0 alone do not imply this inequality: the artificial pair N=I, Fisher(D)=||D||_F^2 gives rho=3/2. It is an algebraic obstruction to that proof shortcut, not a DPP counterexample. The DPP-specific coupling between its conditional odds and Fisher geometry is the missing global step.

The boundary analysis rules out any attempted uniform rho<=c<1 argument. Simultaneous limits with theta approaching 0 or 1, vanishing entries of u, arbitrary unequal soft-eigenvalue rates, and general interior kernels remain outside the boundary subclass proof.

Finite evidence is sharply bounded: 510 original structured rational kernels (420 connected, 90 disconnected), 420 scalar re-evaluations of those connected centers, four higher-precision repeated checks, 18 equal-rate and 12 unequal-rate boundary probes. No FLOAT_CANDIDATE was produced. The original worst normalized-Hessian point has a separate exact rational-log positive-definiteness certificate, but a certified point is not a certified global region.
