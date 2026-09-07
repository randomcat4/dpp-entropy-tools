# R1 certificate result

Status: COMPLETE for verifier packaging and diagonal-midpoint review.

## Verifier

`certify_real_chord.py` accepts a rational real-symmetric center `K`, rational
real-symmetric direction `V`, and rational `t > 0`. It checks strict endpoint
feasibility and computes the DPP full-event entropy gap using exact event
probabilities:

```text
p_K(S)=(-1)^|S^c| det(K-I[S^c]).
```

It returns:

- `CERTIFIED_POSITIVE_GAP` for a strict midpoint-concavity counterexample;
- `CERTIFIED_NEGATIVE_GAP` for a strict concave-sign chord;
- `GAP_UNCERTAIN` when the current rational interval does not separate zero;
- `NOT_FEASIBLE` when an endpoint or complement fails strict positivity;
- `EVENT_PROBABILITY_FAILURE` when exact event probabilities fail positivity
  or normalization.

## Test Summary

Three compact tests were run:

```text
negative_gap.json -> CERTIFIED_NEGATIVE_GAP
zero_direction_uncertain.json -> GAP_UNCERTAIN
infeasible_endpoint.json -> NOT_FEASIBLE
```

The negative-gap test certified a midpoint gap of approximately
`-9.419318110613861e-4`. The zero-direction test produced a symmetric interval
around zero of radius about `4.98e-79`. The infeasible-endpoint test returned a
clean feasibility failure without attempting logarithms.

No positive real-symmetric gap candidate was supplied to this verifier, so this
package makes no counterexample claim.

## Diagonal Midpoint Review

`../verification/diagonal_midpoint_review.md` verifies the auxiliary theorem:
if the chord midpoint is a diagonal strict contraction and `t>0,V!=0`, then the
real-symmetric DPP entropy midpoint gap is strictly negative. The review status
is `CORRECT`.
