# S1 FIRST of PR130

Status: **ACCEPTED_SCOPED**.

This packet independently reviews all four author files in PR130 at immutable
head `4cae5c29effcf01b1fadc7452780b73a58ec94e7`, against base
`1d440702b16b8e65954edde076686dba8f1901ae`.

For every strict bounded half-period-even center `c` and every nonzero bounded
half-period-odd direction `g`, the submitted complete-law argument proves

`0<=h(c)-h(c+t g)<=C t^4`

on an explicit nonempty symmetric legal neighborhood of zero.  Combining this
with the already accepted regularity-free parity matching floor gives

`h(c)-h(c+t g)=Theta(t^4)` as `t->0`.

The proof uses atomwise parity evenness, the exact `s=t^2` complete likelihood,
current-law score cancellation, a nonnormal trace-log bound, Hilbert--Schmidt
extensivity, and a direct thermodynamic value limit.  It does not differentiate
the entropy-rate limit.

No computation, novelty assessment, or merge was performed.  Ordinary
`C^2/C^4` response, off-center curvature, punctured-neighborhood or whole-
interval concavity, general real kernels, and spectral/quantum entropy are
excluded.

