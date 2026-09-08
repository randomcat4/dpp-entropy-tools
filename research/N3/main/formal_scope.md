# Formal verification scope

The archived A2 formal project pins Lean 4.32.0. This installation was found
locally, and the explicit commands `lean +leanprover/lean4:v4.32.0 --version`
and `lake +leanprover/lean4:v4.32.0 --version` exited 0, reporting Lean 4.32.0
and Lake 5.0.0. This is only a toolchain feasibility check.

No N3 Lean theorem is supplied or claimed. This unit's nontrivial certificates
use exact rational arithmetic, rigorously enclosed logarithms and interval
linear solves. Their code and the translation of the mathematical claim
require independent review. The elementary score projection identities have
written proofs; no general entropy theorem has been obtained to formalize.
No other route's formal files or toolchain versions were modified.
