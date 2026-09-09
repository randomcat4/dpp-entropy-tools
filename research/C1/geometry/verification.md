# Verification boundary

Author analytic checks: probability signs and powers, all six affine
directions, off-diagonal factors, exact Fpair projection, near-boundary
N positivity, full M solve rather than arbitrary Lambda tangent, explicit
common-event Fisher cross term, positive reduced determinant, elementary
endpoint signs and IVT zero existence were checked in the proofs.

Author arithmetic: probe.py uses the eight-event polynomials and
mpmath differentiation in each of the six actual matrix coordinates.
Nine prescribed full-support points used 100 decimal digits; six prescribed
sparse points used 110 digits. One additional sparse point audited the
failed reduction's individual M entries and exposed the missing common
term. These runs are floating point diagnostics, not interval certificates.
The failed theoretical predictions remain labeled in attempts.md.

Nonauthor review: the parent reported CORRECT for the frozen proof.md from
its independent audit child. This geometry child did not read or write that
review. The sparse_proof.md candidate was submitted for independent review
after freezing. As of this handoff, its status is PENDING. The parent and
geometry child jointly checking a formula does not count as independent
review. A second new-context review is the parent's responsibility.

No Lean check, global B0 certification, explicit numerical asymptotic
threshold or finite-epsilon zero uniqueness certificate was performed.
