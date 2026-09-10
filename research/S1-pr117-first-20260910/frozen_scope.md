# Frozen scope

## Binding

- repository: `randomcat4/dpp-entropy-tools`
- pull request: `117`
- reviewed head: `70d69bf5c47282c953010518ff264cb2a7a09bf9`
- author base: `bcbf7016e2abc6401b66f39ac9202d235ee32fad`
- review class: independent mathematical FIRST
- computation: none
- novelty review: not performed

Any later PR117 commit requires a fresh or delta-bound review.  No verdict
from PR53, PR82, PR102, PR106, PR110, or PR113 is transferred to the new
arbitrary-`A_0` bridge.  The previously accepted PR53 matching floor is
treated only as the explicitly imported theorem input identified by the
author.

## Accepted statement

Let real `c,g in A_0` obey

- `c(theta+1/2)=c(theta)`;
- `g(theta+1/2)=-g(theta)` and `g != 0`;
- `delta <= c <= 1-delta` a.e. for some `delta>0`.

Put `mu=c_hat(0)`.  For each odd `k` with `g_hat(k) != 0`, there is an
`epsilon>0` such that `c+t g` is strictly legal on `[-epsilon,epsilon]` and

`t -> h(c+t g)+|g_hat(k)|^4 t^4/[8 mu^2(1-mu^2)]`

is concave there, with strictly negative second derivative away from zero
after shrinking the interval.

Here `h` is the classical complete-configuration Shannon entropy rate of the
stationary DPP with the affine kernel `T(c)+tT(g)`.

## Exclusions

This verdict does not claim:

- concavity on the whole legal interval;
- any theorem for merely measurable symbols outside `A_0`;
- general real-kernel finite-dimensional entropy concavity;
- a spectral or von-Neumann entropy formula;
- a common `ell^1` inverse envelope for arbitrary complete-event inverses;
- an entropy counterexample from failure of an inverse method;
- novelty, priority, or machine verification.
