# I05-31 — exact negative rational-kernel point, with positive integrated acceleration and full curvature

Status: **AUTHOR EXACT CALCULATION / PENDING_INDEPENDENT_REVIEW; novelty NOT_ASSESSED.** This note records a failure of the pointwise-in-u auxiliary-kernel positivity strategy. It is explicitly **not** an entropy counterexample.

Use `alpha=1/10` in the natural family and the exact rational point

`beta=999/1000`, `s=999/1000`, `u=1`.

All 64 complete events are retained through the 13 exact generic likelihood types.

## 1. The auxiliary rational kernel is genuinely negative

At this point exact rational summation gives

`R=sum mu z/[1+u(q-1)]`

`= -4652511275248641251547259673277396396430560770738995603060156315177013829721844617061387219436351135945723000000`

`  /234641869065463647119872803882392585968204540713314205480817507948342686413506474822091990896200409106815549`

`<0`,

numerically about `-19828.13763706689`.

Thus the hoped-for certificate `R(alpha,beta,s,u)>=0` on the full four-variable domain is false, already on this exact alpha=1/10 slice. This is a method counterexample only.

## 2. Integrating over u restores a positive complete acceleration

The actual normalized acceleration is

`A_norm=2 sum mu z lambda(q)=2 int_0^1 R du`,

with `lambda(q)=log(q)/(q-1)`.

At the same exact rational `(alpha,beta,s)`, a directed rational atanh expansion with an explicit geometric tail encloses every logarithm. Forty terms give

`6.9381648836224339 < A_norm < 6.9381648836224341`.

The enclosure width is below `1e-38`. Hence the complete integrated acceleration is strictly favorable even though the integrand is very negative at `u=1`.

## 3. Full Fisher-plus-acceleration curvature remains strongly favorable

The complete normalized Fisher term at the same point is the exact positive rational

`17920363609763405858118127359067999825854699458986176861631099015492193935090094325841732102641072000000`

`/21138905218608867433423907248512192563604682622399241719060881881753225645070345022679907046512915549`,

numerically about `847.7432215357995`.

Therefore

`Gamma=-H''(t)/t^2=F_norm+A_norm`

is about `854.681386419422` and is strictly positive. The true Shannon curvature is strictly negative here.

## 4. Consequence for the proof strategy

Pointwise positivity of the integral kernel R is too strong and cannot certify the full natural family. The remaining useful targets are weaker and physically relevant:

1. prove the u-integral `A_norm>=0` directly, allowing cancellations across u; or
2. if integrated acceleration becomes negative, combine it with the full Fisher term before drawing any entropy conclusion.

The negative R point is concentrated in the joint layer `beta -> 1`, `s -> 1`, `u -> 1`; it does not show a compact-middle entropy mechanism. No endpoint-concavity theorem is used to infer the sign above.