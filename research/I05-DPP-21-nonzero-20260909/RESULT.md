# RESULT — nonzero-parameter compact tubes

Date: 2026-09-09.

## PROVED (AUTHOR PROOF), NOT INDEPENDENTLY REVIEWED

Let `beta>0`, `0<mu<1`, and let real `g in A_beta` satisfy

```text
g(theta+1/2)=-g(theta),
g!=0.
```

Choose an odd `k` with `g_hat(k)!=0`. For every `T>0` such that

```text
inf_{theta,|t|<=T}min{mu+t g(theta),1-mu-t g(theta)}>0,
```

there exists `rho>0` with the following property. Every real half-period-invariant `c in A_beta` with

```text
integral c=mu,
||c-mu||_beta<rho
```

satisfies

```text
t -> h(c+t g)+(2/3)|g_hat(k)|^4 t^4
```

concave on the entire prescribed interval `[-T,T]`. In particular, `h(c+t g)` is strictly concave on every nontrivial subchord of that interval.

The proof does not re-center the accepted local theorem at nonzero parameters. It proves joint RPF analyticity in the center and parameter on a tube around the compact constant-centered chord, extends `h''/t^2` through `t=0`, imports the accepted constant-centered `(4/3)|g_hat(k)|^4t^4` whole-line margin, and uses compactness to retain half of that margin for nearby nonconstant centers.

Also proved:

1. an exact RPF/prediction second-variation formula at an arbitrary strict parameter, retaining the local conditional Fisher term, acceleration, and all invariant-measure response terms;
2. an exponentially accurate finite-state transfer-operator curvature interface that can certify a true-rate sign on a compact interval when supplied with directed interval bounds;
3. a beam-splitter obstruction: output occupation mutual information is `O(u^4)` at a midpoint, so the complete quadratic curvature is carried by the unproved occupation-entropy gain, not by the manifestly nonnegative mutual information.

## Explicit fixed family

For

```text
mu=1/3,
g(theta)=cos(2pi theta)/8,
T=2,
c_epsilon(theta)=1/3+epsilon cos(4pi theta),
```

there exists a nonzero amplitude range such that

```text
t -> h(c_epsilon+t g)+t^4/98304
```

is concave on `[-2,2]`. The path is strict, the center is nonconstant, and the line does not pass through a constant symbol. Its mean `1/3` places it outside PR39's mean-`1/2` theorem.

## INCOMPLETE

This work does not prove:

- the whole legal interval for every strict exponentially local center;
- a center radius uniform up to legal endpoints;
- the PR39 fixed example on `[-384,384]`;
- arbitrary measurable-symbol concavity;
- nonnegativity of the beam-splitter occupation-entropy gain;
- a strict true entropy-rate counterexample.

No novelty, priority, or main-branch acceptance is claimed. `verification.md` is an author audit only.