# Attempt and failure ledger

These are proof-route outcomes, not entropy counterexamples.

## 1. Re-centering the accepted local theorem at `t_*!=0`

For

```text
f_t=c+t g,
c(theta+1/2)=c(theta),
g(theta+1/2)=-g(theta),
```

the proposed new center would be `c+t_*g`. It satisfies

```text
(c+t_*g)(theta+1/2)=c(theta)-t_*g(theta),
```

which is not equal to `c+t_*g` unless `t_*=0` or `g=0`. Thus the parity-decoupled hypothesis of PR53 is lost. Applying the local theorem separately at every `t_*` would be circular and invalid.

The compact-tube proof avoids this: it uses joint RPF continuity in the **original even center variable** and the whole-line strict margin at the constant reference center.

## 2. Analyticity plus a global maximum at zero

The parity identity gives

```text
h(c+t g)<=h(c)
```

and the rate is analytic under the strict exponential hypotheses. Neither fact implies concavity. An even analytic function can have a strict maximum at zero while its second derivative changes sign away from zero. The proof therefore transports a quantitative curvature margin, not merely the maximum or analyticity.

## 3. Using only the rate deficit from the parity point

The matching inequality gives a positive lower bound for

```text
h(c)-h(c+t g).
```

A lower bound on a function does not in general determine the sign of its second derivative away from zero. Differentiating that inequality is unjustified. The new theorem uses the deficit only indirectly through the already reviewed radial curvature theorem and RPF continuity; no inequality between functions is differentiated.

## 4. Dropping prediction acceleration or invariant-measure response

For a normalized one-sided conditional `G_t`, the local binary-entropy curvature contains the conditional Fisher term, but the stationary future/past distribution also varies with `t`. The exact formula proved in `proof.md` is

```text
h''=nu(Bddot)+nu(xi u)
    +2nu(psi R Bdot)
    +2nu(psi R(psi u))
    -nu(psi^2 u).
```

Keeping only `nu(Bddot)`, or only its negative Fisher component, is not valid. No general sign was found for the four response terms. The compact-tube theorem bypasses their individual signs by stability from a reference chord with a strict known total margin.

## 5. Pointwise concavity of all complete-event conditionals

The exact conditional kernel after revealing one parity block has the form

```text
A+t^2D_y,
D_y=-C(B-I_{Z(y)})^{-1}C*.
```

The matrices `D_y` are configuration dependent, high rank, and generally indefinite. The average at `t=0` vanishes, but there is no pointwise Hessian sign for every `y` away from zero. Replacing the required averaged total curvature by pointwise conditional concavity would be a stronger unproved assertion.

## 6. Balanced fermionic beam splitter and quantum entropy

For symmetric inputs at `t_*-u` and `t_*+u`, the output occupation law satisfies

```text
midpoint gap=output occupation mutual information+occupation entropy gain.
```

The first term is nonnegative, but the proof shows it is `O(u^4)`. It therefore contributes nothing to quadratic curvature. The entire second-order sign is in the occupation entropy gain, whose nonnegativity remains open. A von-Neumann entropy inequality controls spectral quantum entropy, not the fixed occupation-basis Shannon entropy, and cannot replace this missing term.

## 7. Universal local classical refresh

The main route ledger and accepted PR39 channel audit already rule out a channel depending only on the correlated diagonal blocks that uniformly scales every small cross block. This does not refute a family-specific or nonlocal construction, but it prevents using a universal local refresh as an automatic proof of the present chord.

## 8. Finite-window curvature diagnostics

A finite negative value of `H_n''/n`, even for several window sizes or parameter points, is not a true-rate theorem. The finite-state RPF bridge in `proof.md` requires an explicit volume-independent tail/resolvent error. No floating probe is used as evidence for Theorem CT.

## 9. Endpoint continuation by compactness

The center radius in Theorem CT depends on a positive strict spectral margin on `[-T,T]`. As `T` approaches a radial legal endpoint, this margin may vanish and the uniform event-inverse/RPF neighborhood can collapse. Taking a sequence of compact intervals does not produce one fixed positive center radius valid up to the endpoints. Endpoint coverage remains open.

## 10. Outcome of this round

The whole arbitrary-center problem is not closed. The successful route is a transverse stability theorem around a quantitatively strict reference chord. It covers nonzero parameters and arbitrarily prescribed compact radial intervals, but only for centers in an `A_beta` neighborhood of a constant. The exact general-center RPF Hessian and beam-splitter obstruction are retained as the next interfaces.