# S1 FIRST review of PR117

Status: **ACCEPTED_SCOPED**.

This packet is an independent, version-bound mathematical FIRST review of
PR117, frozen at head
`70d69bf5c47282c953010518ff264cb2a7a09bf9` against base
`bcbf7016e2abc6401b66f39ac9202d235ee32fad`.

The accepted scope is the author theorem for every strict half-period-even
`c in A_0` and nonzero half-period-odd `g in A_0`: for each odd `k` with
`g_hat(k) != 0`, the true stationary DPP complete-configuration Shannon
entropy rate has a nonempty symmetric interval on which

`h(c+t g) + |g_hat(k)|^4 t^4/[8 mu^2(1-mu^2)]`

is concave.  The physical path is `K_t=T(c)+tT(g)`.

The review independently checked the finite-range preconditioner, the real
trace-log branch, configuration-local inverse approximation, the corrected
support count, Bell differentiation of the complete law, absolute
displacement and walk-length domination, both thermodynamic passages, and
the parity/matching curvature step.  In particular, the proof does not use a
common `ell^1` envelope for the reference inverses.

See `review_report.md` for the audit and `frozen_scope.md` for exclusions.
