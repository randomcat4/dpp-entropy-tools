# I05-31 — exact Bernstein certificate for the rational kernel at alpha=1/10

Status: **AUTHOR EXACT CERTIFICATE / PENDING_INDEPENDENT_REVIEW; novelty NOT_ASSESSED.** This is a continuum certificate for an auxiliary rational kernel entering the complete acceleration integral. It is not by itself a full entropy theorem beyond the already stated curvature identity.

Use the notation and denominator reduction in `RATIONAL_KERNEL_CHECKPOINT.md`, specialize `alpha=1/10`, and put

`delta=1-s`, `v=1-u`.

For `0<beta<1`, `0<=s<1`, every denominator

`d_E=(1-u)+u q_E(s)`

is strictly positive. Clearing the product of the 13 distinct positive denominator types gives a common numerator `N(beta,delta,v)` of degree `(18,24,11)`.

## Exact Bernstein region

On the box

`0<=beta<=1`, `0<=delta<=1`, `1/16<=v<=1`,

that is equivalently

`0<=beta<=1`, `0<=s<=1`, `0<=u<=15/16`,

make the affine substitution

`beta=X`, `delta=Y`, `v=1/16+(15/16)Z`, with `0<=X,Y,Z<=1`.

Convert the resulting polynomial exactly from the power basis to the tensor Bernstein basis of its exact multidegree. Every Bernstein coefficient is nonnegative. The smallest coefficient is the positive integer

`27030487060546875000000000000000000000000000000000000`.

Hence the cleared numerator is strictly positive on the closed box, and because every rational denominator is positive on the strict physical chord,

`R(1/10,beta,s,u)>0`

for every `0<beta<1`, `0<=s<1`, `0<=u<=15/16`.

The use of Bernstein form follows the standard positivity principle for rational/polynomial functions on a simplex/box: a polynomial represented in a nonnegative partition-of-unity Bernstein basis lies between the extrema of its Bernstein coefficients. The arithmetic here is exact rational arithmetic; no floating sign decision is used.

## What remains

Only the thin integration layer `15/16<u<=1` remains for the alpha=1/10 full-beta rational-kernel sign. This note does not infer that layer from endpoint concavity and does not call an auxiliary-kernel failure an entropy counterexample. If the remaining layer contains a negative R point, the workflow remains: exact rational point first, then the complete u integral, then full Fisher plus acceleration.