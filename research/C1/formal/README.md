# Formal verification scope

NO_FORMAL_PROOF_OF_B0. The source repository includes an unrelated A2 Std-only Lean component pinned to leanprover/lean4:v4.32.0. That pin was inspected, and installed toolchains 4.29.0, 4.30.0 and 4.32.0 were listed before invoking Lean. Actual L0 checks succeeded:

    lean +leanprover/lean4:v4.32.0 --version
    lake +leanprover/lean4:v4.32.0 --version

Outputs: Lean 4.32.0, commit 8c9756b28d64dab099da31a4c09229a9e6a2ef35; Lake 5.0.0-src+8c9756b. This is only toolchain availability, not a proof check. No C1 formal theorem was created, no target axiom audit was claimed, and no unrelated old theorem was relabeled as C1 coverage. The asymptotic matrix/logarithm analysis requires analytic library and statement work beyond the existing Std-only component. No toolchain or library was downloaded.
