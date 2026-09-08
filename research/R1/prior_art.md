# R1 prior-art notes

Status: lightweight route audit, not a complete novelty certification.

- Russell Lyons, ["Determinantal Probability: Basic Properties and
  Conjectures"](https://arxiv.org/abs/1406.2707) (arXiv:1406.2707), is the route source for the finite DPP
  entropy-concavity question. The public arXiv record describes the paper as a
  survey of DPP constructions, properties, and conjectures.
- Hino and Yano, ["Duality induced by an embedding structure of determinantal
  point process"](https://arxiv.org/abs/2404.11024) (arXiv:2404.11024; Information Geometry, 2024), studies the
  finite DPP as a curved exponential family and records the marginal-kernel and
  L-ensemble relationship. This is useful background for the coordinate system,
  but it is not a proof or disproof of the R1 real-symmetric entropy chord
  question.
- Existing local complex-Hermitian certificates are out of scope for R1 when
  their successful direction is pure imaginary. They are not reused as evidence
  for a real-symmetric chord counterexample.

This is not a complete novelty certification. The auxiliary diagonal-center
lemmas use elementary entropy inequalities; no novelty claim is made for them.

A phase-3 targeted search across arXiv, PMLR, and Project Euclid found standard
DPP definitions, entropy uses, and negative-association background, but no
direct theorem matching the complete-event Shannon entropy concavity statement
for the marginal kernel.  This negative search result is not exhaustive and
is not a novelty claim.  A convenient public definition remains the AMS
Notices survey ["DPPs: Determinantal Point Processes"](https://doi.org/10.1090/NOTI2202),
which states the inclusion-probability convention and the independent
Bernoulli interpretation of diagonal kernels.

The phase-4 trivial `S_3` reduction uses Hillion and Johnson,
["A proof of the Shepp--Olkin entropy concavity conjecture"](https://arxiv.org/abs/1503.01570),
only for concavity of the entropy of a sum of independent Bernoulli variables.
The complete subset entropy has an additional nonconstant, indefinite-Hessian
term, so that theorem does not close the DPP statement by itself.
