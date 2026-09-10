# I05-31 — the joint Fisher–acceleration kernel is an exact reverse-mixture divergence curvature

Status: **AUTHOR ANALYTIC IDENTITY / PENDING_INDEPENDENT_REVIEW; novelty NOT_ASSESSED.** This identity is for the complete law of the true physical affine DPP path. It does not assert positivity by itself.

Let `mu_E=p_E(0)>0` and

`p_E(t)=mu_E q_E(s)`, `s=t^2`,

`q_E=1-a_E s+b_E s^2`,

`v_E=a_E-2s b_E`,

`z_E=(a_E-sb_E)(a_E-6sb_E)`.

For `0<=u<=1` put

`d_E(u)=(1-u)+u q_E=1+u(q_E-1)>0`

at every strict physical point, and define the mixture law

`m_u(E)=(1-u)mu_E+u p_E(t)=mu_E d_E(u)`.

The complete normalized curvature has the exact common-integral representation

`Gamma(s)=-H''(t)/t^2`

`= integral_0^1 J(s,u) du`,

`J(s,u)=sum_E mu_E[4v_E^2/d_E(u)^2+2z_E/d_E(u)]`.            (1.1)

Indeed,

`1/q=integral_0^1 du/[1+u(q-1)]^2`,

`lambda(q)=integral_0^1 du/[1+u(q-1)]`.

Thus (1.1) retains the entire Fisher and acceleration terms and pairs their singular layers at the same value of `u`.

## Reverse-mixture f-divergence identity

For `u>0` define

`h_u(q)=[u(q-1)-log(1+u(q-1))]/u^2`,

and use its continuous limit

`h_0(q)=(q-1)^2/2`.

Then

`h_u'(q)=(q-1)/[1+u(q-1)]`,

`h_u''(q)=1/[1+u(q-1)]^2>0`.                                (2.1)

Since `sum_E mu_E(q_E-1)=0`,

`sum_E mu_E h_u(q_E)`

`=D(mu || m_u)/u^2`,                                         (2.2)

where the divergence is the ordinary classical relative entropy of the two complete laws. Differentiating the true `t` dependence gives

`q_E'(t)=-2t v_E`,

`q_E''(t)=-2(a_E-6s b_E)`.

Also

`q_E-1=-s(a_E-sb_E)`.

Substitution into (2.1) yields the exact identity

`J(s,u)`

`=(1/s) d^2/dt^2 [D(mu || (1-u)mu+u p_t)/u^2]`.              (2.3)

At `u=0`, (2.3) is understood by the chi-square limit in (2.2). No eventwise or likelihood floor is introduced.

## Consequences and limitation

1. Pointwise positivity of `J` is equivalent to convexity in the physical parameter `t` of the normalized reverse-mixture divergence in (2.3).
2. The identity explains why testing acceleration alone is unnecessarily strong: the `d^-1` acceleration layer and `d^-2` Fisher layer belong to the same divergence curvature.
3. Convexity of `h_u` in its scalar argument does **not** by itself prove (2.3) nonnegative, because `q_E(t)` is quartic rather than affine in `t`. Therefore this identity is a reduction, not a hidden proof.
4. The exact negative integrated-acceleration phase in `FULL_PARAMETER_ENDPOINT_PHASE.md` is compatible with possible positivity of `J`: reverse-mixture curvature may be positive even when its separated acceleration component is negative.

The next finite target is therefore precise: certify or refute `J>=0` first on the full `alpha=1/10` three-cube `(beta,s,u)`, using the 13 complete likelihood types and their positive denominators. A negative `J` point would still be only a method obstruction until its `u` integral is evaluated; a positive continuum certificate would prove the whole beta family directly through (1.1).