# Attempt and failure ledger

These entries delimit proof methods. None is a true entropy counterexample.

## 1. Automatic use of the PR59 compact tube

The fixed center displacement is

```text
c-1/2=(1/4)cos(4 pi theta).
```

PR59 gives only an existential transverse radius. It contains no quantitative proof that this fixed amplitude lies inside that radius. Shrinking the amplitude would change the frozen problem. Therefore PR59 cannot certify the present object without a new explicit bound.

## 2. Re-centering at a nonzero parameter

At `t_*!=0`, the proposed center `c+t_*g` is not half-period invariant:

```text
(c+t_*g)(theta+1/2)=c(theta)-t_*g(theta).
```

Thus the accepted parity-decoupled local theorem cannot simply be restarted at every target point. The current proof never makes that step.

## 3. Analyticity, evenness, and a maximum at zero

The law is unchanged by `t -> -t`, and the parity joining shows `h(f_t)<=h(f_0)`. An even analytic function with a maximum at zero can still have positive curvature farther away. These facts do not prove the requested sign on `[1/2,3/2]`.

## 4. Differentiating the true-rate deficit inequality

A lower bound on `h(f_0)-h(f_t)` does not imply a lower bound on its second derivative. The fixed midpoint certificate uses finite conditional entropies plus a uniform rate error; it does not differentiate a function inequality.

## 5. Keeping only the local conditional Fisher term

The independently derived formula is

```text
h''=-nu(psi^2)+nu((psi^2-xi)v)-2nu(psi R(psi v)).
```

The first term is negative, but the other terms contain acceleration and invariant-measure response. No general sign was found for them. Reverse-martingale orthogonality of `psi` does not eliminate the factors containing `v`.

## 6. Using two-dependence as a finite Markov property

The Toeplitz kernel has range two, so the process is two-dependent. This does not make it an order-two Markov chain: the exact conditional contains the inverse of an arbitrarily long signed pentadiagonal event matrix. Treating `H(X_0|X_1,X_2)` as the entropy rate is invalid.

## 7. Negative finite-window or finite-memory curvature

A negative value of `H_n''/n` or of a depth-`r` Markov approximation is only a diagnostic. The curvature interface in `proof.md` requires the explicit conditional-mutual-information derivative tail. Computation issue #74 rejects outputs lacking that remainder.

## 8. Quantum beam-splitter entropy

At a symmetric midpoint the output occupation mutual information is nonnegative but begins at fourth order. The entire quadratic sign is in the occupation-measurement entropy gain. A von Neumann entropy inequality for the quasifree state controls a different entropy and cannot be substituted.

## 9. Direct layerwise signs

Complete entropy curvature has both Fisher and logarithmic acceleration sums. Individual cardinality layers, rare events, or three-point events can have the opposite sign from the total. The certificate and all analytic formulas retain every complete event.

## 10. Crude complex Cauchy bounds for the full entropy

The Boolean log-determinant expansion is uniformly analytic because the full row sum is below one on a neighborhood of the target interval. A direct absolute Cauchy tail, however, is too coarse relative to the approximately `10^-4` curvature scale. The successful value certificate instead uses a two-pass Schur propagation: the conditional influence decays as `rho^(2r)`, and the entropy error is quadratic in that influence.

## 11. Current outcome

A strict fixed-three-symbol true-rate Jensen gap is closed. The pointwise curvature sign over the continuum remains open. The remaining viable routes are:

1. sign or domination in the full Poisson/correlation formula;
2. the outward-rounded finite-memory/Riccati certificate with the explicit derivative tail in #74.

Failure of either sufficient route would not by itself be an entropy counterexample.