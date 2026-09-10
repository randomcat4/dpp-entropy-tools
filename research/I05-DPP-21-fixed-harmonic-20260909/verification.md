# Verification and independent-review contract

This file is an **author self-audit**, not an independent review. The new theorem remains `PROVED (AUTHOR PROOF), NOT INDEPENDENTLY REVIEWED` until a nonauthor checks the frozen head.

## A. Fixed legality

1. Substitute `x=cos(2 pi theta)` and verify

   ```text
   f_t=1/4+x^2/2+(t/8)x.
   ```

2. On `|t|<=3/2`, check the interior minimum `1/4-t^2/128>=119/512` and endpoint maximum `3/4+|t|/8<=15/16`.

3. Confirm that the resulting operator margin is `1/16` for every finite compression. No PR59 tube radius is used.

## B. Complete-event inverse and conditional tail

4. Check the signed complete-event conditional

   ```text
   q_r=1/2-b^T M_r^(-1)b
   ```

   and its first two derivatives. The diagonal of `M_r` is `+1/2` or `-1/2` according to the full future word.

5. Verify the comparison M-matrix with diagonal `1/2`, nearest entry `-13/128`, and next-nearest entry `-1/8` on the complex `1/8`-neighborhood of `[1/2,3/2]`.

6. Recompute all four exact supersolution residuals for `rho=49/64`, especially the center residual `3243/16384`. This yields

   ```text
   |M_r^(-1)_{ij}|<=(16384/3243)(49/64)^|i-j|.
   ```

7. Reproduce the near/far Schur formula. Both propagations from sites `{1,2}` to the remote cut are required. Check

   ```text
   C^3(1661/8192)^2(2445/8192)^2
   <1033420800/1263214441.
   ```

8. Verify the Cauchy derivative factors `j! 8^j` and that the bound is uniform in every complete word and volume.

## C. True-rate midpoint certificate

Run from the repository root:

```sh
python research/I05-DPP-21-fixed-harmonic-20260909/code/certify_midpoint_rate_gap.py --depth 18
```

The program has no third-party dependency.

9. Audit the exact width-two determinant automaton. For a scaled event matrix `32(K-I_Z)`, the diagonal is `+/-16`, first off-diagonal is `1`, `2`, or `3`, and second off-diagonal is `4`.

10. Check the independent small implementation: inclusion determinants are scaled to denominator `32^n`, followed by the full Mobius sum over every superset. It must agree with the signed event determinant for every word through length six.

11. Verify exact positivity and normalization:

    ```text
    N_n(omega)>0,
    sum_omega N_n(omega)=32^n.
    ```

12. Inspect the directed logarithm enclosure. `Context.ln` is evaluated at precision `100`, widened by `10^-90`, and all weighted arithmetic is separately rounded down and up. The certificate must not use an ordinary floating determinant or an unbounded epsilon added to probabilities.

13. Verify

    ```text
    h_r-h=E d(q_infinity||q_r)
    ```

    and the chi-square upper bound `d(a||b)<=(a-b)^2/[b(1-b)]`. With the conditional margin, this gives

    ```text
    0<=h_r-h<=(256/15)C0^2 rho^(4r-12).
    ```

14. At `r=18`, check that the directed lower expression

    ```text
    lower(h_18(1))-E_18
    -[upper(h_18(1/2))+upper(h_18(3/2))]/2
    ```

    exceeds `1/10000`. For the midpoint only, subtract the rate error; for the two endpoints, `h<=h_18` gives the required upper bounds.

15. The result is a strict true-rate Jensen gap in the concave direction. It is not a curvature theorem and not a counterexample.

## D. Poisson/correlation formula

16. Starting from `nu L=nu`, verify the centered linear response

    ```text
    d nu(A)=nu(dot A)+nu(psi R A).
    ```

17. Differentiate `(I-L)v=phi-nu(phi)`, retain the additive normalization constant until it is multiplied by `psi`, and derive

    ```text
    dot v=psi+R(psi v)-Pi(psi v)+constant.
    ```

18. Check every sign and factor in

    ```text
    h''=-nu(psi^2)+nu((psi^2-xi)v)-2nu(psi R(psi v)).
    ```

19. Expand `R=sum L^n Pi` and use the transfer/shift adjoint identity to obtain the correlation form. No claim that the residual correlations are nonpositive is made.

## E. Curvature-tail interface

20. Recheck the real inverse row-sum bound `16` and the conditional derivative bounds

    ```text
    |q_r'|<=9/8,
    |q_r''|<=37/8.
    ```

21. Verify the exact derivatives of binary negative entropy on `[1/16,15/16]`:

    ```text
    M2=256/15,
    M3=57344/225,
    M4=27656192/3375.
    ```

22. Reproduce the Bregman integral bounds `A0,A1,A2`, the complete-event score bounds `|S|<=2(r+1)` and `|S'|<=4(r+1)`, and the final formula for `|d_r''|`.

23. Check the closed sums for a quadratic polynomial times `rho^(4r)`. Only after adding this tail may a finite conditional curvature computation certify the true rate.

24. Issue #74 is a requested heavy computation, not an existing result. No outcome from it is assumed here.

## F. Beam-splitter comparison

25. Verify the balanced output covariance and the exact decomposition

    ```text
    midpoint gap=I_out+E_occ.
    ```

26. Layer-sign conjugation makes every complete output event even in the separation parameter. Since the output law differs from its product law at order two, its mutual information starts at order four. Check `I_out''(0)=0` and `E_occ''(0)=-2h''(t_*)`.

27. Do not replace occupation Shannon entropy with quasifree von Neumann entropy.

## G. Status and novelty

A successful review may accept the strict legality theorem, the fixed true-rate midpoint gap, the Poisson/correlation identity, and the curvature error interface separately. It must not upgrade them to `h''<0` on the entire interval. No novelty, priority, or formal-proof claim is made.