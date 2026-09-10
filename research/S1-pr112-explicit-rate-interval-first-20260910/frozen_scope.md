# Frozen scope

Repository: `randomcat4/dpp-entropy-tools`

Pull request: PR112

Reviewed head: `2ea07741114aa7cd20210dfc84becda378381e7b`

Reviewed base: `bcbf7016e2abc6401b66f39ac9202d235ee32fad`

Reviewed file blob: `b8aab2981230b61d399d9a9411ee8547f8593958`

## Frozen theorem

Let

`f_t(theta)=1/2+(1/4)cos(4 pi theta)+(t/8)cos(2 pi theta)`

and let `h(t)` be the complete-configuration Shannon entropy rate of the
stationary DPP with symbol `f_t`, normalized per original lattice coordinate.
For

`J=[1-2^(-27),1+2^(-27)]`,

the claim is

`h''(t)<-1/2000` for every real `t in J`.

Equivalently, `h(t)+t^2/4000` is concave on `J`; hence, for `u,v in J` and
`0<=lambda<=1`,

`h(lambda u+(1-lambda)v)-lambda h(u)-(1-lambda)h(v)`

`>=lambda(1-lambda)(u-v)^2/4000`.

## Authorized PR77 inputs

Only the following exact accepted PR77 facts are imported:

1. for the same physical affine parameter, `h''(1)<-1/1000`;
2. on the complex disk `|z-1|<=1/8`, the full complete-event predictors obey
   the point-specific comparison estimate with
   `rho=2/3`, `C=288/85`, `A=11/64`, and `B=49/192`.

They are sourced from PR77 head
`2564e25a8b62a72992b9451988cd42e2d5a81834`, file blob
`a6f5a15322f5a36a90042b77c46ce315a848680a`.  PR77 was merged as
`88b0026b76ede02d5b8c5c7a354423771a2d1b28`.

## Exclusions

- the withdrawn `[49/40,51/40]` claim;
- any sign theorem on `[1/2,3/2]`;
- the determinant-lift or lifted-cone package;
- every PR91 result or acceptance claim;
- every other PR112 file;
- numerical or symbolic computation;
- novelty, priority, or publication-strength conclusions.

