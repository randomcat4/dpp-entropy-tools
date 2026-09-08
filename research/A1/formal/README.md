# Formalization coverage

No Lean theorem is claimed. The isolated A1 repository contains no
lean-toolchain, lakefile, existing Lean development or DPP/entropy Mathlib
interface. The installed toolchains were inspected without downloading or
changing them; the available Lean 4.32.0 executable returned version
`4.32.0`, commit `8c9756b28d64dab099da31a4c09229a9e6a2ef35` (exit 0).

This is an L0 toolchain probe only. The present mathematical results are
natural-language proofs, exact symbolic identity checks, and rational
logarithm certificates, followed by independent review. There is no
`LEAN_PARTIALLY_CHECKED` or `LEAN_FULLY_CHECKED` status.

Encoding the full DPP law, its differentiability, and the previously proved
two-point theorem would require a separate formalization project. Compiling
an isolated rational inequality would not certify that missing interface and
was not substituted for it.
