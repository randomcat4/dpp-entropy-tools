# I05-31 — exact boundary-ray asymptotics across the full alpha family

Status: **AUTHOR ANALYTIC PROOF / PENDING_INDEPENDENT_REVIEW; novelty NOT_ASSESSED.** This note distinguishes an auxiliary rational-kernel failure from the true complete Shannon curvature. The physical path remains the genuine affine K path and all complete events, Fisher terms and acceleration terms are retained.

Fix any `0<alpha<1` in the natural family

`A=alpha P+beta Q`, `C=I-A`, `B=sqrt(alpha(1-alpha))P`.

Approach the simultaneous parameter/spectral boundary along the exact ray

`beta=1-epsilon`, `s=t^2=1-epsilon`, `epsilon -> 0+`.

For the rational-kernel endpoint in the integral variable take `u=1`.

Direct exact asymptotic expansion of the 13 generic complete-event types gives the following three limits.

## 1. The pointwise rational kernel is negative at order epsilon^-2

`lim_(epsilon->0+) epsilon^2 R(alpha,1-epsilon,1-epsilon,1)`

`= -8 alpha^2 (alpha-1)^3/(alpha-3)`.

For every `0<alpha<1` this coefficient is strictly negative. Hence the pointwise-in-u positivity strategy fails throughout the full alpha family, not merely at alpha=1/10.

At `alpha=1/10` this becomes `-729/36250`, matching the exact negative rational point reported separately.

## 2. The integrated complete acceleration is positive logarithmically

Let

`A_norm=2 sum_E mu_E z_E lambda(q_E)=2 int_0^1 R du`.

The complete coefficient of `log(1/epsilon)` is

`lim_(epsilon->0+) A_norm/log(1/epsilon)`

`= 8 alpha(alpha-1)(4 alpha^2-4 alpha-1)`.

This is strictly positive for every `0<alpha<1`, because `alpha-1<0` while `4 alpha^2-4 alpha-1<0` on the open unit interval.

Thus the u integration reverses the sign of the most singular pointwise endpoint layer: a negative `epsilon^-2` value at u=1 does not imply negative integrated acceleration.

At `alpha=1/10` the coefficient is `612/625`.

## 3. The full normalized Fisher term is even more singular and positive

For

`F_norm=sum_E 4 mu_E(a_E-2s b_E)^2/q_E`,

exact expansion yields

`lim_(epsilon->0+) epsilon F_norm`

`= -16 alpha(alpha-1)^2(2 alpha-9)/[(2 alpha-5)(2 alpha-3)]`.

Every factor shows that this is strictly positive on `0<alpha<1`. Thus along this entire boundary ray

`F_norm = Theta(epsilon^-1)`,

while

`A_norm = +Theta(log(1/epsilon))`.

Consequently the complete normalized curvature

`Gamma=F_norm+A_norm`

is strongly positive on this ray sufficiently near the boundary; equivalently the true Shannon curvature is strongly negative there.

## 4. Interpretation

This is a precise mechanism obstruction. The auxiliary integral kernel R can diverge to `-infinity` at u=1 even though its u-integral is positive and the full Fisher term has a stronger positive pole. Therefore any proof of the natural two-parameter family must permit cancellations in u and cannot demand pointwise positivity of R.

Conversely, this boundary theorem does not prove any compact-middle sign. It is not used to infer the interior from endpoint behavior.

The next unresolved object is the integrated acceleration on the strict compact middle after exploiting the exact 13-type symmetry and the complement map `(alpha,beta)->(1-alpha,1-beta)`.