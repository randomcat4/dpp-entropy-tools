# Problem

## Original Problem

Build a reusable T3 toolchain for strict finite DPP entropy calculations. The
tool must accept a rational kernel `K`, rational direction `D`, a path interval
or chord points, and precision/certification settings; it must return strict
feasibility information, exact or interval-enclosed event probabilities, entropy
curvature or chord gap bounds, a coverage report, and explicit failure reasons.

The first run target is a minimal closed loop: certify or refuse one
non-trivial all-subsets finite DPP entropy chord gap for small rational input.

## Target Strength

Reference prototype plus sound certificate schema. A positive result is a
machine-reproducible finite certificate, not a theorem about all DPP kernels.

## Original Source, Intent, And Prior Value

- Source: public issue #3 and `prompts/T3.md` in this repository, started
  2026-09-07.
- Intent: make a correctness-first tool that can later serve T1/T2 by checking
  small rational objects and rejecting floating-point false positives.
- Forbidden trivial reading: computing `det(K_S)` for exact events. That is an
  inclusion probability for a marginal-kernel DPP, not the full event mass
  except in special degenerate cases.
- Precommitted value: a reusable, independently reproducible certificate path
  with clear coverage and refusal behavior.

## Acceptable Results

- A strict certificate for a finite rational chord instance.
- A deterministic refusal with a minimal failure reason.
- A reliable independent reference enumerator that catches formula or
  floating-point mistakes.
- A precise blocker showing which extra arithmetic or interval method is needed.

## Disallowed Shortcuts

- Replacing exact all-subsets masses by principal minors alone.
- Adding an arbitrary epsilon to hide `p = 0`.
- Treating finite numerical non-failure as a general theorem.
- Using ordinary floating point, automatic differentiation, or symbolic
  recurrence output as a strict certificate without outward rounding and a
  checkable error bound.
- Deleting failed certificates, false-positive examples, or refusal records.
