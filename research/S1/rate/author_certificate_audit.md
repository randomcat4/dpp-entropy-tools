# Audit of the Route-Owner n=8 Rate Certificate

STATUS: `CORRECT` for the stated fixed baseline, conditional on the standard Lyons--Steif DPP conditioning, negative-association, and entropy-rate facts already allowed by the frozen S1 task.

Scope audited:

- frozen route-owner commit `a98811c6597577f73128aaed3fd7dde6169af350`
- `research/S1/main/rate_certificate_proof.md`
- `research/S1/main/rational_rate_certificate.py`
- `research/S1/main/rational_rate_n8.json`
- the M64 boundary residual certificate already cross-checked in `artifacts/boundary_compare.json`

The conclusion is only:

```text
(h(f_-)+h(f_+))/2 - h(f_0) < 0
```

for the single frozen rational benchmark.  It is not a proof or disproof of Lyons--Steif Conjecture 9.2.

## Independent Comparison

My independently implemented outer-factor method gives, at the same suffix length `r=8`,

```text
lower gate L_+(8)-U_0(8) = -2.6204663531426142e-05
upper gate U_+(8)-L_0(8) = -2.6051588097764089e-05
```

The route-owner strict interval certificate gives

```text
gap lower = -2.6204849038956574e-05
gap upper = -2.6051480851662238e-05
```

The strict enclosure safely contains the independent floating-point computation, with outward slack on both sides.

## Boundary Kernel Chain

The M64 residual certificate does not trust the numerical linear solve.  It records dyadic rational approximate solutions, recomputes the half-line residual exactly, and uses the uniform margin `epsilon=3/50` to bound the operator error.  The recorded operator errors are:

```text
f_0:       1.1858581e-11
f_tau:     2.0123569e-11
1-f_0:     2.3571931e-22
1-f_tau:   2.5470632e-21
```

My outer-factor corner comparison agrees with those rational corners to at most `8.3266727e-16`, so the residual certificate and the Lyons--Steif outer-kernel formula are addressing the same finite corner object.

The complement orientation is correct: the all-zero past for the original process is computed as the complement of the all-one past for the `1-f` process, replacing the leading corner by `I-A_{1-f}` while leaving the ordinary Toeplitz tail unchanged.

## Probability and Error Chain

The determinant formula in `event_masses` is algebraically correct.  For a zero bit it changes `K_ii` to `K_ii-1` and multiplies the final determinant by `(-1)^{number of zeros}`, which is the same as using rows `I-K` for zero-conditioned coordinates.  The script checks:

```text
exact integer Bareiss divisibility
exactly real Hermitian determinants
strictly positive Fraction event masses
exact mass normalization to one
```

The Schur-complement perturbation bound for a one-site conditional probability is also correct.  For

```text
E = Q_PP - diag(1_{gamma=0})
```

the signed matrix argument gives `||E^{-1}|| <= 1/a` when the kernel margin is `a`.  Along the segment between the true boundary kernel and the rational approximation, `a=epsilon-delta`, and differentiating the finite Schur complement gives the stated uniform bound

```text
e = delta * (1 + ((1+delta)/(epsilon-delta))^2).
```

This avoids any division by a small cylinder probability.  The script then verifies `lo <= q <= hi` for the ordinary finite conditional probability as an additional sanity check.

## Entropy-Rate Chain

The lower bound uses finite suffix weights from the ordinary stationary process and the minimum binary entropy over the certified interval `[lo_gamma, hi_gamma]`.  This is valid because the whole-past conditional probability lies in that interval almost surely on the suffix cylinder.  The upper bound is the standard finite conditional entropy

```text
H(X_0 | X_{-n},...,X_{-1}),
```

which is above the entropy rate.  No finite-window entropy extrapolation, asymptotic fit, entropy-rate derivative, or exchange of limit and derivative is used.

The interval-log step is appropriate for the final sign claim: all inputs to binary entropy are rational intervals; endpoint entropies are interval-evaluated; the final lower gap subtracts the outward upper center bound from the outward lower endpoint bound, and the final upper gap subtracts the outward lower center bound from the outward upper endpoint bound.

The produced rational upper endpoint is strictly negative:

```text
-148727663748433704622488410027642662541253
/5708990770823839524233143877797980545530986496 < 0.
```

Therefore the fixed baseline has a certified negative entropy-rate gap.

## Limitations

No critical gaps were found.  The proof is not mechanically formalized, and it relies on the standard DPP source facts above.  The result excludes one fixed benchmark as a positive counterexample; it does not establish any family theorem or global conjecture result.
