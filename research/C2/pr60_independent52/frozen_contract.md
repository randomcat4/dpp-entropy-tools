# PR60 independent machine-certificate contract

Frozen PR60 source: `f869fd251c0d6fdad737b6d5efa287307795a87d`.
Frozen main: `9dcb6e9079ca57f94e0e30d63161cda89ca61fae`.
Public claim: issue52 comment5604172029.

This new unit independently checks the finite exact chain behind the
full-r Lambda-zero candidate. It is separate from completed PR57 and does
not inherit any old arithmetic window or use r=0 positivity as a premise.

## Machine obligations

1. Build the displayed Gram/Schur Rstar from its ingredients and the short
   Rbar in PR60 proof.md(16); prove the entrywise identity
   `Rbar(t=u^4)=(u/4)Rstar(u)` with exact rational arithmetic.
2. Clear denominators to Ahat and compute its determinant. Extract fresh P
   by exact polynomial division by `8tJ^3L^3C^3`, with J=1-t,
   L=1-r^2t, C=1-r^2t^2. Store the quotient, zero remainder and the determinant
   normalization; do not supply an archived P to construct the determinant.
3. Prove P is an integer polynomial and check its full coefficients. Only
   after construction compare to the six statically extracted author
   coefficient-polynomial strings, assembled as displayed in proof.md(5).
4. Independently transform P into Q under the chart
   `mu=(X-1)/(X+1),nu=(Y-1)/(Y+1),r=R/(1+R),t=T/(1+T)`.
   Verify the exact clearing identity with independent transform mechanisms.
   Check every position in the 5x5x11x7 box, including zeros. Compare the
   claimed 1731 positive entries, 194 zeros, minimum192, constant432 and
   all 25 grouped counts/minima to the frozen display.
5. Check signflip/leaf-exchange polynomial identities and the exact positive
   seed, storing complete expressions/coefficients and per-layer results.

Construction inputs are displayed formulas, not imports or execution of the
PR60 author scripts. Those script files are preserved as immutable source
references only. The old r=0 checker and its outputs are not construction
or theorem inputs. All mathematical arithmetic is exact integer/rational;
Float atoms are rejected. No numerical tolerance or sampling substitutes
for a polynomial identity.

## Scope and review roles

The source's full chart is X,Y,T>0,R>=0, covering 0<=r<1; leaf exchange
addresses r<0. Matrix normalization/symmetry/seed equalities are machine
obligations. C1 separately owns the mathematical bridge FIRST, including
correct fixed-direction meaning, full-domain coverage, nonvanishing,
inertia, integration and any extended claims in continuation.md.
C2 supplies independent machine evidence and does not certify those analytic
claims merely because arithmetic passes. C3 receives the scoped result.
No duplicate C1 FIRST or C3 SECOND is assigned here.

This unit does not check PR60's Lambda-nonzero band or radial obstruction,
PR58's 64-event certificate, PR59's finite-memory code, novelty, or Lean.
No general scan or entropy-rate calculation is launched.

## Resource and stop contract

One new total 2700-second window from the first new arithmetic launch;
one live arithmetic process, 16GiB address-space cap, no GPU. Use one CPU
and one numerical-library thread. This lies below the wider8CPU/32GiB
allocation and leaves unrelated server jobs untouched.

Freeze source before execution and record PID, UTC start, absolute hard
deadline, invocation, environment and exit. The window is shared by every
necessary bounded implementation repair and cannot be reset. Stop arithmetic
on success, a strict mathematical mismatch, or the deadline. Preserve every
completed layer and failure. No silent extension, resource increase, or
fallback to a generic scan. Root alone launches under the execution guard.

No source preparation arithmetic has run. No global software changes,
private connection data in public files, or access to C:/canglan/.