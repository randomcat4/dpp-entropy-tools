# Rounds and coverage

## Round 0: initialization and scope audit

- Read public AGENTS, COMMON protocol, PR #11 frozen hierarchy and two C2
  reviews. User's later real-domain and model authorization controls scope.
- Created an isolated A2 branch and checked existing local/remote state.
- Remote resources were ample; other processes were left untouched.
- Local authenticated public-repository access worked after process-local
  removal of stale proxy settings. Remote HTTPS clone failed its CA check;
  a public git bundle will supply the isolated remote checkout.
- No mathematical computation or search has started yet.

## Round 1: a concrete path outside the old representation

- Two geometric versions considered: physical angle t, then the selected
  rational rotation. One sign family was frozen as v2.
- The endpoint eigenvalues prove exact feasibility; noncommuting midpoints
  obstruct both old fixed-data midpoint forms under any common scalar
  reparameterization or fixed orthogonal representation.
- Author proof derives every exact event from a generating determinant and
  gives Delta=-G(x^2)t^2+O_J(t^3 log(1/t)), uniformly on compact J in (0,1).
  This excludes the selected path near zero but leaves shrinking x outside.
- Candidate commit: ab4d57cdbdc782fd033178795da9873db01bf7be.
- A separate implementation passed its toy full-law and one-chord smoke
  before two bounded jobs: 48 symbolic event formulas and six further rational
  chords. All seven Delta intervals are strictly negative. No global
  inference is drawn from the seven points.
- Job wall times: smoke 0.135 s, symbolic 1.435 s, six-chord certificate 1.163 s.
  At most two one-thread jobs overlapped, each capped at 4 GiB. All exited 0.

## Round 2: uniform estimates and an explicit failure of extrapolation

- A separate analytic unit proposed four objects: zero-safe entropy error,
  matrix perturbation error, a uniform moving mixed-family estimate, and a
  shrinking-direction crossover. No computation was run by that author.
- These were frozen separately as v3; the v2 assumptions were unchanged.
- Candidate commit: 5084d3966a3eccc3ad5b497f1da6eab08fe7554a.
- The crossover gives three distinct leading scales and an explicit error
  bound. It invalidates informal substitution into a fixed-data asymptotic,
  while preserving the old theorem and the already known two-point sign.
- An independent reviewer received immutable v2 and v3 candidate packets;
  neither author reviews their own proof.

## Partial formal check

- Lean 4.32.0 was available; no Mathlib project/cache was used or downloaded.
- Five fixed integer matrix identities compiled with exit 0, with only
  propext in their printed axiom dependencies. The entropy and asymptotic
  statements are not Lean-checked. See formal/README.md.
