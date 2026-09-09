# Remaining-window continuation ledger

Original absolute execution window: 2026-09-09 11:22:28–12:07:28 UTC.

| Arithmetic PID | Owner | Start UTC | End UTC | Outcome |
|---|---|---|---|---|
| 172454 | Compute author | 11:22:28 | 11:54:46 | Scoped implemented derivation checks pass; both factor stages hit JSON Integer serialization error |
| 173320 | C2 root | 11:59:57 | 12:00:41 | Saved Rstar second/third/fourth determinants and factors, both cases |
| 173433 | C2 root | 12:03:32 | 12:03:33 | Exact residual-polynomial coefficient tables, both cases |

All three wrapper exits were 0, but the original per-stage errors are preserved
and must not be overridden by the wrapper code. All author PIDs were confirmed
exited before ownership passed to the fresh r=0 reviewer. There was never more
than one live arithmetic process. Each used one thread, CPU affinity, a 16 GiB
virtual-memory limit, no GPU, and an external timeout at the original deadline.

The initial intended one-process pipeline stopped because of an implementation
error. The sequential repair and coefficient phase were publicly recorded
before launch in issue52. They consumed only the remainder of the original
window; no new 45-minute allocation or duplicate reconstruction was used.

`continue_saved_rstar.py` was frozen at local commit
`af7ef42c6fc3f8e02dff0607a0e08b8f60c4b7d8` before launch; the coefficient
checker was frozen at `3eb686784fc8e0c08c73aab21024523e34483b0d`. Both exact
scripts are also included unchanged in candidate commit
`521e96c6027c14a61d60fea8e031f874ef14f1e0`. The original executed source has only
the one documented environment-recording difference from its portable public
copy. Matrix data and coefficients were not changed when sanitizing metadata.

The determinant continuation uses exact rational-function DomainMatrix
arithmetic on the saved four-dimensional matrices; it does not import the
original checker. The coefficient phase reads the saved fourth determinant's
residual factor and performs integer binomial transformations. Neither phase
performs a scout. Fresh review, not these author statuses, decides acceptance.
