# Prior-Art Ledger

Status: preliminary, not a full novelty audit.

## Sources Checked In This Round

- Russell Lyons, "Determinantal Probability: Basic Properties and Conjectures",
  arXiv:1406.2707, submitted 2014-06-10. The arXiv abstract describes basic DPP
  constructions, properties, examples, and conjectures.
- Russell Lyons and Jeffrey E. Steif, "Stationary Determinantal Processes:
  Phase Multiplicity, Bernoullicity, Entropy, and Domination", arXiv:math/0204324,
  v5 dated 2003-01-23 and published in Duke Mathematical Journal. The arXiv
  abstract states that the paper studies stationary DPPs, estimates entropies,
  and relates these processes to stochastic domination.
- Hideitsu Hino and Keisuke Yano, "Duality induced by an embedding structure of
  determinantal point process", arXiv:2404.11024, submitted 2024-04-17. The
  arXiv abstract states that it studies information-geometric structure,
  exponential-family embedding curvature, and marginal/L-ensemble duality.

## Current Relevance To T3

- This route is not claiming a new DPP theorem yet; it is building a
  reproducible strict finite certificate tool.
- The finite exact-event entropy calculation is standard finite probability
  bookkeeping, but the specific public artifact may still be useful as a
  correctness gate for T1/T2.
- Stationary entropy-rate and information-geometric curvature are nearby topics
  but not certified by v1.

## Open Prior-Art Tasks

- Add exact references for finite marginal-kernel DPP event probabilities.
- Check whether any existing package already offers rational or interval DPP
  entropy certificates with coverage/hash metadata.
- If T3 later claims new mathematical content, perform a full source-level
  novelty audit before promoting beyond prototype.
