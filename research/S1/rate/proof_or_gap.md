# Proof or Gap

Status: `INCOMPLETE` for a strict machine-checkable sign certificate.  The mathematical rate-bound formula is complete; the remaining gap is outward interval propagation through finitely many determinants and logarithms.

## 1. Finite-Suffix Upper Bound

Let `w in {0,1}^r` be a word on the suffix sites `-r,...,-1`.  Define

```text
q_f(w) = P_f(X_0=1 | X_{-r}^{-1}=w),
U_r(f) = sum_w P_f(X_{-r}^{-1}=w) h_2(q_f(w)).
```

Here `h_2(q)=-q log q-(1-q)log(1-q)`.

By the martingale convergence theorem for finite-valued stationary processes,

```text
h(f) = H(X_0 | X_{-1},X_{-2},...) = lim_{r->infty} U_r(f),
```

and conditioning reduces entropy, so

```text
h(f) <= U_r(f)
```

for every finite `r`.  Every probability in `U_r` is a finite exact-pattern DPP probability on `r+1` sites and is computable by the standard inclusion-exclusion determinant formula.

## 2. Extreme-Past Lower Bound

Fix a suffix word `w`.  Conditional DPPs remain negatively associated, and the event `{X_0=1}` is increasing in the unconditioned coordinates.  Hence, after conditioning on the suffix `w`, the prediction probability is minimized by setting all earlier past bits to `1` and maximized by setting them all to `0`, in the limiting sense used in Lyons--Steif Section 6.

Let `nu_f` be the all-one past limit.  Define

```text
alpha_f(w) = nu_f(X_r=1 | X_0^{r-1}=w).
```

For the all-zero past, pass to the complement process, whose symbol is `1-f`.  If `bar w` is the bitwise complement of `w`, define

```text
beta_f(w) = 1 - alpha_{1-f}(bar w).
```

Then for every infinite past with suffix `w`,

```text
alpha_f(w) <= P_f(X_0=1 | full past) <= beta_f(w).
```

Therefore

```text
L_r(f) =
  sum_w P_f(X_{-r}^{-1}=w)
        min_{q in [alpha_f(w), beta_f(w)]} h_2(q)
```

is a true lower bound:

```text
L_r(f) <= h(f).
```

This lower bound does not require a convergence rate for `L_r`.  If one finite `r` separates the desired sign, the entropy-rate sign follows immediately.

## 3. The Fejer--Riesz Corner Question

Assume `f` is a strictly positive trigonometric polynomial of degree `m`.  Fejer--Riesz gives a unique outer polynomial, normalized with positive constant term,

```text
phi_f(z) = sum_{s=0}^m v_s z^s,
|phi_f(e^{2 pi i x})|^2 = f(x).
```

Lyons--Steif Theorem 6.12 gives the all-one boundary kernel

```text
A_f(j,k) = sum_{ell=0}^{min(j,k)} v_{j-ell} conjugate(v_{k-ell})
```

on `j,k >= 0`, with `v_s=0` outside `0<=s<=m`.  The ordinary future Toeplitz kernel is

```text
T_f(j,k) = fhat(j-k)
         = sum_s v_s conjugate(v_{s-(j-k)}).
```

If `max(j,k) >= m`, the truncated sum in `A_f(j,k)` already contains exactly the nonzero terms in the full convolution sum for `T_f(j,k)`.  Thus

```text
A_f(j,k) = T_f(j,k) whenever max(j,k) >= m.
```

The difference `A_f-T_f` is supported entirely in the leading `m by m` corner.  The same is true for `1-f`.  Consequently the extreme-past kernels needed for `alpha_f` and `beta_f` are finite, effective inputs for every finite suffix length `r`: use the ordinary banded Toeplitz matrix and replace only its leading `m by m` corner.

Answer to the assigned question: yes, under strict positivity of both `f` and `1-f`, finite Fejer--Riesz outer factors make the extreme-past boundary kernel differ from the usual Toeplitz kernel only by a finite leading corner.  This gives true finite-`r` rate bounds via the formulas above.  It does not by itself prove that these bounds converge at any explicit rate, and no limit is differentiated.

## 4. Certificate Gates

For the S1 benchmark, reflection gives `h(f_-)=h(f_+)`.  A positive counterexample is certified once outward bounds satisfy

```text
G_pos = L_+^cert - U_0^cert > 0.
```

If the computed approximations are `Ltilde_+` and `Utilde_0` with certified absolute errors `e_L` and `e_U`, the usable gate is

```text
Ltilde_+ - Utilde_0 > e_L + e_U.
```

A strict negative exclusion of this benchmark is certified once

```text
G_neg = U_+^cert - L_0^cert < 0,
```

or, without using reflection,

```text
((U_+^cert + U_-^cert)/2) - L_0^cert < 0.
```

## 5. Benchmark Result at r=16

The script `scripts/rate_bounds.py` implements the formulas above with floating-point spectral factors and determinant arithmetic.  It is a numerical witness, not an interval prover.

The `r=16` output gives:

```text
h(f_+) in [0.69239896730095973, 0.69239896730172723]  numerical
h(f_0) in [0.69242509149653586, 0.69242509149717146]  numerical

L_+(16) - U_0(16) = -2.6124196211729789e-05
U_+(16) - L_0(16) = -2.6124194808629930e-05
```

The maximum extreme-past interval width is:

```text
f_+ : 2.5952618e-07
f_0 : 2.2718902e-07
```

No suffix interval had reversed order in the numerical run.  The finite block check also reproduces the route owner's baseline:

```text
Delta_H12 = -0.00027903229140768815
last conditional increment gap at r=12 = -2.612419544123501e-05
```

The current positive-counterexample gate is negative by about `2.6e-5`.  Thus this fixed benchmark cannot certify the desired positive counterexample through the rate bounds.  It instead appears to be a strict negative-rate case, pending outward arithmetic.

## 6. Cross-Check Against the Rational Boundary Residual

The route owner's `boundary_residual_M64.json` gives rational half-line boundary kernel enclosures with operator error upper bounds:

```text
f_0:       1.1858581e-11
f_tau:     2.0123569e-11
1-f_0:     2.3571931e-22
1-f_tau:   2.5470632e-21
```

The cross-check in `artifacts/boundary_compare.json` compares those rational leading corners with the outer-factor kernel used here.  The maximum observed corner difference is at most `8.4e-16`, comfortably below the residual certificate scale.

This means the remaining strict certificate does not need root isolation for the outer polynomial.  It can use the route owner's rational boundary-kernel enclosures directly.

## 7. Exact Remaining Gap

To turn the numerical negative exclusion into a strict certificate, one must still propagate outward errors through:

1. finite Toeplitz exact-pattern probabilities for `U_+(16)` and `L_0(16)` weights;
2. boundary determinant ratios defining `alpha` and `beta` for the `2^16` suffix words;
3. binary entropy logarithms.

The needed total slack is only

```text
2.6124194808629930e-05
```

for the reflection-based negative exclusion gate.  The available M64 boundary operator errors are `<=2.1e-11`, so the expected determinant/log interval budget is far below the gate if implemented with rational or directed high-precision arithmetic.

Executable finite workload at `r=16`:

```text
3 symbols
sum_{r=1}^{16} 2^r = 131070 suffix words per symbol
24570 block atoms for the n<=12 cross-check
largest determinant size 17 by 17
single thread, well below 4 GiB in the numerical run
```

This is a precise mechanical gap, not a mathematical missing lemma.
