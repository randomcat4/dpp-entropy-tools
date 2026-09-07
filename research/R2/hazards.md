# Hazards

- **Sign convention:** `Delta=average endpoints-midpoint`; positive is the
  desired violation.
- **Exact events:** all entropy terms use Mobius-inverted exact masses.
- **Two levels of variation:** each chord is affine at fixed `epsilon`, while
  its center and sampled half-length vary across the outer family.
- **Feasibility:** formal off-block tangents at an exact projection are not
  two-sided feasible; the diagonal `epsilon` buffer is essential.
- **Zero probabilities:** events absent at `P` can appear at orders
  `sqrt(epsilon)`, `epsilon`, or higher at the amplitude level.  Entropy uses
  probability, not amplitude, scales.
- **Plucker zeros:** size-`r` coordinate events with `det(U_S)=0` can acquire
  order-`epsilon` mass after the subspace rotates and contribute a logarithmic
  term.
- **Spectral defects:** one missing occupied mode and one selected empty mode
  are distinct first-order classes; dropping either loses a factor.
- **Remainders:** pointwise `o(epsilon log(1/epsilon))` is insufficient for the
  displayed `O(epsilon)` claim unless all finitely many event classes are
  controlled.
- **Multiplicity:** repeated eigenvalues require subspace/projector reasoning,
  not individually labeled eigenvector derivatives.
- **Gauge:** `phi_S` must be invariant in `Z` under fixed orthogonal changes of
  the chosen `U,V` frames, even though individual signed amplitudes vary.
- **Boundary value:** `tau||B||_op=1` may create exact 0/1 eigenvalues and is
  excluded from frozen v1.
- **Scope inflation:** a negative asymptotic coefficient excludes only this
  family; it is not evidence of global concavity.
- **Singular Schur residuals:** residual PSD is insufficient without kernel
  annihilation; the scalar residual-zero example is infeasible at every small
  scale.
- **Signed cofactors:** deletion cofactor vectors require alternating column
  signs. Omitting them preserves some diagonal checks but creates false
  off-diagonal tomography kernels in rank at least three.
- **Gate ordering:** a positive `C_2` is irrelevant unless every earlier
  coefficient, including the finite order-`epsilon` coefficient, vanishes.
- **Unequal scales:** multiple-flip baseline mass may exceed the target
  transverse scale. The proof must bound its entropy change, not its absolute
  entropy.
- **Tomography equality:** matching only traces is weaker than matching every
  one-hole and one-particle exact-event rate.
