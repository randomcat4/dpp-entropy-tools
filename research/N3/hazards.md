# Mathematical hazards

- Quantifiers: all real symmetric directions and arbitrary strict kernels;
  no replacement by eigenvalue-only, PSD-only or commuting directions.
- Exact atoms: inclusion minors must undergo Mobius inversion; entropy of
  cardinality is a different functional.
- Coordinates: off-diagonal basis directions alter two matrix entries;
  weighted traces and Hessian derivatives retain the factor two.
- Stationarity: the target optimizer minimizes A=F+det(N)G, not F alone.
  The final stationary certificate encloses the exact solve, not a rounded
  direction advertised as exact.
- Projection: Q_k and F_pair are smaller than F. Nonnegative discarded
  information may be essential, even at the true optimizer.
- Boundaries: rare atoms have different scales. Large Fisher contributions
  and their cancellation in a projection require explicit remainder control.
- Sign: B=-Hess H; positive B is negative entropy curvature. A shortcut's
  negative gap is not a positive entropy chord.
- Certification: numerical scouts, exact finite certificates, analytic
  family results, independent review and novelty have separate labels.
- Circularity: SM-close is EQUIVALENT_BLOCKER; no general matrix identity
  can substitute for the missing DPP-specific alignment lower bound.
