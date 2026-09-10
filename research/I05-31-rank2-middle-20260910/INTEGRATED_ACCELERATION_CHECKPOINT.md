# I05-31 continuation — integrated-acceleration checkpoint

Status: **AUTHOR ANALYTIC CHECKPOINT / PENDING_INDEPENDENT_REVIEW; novelty NOT_ASSESSED.** The source comparison was refreshed against `main@1d440702b16b8e65954edde076686dba8f1901ae`; PR116 had no submitted review or conversation comment at this freeze. This file is a checkpoint before continuing the same task, not a completed sign theorem.

All quantities below concern complete-configuration Shannon entropy of the true physical affine path

`K(t)=[[A,tB],[tB,C]]`,

with

`A=alpha P+beta Q`, `C=I-A`, `B=sqrt(alpha(1-alpha)) P`,

`Q=11^T/3`, `P=I-Q`, `0<alpha,beta<1`. Every complete event, Fisher term and acceleration term is retained.

For `s=t^2`, write the exact complete likelihoods

`p_E(t)=mu_E q_E(s)`, `q_E=1-a_E s+b_E s^2`,

`z_E=(a_E-sb_E)(a_E-6sb_E)` and

`lambda(q)=log(q)/(q-1)=integral_0^1 du/[1+u(q-1)]`.

The normalized acceleration and full normalized curvature are

`A_norm(alpha,beta,s)=2 sum_E mu_E z_E lambda(q_E)`,

`Gamma=sum_E 4 mu_E(a_E-2sb_E)^2/q_E + A_norm`.

## Exact parameter and event symmetry

Replacing `(alpha,beta)` by `(1-alpha,1-beta)` interchanges `A` and `C` while leaving `sqrt(alpha(1-alpha))` unchanged. Swapping the two observed three-coordinate blocks therefore gives the same physical kernel. Consequently

`A_norm(alpha,beta,s)=A_norm(1-alpha,1-beta,s)`

and the same identity holds separately for the complete Fisher term and `Gamma`. Thus it is enough to analyze `0<alpha<=1/2`, with beta transformed simultaneously when needed. This is an observed-coordinate permutation identity, not a spectral-entropy argument.

The 64 events form 20 simultaneous-permutation orbits `(abs(S),abs(T),abs(S intersect T))`. Seven orbit pairs have identical `(a,b,q)`, leaving 13 generic logarithm types. Complementing an event and swapping blocks realizes the corresponding pairings and preserves the original positive decoupled weights after the displayed parameter transformation.

## Boundary facts that do not settle the middle

At `s=0`, every `q_E=1`, so

`A_norm(alpha,beta,0)=2 sum_E mu_E a_E^2>0`.

At the legal endpoint, PR102/main supplies the full-curvature boundary mechanism, and the separately proved PR116 ray calculation gives positive acceleration on one singular ray. Neither fact is used to infer a compact-middle sign.

The pointwise integral kernel `R=sum mu z/[1+u(q-1)]` is already known to fail positivity near `u=1`; therefore the present target is the integrated quantity itself. A negative auxiliary kernel is not an entropy counterexample. The required order remains: exact negative `A_norm` point, if any; then the complete Fisher; only then a conclusion about `Gamma`.

The next proof attempt will use the 13 exact logarithm types, the above half-domain reduction, and exact directed logarithm/Bernstein or algebraic comparison. No earlier checker or finite budget is reused.