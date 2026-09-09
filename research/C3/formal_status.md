# Formal verification status

The inherited repository contains an unrelated A2 exact-matrix Lean project
pinned to leanprover/lean4:v4.32.0. The installed-toolchain inventory and the
actual executables were checked. Reported versions:

    Lean 4.32.0, commit 8c9756b28d64dab099da31a4c09229a9e6a2ef35
    Lake 5.0.0-src+8c9756b (Lean version 4.32.0)

Both version commands exited 0. The inspected runtime provides Init, Std,
Lean and Lake; no Mathlib project/cache was identified in the inspected
existing proof setup. A2's file proves unrelated integer matrix identities.

This is an L0 toolchain feasibility check only. No C3 theorem was encoded
or compiled. The central analytic KL/derivative/entropy-rate statements have
not been checked by Lean. No toolchain or Mathlib download was initiated,
and no version was changed. There is no LEAN_FULLY_CHECKED or
LEAN_PARTIALLY_CHECKED claim for C3.
