# Certifiable complexity reductions

Status: CANDIDATE design. No strict numerical reduction is implemented here,
and no measured runtime, memory or novelty improvement is claimed. "Ready"
below means specified sufficiently for the core owner to implement and test.
Bounds count exact arithmetic operations unless explicitly stated; rational
coefficient bit growth and log precision remain additional costs.

## 1. Cache minor polynomials and use the fast superset transform (ready)

For an affine `n x n` rational matrix, each inclusion minor has degree at most
its subset size. Compute each of the `2^n` minor polynomials once. Use a
fraction-free polynomial determinant or exact evaluation/interpolation with
enough distinct rational nodes and a checked degree bound. Singular numerical
pivots require exact pivot handling; inverse-based recurrences are not valid at
all boundary kernels.

Initialize `p[mask]=m[mask]`. For each bit `i`, for every mask not containing it,
replace `p[mask]` by `p[mask]-p[mask | (1<<i)]`. After all bits, `p[mask]` is the
exact configuration polynomial. Each stage reads the bit-set half, which that
stage does not mutate. The transform costs `n*2^(n-1)` polynomial subtractions
instead of the `3^n` terms across separate inclusion-exclusion sums. With at most
`n+1` coefficients, this is `O(n^2 2^n)` rational coefficient operations and
`O(n 2^n)` rational storage. This excludes constructing the minor polynomials.

Differentiate once, then evaluate cached `p,p',p''` by Horner on every interval
cell; determinant computations no longer repeat after each precision increase
or split. Store cache keys binding exact `K,D`, coordinate convention and method
version. Cache values are exact rational coefficients, not previous rounded
evaluations. Direct mixed-row determinants supply an independent cross-check.

Evidence: all masks present once, exact transform identities, degree bounds,
normalization and derivative sums. The logical event denominator remains `2^n`.
Optional export of every event still has an exponential output-size lower bound.

## 2. Endpoint-only feasibility (ready)

For real symmetric affine paths on `[a,b]`, every path matrix is a convex
combination of its endpoint matrices. Check both endpoint contractions exactly,
including singular ones. This replaces feasibility checking in each of `q`
subdivision cells with four endpoint PSD checks (`K` and `I-K` at each end).
The evidence includes endpoint values and the affine convex-combination identity.
This shortcut does not certify entropy curvature between endpoints and is not
valid for a general nonlinear path without an additional proof.

## 3. Common coordinate blocks and diagonal kernels (ready)

Build the undirected graph with edge `(i,j)` iff `K_ij` or `D_ij` is exactly
nonzero. Its connected components give a common coordinate permutation making
both matrices block diagonal. Never infer blocks by thresholding small entries.
The probability generating determinant factors across these blocks, so exact
configurations have product masses and Shannon entropy is the sum of block
entropies. Therefore curvature and chord gaps add as well.

For block sizes `b_1,...,b_r`, entropy work can use `sum_j 2^b_j` block events
instead of materializing `2^n` full events, plus interval additions and a budget
allocation whose final widths sum to at most the requested width. A diagonal
path is the Bernoulli special case, with `O(n)` scalar entropy contributions.
This is a full-distribution factorization, not entropy computed from inclusion
probabilities or eigenvalues of a general kernel.

Evidence: explicit permutation, exact zero off-block entries in both matrices,
each block's evidence and the factorization rule. Report full event count `2^n`,
number explicitly materialized, and number represented by the checked product.
If the caller asks for every full event jet, reconstruct products and derivatives
and acknowledge `Omega(2^n)` output cost. A common orthogonal eigenbasis is not a
substitute: Shannon entropy of coordinate configurations is not generally
invariant under arbitrary basis changes.

## 4. Deterministic adaptive interval subdivision (ready)

Start with the requested domain. Evaluate cached event polynomials and jets with
outward arithmetic. Split an unresolved cell at its exact rational midpoint;
prioritize positivity failures, then the widest result enclosure, with left
endpoint as deterministic tie-breaker. Precision doubles up to `max_bits`; both
precision changes and splits count against finite budgets. Reuse immutable
polynomials, never a parent cell's sign conclusion without valid containment.

Retain a split tree with rational endpoints and leaf status, so the checker can
prove full coverage. The final uniform curvature enclosure is the hull of all
leaf enclosures. Subdivision can reduce dependency overestimation and avoid
reevaluating already-resolved regions, but has no guaranteed speedup or finite
termination near a true zero/sign change. Never discard inconvenient leaves.
Single-point chord calculations benefit from precision refinement, not from
claiming a path subdivision proves additional chord weights.

## Future options requiring additional witnesses

- Symmetry orbits: prove an exact site permutation preserves both `K` and `D`
  before reusing event polynomials and multiplying contributions by orbit size.
  Store representatives, multiplicities and complete partition coverage. Equal
  approximate probabilities or equal eigenvalues do not establish this symmetry.
- Particle-hole pairs: `p_S(K)=p_complement(S)(I-K)` links two kernels. Reusing
  paired events on the same path requires an exact symmetry mapping of that path,
  possibly `t -> a+b-t`; an equality at one point is insufficient for jets.
- Bernstein polynomial enclosures can tighten probability lower bounds before
  using higher precision. Conversion, sign/range bounds and root isolation must
  have exact witnesses before they can replace the basic interval method.

## Benchmark after correctness closes

Compare against the independent complete-event determinant implementation on the
same exact requests, precision goal and machine allocation. Record input and
certificate hashes, explicit/logical event counts, determinant evaluations,
transform operations, cell/precision history, elapsed time, peak memory and
outcomes. Include a coupled case where blocks do not help and a near-boundary
case where splitting exhausts its cap. A failed run is not a speedup. No benchmark
has been executed by this interface deliverable.
