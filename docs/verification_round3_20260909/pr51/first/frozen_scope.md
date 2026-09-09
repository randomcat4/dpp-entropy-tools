# PR51 first-review frozen scope

Status: first independent nonauthor review scope, before any arithmetic execution.

Frozen source: PR51 head `4baebc317896278dcb8f0947d308fdce037c87cf`, public source directory `research/I05-22-missing-edge-20260909/`.

Files read in full:

- `proof_half_filled.md`
- `sources_and_routes.md`
- `verification.md`

Claim under review, exactly as frozen in `proof_half_filled.md:7-23`:

\[
K(b,c)=\begin{pmatrix}1/2&0&b\\0&1/2&c\\b&c&1/2\end{pmatrix},\qquad bc\ne0,\quad 4(b^2+c^2)<1.
\]

For every nonzero real symmetric `3 x 3` direction `D`,

\[
\left.{d^2\over dt^2}H(K(b,c)+tD)\right|_{t=0}<0.
\]

Review includes:

- full eight complete-event probabilities, jets, Fisher term, and acceleration identity;
- complement/sign involution and exact `2+4` Hessian decomposition;
- two-dimensional sector positivity;
- four-dimensional sector formula, exact rational derivative matrix, determinant, seed minors at `r=0`, inertia continuation in `|r|<1`, and integration from singular `G_0`;
- sign changes of `b,c` and near-boundary / near-axis limits stated in the source;
- the illustrative Jensen computation only within its declared rational interval-error scope.

Exclusions:

- general unequal diagonal missing-edge centers;
- general real three-point entropy concavity;
- arbitrary chords leaving the half-filled family;
- novelty, publication priority, CI status, proof-assistant certification, and private Drive code;
- using PR41 or PR43 as accepted theorem black boxes;
- finite examples as proof of the two-parameter theorem.

Verdict scale:

- `ACCEPTED_SCOPED`: the public proof establishes the frozen PR51 theorem in the scope above.
- `NEEDS_FIX`: the claim may be true, but the public proof has a repairable gap or inaccurate statement.
- `REFUTED`: a counterexample satisfies the frozen assumptions and violates the conclusion.
- `INCOMPLETE`: the review cannot certify or refute within this bounded unit.
