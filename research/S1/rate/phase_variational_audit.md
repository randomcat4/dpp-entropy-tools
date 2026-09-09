# Audit of the P0 Variational Rate Certificate

STATUS: `CORRECT` for the stated fixed P0 pair at route-owner commit `3c01dc00a663f1fa854c57ee23d52e327b8c1e32`.

This audit covers only the second fixed pair exclusion.  It does not prove or disprove Lyons--Steif entropy-rate concavity.

Audited files:

- `research/S1/main/phase_candidate.json`
- `research/S1/main/phase_boundary_M64.json`
- `research/S1/main/phase_variational_M64.json`
- `research/S1/main/variational_boundary.py`
- `research/S1/main/variational_boundary_proof.md`
- `research/S1/main/phase_rate_n8.json`
- the unchanged `research/S1/main/rational_rate_certificate.py`

## Fixed Object

The candidate is:

```text
p = 1/2
a = (3/10, 3/25, 1/25)
b = (0, 3/25, -1/25)
tau = 1/8
epsilon = 1/50
```

The margin is valid by the triangle bound:

```text
sum |a_k| + tau sum |b_k|
= 3/10 + 3/25 + 1/25 + (1/8)(3/25+1/25)
= 23/50 + 1/50
= 12/25 < 1/2,
```

so `1/2 - 12/25 = 1/50`.  The recorded `epsilon=1/50` is exactly the triangle-bound margin and is safe for both `f_t` and `1-f_t`.

## Variational Identity

Let `T >= epsilon I` be the half-line past Toeplitz operator, `B` the past-to-future block, `C` the future block, `Y=T^{-1}B`, and `R=B-TX` for a finitely supported rational approximation `X`.

The true all-one boundary kernel is

```text
C_infty = C - B* T^{-1} B.
```

Define

```text
H_X = B*X + X*B - X*T*X,
A_X = C - H_X.
```

Then

```text
A_X - C_infty
= B*T^{-1}B - B*X - X*B + X*T*X
= (B-TX)* T^{-1} (B-TX)
= R* T^{-1} R.
```

Thus `A_X-C_infty` is positive semidefinite and has operator norm at most

```text
||R||_F^2 / epsilon.
```

The script uses the already recorded rational residual bound `r_bound >= ||R||_F`, so its `delta = r_bound^2/epsilon` is a valid rational operator-norm error.  This is stronger than the prior linear residual estimate and does not require trusting the numerical solve that originally proposed `X`.

## Code Check

`variational_boundary.py` recomputes `R` exactly from the candidate coefficients and dyadic `X`, checks that the recomputed `r_bound` equals the recorded residual bound, reconstructs the old corner, and checks exact equality with the prior `corner_rational`.  Only then does it apply

```text
corner = old - sym(X*R).
```

Because

```text
sym(X*R) = sym(X*B) - X*T*X,
```

and `old = C - sym(B*X)`, this gives

```text
corner = C - B*X - X*B + X*T*X = A_X.
```

The four recorded variational error bounds are:

```text
t=0,   f:     1.41161563e-56
t=0,   1-f:   5.97468879e-15
t=1/8, f:     1.96349675e-53
t=1/8, 1-f:   1.22982113e-14
```

All are far below `epsilon=1/50`, so the previously audited Schur conditional-probability perturbation bound applies unchanged.

## Independent Outer-Factor Comparison

Using my existing outer-factor boundary implementation, the leading `3 by 3` variational corners agree numerically with the Lyons--Steif outer kernels:

```text
t=0,   f:     max difference 5.75773838e-17
t=0,   1-f:   max difference 1.86304162e-16
t=1/8, f:     max difference 1.33226763e-15
t=1/8, 1-f:   max difference 1.33226763e-15
```

This confirms that the variational correction is still approximating the same extreme-past boundary kernels used by the rate proof.

## Rate Certificate Applicability

`phase_rate_n8.json` uses the unchanged, previously audited `rational_rate_certificate.py`; its source hash is still:

```text
d94a0794927102e7b530319f196db34abe8b28be4a0a6594d4f4a7e8c7125b5b
```

The phase variational boundary artifact hash used by the rate certificate is:

```text
a0e34915741a58bbd790b0ba69bc0716eaa924ceb8e984ec1fcf6d53566efa23
```

The run enumerated `3072` exact determinants, checked exact rational normalization, and evaluated logarithms with interval arithmetic.  Its final gap enclosure is:

```text
lower = -5.826508824139247e-06
upper = -4.7241912213614966e-06
```

The upper endpoint is strictly negative, so the fixed P0 pair is rigorously excluded as a positive counterexample once the audited source facts are accepted.

## Independent Rate Comparison

My outer-factor finite-suffix implementation, without the route-owner interval machinery, gives:

```text
r=8:
  L_+(8)-U_0(8) = -5.82650604108e-06
  U_+(8)-L_0(8) = -4.72419257302e-06

r=12:
  L_+(12)-U_0(12) = -5.27445936793e-06
  U_+(12)-L_0(12) = -5.27045721932e-06
```

The `r=8` values fall inside the strict n=8 enclosure, and the `r=12` values support the same negative sign.

## Notes

No critical gaps were found.  A minor bookkeeping note: the existing `frozen_objects.json` I read still appears to describe the earlier B0 object, so I did not rely on it as the P0 manifest.  The audited P0 object is instead pinned by commit `3c01dc00a663f1fa854c57ee23d52e327b8c1e32`, `phase_candidate.json`, and the hashes recorded in `phase_rate_n8.json`.

The result is a second fixed-pair exclusion only.  It does not certify a phase-family theorem, a mixed-edge dominance theorem, or the global scalar entropy-rate conjecture.
