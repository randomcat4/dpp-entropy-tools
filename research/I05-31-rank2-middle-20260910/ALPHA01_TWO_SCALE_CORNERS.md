# I05-31 — exact two-scale corner asymptotics at alpha=1/10

Status: **AUTHOR ANALYTIC PROOF / PENDING_INDEPENDENT_REVIEW; novelty NOT_ASSESSED.** These are exact asymptotic consequences of the thirteen complete-event types. They distinguish parameter-boundary disappearance from the physical spectral endpoint. They retain the full Fisher and acceleration sums and are not used to infer a compact-middle sign.

Put `delta=1-s` and fix `alpha=1/10`.

## 1. The beta=0 corner

Approach the joint corner through

`beta=x delta`, with fixed `0<=x<infinity`, `delta->0+`.

Four endpoint groups control the logarithmic acceleration order. In the limiting beta-zero table:

- the type `q=(s+9)(1-s)/9` is simple, has total weight `729/2500`, and endpoint `z=14/9`;
- the two types whose common limit is `q=(9s+1)(1-s)` have combined weight `9/2500` and endpoint `z=46`;
- the type `q=(1-s)^2` has weight `81/5000`, endpoint `z=-4`, and double logarithmic order.

All other types are either endpoint-positive or have weights that vanish at least linearly in `delta`. Therefore

`A_norm/log(1/delta) ->612/625`.                              (1.1)

The coefficient is independent of the fixed crossover ratio `x`. It is strictly positive.

For the Fisher term, only three simple groups contribute at order `delta^(-1)`. Direct substitution into their exact `q,v,W` expressions gives

`delta F_norm -> f0(x)`,                                     (1.2)

where

`f0(x)=162/[125(1+5x)]`

`     +12/[125(1+15x)]`

`     +6/125`.                                                (1.3)

Thus

`f0(x)>6/125`                                                 (1.4)

for every finite `x>=0`, and the same positive number is the outer limit as `x->infinity`.

At `x=0`, `f0(0)=36/25`, the beta-zero endpoint coefficient. The limit `x->infinity` gives `6/125`, agreeing with the fixed-small-beta phase approached after the physical endpoint limit is taken first.

## 2. The beta=1 corner

Now put

`1-beta=x delta`, with fixed `0<=x<infinity`.

At beta one, the endpoint-zero types consist of two `q=(s+9)(1-s)/9` groups, one `q=(9s+1)(1-s)` group, and one double `q=(1-s)^2` group. The complete logarithmic coefficient is again

`A_norm/log(1/delta) ->612/625>0`.                            (2.1)

The normalized Fisher crossover is

`delta F_norm -> f1(x)`,                                     (2.2)

with

`f1(x)=324/[125(3+5x)]`

`     +162/[125(9+5x)]`

`     +54/125`.                                               (2.3)

Consequently

`f1(x)>54/125`                                                (2.4)

for every finite `x>=0`, with the same positive outer limit as `x->infinity`.

At `x=0`, `f1(0)=36/25`. At `x=1`, (2.3) agrees with the previously recorded exact diagonal-ray Fisher coefficient.

## 3. Why this does not contradict the negative fixed-parameter acceleration phase

The limits do not commute. For a fixed sufficiently small positive beta, `FIXED_PARAMETER_ENDPOINT_PHASE.md` gives

`A_norm=L(1/10,beta)log(1/delta)+O(1)`

with `L<0`. In the inner corner chart `beta=xdelta`, however, additional likelihood types also become endpoint-small. Their positive logarithmic terms enter at the same order and change the coefficient to `612/625`.

The Fisher coefficient has no such sign problem: the rational crossover functions (1.3) and (2.3) stay uniformly positive and match their outer fixed-parameter limits. Thus neither parameter corner offers a true entropy counterexample.

These formulas provide exact stopping data for a projective Bernstein proof: the charts `beta=delta x` and `1-beta=delta x` have strictly positive leading Fisher coefficients, while the remaining region has beta separated from its parameter boundary relative to delta.