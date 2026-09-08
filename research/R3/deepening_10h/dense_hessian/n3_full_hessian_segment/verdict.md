# D10-S8 author verdict

STATUS: `CORRECT` for the stated continuous interval certificate;
`INCOMPLETE` globally.  A fresh non-author audit is preserved under
`verifications/`.

The S8 work produces a genuine continuous full-Hessian certificate, not just a
finite grid.  Along the M8 Section 5 rational line

\[
K(t)=K_0+tR
\]

the exact-event Shannon entropy Hessian is certified strictly negative
definite on the whole six-dimensional observation-coordinate space
`\mathrm{Sym}(3)` for every

\[
t\in[-6/25,6/25].
\]

This strictly contains the originally prioritized M8 product-certified
`|t|<=1/100` segment and expands the S5 phenomenon from a single point/tiny
ball to a visibly nondegenerate rational interval.

What is proved by the candidate certificate:

- continuous interval coverage by rational subdivision;
- exact-event semantics from
  `p_S=(-1)^|S^c|det(K-I_{S^c})`;
- rigorous natural-log intervals;
- strict Gershgorin positivity of `B=-Hess H`;
- full symmetric directions, hence arbitrary PSD/NSD and noncommuting
  directions on this segment.

What is not proved:

- no global dense-Hessian theorem;
- no theorem for every M8 product-region kernel;
- no proof that `49/200` or `1/4` actually fail mathematically;
- no novelty or external-prior certification;
- no claim beyond the independently checked interval certificate.

Boundary attempts were retained.  The current Gershgorin certificate closes at
`6/25` and fails at `49/200` and `1/4`; float grid probes at those failed radii
remain negative, so the blocker is the proof method rather than a known positive
curvature direction.

The fresh audit independently rebuilt the exact-event jets, six-coordinate
Hessian, rational logarithm intervals, all 173 subdivision leaves, and the
Gershgorin test without importing the author certificate module.  It found
zero failed leaves, minimum certified row margin
`0.0002662575324700432790390645911...`, atom lower bound
`63029/5000000`, and strict spectral margin `1/25`.  It also checked the
connected, heterogeneous-diagonal, and distinct-spectrum assertions exactly.
