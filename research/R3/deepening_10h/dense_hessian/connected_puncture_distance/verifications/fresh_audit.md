# D10-U5 independent audit

STATUS: CORRECT for the P4 small-puncture full-Hessian theorem and, using the verified U4 diameter-two and disconnected results, the n=4 connected iff classification.

The arbitrary-dimension shortest-path coefficient rule remains a CANDIDATE. General connected-support sufficiency remains INCOMPLETE. The 38-graph/228-target n4 replay and the four-graph/40-target n5 batch remain SCOUT, not proofs over arbitrary parameters.

The author's displayed universal mixed-entry cancellation was supported in the author script only at one rational diagonal/weight assignment. That finite calculation alone is insufficient. This audit independently reconstructs the necessary *formal parameter identities*, with all four second moments, all four third moments, and all three path weights left symbolic. The universal statement is accepted on those independently checked identities and the analytic argument below, not by upgrading the author's fixed point. The author should reference this formal certificate wherever section 4 currently cites only its numerical-parameter scout.

## Frozen scope and hashes

Audited author SHA256 values:

- frozen_claim.md: `28f6358edb6d77a8f97ef2f55ade497dd8715e97419c771b19322195c23c0ddd`
- proof_candidate.md: `72ddb5f48f410d8abb713e7f671ba0ffb57ada31cf6420ac08f6e6fc00d5e4cd`
- verdict.md: `1658785c0fe3d6e762e19181dc0828a1c724db8a6f1f11d600197f922ed4f7d0`
- connected_distance_scout.py: `6edbc8eb33bee157c1c10c8bf468bba8aabceb4d0d551c630abb19ab3c4afdd6`
- scout_results.json: `6e13034c0a8392068e44ecf7a8a3ba597a3974520e921e9a915a35fee166f9d6`

All additional author hashes are recorded in independent_formal_results.json. The author scout was read but never imported or executed. Only files in this verifications directory were created. No shared index, author document, or prior certificate was modified.

## 1. Exact events and an independent finite symbolic certificate

For a strict diagonal X, define a_S and zeta_i as in the author statement. Starting directly from inclusion-probability Mobius inversion,

p_S(X+Z)=(-1)^{|S^c|}det(X+Z-I_{S^c}).

Expanding this determinant by its diagonal entries proves

p_S/a_S=1+R_S,  R_S=sum_{|T|>=2}det(Z_T) product_{i in T}zeta_i.

No principal minor is substituted for an exact event. The independent script reconstructs the determinant-permutation polynomial, obtaining 16 likelihood terms for n=4, without importing any author module. A separate direct-Mobius rational gate checks all 16 atoms at a dense rational perturbation; the probabilities agree exactly, sum to one and are positive. This numerical gate is a semantic sanity check; the determinant identity above supplies the general equivalence.

The product reference law makes the zeta_i independent, with

E zeta_i=0, E zeta_i^2=w_i, E zeta_i^3=q_i,
E zeta_i^4=w_i^3-3w_i^2,

where w_i=1/(x_i(1-x_i)) and q_i=(1-2x_i)w_i^2. Fixed singleton marginals remove the log(a_S) contribution, and E R=0. Thus

H(X+Z)-H(X)=-E R^2/2+E R^3/6-E R^4/12+O(||Z||^9).

In this formula only terms of total Z degree at most eight are retained from each displayed power. Since R starts at degree two, R^5 and higher cannot affect this truncation. All atoms are positive near each strict diagonal point, so the expansion is jointly real analytic in x and Z. Its z derivatives of order j<=2 have remainder O(||Z||^(9-j)); taking x derivatives does not lower the Z degree.

The independent script expands the finite determinant products and their character moments, keeping w_1,...,w_4 and q_1,...,q_4 as formal variables. There are 94 nonzero (edge-monomial, moment-monomial) terms. The full 94-term polynomial is stored in the JSON, together with the 16 likelihood terms. In particular this is an exact finite polynomial-identity verification, not evaluation of a finite set of x values. Coefficients vanish as polynomials even before imposing any additional relation between w and q. The retained path weights a,b,c also remain formal.

## 2. All 36 entries, not merely six diagonal curvatures

Use the observation off-diagonal coordinates e=(12,13,14,23,24,34), with E_ij+E_ji as the coordinate direction. Their P4 distances are d=(1,2,3,1,2,1). The independent certificate differentiates the full six-variable entropy polynomial twice, THEN sets z12=epsilon*a, z23=epsilon*b, z34=epsilon*c and the other coordinates to zero.

For each ordered pair (e,f) it verifies that all coefficients below degree d(e)+d(f) vanish. At exactly this degree every mixed entry vanishes, while diagonal entries are

-6*(w1*w2*a^2,
    w1*w2*w3*a^2*b^2,
    w1*w2*w3*w4*a^2*b^2*c^2,
    w2*w3*b^2,
    w2*w3*w4*b^2*c^2,
    w3*w4*c^2).

All coefficients are strictly negative for the frozen assumptions. The following table gives the first potentially nonzero degree found in the degree-eight entropy jet; a dash means that the corresponding Hessian entry has no term through degree six and hence is O(|epsilon|^7).

| |12|13|14|23|24|34|
|---|---:|---:|---:|---:|---:|---:|
|12|2|5|—|6|—|—|
|13|5|4|—|5|—|—|
|14|—|—|6|—|—|—|
|23|6|5|—|2|5|6|
|24|—|—|—|5|4|5|
|34|—|—|—|6|5|2|

Entries involving q_i may vanish at special x, so this is an order bound, not a universal assertion of a nonzero coefficient. The largest scaling exponent sum is six. Therefore the O(|epsilon|^7) analytic remainder still tends to zero after every required scaling. No uncontrolled high-order term can affect the limit.

The endpoint y=z14 coefficient can also be checked by hand. In R4^2 the coefficient of a^2*b^2*c^2*y^2 is 6; multiplication by -1/2 gives -3 product(w). In R2^2*R4 there are two matching contributions of multiplicity two, giving +2 product(w) after multiplication by 1/2. In R2^4 the four distinct edges have 24 orderings, giving -2 product(w). The entropy coefficient is -3 product(w); the y-y derivative is -6 product(w). Thus the author's -6 is correct and is a Hessian coefficient, not an entropy coefficient.

## 3. Diagonal and mixed blocks

Because the entropy offset starts at total off-diagonal degree four,

H_xx=-diag(w_1,w_2,w_3,w_4)+O(epsilon^4).

For the x-z block one must not simply use a common O(epsilon^3) estimate, since the endpoint coordinate is scaled by |epsilon|^-3. The formal first-derivative computation gives stronger separate bounds, valid identically in x:

H_{x,z_e}=O(epsilon^3) for supported edges,
H_{x,z_e}=O(epsilon^6) for e=13,24,
H_{x,z14}=O(epsilon^8).

The last follows because the first z14 derivative of the degree-eight entropy polynomial vanishes completely on P4; the analytic remainder gives degree at least eight after that derivative. The first-gradient identities are rational functions of x that vanish identically where asserted, so differentiating in x preserves the vanishing orders. The script's recorded first-gradient orders are (3,6,null,3,6,3), with null meaning zero through degree seven. Consequently all x-z blocks tend to zero after the proposed distance scaling.

## 4. Congruence, strictness and quantifiers

Let S_epsilon=diag(I_4, |epsilon|^-d(e)). For every epsilon!=0 this real diagonal matrix is invertible. The independently reconstructed blocks show operator-norm convergence

S_epsilon^T Hess H(X+epsilon A) S_epsilon
  -> diag(-w_1,...,-w_4, six negative constants above).

The leading diagonal powers are even, so the two one-sided limits coincide. All scaled mixed entries vanish. Since the limit is strictly negative definite, its least negative eigenvalue is separated from zero for each fixed admissible (X,A). Continuity of matrix eigenvalues then gives a positive epsilon threshold. Congruence preserves inertia, proving the original full Hessian strictly negative definite, on all Sym(4), for every sufficiently small nonzero epsilon.

Strict feasibility is independently enforced by shrinking the same threshold until |epsilon|*||A||_op < min_i{x_i,1-x_i}. This is not a direction-specific argument: every real symmetric Hessian direction is covered. No uniform threshold over x approaching 0 or 1, or over path weights approaching zero, has been established or claimed. At any fixed allowed epsilon, strictness and analyticity also give an ambient open strict-kernel neighborhood; its radius may shrink with epsilon.

## 5. n=4 classification and U4 dependency

The U4 proof and its nonauthor fresh_audit.md were inspected for the two imported statements: connected diameter at most two is sufficient; disconnected support supplies an exact flat cross-component direction at every strictly feasible point. The statements and hypotheses match those used here. This audit does not newly claim authorship of those results.

A connected four-vertex graph has diameter at most three. If its diameter is three, any shortest length-three path visits all vertices; every extra edge among these four vertices would shorten the distance between its endpoints. Hence the graph is exactly a relabelled P4. This proves the graph-theoretic reduction without using the count of 38 labelled graphs.

Together, the universal P4 identity certificate and U4 prove the frozen n=4 necessary-and-sufficient classification. The word 'connected' concerns the fixed support of A, not a graph reconstructed from a finite perturbation tolerance.

## 6. Finite batch accounting and general scope

Independent enumeration of all 64 subsets of the six possible edges produces exactly 38 connected labelled graphs. Their support lists agree with all 38 author output records. At the author's fixed rational x and deterministic nonzero weights of denominator 29, this audit independently specializes its own entropy polynomial, reconstructs every limiting 6x6 matrix, and exactly reproduces all six LDL pivots in each author record. This also reproduces all 38*6=228 diagonal shortest-path coefficients. Full independent target coefficients, weights and pivots are retained in the JSON, without denominator truncation.

The author's n4 shortest-path scout output only retains its aggregate target count; its source has the explicit six-target-per-graph loop. The independent replay supplies the missing per-target records here. The separate n5 output contains four selected graphs and ten target records each, totaling 40. These n5 counts and the author's loop scope were checked; this audit did not independently replay all 40 n5 coefficient calculations. No arbitrary-n conclusion relies on them.

The general '-6 times shortest-path squared sum' formula is explicitly labelled a heuristic/candidate in the frozen claim, proof and verdict. In particular, the same-vertex-set/multiple-shortest-path cross terms and mixed limiting blocks are not proved. The scope exclusions are correct. Neither negative diagonal coefficients nor finite LDL checks may be promoted to general full-Hessian negativity.

## 7. Reproduction, denominators, failures, and final layer verdicts

Run from repository root:

```text
& 'C:/Users/UIO/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe' research/R3/deepening_10h/dense_hessian/connected_puncture_distance/verifications/independent_formal_audit.py
```

Standard-library only; no random samples, external tools, or author-module import. The proof-identity arithmetic uses rational coefficients with unrestricted exact denominators. The dense direct-Mobius gate uses diagonals (1/5,1/3,3/5,3/4) and six off-diagonals (1,...,6)/100. The displayed path sanity uses weights (1/3,-2/5,3/7), reproducing diagonal constants (-75/4,-25/2,-600/49,-18,-864/49,-1200/49).

All three script executions completed with exit code 0: initial formal identity check, extension to 38-graph replay, and final full-polynomial output freeze. Final elapsed time was 0.2031714916229248 seconds. One intermediate apply_patch failed to match a context line and made no change; it was reapplied successfully. No mathematical check failed and no candidate was discarded in this audit.

- Independent script SHA256: `1031ebdc36caf2319b0cc3fe023723af3d0b91c7987be742810d01f8d911642d`
- Independent JSON SHA256: `b89df8dadb07091d5f474c26972b5abb71970e4d89f1cf1d84674a4f9c0838f3`

The JSON records runtime, so its raw hash can change on rerun even if every mathematical witness is identical. Author/dependency hashes and exact witness fields must also be compared.

Layered verdict:

- Exact-event semantics, full P4 scaled limit, mixed-block orders, congruence and strict feasibility: CORRECT, now independently reconstructed symbolically for arbitrary frozen parameters.
- n=4 connected iff classification: CORRECT, with the stated verified U4 dependencies.
- 38 n4 graphs and 228 targets: exact replay agrees, SCOUT-only evidentiary role.
- Four n5 graphs and 40 targets: accounting agrees; coefficient batch not independently replayed here, SCOUT-only.
- General shortest-path rule/general connected theorem: INCOMPLETE, correctly kept outside the proved scope.

This is a correctness audit using the math-theorem verification workflow, not a novelty audit and not a Lean/formal-kernel certification.
