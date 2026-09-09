# Formal feasibility

The inherited project pins leanprover/lean4:v4.32.0. This run actually probed
Lean 4.32.0 (commit8c9756b28d64dab099da31a4c09229a9e6a2ef35) and Lake
5.0.0-src+8c9756b; both probes exited 0. See toolchain_probe.txt.

The public main tree contains the older standalone formal directory but no
Mathlib/lakefile project covering these entropy, matrix-operator and stochastic
coupling proofs. There is no low-cost existing formal implementation of the
new load-bearing results to build. No new Lean theorem was created or checked,
and no global toolchain or library was installed. Status: L0 environment only.
