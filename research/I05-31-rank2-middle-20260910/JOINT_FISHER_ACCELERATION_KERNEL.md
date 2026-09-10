# I05-31 continuation — a joint resolvent kernel for the full Shannon curvature

Status: **AUTHOR ANALYTIC CHECKPOINT / PENDING_INDEPENDENT_REVIEW; novelty NOT_ASSESSED.** This identity is exact for the complete law. It is uploaded before continuing the same proof attempt. No pointwise positivity theorem is claimed in this checkpoint.

Let `mu_E=p_E(0)` and, for the true physical rank-two path, write

`p_E(t)=mu_E q_E(s)`, `s=t^2`, `q_E=1-a_E s+b_E s^2`,

`v_E=a_E-2s b_E`, `z_E=(a_E-sb_E)(a_E-6sb_E)`.

For `0<=u<=1` put

`d_E(u)=(1-u)+u q_E=1+u(q_E-1)>0`

at every strict physical point. The two elementary resolvent identities

`log(q)/(q-1)=integral_0^1 du/d_E(u)`,

`1/q=integral_0^1 du/d_E(u)^2`

turn the **full** normalized curvature into

`Gamma(s)=-H''(t)/t^2=integral_0^1 J(s,u) du`,               (1)

where

`J(s,u)=sum_E mu_E [4 v_E^2/d_E(u)^2+2 z_E/d_E(u)]`.        (2)

Thus Fisher and acceleration are not estimated separately in (2); both are retained and placed on the same resolvent scale. This matters near `u=1`, where an adverse acceleration pole of order `d^-1` is accompanied by the exact Fisher density of order `d^-2`.

There is also an exact divergence interpretation. Define the genuine probability mixture

`p_{u,t}(E)=(1-u)mu_E+u p_E(t)=mu_E d_E(u)`

and

`D_u(t)=D(mu || p_{u,t})=-sum_E mu_E log d_E(u)`.

For `u>0`, direct differentiation gives

`D_u''(t)=sum_E mu_E [u^2(q_E')^2/d_E^2-u q_E''/d_E]`.

Here `q_E'=-2t v_E`, `q_E''=-2(a_E-6sb_E)`, and the complete normalization identity `sum_E mu_E q_E''=0` permits replacing `1/d_E` by `1/d_E-1=u s(a_E-sb_E)/d_E` in the second sum. Therefore

`D_u''(t)/(u^2 t^2)=J(s,u)`.                                (3)

Equation (3) is a reverse-KL curvature identity for an actual classical mixture of the two complete laws. It is not a spectral entropy or an affine-L argument.

For the natural exchangeable family, a mechanism-directed numerical scout at `alpha=1/10` found a positive interior minimum of `J` over the full `(beta,s,u)` cube, despite the previously proved negativity of the acceleration-only kernel `R` near `u=1`. This observation is **not** a certificate. The next task is to clear the positive `d_E^2` denominators typewise and seek an exact Bernstein/square certificate; if `J` itself fails, the workflow remains exact rational point first and then the `u` integral.