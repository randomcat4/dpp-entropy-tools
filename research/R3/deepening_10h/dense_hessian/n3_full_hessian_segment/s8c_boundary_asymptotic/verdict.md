# D10-S8c verdict

STATUS: `CORRECT`. A fresh non-author audit is preserved under
`verifications/`.

The full real Sym(3) entropy Hessian is strictly negative definite at every
K(t) on 29/100 <= t < 3/10. This covers arbitrary symmetric directions,
including noncommuting directions, not just the tangent of the frozen line.

Only the empty atom vanishes at the endpoint, to first order; a
congruence-scaled Hessian limit has a positive pole component, two positive
logarithmic components and a positive finite 3x3 block. An analytic scalar
Schur majorant, certified by rational interval arithmetic, covers
[299/1000,3/10). Six rational congruence leaves cover [29/100,299/1000]. Thus
this is a continuous-interval proof, not a finite scout inference.

The endpoint is excluded. No global entropy concavity, uniform endpoint spectral margin, or full boundary Hessian is asserted. Each interior point has an ambient open neighborhood by continuity, but no uniform neighborhood radius is supplied.

The h=1/100 coarse tail bound failed and is retained. No positive curvature was
observed or claimed. The audit independently rebuilt the exact-event/Mobius
atoms and full six-coordinate interval Hessian, checked the bridge and tail
certificates, and found no blocking gap. Existing S8/S8b files were not
modified.
