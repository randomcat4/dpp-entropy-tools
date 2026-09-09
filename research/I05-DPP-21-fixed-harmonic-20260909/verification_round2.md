# Supplemental independent-review contract

This is an author checklist, not a review.

## 1. Fixed point-curvature certificate

Review `point_curvature.md` and `code/certify_point_curvatures.py` independently of the midpoint checker.

1. Verify that the event-jet automaton returns derivatives with respect to the genuine parameter `t`. Since the scaled nearest entry is `2t`, first and second interpolation derivatives in that entry are multiplied by `2` and `4`.
2. Check exact normalization of all three jet layers: `sum N=32^n`, `sum N'=sum N''=0`.
3. Check the full finite formula

   ```text
   H_n''=-(1/32^n)sum[N'^2/N+N''log N].
   ```

4. Recompute the point-specific comparison residuals, Cauchy radii, two-pass Schur constants, and the infinite quadratic-geometric sums from depth `18`.
5. Confirm that the directed upper enclosure for the true rate is below `-1/2500`, `-1/1000`, and `-1/500`, respectively.
6. Do not infer any sign between the certified points.

## 2. Full-Fisher projection

Review `fisher_projection.md` and `code/check_pair_fisher_projection.py`.

7. Reconstruct the two-, three-, and four-site inclusion determinants from the stated Toeplitz kernel, then verify all covariance polynomials.
8. Check two-dependence carefully: adjacent-pair observables at lag at least four have supports whose mutual distance exceeds two and are independent.
9. Verify the finite Cauchy-Schwarz score projection before taking a limit.
10. Check the right-to-left score decomposition, uniform bounded boundary remainder, reverse-martingale orthogonality, and therefore

    ```text
    lim I_n/n=nu(psi^2).
    ```

11. Verify the monotonicity of `t^2/V(t)` and the uniform exact lower bound `16/286141`.
12. This is a lower bound on the complete Fisher rate; it is not a replacement for the acceleration term.

## 3. Continuum boundary

13. The whole interval remains `INCOMPLETE`. The only authorized route to promote a finite-memory interval computation is the explicit true-rate remainder in `proof.md` / issue #74.
14. A failure of the finite-memory sufficient budget is not a counterexample. A counterexample requires three fixed legal symbols and rigorous true-rate intervals with a positive Jensen difference.
15. No new statement in this branch inherits a PR59 verdict; review every new file at its actual frozen head.