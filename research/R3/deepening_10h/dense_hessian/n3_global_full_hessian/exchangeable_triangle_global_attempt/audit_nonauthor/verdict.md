# D10-U10h fresh non-author audit verdict

STATUS: INCOMPLETE_GLOBAL

Layered audit result: the new algebraic identities and the four compact
boundary-strip proof candidates pass my independent checks.  The full
exchangeable-triangle domain remains INCOMPLETE exactly as the author states:
corner approaches and the separated compact middle are not certified.

## Frozen inputs

Complete SHA-256 input table is in `results.json`.  Key frozen inputs:

- `exchangeable_triangle_global_attempt/proof_or_blocker.md`
- `exchangeable_triangle_global_attempt/sanity.py`
- `exchangeable_triangle_global_attempt/sanity.json`
- `exchangeable_triangle_subfamily/fresh_audit.md`
- `exchangeable_triangle_subfamily/proof_or_blocker.md`

The author `sanity.json` source hashes for `frozen_problem.md`,
`proof_or_blocker.md`, and `sanity.py` match the current files.

## Fisher missing-information formula

The rank-one formula

```text
F = diag(u,2v) - kappa (u,-v)(u,-v)^T
```

is correct.  I checked the three rational Fisher identities exactly after
clearing denominators with an independent bivariate `Fraction` polynomial
engine.

The factor `2` in the beta complete-data Fisher is necessary.  The audit
script explicitly tests the wrong `diag(u,v)` variant and confirms the
`bb` identity becomes a nonzero polynomial.  Direct latent checks at
`(alpha,beta)=(1/5,2/5)` and `(3/7,5/8)` give the same `kappa` as the
author formula; dropping the factor two halves the missing-variance value.

## `n_beta` / `n_alpha` placement

The log-acceleration grouping is correct:

```text
C_ab = F_ab - 2 n_beta,
C_bb = F_bb - 2 n_alpha.
```

Layerwise exact polynomial checks verify:

```text
mult_k p_k,ab = 2(ell_coeff_k + beta Lambda_coeff_k)
mult_k p_k,bb = 2(ell_coeff_k + alpha Lambda_coeff_k).
```

Independent Decimal samples match the direct entropy Hessian with residual
at most `1e-166`.  Swapping the placements produces visible errors, e.g.
about `2.59e-2` at `(0.2,0.4)` and about `13.94` near `(0.01,0.99)`.

## Boundary strips

The two normalized edge limits are consistent and have the stated positive
targets:

```text
alpha Delta_T -> beta^2 L(beta),
beta  Delta_T -> 2/(1-alpha),
L(beta)=2/[beta(1-beta)]-2 log(4/3)>0.
```

The complemented edges follow by true DPP complementation:

```text
(1-alpha) Delta_T -> (1-beta)^2 L(beta),
(1-beta)  Delta_T -> 2/alpha.
```

At `epsilon=1e-20`, representative relative errors are around `1e-17` in
the independent Decimal checks.  These computations are sanity checks only;
the proof mechanism is the asymptotic expansion plus compact transverse
intervals.

The uniform-remainder argument is sound for every fixed `r>0`: away from
corners, all non-vanishing atoms are uniformly bounded below, rational
derivatives are uniformly bounded, and the small parameters times powers of
`|log epsilon|` vanish uniformly.  The strips therefore have existential
width `epsilon_r`, but no effective width is certified.

## Full `Sym(3)` quantifier

The full-Hessian statement is legal only through the already-reviewed U10f
standard-block theorem:

1. U10f gives the exact `S3` split into the invariant two-dimensional block
   and a strictly positive four-dimensional standard block for every strict
   connected exchangeable triangle.
2. U10h proves `Delta_T>0` only in the four compact boundary strips.
3. Combining these gives full `Sym(3)` positivity in those strips.

This does not re-prove U10f, does not provide a uniform standard-block
eigenvalue at the boundary, and does not cover the full square.

## Blockers and invalid shortcuts

The alpha/beta swap is not an entropy symmetry.  The exact witness is
independently reproduced:

```text
125[H(1/5,2/5)-H(2/5,1/5)]
 = 226 log 2 - 71 log 3 + 28 log 7 - 38 log 19 != 0.
```

Nonzero prime exponents certify non-equality by unique factorization.

The shortcut `C_ab>=0` is false.  Near `beta->0`, independent samples show
`C_ab<0`; for example at `(alpha,beta)=(0.5,1e-6)`,
`C_ab≈-20.0474897` while `Delta_T≈3.9995e6>0`.  This confirms the author's
blocker: the positive `C_bb` pole, not entrywise positivity, controls the
mixed logarithmic term.

## Author finite sanity

The frozen author sanity denominator is internally consistent:

```text
base=6, boundary=60, diagonal=20, total=86,
failures=0, positive_curvature_candidates=0.
```

This remains finite SCOUT.  It is not an interval proof and not a global
certificate.

## Final classification

- Analytic identities: PASS.
- Fisher factor two: PASS.
- `C_ab/C_bb` placement: PASS.
- Four compact boundary-strip candidates: PASS, with existential widths.
- Complemented opposite edges: PASS.
- Full `Sym(3)` strip conclusion via U10f: PASS within that dependency.
- Swap symmetry shortcut: REJECTED.
- `C_ab>=0` shortcut: REJECTED.
- Global `Delta_T>0` on the full strict square: OPEN / INCOMPLETE.

No critical gap was found in the scoped U10h boundary-strip candidates.
