# T1 verdict

Stage status: CANDIDATE, final domain review in progress.

The first independent reviewer returned STATUS: CORRECT on pinned commit
`a71d52bc8c5b45df9ea4795343c290899a2d1f84`. The complete report is
[fresh_v1.md](verifications/fresh_v1.md); its scope includes the frozen theorem,
anonymous proof, exact rational checker, and the two non-seed inputs. The main
instance did not rewrite the proof. A second context-isolated reviewer is
checking the same frozen mathematical files without access to the first verdict.

The candidate is a useful sufficient test: for real strict-contraction K and
D=iA supported on existing support-graph bridges, H'' is negative exactly when
A is nonzero. The checker uses exact rational positivity and graph checks and
evaluates no event probabilities. Dense blocks connected by single bridges are
an unbounded covered family; the n=30 concrete case avoids its 2^30 event law.

Practical usefulness, correctness and explicit scope are the delivery criteria.
Novelty is not required. Existing rank-one concavity is credited in prior_art.md.
No claim is made about cyclic active edges, arbitrary real directions, boundary
kernels, stationary entropy rates, or a numerical magnitude enclosure.

Boundary and alternative-route files in exploration/ retain CANDIDATE status;
the first proof review does not certify them. No formal Lean verification was
performed. Final closure will preserve the reviewed theorem and code hashes.
