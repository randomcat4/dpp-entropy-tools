# S1 fresh delta-FIRST for PR82 at `290a8406`

This packet records a version-bound mathematical/source FIRST for the two-commit delta from the previously reviewed PR82 source head `365347e` to

`290a84064eaae2e857d637f58531e95f4ca3cb3b`.

The only new mathematical source is `c4_response_spatial_truncation_p4_multiscale.md`.  The other changed file is the project README, which repairs source navigation and keeps the new quantitative lemma explicitly outside the earlier frozen review.

## Verdict

`CORRECT_WITHIN_SCOPE`, with two non-blocking local clarifications recorded in `review_report.md`.

For every `a=p/2>2` and every `0<eta<a-2`, the canonical frozen-memory conditional chain has, through response order two in `s=t^2`, the two-cutoff error

\[
C_{\eta,F}\left(M^{-\eta}+N^{-a}M^3\right).
\]

Taking `M=floor(N^{a/(3+eta)})` gives rate `N^{-a eta/(3+eta)}` for all sufficiently large `N`.  Hence every exponent strictly below `a(a-2)/(a+1)` is available.  The endpoint exponent is a supremum and is not claimed.

This is a response approximation for the normalized canonical finite-memory conditional chain.  It is not a finite-section DPP entropy identity and does not extrapolate a finite-window Hessian sign.

No computation, formal verification, novelty assessment, SECOND, author edit, or merge was performed.
