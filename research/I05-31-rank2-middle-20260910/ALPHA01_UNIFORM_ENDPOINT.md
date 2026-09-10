# I05-31 — an explicit beta-uniform endpoint band at alpha=1/10

Status: **AUTHOR ANALYTIC PROOF / PENDING_INDEPENDENT_REVIEW; novelty NOT_ASSESSED.** This theorem keeps the true affine physical kernel, all 64 complete events, the complete Fisher sum and the complete acceleration sum. It supplies an explicit endpoint band only; it is not used to infer the unresolved compact middle.

Fix `alpha=1/10` in the natural family and let `0<beta<1`. Put

`delta=1-s=1-t^2`.

The claim is

`Gamma(beta,s)=-H''(t)/t^2 >0`                                (0.1)

for every

`0<delta<=10^(-22)`.                                         (0.2)

Thus the complete Shannon curvature is strictly negative in this band, uniformly over the entire beta interval.

## 1. A uniform complete-likelihood floor

Each of the thirteen exact type likelihoods has

`q_i(s)=1-a_i s+b_i s^2`.

Direct coefficient extraction from the table in `TWO_PARAMETER_ALPHA01_CHECKPOINT.md` gives

`a_i<=2`                                                      (1.1)

for every `0<=beta<=1`; equality occurs only in a double-root specialization. At the legal endpoint every extended type has `q_i(1)>=0`. Therefore

`q_i(s)-(1-s)^2`

` =s[(2-a_i)+(b_i-1)s]>=0`,                                  (1.2)

because the bracket is affine in `s`, is nonnegative at `s=0` by (1.1), and is `q_i(1)>=0` at `s=1`. Hence

`q_i(s)>=delta^2`                                             (1.3)

for all thirteen types and the whole closed parameter box. On the strict physical domain all likelihoods are positive.

Since `lambda(q)=log(q)/(q-1)` is positive and decreasing,

`lambda(q_i)<=lambda(delta^2)`.

A direct inspection of the thirteen rational coefficients, whose beta-denominators are products of `7beta+2` and `17beta+1`, gives the deliberately coarse uniform bounds

`|a_i|<=2000`, `|b_i|<=2000`.                                (1.4)

Thus, for `0<=s<=1`,

`|z_i|=|(a_i-sb_i)(a_i-6sb_i)|<=56,000,000`.                 (1.5)

The original decoupled type weights are nonnegative and sum to one. Consequently the **entire** normalized acceleration, with no event removed, obeys

`|A_norm|=|2 sum_i W_i z_i lambda(q_i)|`

` <=112,000,000 lambda(delta^2)`.                             (1.6)

For `0<delta<=1/2`,

`lambda(delta^2)=2 log(1/delta)/(1-delta^2)`

` <=(8/3) delta^(-1/2)`,                                     (1.7)

using `log x<=sqrt(x)` for `x>=1` and `1/(1-delta^2)<=4/3`. Therefore

`A_norm>=-(896,000,000/3) delta^(-1/2)`.                     (1.8)

This is intentionally crude but uniform in beta.

## 2. One actual complete-event type supplies a uniform Fisher pole

Use the final type in the thirteen-row table. Set

`D=(7beta+2)(17beta+1)`,

`R=81beta^2-81beta+18`,

`N=D+R=20(10beta^2-2beta+1)`.

Its exact weight, likelihood and physical derivative coefficient are

`W=3D/5000`,

`q=delta(N-R delta)/D`,

`v=(N-2R delta)/D`.                                          (2.1)

This is one of the six complement-swapped aligned endpoint events; retaining its Fisher term is legitimate because every omitted Fisher term is nonnegative. On `0<=beta<=1`,

`N>=18`, `|R|<=18`.                                          (2.2)

For `0<delta<=1/100`, (2.2) gives

`N-2Rdelta >=(49/50)N`,

`N-Rdelta <=(101/100)N`.                                     (2.3)

Hence this single grouped type contributes

`F_norm >=4W v^2/q`

` =(3/1250) (N-2Rdelta)^2/[delta(N-Rdelta)]`

` >=[129654/3156250] delta^(-1)`

` >(1/25) delta^(-1)`.                                       (2.4)

No marginal or spectral Fisher proxy replaces the complete Fisher expression: (2.4) is a retained sub-sum of the actual six-event complete Fisher contribution.

## 3. Fisher dominates every acceleration term in an explicit band

Combining (1.8) and (2.4),

`Gamma=F_norm+A_norm`

` >(1/25)delta^(-1)-(896,000,000/3)delta^(-1/2)`.             (3.1)

For `delta<=10^(-22)`, the right side is strictly positive, since

`sqrt(delta)<=10^(-11)<3/22,400,000,000`.

This proves (0.1)-(0.2). The bound is far from optimized; its purpose is to close the entire moving-beta endpoint layer without appealing to a sampled grid or to endpoint asymptotics with beta held fixed.

## 4. Scope

- The theorem includes beta arbitrarily close to zero or one; no compact beta subinterval is hidden.
- It is a genuine full Fisher-versus-full acceleration comparison. The acceleration may be negative and even logarithmically divergent in the phase described in `FIXED_PARAMETER_ENDPOINT_PHASE.md`.
- The width `10^(-22)` is only a conservative analytic band. No claim is made that it is sharp.
- Nothing here proves the sign on `0<=s<=1-10^(-22)`. That remaining compact set is the exact target of the joint-integrand/Bernstein contract.