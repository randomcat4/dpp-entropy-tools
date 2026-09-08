# D10-U6/S10 verdict

STATUS: `CORRECT`. A fresh non-author audit is preserved under
`verifications/`.

Assuming the already independently verified U3/S9 theorem, every strict
diagonal kernel is a boundary point of the open set of
full-Hessian-negative kernels.  Almost every zero-diagonal puncture direction
on the sphere (open, dense, full measure) enters that set for all sufficiently
small nonzero radii.  Uniformly over a compact diagonal box, every fixed
full-edge angular sector `min|A_ij|>=eta` has one common small radius and
positive angular measure. The audit separately checked the two-point sphere
case `n=2`, the Frobenius normalization, the compact-uniform quantifiers, and
the ambient-measure passage.

This is a topological/measure corollary, not a claim that negative-Hessian
kernels are dense throughout the full strict domain. The zero-diagonal radial
sector itself has zero ambient measure; positive ambient measure follows by
choosing one punctured point in the negative-Hessian set and then using ambient
openness.
