# R1 rounds

## Round 0: setup and calibration

Status: RUNNING.

Public checkout branch: `research/R1`.

Initial components:

- `param_opt/`: bounded full-Hessian spectral parameter search over
  `n=3,...,10`.
- `prob_deriv/`: independent exact-event and directional-derivative reference.
- `certificate/`: exact rational chord verifier for a JSON candidate.

The first required tests are derivative calibration against finite differences,
exact event probability identities, and strict rejection of complex-direction
certificates as out of scope.

## Round 1: independent formula and optimizer lanes

Status: INCOMPLETE/NO_HIT finite evidence.

The probability/derivative lane completed an independent implementation check
for n=2,...,5. It verified exact inclusion-exclusion event probabilities
against the L-ensemble formula on a rational 3 by 3 kernel, checked
finite-difference first and second entropy derivatives, and confirmed
`sum p'_S=sum p''_S=0` to floating precision. Largest reported Hessian
finite-difference error was below `1e-7` in the main n=2,...,5 table.

The optimization lane completed two bounded batches over n=3,...,10:

```text
batch01: 4,960 objective calls, seed 202609081, positive > 1e-6: 0
batch02: 8,242 objective calls, seed 202609082, positive > 1e-6: 0
```

The best reported value was `-6.245093781582534e-15` at n=3, with direct
midpoint gap `-3.960165528837933e-12`. This is a near-flat negative object, not
a counterexample.

## Round 2: strict certificate tool

Status: IMPLEMENTED, with no positive candidate supplied.

The corrected rational verifier checks strict endpoint feasibility by exact
Sylvester minors, rebuilds every exact DPP event probability, and bounds the
entropy gap using rational logarithm intervals. Its three bounded tests return:

```text
negative feasible chord -> CERTIFIED_NEGATIVE_GAP
zero direction          -> GAP_UNCERTAIN
infeasible endpoint     -> NOT_FEASIBLE
```

An earlier exploratory scope deviation produced extra scout files in the work
tree. They are deliberately excluded from the committed search denominator and
result claims.

## Round 3: structured diagonal-center family

Status: VERIFIED_FOR_FAMILY.

The diagonal-center Hessian proof gives, for every diagonal strict contraction
K and every real symmetric direction V,

```text
D^2 H(K)[V,V] = - sum_i V_ii^2/(p_i(1-p_i)) <= 0.
```

An independent proof shows the stronger finite-chord statement: every
nontrivial feasible real-symmetric chord centered at a diagonal strict
contraction has strictly negative midpoint gap. The first pre-freeze wording
omitted `t>0`; the `t=0` equality counterexample and the repaired frozen
statement are both retained.

Both frozen statements and proofs were fixed in commit
`a49051d2f768ec2b926a2e4d68d5286b054f9656`. Reviewers who did not author the
respective proofs read the committed blobs via `git show`; both returned
`STATUS: CORRECT`. The reviews record the commit and Git blob IDs.
