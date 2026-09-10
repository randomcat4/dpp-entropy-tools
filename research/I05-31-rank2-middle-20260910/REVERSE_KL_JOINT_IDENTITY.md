# I05-31 — the joint `u` integrand is an exact reverse-KL curvature

Status: **AUTHOR ANALYTIC PROOF / PENDING_INDEPENDENT_REVIEW; novelty NOT_ASSESSED.** This is an identity for the complete observed law. It neither discards events nor changes the physical affine kernel path.

Let `mu_E=p_E(0)` and, on a strict point of the natural rank-two chord,

`p_E(t)=mu_E q_E(s)`, `s=t^2`,

`q_E=1-a_Es+b_Es^2`,

`v_E=a_E-2sb_E`, `h_E=a_E-6sb_E`,

`w_E=a_E-sb_E`, `z_E=w_Eh_E`.

For `0<=u<=1` form the genuine probability mixture

`p_u(E;t)=(1-u)mu_E+u p_E(t)=mu_E d_E(u)`,

`d_E(u)=(1-u)+u q_E(s)>0` on the strict physical chord.

Define the reverse relative entropy

`D_u(t)=D(mu || p_u(t))=-sum_E mu_E log d_E(u)`.

Then

`D_u''(t)=s u^2 J(u)`,                                      (1.1)

where

`J(u)=sum_E mu_E [4v_E^2/d_E(u)^2+2z_E/d_E(u)]`.             (1.2)

Consequently the complete normalized Shannon curvature has the exact representation

`Gamma(s)=-H''(t)/t^2=int_0^1 J(u) du`,                      (1.3)

because `int_0^1 du/d^2=1/q` and `int_0^1 du/d=lambda(q)`.

## Proof of (1.1)

The physical derivatives are

`q_E'(t)=-2t v_E`,

`q_E''(t)=-2h_E`.

Therefore

`D_u''=sum_E mu_E[(u q_E')^2/d_E^2-u q_E''/d_E]`

` =4su^2 sum_E mu_E v_E^2/d_E^2`

`   +2u sum_E mu_E h_E/d_E`.                                (1.4)

The exact complete-law cancellations give

`sum_E mu_E h_E=sum_E mu_E(a_E-6sb_E)=0`.

Also

`1-d_E=u(1-q_E)=usw_E`.

Hence

`sum_E mu_E h_E/d_E`

` =sum_E mu_E h_E(1/d_E-1)`

` =us sum_E mu_E w_Eh_E/d_E`

` =us sum_E mu_E z_E/d_E`.                                  (1.5)

Substitution in (1.4) proves (1.1). At `u=0` both sides vanish continuously.

## Interpretation and limitation

Pointwise `J(u)>=0` would mean that, for every mixture level, the reverse KL from the decoupled complete law to the mixture has nonnegative physical `t` curvature. It is a sufficient route to Shannon concavity, not a reformulation that may silently omit acceleration.

The earlier negative acceleration kernel `R=sum mu z/d` does not decide (1.2): its negative layer is paired at the same denominator scale with `4sum mu v^2/d^2`. Conversely, a negative `J` point would still be only a reverse-KL-curvature obstruction; the `u` integral in (1.3) must be evaluated before assigning any Shannon-entropy status.