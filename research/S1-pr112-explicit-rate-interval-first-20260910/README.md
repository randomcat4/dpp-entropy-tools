# S1 FIRST of the explicit PR112 rate interval

Status: **ACCEPTED_SCOPED**.

This packet independently reviews exactly one author file from PR112:

`research/I05-DPP-27-lifted-cone-20260910/explicit_rate_interval.md`

at immutable blob `b8aab2981230b61d399d9a9411ee8547f8593958`, contained in
PR112 head `2ea07741114aa7cd20210dfc84becda378381e7b` against base
`bcbf7016e2abc6401b66f39ac9202d235ee32fad`.

Using only the exact accepted PR77 center anchor and its point-specific
complete-event comparison constants, the reviewed file proves that, for

`f_t(theta)=1/2+(1/4)cos(4 pi theta)+(t/8)cos(2 pi theta)`,

the true complete-occupation Shannon entropy rate per original coordinate
satisfies

`h''(t)<-1/2000`

throughout

`[1-2^(-27),1+2^(-27)]`.

Consequently `h(t)+t^2/4000` is concave there and the displayed quantitative
Jensen gap follows.

The verdict excludes the withdrawn interval `[49/40,51/40]`, the whole
lifted-cone package, the macroscopic interval `[1/2,3/2]`, PR91, computation,
and novelty.  No other file in PR112 is reviewed or accepted by this packet.

