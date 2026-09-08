# N4: connected real kernels in dimensions four and higher

Status: `ACTIVE_RESEARCH`; the global question is `INCOMPLETE`.
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
