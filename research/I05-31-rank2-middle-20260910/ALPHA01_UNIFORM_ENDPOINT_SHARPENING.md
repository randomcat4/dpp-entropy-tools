# I05-31 — sharpened beta-uniform endpoint band at alpha=1/10

Status: **AUTHOR ANALYTIC PROOF / PENDING_INDEPENDENT_REVIEW; novelty NOT_ASSESSED.** This note replaces only the deliberately crude width in `ALPHA01_UNIFORM_ENDPOINT.md`. It keeps all complete-event acceleration terms and uses a retained complete-event Fisher sub-sum. It does not infer the compact middle from endpoint behavior.

Let `delta=1-s`. For every `0<beta<1`,

`Gamma(beta,s)=-H''(t)/t^2>0`                                (0.1)

whenever

`0<delta<=10^(-4)`.                                          (0.2)

## 1. Exact global control of the adverse acceleration mass

Write

`w=a-sb`, `h=a-6sb`, `z=wh`.

For real `w,h`, if `wh<0` then

`-wh<=(w-h)^2/4`.

Here `w-h=5sb`, hence eventwise

`(-z)_+ <=(25/4)s^2 b^2`.                                   (1.1)

The exact complete moment already derived for `alpha=1/10` is

`M_b=sum_E mu_E b_E^2`

` =[(5beta+1)^2(32beta^2-7beta+2)^2]`

`  /[(7beta+2)^2(17beta+1)^2]`.                              (1.2)

All factors in (1.2) are positive. Moreover

`(7beta+2)(17beta+1)`

` -(5beta+1)(32beta^2-7beta+2)`

` =2beta(1-beta)(80beta+19)>=0`.                             (1.3)

Therefore

`M_b<=1`                                                      (1.4)

throughout the entire beta interval. Combining (1.1)-(1.4), the total original-weight negative acceleration mass satisfies

`N:=sum_E mu_E(-z_E)_+ <=25/4`.                              (1.5)

The thirteen-type likelihood floor proved in `ALPHA01_UNIFORM_ENDPOINT.md` is

`q_E(s)>=delta^2`.

Since `lambda` is decreasing, every adverse term obeys

`z_E lambda(q_E)>=-(-z_E)_+ lambda(delta^2)`.

All favorable terms may be retained or discarded when forming a lower bound. Hence the **full** normalized acceleration satisfies

`A_norm=2sum_E mu_E z_E lambda(q_E)`

` >=-(25/2)lambda(delta^2)`.                                 (1.6)

No individual adverse atom is removed from the law.

## 2. Retain the aligned six-event Fisher group

For the last generic type in the exact table, put

`D=(7beta+2)(17beta+1)`,

`R=81beta^2-81beta+18`,

`N0=20(10beta^2-2beta+1)`.

Its total weight, likelihood and derivative coefficient are

`W=3D/5000`,

`q=delta(N0-Rdelta)/D`,

`v=(N0-2Rdelta)/D`.

As proved in the preceding endpoint note, `N0>=18`, `|R|<=18`, and for `delta<=1/100` this actual six-event Fisher sub-sum gives

`F_norm>=1/(25delta)`.                                       (2.1)

Every other complete Fisher term remains nonnegative.

Combining (1.6) and (2.1),

`delta Gamma`

` >=1/25-(25/2)delta lambda(delta^2)`

` =1/25-25delta log(1/delta)/(1-delta^2)`.                   (2.2)

## 3. Exact endpoint-width comparison

For `0<delta<e^(-1)`, the function

`delta log(1/delta)/(1-delta^2)`

is increasing, because its derivative has numerator

`log(1/delta)-1+delta^2[log(1/delta)+1]>0`.

It is therefore enough to test the right endpoint `delta=10^(-4)`. The elementary rational bound

`log 10<7/3`                                                  (3.1)

follows, for example, by lower-bounding the exponential series for `exp(7/3)` through a finite positive partial sum and obtaining a value greater than ten. Thus

`25delta log(1/delta)/(1-delta^2)`

` < [25/10000]*(28/3)/[1-10^(-8)]`

` <1/25`.                                                     (3.2)

The final comparison in (3.2) is an exact rational cross-multiplication. Equations (2.2)-(3.2) prove (0.1)-(0.2).

## 4. Interpretation

The improved band is uniform over beta arbitrarily close to zero or one. It remains conservative, but it reduces the unresolved exact certificate to the genuine compact rectangle

`0<=s<=9999/10000`, `0<beta<1`.

The proof does not assert that the integrated acceleration is nonnegative: `FIXED_PARAMETER_ENDPOINT_PHASE.md` proves that it is negative logarithmically in an explicit open parameter phase. The complete Fisher controls that phase here.