# N4: connected real kernels in dimensions four and higher

Status: `STOPPED_SUBSTANTIVE`; the global question is `INCOMPLETE`.
Baseline: `fa504ec74e16843fafc395880d7ba99b4c1d2129`.
Coordination: public issue #21; this route owns only `research/N4/`.

We test concavity of the full configuration Shannon entropy of finite real
DPPs on strict positive contractions. The sign convention is
`Delta=(H(K-tD)+H(K+tD))/2-H(K)`; a counterexample requires strict positivity.
See [frozen statement](frozen_theorem_v1.md) and [checkpoint](checkpoint.md).

First unit: four-vertex complete and diamond graphs, inequivalent cycle
signs, unequal diagonal entries, moving eigenvectors and multiple spectral
slack scales. Save the maximal-curvature direction, feasible radius, and
eventwise Fisher/acceleration decomposition before deciding whether to expand.
Three independent children own `mechanism/`, `search/`, and `review/` in
separate checkouts. All computations start single-threaded, with at most two
simultaneous numerical jobs initially. No GPU; route ceiling 8 CPU threads
and 32 GiB. Other routes and jobs must not be modified.

Finite non-hits, numerical stability, rigorous finite certificates, general
proofs, independent review, and novelty are separate evidence classes.
Existing R2 fixed-data projection and A2 compact moving-frame exclusions
are inherited scope boundaries, not new N4 results.

## Completed results

- **Reviewed restricted theorem:** for any number of independent leaves with
  fixed marginal probabilities and fixed nonzero connection vectors, entropy
  is jointly strictly concave along nontrivial finite chords in the central
  real 2 by 2 block and all scalar connection lengths, including zero lengths.
  [Proof](mechanism/mixed_gain_attempt.md), [review](review/m2_mixed_gain_review.md).
- **Reviewed conditional exclusion:** for fixed strict central data with leaf
  scales r^2 and r^4 and strictly negative limiting single-column Hessians,
  the normalized two-column interaction is O(r^3). A displayed rational
  benchmark satisfies the Hessian premise by rigorous log intervals.
  [Proof](proofs/two_scale_candidate.md), [review](review/two_scale_candidate_review.md),
  [benchmark](review/p2_benchmark_review.md).
- **Finite evidence:** 514 retained research kernel evaluations and 3930 affine
  chords in dimension four, including repeats; no positive candidate. The
  near-unit gain .998972 was traced to a common rare-event Fisher term.
  [Search checkpoint](search/checkpoint.md), [diagnosis](search/batch3_report.md).
- **Independent finite certificates:** three rational fixtures have strict
  feasible endpoints and strictly negative gaps. Rationalized fixtures are
  distinct from their binary64 source objects. [Ledger](review/run_ledger.md).

One fresh non-author reviewer checked both scoped proofs and arithmetic
premises. These are not two independent reviewers of a main conclusion.
No unrestricted result, novelty certification or full Lean proof is claimed.
See [verdict](verdict.md), [checkpoint](checkpoint.md), and
[reproduction](reproduction.md). No automatic restart is scheduled.
