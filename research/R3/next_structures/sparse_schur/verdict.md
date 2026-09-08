# NS-1 verdict

Status: DEEP.

The path-sparse L-ensemble subroute should be advanced as a new exact entropy
evaluator for R3.  It is genuinely outside the verified old grouped
block-exchangeable reduction, has a self-contained Schur/run-factorization
derivation, and passed small exact Mobius validation.

## What is accepted

Accepted object:

```text
real symmetric positive definite tridiagonal L on a path,
K = L(I+L)^(-1).
```

Accepted algorithm:

```text
p_K(S)=det(L_S)/det(I+L),
det(L_S)=product of selected-run interval determinants,
H(K)=log Z - T/Z by the O(n^2) run dynamic program.
```

Accepted validation:

```text
n=6 and n=8 direct Mobius atom checks passed exactly.
n=12 reduced-only smoke used 78 interval states instead of 4096 events.
```

This is an entropy computation route, not a certified concavity violation.

## Why it is not the old structure

The old verified reduction uses repeated row types and group-count orbits.
This route uses heterogeneous nearest-neighbor path sparsity in the
L-ensemble.  Event weights depend on the ordered run decomposition of the
selected set.  A generic heterogeneous path has no nontrivial coordinate
permutation orbit that would reduce events to group counts.

## Nonclaims

* No real counterexample candidate was found or certified.
* No conclusion is made for all real symmetric DPP kernels.
* No finite `n<=8` validation is promoted to a general theorem.
* No generic low-treewidth/tree/arrowhead entropy DP is claimed.
* No affine marginal-kernel chord closure is claimed for path-sparse `L`.
* Decimal entropy values are diagnostic; final gap signs still need directed
  interval arithmetic.

## Minimum remaining obligations

1. Fresh-context verification of `route_note.md` and `path_schur.py`, especially
   the recurrence indexing and the equality with direct Mobius atoms.
2. Add outward-rounded logarithm intervals before using the evaluator for any
   strict sign claim.
3. Decide how to evaluate affine marginal-kernel chords:
   find triples whose endpoints and midpoint all have path-sparse `L`, or
   prove a sparse-marginal-`K` recursion, or supply a certified midpoint loss
   bridge.
4. For generic tree or arrowhead versions, either prove a finite Schur-message
   state compression or keep them in HOLD with the current blockers.

## Handoff

Promote NS-1A only:

```text
Path-sparse L exact entropy evaluator, status DEEP.
```

Keep the broader wording honest:

```text
Generic low-treewidth exact DPP entropy, status HOLD.
Affine real chord search using this evaluator, status HOLD until midpoint
closure or a certified bridge is supplied.
```
