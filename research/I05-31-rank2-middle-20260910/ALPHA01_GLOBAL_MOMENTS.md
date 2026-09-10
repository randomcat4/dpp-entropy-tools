# I05-31 continuation — beta-uniform global acceleration moments at alpha=1/10

Status: **AUTHOR ANALYTIC DERIVATION / PENDING_REVIEW; novelty NOT_ASSESSED.** This note uses the 13 exact complete-event likelihood types in `TWO_PARAMETER_ALPHA01_CHECKPOINT.md`. It does not claim the logarithm-weighted acceleration sign by itself.

For `0<beta<1`, `0<=s<=1`, write as usual

`q_E(s)=1-a_E s+b_E s^2`, `mu_E=p_E(0)`,

`v_E=a_E-2s b_E`, `z_E=(a_E-sb_E)(a_E-6s b_E)`.

Exact summation over all 64 complete events (equivalently the 13 generic symmetry types with their original decoupled weights) gives

`M_a := sum mu a^2`

` = 6(80 beta^3-15 beta^2+15 beta+1)^2 / [(7 beta+2)^2(17 beta+1)^2]`,

`M_ab := sum mu a b`

` = -18 beta^2(1-beta)^2(10 beta-1)^2 / [(7 beta+2)^2(17 beta+1)^2] <= 0`,

and

`M_b := sum mu b^2`

` = (5 beta+1)^2(32 beta^2-7 beta+2)^2 / [(7 beta+2)^2(17 beta+1)^2] > 0`.

Therefore the two complete global quadratic moments entering the true normalized curvature satisfy identically

`sum mu v^2 = M_a-4s M_ab+4s^2 M_b > 0`,

`sum mu z = M_a-7s M_ab+6s^2 M_b > 0`.

The second statement is especially relevant: before the logarithmic secant weights `lambda(q_E)=log(q_E)/(q_E-1)` are applied, the **aggregate acceleration polynomial has favorable sign throughout the entire beta family and entire legal chord**. Since some individual `z_E` are negative, the only remaining way for the complete acceleration contribution

`A_norm(beta,s)=2 sum mu z_E lambda(q_E)`

to become negative is an event-to-event reweighting effect caused by the variation of `lambda(q_E)`. Thus the remaining obstruction is now precise: control the covariance between `z_E` and the decreasing secant weight `lambda(q_E)`, not the unweighted signed moment.

This is not an endpoint argument and does not infer the middle from PR102. No Fisher term has been discarded; the full curvature remains

`Gamma=sum mu[4v^2/q+2z lambda(q)]`.
