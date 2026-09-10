# Frozen scope

## Binding

- repository: `randomcat4/dpp-entropy-tools`
- pull request: `125`
- reviewed head: `87897b307818e9eab84ad465b24b4aeb037a1dc1`
- author base: `b3ada9f6bb23e3efd2e1a4d2a2977d50b61fb4d7`
- review class: independent mathematical/source FIRST
- computation: none
- novelty: not assessed

Any later author commit requires a fresh or exact delta review.

## Accepted general KL statement

For real `c,f in L^infinity(T)` with
`a<=c,f<=1-a` almost everywhere, the complete occupation laws of the finite
Toeplitz DPP kernels satisfy

`limsup_(n->infinity) n^(-1) D(P_(n,f)||P_(n,c))`

`<= integral_T d_Ber(f(theta)||c(theta)) dtheta`.

## Accepted half-period consequence

For a strict half-period-even center `c` and half-period-odd nonzero direction
`g`, on any sufficiently small symmetric interval kept inside one fixed
spectral strip,

`0 <= h(c)-h(c+t g) <= integral d_Ber(c+t g||c)`.

The exact `t`/`-t` complete-law symmetry yields the symmetric central
second-difference bound and

`limsup_(t->0) [h(c)-h(c+t g)]/t^2`

`<= (1/2) integral g^2/[c(1-c)]`.

The separately accepted PR53 matching floor may be added as the stated lower
bound for each selected nonzero odd Fourier coefficient.

## Exclusions

This verdict does not claim:

- existence of an entropy-rate second derivative;
- `C^2`, `C^4`, or analyticity;
- local concavity away from the center;
- whole-legal-interval concavity;
- a finite- or continuous-state HMM representation of the DPP;
- spectral or von-Neumann entropy equality with configuration entropy;
- general finite real-kernel Shannon concavity;
- an entropy counterexample;
- novelty or machine verification.

