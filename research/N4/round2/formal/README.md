# Mechanical verification scope

Status: TOOLCHAIN_SMOKE_ONLY. No Lean proof of a round-two mathematical
statement has been completed. This is not LEAN_PARTIALLY_CHECKED.

The inherited read-only A2 example pins leanprover/lean4:v4.32.0 and imports
Std only. On 2026-09-09 the installed versions 4.29.0, 4.30.0 and 4.32.0 were
listed, then explicit 4.32.0 lean/lake version commands exited zero:
Lean 4.32.0, commit 8c9756b28d64dab099da31a4c09229a9e6a2ef35;
Lake 5.0.0-src+8c9756b. The configured shared Mathlib cache was absent.
No other route was modified and no dependency download was started.

The analytic DPP/entropy statements have not been translated, built or
audited by Lean. Exact Fraction arithmetic and rational logarithm intervals
are finite computational certificates, not kernel-checked general theorems.

