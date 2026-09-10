# DPP32 n=6 theorem: strict squared-coupling information convexity

Status: **AUTHOR_PROOF / PENDING_REVIEW**. Date: 2026-09-10.

This is a finite-volume continuum theorem for the same fixed Toeplitz family as PR112/PR115. It uses complete-event Shannon entropy only. It is not a finite sample, not a spectral-entropy calculation, and not yet the entropy-rate theorem.

## Statement

Let `K_t` be the six-coordinate compression of

    f_t(theta)=1/2+cos(4*pi*theta)/4+t*cos(2*pi*theta)/8,

and put `s=t^2/256`. Split the six coordinates into

    E={0,2,4},   O={1,3,5}.

Let

    D_6(s)=D(P_{K_t} || P_{K_0})=I(X_E;X_O).

Then, on the full interval

    0 <= s <= 9/1024,

which contains the squared couplings corresponding to `0<=t<=3/2`,

    D_6''(s) > 29.                                      (1)

In particular `D_6` is strictly convex in squared coupling throughout this interval.

## Conditional affine-kernel reduction

Each parity marginal has the fixed three-point kernel

    C = [[1/2,1/8,0],
         [1/8,1/2,1/8],
         [0,1/8,1/2]].

After factoring `sqrt(s)=t/16` from the cross-parity block, the unscaled incidence matrix is

    B = [[1,0,0],
         [1,1,0],
         [0,1,1]].

For each complete configuration `e in {0,1}^3` on E, define the signed complete-event matrix

    A_e=C-I_{E\e}

and

    M_e=B^T A_e^{-1} B,       C_e(s)=C-s M_e.          (2)

The complete-event Schur identity from CHECKPOINT.md proves that the conditional law of `X_O` given `X_E=e` is exactly the DPP with correlation kernel `C_e(s)`. The E-event probability `p_E(e)` is independent of `s`. Therefore

    D_6''(s)
      = -sum_e p_E(e)
          D_K^2 H_DPP(C_e(s))[M_e,M_e].                (3)

All eight E configurations have positive probability and their weights sum to one.

## Exact complete-event curvature formula

Fix one e. For each complete O-event `o`, write

    p_o(s)=(-1)^{|O\o|} det(C_e(s)-I_{O\o}).           (4)

These are the eight actual conditional event probabilities. Since `C_e(s)` is affine in `s`, each `p_o` is a rational polynomial of degree at most three and

    sum_o p_o(s)=1.

For full Shannon entropy

    H_e(s)=-sum_o p_o(s) log p_o(s),

ordinary differentiation gives exactly

    -H_e''(s)
      = sum_o (p_o'(s))^2/p_o(s)
        +sum_o p_o''(s) log p_o(s).                    (5)

The first sum is the complete conditional Fisher information. The second is the entire event-acceleration contribution. Equation (5), rather than the Fisher term alone, is what is certified below.

## Exact continuum certificate

`n6_exact_check.py` constructs every matrix in (2), all 64 conditional complete-event polynomials in (4), and checks their normalization symbolically. It subdivides `[0,9/1024]` into the eight exact rational cells

    [9j/8192, 9(j+1)/8192],   j=0,...,7.               (6)

Polynomial ranges for `p,p',p''` are enclosed by exact rational interval Horner evaluation. No parameter samples are used as extrema.

For the logarithms the checker uses the exact identity

    log x = 2 sum_{k=0}^N y^(2k+1)/(2k+1) + R_N,
    y=(x-1)/(x+1),

with `N=36` and the rigorous rational remainder bound

    |R_N| <= 2 |y|^(2N+3)/[(2N+3)(1-y^2)].             (7)

On each event/cell the lower Fisher bound is zero only when the exact interval enclosure of `p'` crosses zero; otherwise it uses

    (min |p'|)^2 / max p.

The acceleration products `p'' log p` are multiplied as signed rational intervals. Summing all eight event contributions in (5) gives, for every one of the `8 paths x 8 cells`, the exact comparison

    -H_e''(s) > 29.                                    (8)

The smallest certified interval lower bound occurs for `e=(1,0,1)` on the final cell. Its decimal rendering is about `29.2106953512`, but the theorem uses only the exact rational assertion `>29`.

A successful author-local execution of this exact checker in the current research session printed

    AUTHOR_LOCAL_EXACT_PASS
    conditional_paths 8
    s_cells_per_path 8
    complete_conditional_events_per_path 8
    log_atanh_terms 37
    exact_uniform_lower_bound > 29
    worst_path (1, 0, 1) worst_cell 7
    independent_review PENDING

This execution is author evidence, not independent arithmetic review.

Finally, averaging (8) with the fixed positive weights `p_E(e)` in (3) proves (1).

## Scope

The theorem closes the first finite window that was not already covered by the accepted two-dimensional entropy-concavity theorem. It does **not** imply `D''(s)>=0` for the infinite parity mutual-information rate, and it does not by itself prove physical `h_tt<=0`. The exact finite-to-rate identity in CHECKPOINT.md shows what further n-uniform control is required.

No PR112 interval certificate and no superseded S2 `r1` computation is used here. Novelty is unassessed.
