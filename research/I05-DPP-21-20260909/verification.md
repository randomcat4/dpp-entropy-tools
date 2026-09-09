# Verification and review map

This file is an **author self-audit**, not an independent review. The theorems in `finite_range_local_theorem.md` and `exponential_wiener_extension.md` remain `PROVED (AUTHOR PROOF), NOT INDEPENDENTLY REVIEWED` until a nonauthor checks them.

## Exact checker actually run

Environment:

```text
Python 3.13.5
Linux x86_64
third-party dependencies: none
```

Command from the repository root:

```sh
python research/I05-DPP-21-20260909/code/check_rudin_shapiro_example.py
```

Recorded output:

```text
research/I05-DPP-21-20260909/output/rudin_shapiro_exact.json
```

The checker uses only integer arithmetic and `fractions.Fraction`; there is no numerical tolerance or rounding error. It verifies:

```text
|P_4|^2+|Q_4|^2=32 on the unit circle
```

by exact autocorrelation cancellation, the 16 displayed coefficients of `P_4`,

```text
||c-1/2||_W=15/16,
2||c-1/2||_W=15/8>1,
g_hat(1)=1/128,
gamma=1/16384,
alpha=1/(3*2^27),
```

and positivity of `(7-4sqrt(2))/16` through the exact inequality `49>32`.

It does not compute an entropy, a finite-window curvature, or an entropy rate, and is not cited as proof of either theorem.

## Load-bearing analytic checks

A nonauthor review should check the following in order.

1. **Complete-event inverse.** For `M_x=K-I_Z`, verify the signed accretivity identity

   ```text
   Re(v*J M_x v)=v_S*K_SS v_S+v_Z*(I-K_ZZ)v_Z
   ```

   and hence the singular-value lower bound for every zero/one pattern.

2. **Banded inverse decay.** Verify the identity

   ```text
   M_x^{-1}=sum_{r>=0} M_x(I-M_x^2)^r
   ```

   and the support count leading to Lemma 4.2 of the finite-range proof.

3. **Finite-range common complex neighborhood.** Check that the weighted Schur norm is submultiplicative, that Lemma 4.2 gives a volume/configuration-uniform bound on `M_x(0)^{-1}`, and that the Neumann radius `(2B_0B_g)^{-1}` applies simultaneously to every finite event matrix.

4. **Finite-range remote-conditioning estimate.** With the long future block split into near and far pieces, write

   ```text
   S=M_near-E M_far^{-1}F,
   S^{-1}-M_near^{-1}=S^{-1}(E M_far^{-1}F)M_near^{-1}.
   ```

   Because `E M_far^{-1}F` has near-block row and column support only within the Fourier range of the cut, the two outer inverse propagations from site zero to the cut decay exponentially.

5. **Exponential-Wiener truncation.** In `exponential_wiener_extension.md`, verify that the truncated band matrix `B_Z=M_Z-E_W` satisfies

   ```text
   sigma_min(B_Z)>=3delta/4,
   ||B_Z||<1,
   ```

   and that its weighted inverse norm grows at most linearly in the truncation bandwidth `W`. Check that

   ```text
   ||E_W||_{a_W}<=exp(-beta W/2)||c||_beta
   ```

   beats this growth and makes the weighted Neumann series uniform in every volume and configuration.

6. **Infinite-range remote-conditioning estimate.** Check the block identity

   ```text
   [M_R^{-1}]_NN-M_N^{-1}
   =M_N^{-1}E_NF S_F^{-1}E_FN M_N^{-1}.
   ```

   In the weighted norm, a row localized at site zero and propagated into `F=[r+1,R]` has ordinary mass `O(exp(-ar))`; direct current-to-`F` Fourier tails have the same bound. This supplies the extension's uniform Hölder conditional estimate.

7. **Hölder/Ruelle passage.** Check that the finite conditional probabilities converge uniformly in a complex disk to a positive Hölder normalized `g`-function for real parameters. Apply the finite-alphabet Ruelle-Perron-Frobenius theorem at the baseline and the displayed Riesz-projection argument for analytic dependence. No claim is based on psi-mixing alone.

8. **Rate formulas without derivative-limit exchange.** Expand finite entropy and finite relative entropy from right to left. The sum of finite-tail versus infinite-tail logarithmic errors is bounded by a geometric series, hence `O(1)` independently of block length. Dividing by volume gives the rate formulas before any differentiation.

9. **Vanishing `s=t^2` linear term.** In differentiating

   ```text
   nu_s(log(G_s/G_0)),
   ```

   the eigenmeasure derivative multiplies the zero observable at `s=0`; the remaining term integrates to zero from `G_s(0x)+G_s(1x)=1`.

10. **True-rate fourth-order lower bound.** Check the step-`k` matching count, negative association for nonnegative decreasing functions on disjoint edge-coordinate sets, the KL variational optimization, and the binary expansion. The limit is taken in the finite inequality at each fixed `t`; no finite coefficient is extrapolated.

11. **Curvature constant.** From

   ```text
   A>=C_k=gamma^2/[4mu^2(1-mu^2)]
   ```

   verify that a smaller interval gives `R''(t)>=6C_k t^2`, and that adding

   ```text
   alpha_k t^4,  alpha_k=C_k/2,
   ```

   contributes exactly `6C_k t^2` to the second derivative.

## Computation and error boundary

No heavy computation, interval arithmetic, sampling, or finite-size extrapolation is used by either theorem. Therefore no separate compute issue was opened. The older balanced-beam-splitter floating probe remains a diagnostic of a different open route and has no role in the result.

## Remaining mathematical scope

The review should not upgrade the result beyond its quantifiers. The strongest theorem is local in `t`, requires an exponentially weighted Fourier sum and a strict pointwise margin at the center, and does not settle the full legal interval. The arbitrary measurable-symbol concavity question remains `INCOMPLETE`.