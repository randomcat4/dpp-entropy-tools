# R3 structure coverage matrix

Conclusion: **CRITICAL_GAPS** for any claim that the listed structured families
cover the full real-symmetric strict-contraction domain. **CORRECT** only means
that a family-specific certificate covers the family it names. **INCOMPLETE**
means the family may be useful but lacks a frozen proof or exact certificate.

| Scope or family | What it can certify | Required denominator / coverage evidence | Boundary not covered | R3 verdict use |
| --- | --- | --- | --- | --- |
| Single frozen rational chord | One finite instance `K_-=M-D`, `K_+=M+D` | `3*2^n` represented event laws, or a proved complete orbit quotient; exact hashes and gap lower bound | No neighborhood, no all-real claim, no rate claim | Can be **CORRECT** for that instance only |
| Small-n exhaustive exact enumeration | All events for all named small matrices | Exact event masses by Mobius plus independent mixed-row determinant cross-check | Larger `n`, symbolic families, high-dimensional generic directions | Strongest point certificate; still not universal |
| Repeated-row / repeated-type families | Kernels invariant under a declared coordinate type partition | Explicit symmetry group, orbit list, orbit sizes summing to `2^n`, proof that `K_-,M,K_+` preserve every orbit | Any perturbation breaking row/type equality; generic real symmetric matrices | Useful for a structured theorem; never full real domain |
| Block-exchange / swap-invariant families | Kernels invariant under exchanging specified blocks or coordinates | Group action, stabilizers, orbit representatives, exact block/event probabilities for each orbit | Unequal blocks, asymmetric couplings, arbitrary off-block entries | Family-specific only; "exchangeable" is a hypothesis, not coverage |
| Low-rank update `M + UV^T` or `M + tD` with low-rank `D` | A low-dimensional submanifold of directions | Rank witness, exact entries, feasible interval, exact gap or rigorous T2 transfer | Generic tangent space has dimension `n(n+1)/2`; low rank alone does not imply entropy area law | Candidate generator; not a domain reduction |
| Block direct sums | Additivity of already certified finite gaps | Component certificates, multiplicities, total entropy additivity, normalized gap accounting | No new seed; per-site gap can vanish if bad blocks have zero density | Amplifies only an existing sign |
| T2 finite-block transfer | Transfer a certified block gap through controlled off-block coupling | Fixed partition, exact block gap, endpoint loss bounds, block buffer `eta`, strict error inequality | No seed generation, no unbuffered bound, no scalar stationary/rate transfer | Error-control lemma only |
| T3 PR #6 certificate prototype | Candidate finite exact-event certificate interface | Fresh verifier bound to commit, independent event-law recomputation, schema/hash/coverage checks | Public PR #6 is Draft/CANDIDATE; no verifier file or `VERIFIED` state | Cannot be used as verified without new-context audit |
| Random or grid search over real kernels | Produces candidates and falsifies some local statements | Full manifest, seed, planned/started/completed/failed counts, exact post-hoc certificates for survivors | Non-hits prove nothing globally; selection bias; grids miss open sets unless covered by interval proof | Diagnostic only |
| Floating high-precision scans | Numerical hints and regression fixtures | Precision, rounding mode, residuals, exact replay inputs; then strict rational/interval certificate | Final sign, feasibility, near-zero probabilities, tiny gaps | Never sufficient for `CORRECT` |
| Pure imaginary bridge from T1 | May help complex/Hermitian directions under its own hypotheses | Frozen theorem and proof that direction really lies in the certified class | User specified R3 real direction; pure imaginary bridge does not apply | Not usable for R3 real certificate |
| Complex-to-real realification | Only if a separate entropy-preserving theorem is proved | Exact map, ground-set relation, law preservation, entropy relation, gap sign preservation | Standard `2n x 2n` real block representation changes the ground set and atom law | Not a shortcut |
| Finite-window to entropy-rate passage | A separate rate theorem | Uniform gap density, limit order, tightness/continuity proof, scalar kernel construction | Fixed finite gap may vanish after normalization; periodic block process not scalar stationary | Outside current R3 certificate |

## Full-domain dimension warning

The real symmetric `n x n` affine tangent space has dimension

```text
n(n+1)/2.
```

Repeated-type, exchangeable, low-rank, Toeplitz, banded, graph-gluing and block
families occupy special lower-complexity subsets unless a theorem proves
otherwise. Finding a certified gap in one family disproves a universal concavity
statement if the object satisfies the original full-domain hypotheses, but
failure to find a gap in any finite collection of families is not evidence for
the universal theorem.

## Minimum coverage report

Every R3 run must include a denominator table:

```text
candidate_families_planned
candidate_families_started
candidate_families_completed
candidate_families_failed
candidate_instances_planned
candidate_instances_started
candidate_instances_completed
candidate_instances_failed
candidate_instances_certified
events_planned
events_completed
events_represented
orbits_planned
orbits_completed
random_draws
random_seed
```

If no random search was used, record `random_draws=0` and `random_seed=null`.
If a family is claimed symbolically, the denominator must be the quantified
parameter set and proof obligations, not just the examples printed in logs.

## Verdict mapping

Use **CORRECT** only for a named finite object or named structure family whose
quantifiers are exactly proved.

Use **CRITICAL_GAPS** for any statement of the form:

- repeated-row families cover all real kernels;
- block-exchange families cover all real kernels;
- low-rank perturbations are representative of all real directions;
- direct sums create a seed without an existing component gap;
- finite non-hits imply global concavity;
- complex or pure-imaginary results automatically transfer to real symmetric
  chords.

Use **INCOMPLETE** for unexplored families, failed runs, partial grids, PRs still
marked candidate, or structure reductions whose orbit/stabilizer proof is not
yet frozen.
