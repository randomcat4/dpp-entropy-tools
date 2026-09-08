# Partial Lean check: fixed frame algebra

Status: LEAN_PARTIALLY_CHECKED for the five exact integer matrix identities
in FrameAlgebra.lean; the full entropy theorem is not formalized.

Actual toolchain: Lean 4.32.0, commit
8c9756b28d64dab099da31a4c09229a9e6a2ef35, Lake 5.0.0.
No repository Lean project or Mathlib dependency was present. The installed
toolchain was selected explicitly without changing global configuration,
installing another toolchain, or downloading Mathlib.

Run from this directory with Lean 4.32.0:

```text
lean FrameAlgebra.lean
```

Exit code: 0. The accompanying build.log records that every proved statement
depends only on propext. The source contains no admitted goals, extra axioms,
or unsafe proof bypasses.

The formal matrices use zero-based Fin 4 indices and are exactly the integer
A and B printed in Section 2 of the v2 proof. Checked facts are A^2=I,
B^2=I, AB=-BA, (AB)_(0,3)=-1 and AB != BA. Matrix multiplication is written
as the explicit sum of four integer products. This checks the fixed algebra
data; it does not encode real-valued parameter formulas, spectral
feasibility, entropy, event probabilities, or asymptotic remainders.
Those claims retain their separate natural-language review status.
