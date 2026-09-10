# PR82 static-fix record

This successor does not modify the reviewed PR82 proof packet.

The PR82 branch README was repaired separately at commit
`290a84064eaae2e857d637f58531e95f4ca3cb3b` so that:

1. the scoped FIRST and isolated SECOND are attached only to the frozen
   qualitative `p>4` theorem at `6ecc004a...`;
2. the later `3209...` quantitative files remain unreviewed author results;
3. `c4_response_p4_boundary_correction.md` has explicit priority over the stale
   displayed equations `(7.3)--(7.5)` in the historical main proof;
4. the withdrawn raw frozen-memory response rate is not part of the
   authoritative theorem chain.

The historical source lines are preserved as evidence of the failed extra
claim rather than silently rewritten.  The correction file contains the valid
replacement: a finite time-correlation/Poisson cutoff, not the withdrawn raw
stationary frozen-memory derivative rate.
