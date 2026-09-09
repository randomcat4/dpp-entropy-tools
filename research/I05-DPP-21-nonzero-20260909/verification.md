# Verification and independent-review contract

This file is an **author self-audit**. It is not an independent review. The new statements remain `PROVED (AUTHOR PROOF), NOT INDEPENDENTLY REVIEWED` until a separate reviewer checks the frozen branch head.

## A. Load-bearing checks for Theorem CT

1. **Accepted dependencies and scope.** Verify that the proof uses only:
   - PR53's final accepted exponentially weighted event-inverse/RPF machinery and the vanishing `t^2` rate coefficient at the parity point;
   - PR34's accepted constant-centered whole-legal-interval correction `(4/3)|g_hat(k)|^4t^4`.

   No open PR or stale issue status is a premise.

2. **Uniform event inverse over a compact radial chord.** For

   ```text
   f_t^0=mu+t g, |t|<=T,
   ```

   check the common pointwise margin, the signed accretivity estimate for every `K-I_Z`, the uniform Fourier truncation, the banded polynomial inverse, and the weighted Neumann restoration. All zero/one patterns must remain included.

3. **Banach-parameter analyticity.** Check that a small center perturbation `u` and local complex parameter perturbation `z-t_*` enter the genuine kernel linearly. The weighted inverse radius must be independent of the word and volume.

4. **Remote-conditioning estimate.** Reproduce the near/far Schur-resolvent argument giving exponential convergence of every complete-event one-sided conditional, uniformly in the center/parameter polydisc. No probability lower bound for an individual rare word may be used.

5. **RPF identification before differentiation.** Verify that the finite right-to-left entropy chain has an `O(1)` total conditional-tail error, so

   ```text
   h=-nu(log G)
   ```

   is established before taking parameter derivatives.

6. **Parity and the missing quadratic term.** Half-period symmetry makes the rate even, but evenness alone is insufficient. Check the relative-entropy-rate formula and the normalization calculation

   ```text
   partial_s nu_s(log(G_s/G_0))|_0=0
   ```

   for `s=t^2`. This is what proves `partial_t^2F(u,0)=0`.

7. **Analytic division.** Verify that

   ```text
   Psi(u,t)=F_tt(u,t)/t^2,
   Psi(u,0)=F_tttt(u,0)/2
   ```

   is jointly analytic on the half-period-even center subspace.

8. **Radial curvature constant.** From accepted concavity of

   ```text
   F(0,t)+(4/3)lambda_k t^4
   ```

   check

   ```text
   Psi(0,t)<=-16lambda_k
   ```

   including the limit at zero.

9. **Uniform transverse stability.** The compact set is `{0}x[-T,T]`, not an infinite-dimensional center ball. Check the finite-cover argument that gives one `rho>0` with

   ```text
   Psi(u,t)<=-8lambda_k
   ```

   for every `||u||_beta<rho` and every `|t|<=T`.

10. **Final correction and strict Jensen gap.** The second derivative of `(2/3)lambda_k t^4` is exactly `8lambda_k t^2`. Check the sign at `t=0` and strict convexity of `t^4` for distinct endpoints.

## B. RPF Hessian checks

11. With

   ```text
   R=(I-L)^(-1)Pi,
   dot L(A)=L(psi A),
   ```

   verify the linear-response identity

   ```text
   d nu(A)=nu(dot A)+nu(psi R A).
   ```

12. Verify

   ```text
   dot B=-L(psi phi),
   ddot B=-L((xi+psi^2)phi+psi^2).
   ```

   In particular, `-L(psi^2)` is retained as the conditional Fisher term.

13. Differentiate the Poisson equation `(I-L)u=B-h`. The normalization constant in `dot u` may be omitted only after multiplication by `psi`, using `nu(psi)=0`.

14. Check the resolvent identity

   ```text
   R(LA)=RA-Pi A
   ```

   and then every coefficient in

   ```text
   h''=nu(ddot B)+nu(xi u)
       +2nu(psi R dot B)
       +2nu(psi R(psi u))
       -nu(psi^2u).
   ```

15. The sufficient norm bound in `proof.md` is one-sided only. It is not asserted to hold automatically and must not be promoted to a universal theorem.

## C. Finite-state interval bridge

16. Check that finite-future conditionals and their first two parameter derivatives converge in one fixed weaker Hölder norm on a compact strict interval.

17. Use a common spectral contour and the resolvent identity to obtain uniform convergence of the invariant functional and centered resolvent. A finite Markov computation is a true-rate certificate only after its explicit geometric remainder is included.

18. No interval computation is claimed in this round. The finite-state interface is analytic/proved, not an executed certificate.

## D. Beam-splitter checks

19. Verify the balanced covariance

   ```text
   K_out(u)=[[M,uK_g],[uK_g,M]]
   ```

   from the genuine endpoint kernels, with no observed-basis diagonalization.

20. Check the exact classical decomposition

   ```text
   midpoint gap=I_out+E_occ
   ```

   for every finite window, then its per-cell stationary version.

21. At `u=0`, the doubled law is the product of fixed marginals. Layer-sign conjugation makes every complete event even, so the law changes at order `u^2` and its relative entropy at order `u^4`. Check

   ```text
   I_out''(0)=0,
   E_occ''(0)=-2h''(t_*).
   ```

22. Do not replace occupation Shannon entropy by von-Neumann entropy. The known fermionic quantum inequality is not a proof of `E_occ>=0`.

## E. Exact example-only checker

Run from the repository root:

```sh
python research/I05-DPP-21-nonzero-20260909/code/check_explicit_family.py
```

The script uses Python's `fractions.Fraction` and integer arithmetic only. It checks the displayed Fourier coefficient, quartic constants, radial legality margin on `[-2,2]`, and the elementary strict margin for `|epsilon|<=1/24`. It does not compute a DPP entropy, curvature, RPF operator, or entropy rate.

Expected output path:

```text
research/I05-DPP-21-nonzero-20260909/output/explicit_family_exact.json
```

## F. Error and computation boundary

Theorem CT has no numerical error term. Its finite-to-rate passage is the exact RPF formula obtained from a geometrically summable `O(1)` block error. The example checker has no rounding tolerance.

No heavy elimination, interval arithmetic, or enumeration was required, so no compute issue was opened. Any future implementation of the interval certificate (7.4) in `proof.md` must freeze the symbol, interval, conditional depth, spectral-contour bound, directed rounding rules, and the geometric tail constant before execution.

## G. Final scope

A successful review may accept only the compact radial-tube theorem, the exact RPF Hessian, the finite-state error interface, and the beam-splitter second-order obstruction. It must not upgrade the result to arbitrary centers, legal endpoints, the full PR39 example interval, or a counterexample. Novelty remains unassessed.