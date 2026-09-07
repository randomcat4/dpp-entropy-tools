# Local Toolbox Exclusion Table

## Problem And Frozen Version

- Problem: T3 strict finite DPP entropy certificate tools.
- Frozen version: `frozen_theorem_v1.md`.
- Date: 2026-09-07.
- Maintainer: T3 main instance.

## Exhausted Or Excluded Local Tools

### TOOL-1: Large Random Scans

- Family: high-throughput random search over kernels/directions.
- Native formulation: sample many finite DPP kernels and estimate entropy signs.
- Status: EXCLUDED_BY_USER.
- Basis: AGENTS.md, COMMON.md, and T3.md all require first building a reusable
  tool and explicitly forbid replacing this phase with large brute-force scans.
- 0D exclusion scope: exclude random-search throughput as evidence for v1.

### TOOL-2: Ordinary Floating Point As Certificate

- Family: double precision, autodiff, or high precision without outward error
  control.
- Native formulation: compute probabilities and entropy values numerically and
  read off the sign.
- Status: EXCLUDED_BY_USER.
- Basis: T3.md requires rational/interval envelopes and rounding direction for
  strict conclusions.
- 0D exclusion scope: exclude certificate claims whose only sign evidence is
  ordinary numeric evaluation.

### TOOL-3: Inclusion-Minor Entropy

- Family: using only `det(K_S)` as if it were the probability of exact event
  `X = S`.
- Native formulation: compute `-sum_S det(K_S) log det(K_S)`.
- Status: KNOWN_BARRIER.
- Basis: T3.md warns that exact all-subsets DPP probabilities must not be
  confused with inclusion-event principal minors.
- 0D exclusion scope: exclude any tool that does not perform Mobius inversion
  or an equivalent exact-event calculation.

### TOOL-4: Epsilon Regularization Of Zero Probabilities

- Family: replace `p=0` by `p=epsilon` before logging.
- Native formulation: add a small positive constant to avoid `log(0)`.
- Status: EXCLUDED_BY_USER.
- Basis: T3.md requires mathematical limits for zero probability.
- 0D exclusion scope: exclude ad hoc smoothing as certification.

## Boundary Notes

- External interval arithmetic, exact algebra, Sturm or Bernstein polynomial
  methods, and formal proof tooling remain allowed if recorded and reproducible.
- Diagnostic floating-point scripts are allowed only when labeled
  diagnostic-only and cross-checked before certification.
- Literature status remains preliminary until fuller prior-art audit.

## Compact Exclusion List For 0D

- Large random scans: scope=throughput or finite non-hit evidence for v1;
  basis=user and repo protocol excluded it.
- Ordinary floating point/autodiff: scope=strict certificate sign claims;
  basis=no outward error control.
- Inclusion-minor entropy: scope=exact event entropy for marginal-kernel DPPs;
  basis=wrong event formula outside special cases.
- Epsilon smoothing: scope=handling `p=0`; basis=must use `0 log 0` limit.
