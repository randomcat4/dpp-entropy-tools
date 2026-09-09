# Status

2026-09-09 11:34 UTC: RUNNING, analytic formula audit and independent structural review complete; global sign remains open.

- Complete literal input and author continuation source are frozen.
- Main queue was read; the PR47 merged successor is preserved by publishing only this new subtree on a separate branch.
- Three bounded direct tasks are assigned: computation, analytic formula audit, analytic structure attack. Only the computation unit may launch arithmetic.
- Initial process budget is one shared 2700-second execution window, one thread, 16 GiB, no GPU.
- The fresh analytic event-to-M audit is `CORRECT` at the identity scope. It reconstructs all eight atoms, first jets, Fisher split, second-jet log coefficients, Lambda-zero cancellation, Q signs/factors, constant marginal derivative and initial matrix. No arithmetic process was used for this review. See `formula_review/FORMULA_REVIEW.md`.
- The structural unit produced an exact 2+4 congruence/Schur reduction of the already formed M. Its two Fisher-invisible directions have a positive diagonal block; an explicit four-dimensional matrix retains the remaining sign obligation. A fresh nonauthor analytic review is `CORRECT_WITH_SCOPE` for the complete reduction, including the fixed-direction derivative bookkeeping, Schur factors, and inverse map. See `structure/STRUCTURE.md` and `structure_review/REVIEW.md`.
- A separate reviewed determinant addendum gives `det M = 16*n1*n2*u^12*a^5*b^5*v*w*det Rstar`. This reduces the determinant sign obligation but does not settle it. Root separately verified that the review's local source subtree equals the named public source subtree; see `source_version_notes.md`.
- Independent machine reconstruction and the bounded sign computation remain with the sole execution owner. Both initial analytic units and the fresh structural review have finished. No computation PID or global sign result has yet been reported.

The half-filled root theorem remains with C3. No general Lambda-zero sign is assumed from that theorem or from previous floating scouts.
