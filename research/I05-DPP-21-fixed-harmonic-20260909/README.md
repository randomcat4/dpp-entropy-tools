# I05 DPP21 fixed two-harmonic true-rate unit

Issue: #65. Branch: `research/I05-DPP-21-fixed-harmonic-20260909`.

Base: `main@9dcb6e9079ca57f94e0e30d63161cda89ca61fae`.

## Status

**PROVED (AUTHOR PROOF), NOT INDEPENDENTLY REVIEWED:**

1. the fixed path

   ```text
   f_t(theta)=1/2+(1/4)cos(4 pi theta)+(t/8)cos(2 pi theta)
   ```

   is strictly legal on `[-3/2,3/2]`, with the uniform pointwise margin `1/16`;
2. the three fixed true entropy rates satisfy the strict, rigorously certified Jensen inequality

   ```text
   h(f_1)-[h(f_{1/2})+h(f_{3/2})]/2 > 1/10000.
   ```

The second statement is a true stationary entropy-rate result, not a finite-window extrapolation. It uses exact complete-event determinants at conditioning depth `18`, directed logarithm enclosures, and an analytic conditional-mutual-information tail bound.

**INCOMPLETE:** proving `h''(t)<0` at every `1/2<=|t|<=3/2`, or finding a strict true-rate counterexample there.

No statement in this directory inherits independent acceptance from PR59. At the start of this unit PR59 had only the author's review-request comment and no substantive nonauthor verdict.

## Exact objects and conventions

All logarithms are natural. Inclusion probabilities are `det K_T`; complete events are obtained by Mobius inversion, equivalently

```text
P(X=S)=(-1)^{|S^c|}det(K-I_{S^c}).
```

Every use of `t` is the genuine affine path in the correlation kernel. No event, Fisher term, prediction acceleration, or invariant-measure response is discarded.

The finite Toeplitz compression has

```text
K_t(i,i)=1/2,
K_t(i,i+/-1)=t/16,
K_t(i,i+/-2)=1/8,
K_t(i,j)=0 for |i-j|>2.
```

## Main files

- `frozen_statement.md`: exact theorem, certificate quantifiers, and open scope.
- `proof.md`: legality, comparison-matrix inverse decay, conditional tail, true-rate Jensen passage, Poisson/correlation Hessian, and finite-memory curvature interface.
- `code/certify_midpoint_rate_gap.py`: exact integer complete-event enumeration and directed decimal logarithm certificate.
- `output/midpoint_rate_certificate.json`: frozen pass statement and exact run parameters.
- `sources.md`: primary literature and the exact role of each source.
- `attempts.md`: failed routes and why they do not imply either curvature or a counterexample.
- `verification.md`: author self-audit and independent-review contract.

The exact certificate checks its signed-event implementation against a separate inclusion-minor/Mobius implementation on all words through length six. Its main depth-18 run uses a fraction-free finite-state determinant automaton, not floating determinants.

## Heavy curvature computation

Issue #74 freezes a separate outward-rounded RPF/finite-memory curvature job for the full interval `[1/2,3/2]`. It requires a true-rate tail/resolvent enclosure; a negative finite-window Hessian is explicitly insufficient. The analytic work in this branch does not assume any result from that issue.

## Boundary of the present result

The certified midpoint gap supports concavity for one nonzero chord, but it does not imply local or global curvature. Analyticity, evenness, and the fact that `t=0` maximizes entropy do not fill that gap. The five-term/Poisson RPF response still has no general sign for this fixed process.