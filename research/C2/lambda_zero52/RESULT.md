# Bounded result: partial progress, global sign open

The initial issue52 computation and its remaining-window repair are complete.
All author arithmetic PIDs have exited. No arithmetic was launched by the
fresh r=0 reviewer after the original deadline.

| Claim or artifact | Disposition |
|---|---|
| Eight-event analytic derivation of the literal M | Independent analytic audit CORRECT |
| Exact 2+4 Schur reduction and determinant bookkeeping | Two nonauthor structural audits accept the scoped algebra |
| Positive seed at mu=nu=r=0, u=1/2 | Separate nonauthor review CORRECT |
| Implemented machine event/Fisher checks | Pass, with the explicit analytic log-derivative dependency retained |
| Original determinant run | Both stages failed on JSON Integer serialization; failures preserved |
| Repaired r=0 and full-r fourth determinants | Computed and factored from saved Rstar, within the same original window |
| r=0 coefficient certificate candidate | 389 positive nonzero coefficients; fresh review INCOMPLETE, not ERROR |
| Full-r coefficient test | 6415 positive and 146 negative nonzero coefficients; no sign certificate |
| Rational negative direction or entropy counterexample | None produced |

The r=0 review accepts the analytic domain, sign and inertia implication
conditional on the recorded exact identities. It did not independently rebuild
the chain `Rstar -> det -> P -> Q`: its clock check was after the hard arithmetic
deadline, so no review arithmetic was launched. See `r0_review/REVIEW.md`.
The candidate is not promoted to an independently certified r=0 theorem.

For a complete r=0 acceptance, the remaining concrete obligation is a fresh
independent check of the saved Schur matrix, determinant factor and full integer
Cayley expansion. C3 reserves a separate second analytic/source/certificate
audit and owns integration; C2 has not started a duplicate second or a new
arithmetic allocation.

For full r, the exact determinant factor and transformed coefficient table are
saved, but mixed coefficients show only failure of this sufficient test. They
do not exhibit a negative polynomial value or an M obstruction. A genuine
global domain certificate or exact negative point/direction is still needed.

Start with `resume/R0_CANDIDATE.md` for the proposed r=0 proof, `resume/outputs/`
and `resume/coefficient_outputs/` for the exact objects, and
`resume/RUN_LEDGER.md` plus `compute/REPORT.md` for execution and failure scope.
