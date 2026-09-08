# Certificate contract 0.1

Status: CANDIDATE. Strict engine integration: INCOMPLETE.
The schema and its smoke check are implemented; numerical commands below are
proposed contracts, not existing commands.

## Input and scope

Submit one UTF-8 JSON object with `kind="request"` conforming to
`certificate.schema.json`. Reject duplicate JSON keys, unknown fields, NaN,
Infinity, floats where integers are required, and files over 1 MiB before
expensive work. Rational numbers are reduced strings `numerator/denominator`,
positive denominator, no leading zeros, and canonical zero `0/1`. Exact parsing
must never pass through binary floating point. Each rational string is at most
1024 characters; matrix dimension is 1 through 8 in this version.

`K` and `D` are real, square, exactly symmetric, equal-size rational matrices.
`kernel_model="real_symmetric_contraction"` identifies a marginal kernel, not an
L-ensemble matrix. `path=[a,b]` has rational `a<b`; the actual path is `K+tD`,
not an interpolation whose endpoints are `K` and `D`. All requests first require
`0 <= K(t) <= I` on the full closed path, including curvature-at-point requests.
An unsupported model, dimension or resource budget receives a structured refusal.

| Request type | Additional fields | Exact quantity/predicate |
| --- | --- | --- |
| `feasibility` | `scope="path"`, `predicate="feasible"` | PSD contraction on every `t` in `[a,b]` |
| `entropy_chord_gap` | `scope="point"`, `weight=lambda`, sign predicate | `H((1-lambda)a+lambda b)-(1-lambda)H(a)-lambda H(b)`, `0<lambda<1` |
| `curvature` | `scope="point"`, `at=t0`, sign predicate | Classical two-sided `H''(t0)` with `a<t0<b` |
| `curvature` | `scope="path"`, sign predicate | A uniform finite enclosure for `H''(t)` throughout `[a,b]`, endpoint values interpreted as one-sided limits |

`H(t)=-sum_S p_S(t) log(p_S(t))`, in nats, sums over all `2^n` exact
configurations. A chord request evaluates a single stated weight; it makes no
claim about every chord or global concavity. A path-curvature request cannot be
satisfied by a finite grid. No finite-window result is an entropy-rate result.

`predicate` is `gt_zero`, `ge_zero`, `lt_zero` or `le_zero`. For a bound `[L,U]`,
these require respectively `L>0`, `L>=0`, `U<0`, or `U<=0`. Disproof needs the
exact logical negation. On a path, disproof of a universal sign claim requires a
certified point or subinterval counterexample; a loose uniform enclosure spanning
zero is not a disproof. Strict enclosures too wide to decide the predicate yield
`INCOMPLETE`, and cannot increment certified coverage.

## Exact events, jets and feasibility

Let `m_A(t)=det((K+tD)_A)`, with `m_empty=1`. The defining identity is
`Pr(A subset X)=m_A`, not `Pr(X=A)=m_A`. See
[Lyons (2014), equation (1.1)](https://arxiv.org/html/1406.2707v1#S1).
The exact event polynomial is

```text
p_S(t) = sum_{A superset S} (-1)^(|A|-|S|) m_A(t).
```

Enumerate bitmasks `0 .. 2^n-1`, with bit `i` denoting zero-based site `i`.
Polynomials use increasing powers of the original `t` and rational coefficients;
canonical zero polynomial is `["0/1"]`. A jet is raw `(p,p',p'')`, not Taylor
coefficients `(p,p',p''/2)`. Prove `sum p=1`, `sum p'=0`, `sum p''=0` exactly.
Probability enclosures must be nonnegative by proof, not clipped to `[0,1]` to
hide a failure. An optional `include_events` artifact contains each mask once,
the exact polynomial and requested jet enclosures; range enclosures of `p`, `p'`
and `p''` are not claims that their extremes occur together.

The independent reference path can compute `p_S=det(M_S)`, where row `i` of
`M_S` is row `i` of `K(t)` for `i in S` and of `I-K(t)` otherwise. These mixed
row determinants provide exact-configuration probabilities without an inverse
of `I-K`. Core and reference should not share the Mobius transform implementation.

For affine symmetric paths, endpoint PSD for both `K(a), I-K(a)` and
`K(b), I-K(b)` suffices by convexity. A simple evidence format is the exact list
of all principal minors for each endpoint matrix, all nonnegative. Leading
principal minors alone are insufficient for semidefinite matrices. A smaller
rational LDL witness may replace the list if the checker verifies the exact
factorization, permutations and semidefinite handling. A negative principal
minor at an endpoint disproves path feasibility; unresolved numerics do not.
No nonsingularity assumption on `K` or `I-K` is allowed.

## Precision and boundary rules

The caller supplies `initial_bits`, `max_bits`, rational positive
`absolute_width`, and finite `max_cells`, `max_seconds`, `threads`, `memory_mib`.
Require `initial_bits<=max_bits`. Width refers to the final requested quantity,
not merely each event. Acceptance requires both the width goal and the predicate
decision. A strict opposite conclusion within the width budget may be returned
as `disproved`. Feasibility uses exact signs and has no numeric width target.
Caps are hard limits, not promises of success; run one local worker by default.
The per-request maximum of one thread in v0.1 does not override aggregate T3
limits. Check resource allocation before executing; never silently raise caps.

Every finite endpoint in a strict result is an exact rational string. Interval
operations must round lower bounds down and upper bounds up; record backend,
version, working bits per cell and the reason its operations enclose the exact
result. Ball arithmetic is acceptable only if conversion of midpoint +/- radius
to rational bounds is itself outward. Ordinary floats plus printed error bars
are insufficient. Exact rational algorithms need no floating-point rounding.

For logarithms, a valid dependency-free future backend can reduce a positive
rational argument to `x=2^k*y`, `1<=y<=2`, and evaluate

```text
log(y) = 2 sum_{j=0}^{N-1} z^(2j+1)/(2j+1) + R_N,
z = (y-1)/(y+1),
0 <= R_N <= 2*z^(2N+1)/((2N+1)*(1-z^2)).
```

Enclose `log(2)` the same way and multiply its interval by signed integer `k`
with interval arithmetic. Monotonicity gives bounds for a positive interval.
The rational tail bound follows by bounding all remaining denominators by
`2N+1` and summing a geometric series. This is a specification option, not an
implemented or independently verified transcendental backend in this change.

Use `-0 log 0=0` by continuity. At chord evaluation points, exact polynomial
evaluation identifies zeros and omits their entropy terms. A positive rational
mass, however tiny, must retain its term. A nonzero mass whose interval reaches
zero requires refinement or refusal; it is not an exact zero.

Where all non-identically-zero masses are strictly positive,

```text
H'' = -sum_S [p_S''*(log(p_S)+1) + (p_S')^2/p_S].
```

The `+1` part may be cancelled only after proving `sum p''=0`. Identically zero
polynomials contribute zero at every derivative order. A zero at just one point
is different: `0 log 0=0` alone does not justify entropy derivatives there.
Version 0.1 refuses curvature on any requested domain containing a proved zero
of a non-identically-zero event polynomial, using `ZERO_CURVATURE_UNSUPPORTED`.
It does not invent a finite value for a divergent or unresolved limit. If
positivity is merely unresolved after refinement, use `PRECISION_EXHAUSTED`.
An extension supporting finite/infinite limits must specify multiplicities and
one-sided asymptotics with independently checkable evidence. Never add epsilon.

## Command proposal and failures

```text
python -m dpp_entropy_tools certify --input request.json --output response.json --artifacts evidence/
python -m dpp_entropy_tools check --input request.json --response response.json --artifacts evidence/
```

`certify` performs a single bounded request. No batch scan, network use or hidden
precision escalation is implied. Refusal policy is always `strict_only`, with
`on_unresolved="refuse"` and `zero_probability="exact_limit_or_refuse"`; callers
cannot ask to fall back to approximate certification. `check` is a future
mathematical checker distinct from the existing `specs/check_contract.py`.

| Exit | Outcome | Meaning |
| --- | --- | --- |
| 0 | `proved` | Strict complete evidence establishes the exact predicate |
| 1 | `disproved` | Strict complete evidence establishes its negation |
| 2 | `refused` | Invalid/unsupported request; no claim about its truth |
| 3 | `incomplete` | Undecided sign/width/positivity or exhausted budget |
| 4 | `failed` | Internal arithmetic, witness, integrity or implementation failure |
| 130 | `interrupted` | Cooperative cancellation; remaining cells stay unresolved |

If a downstream entropy request has a rigorously infeasible path, refuse it with
`INFEASIBLE_PATH`; do not label its entropy predicate false. A feasibility request
may instead be strictly `disproved`. Record reason codes and affected request,
event masks or cell identifiers when available. Unsupported features are refusals,
not numerical failures. An operating-system kill may prevent a terminal response:
the parent records the actual exit code, missing output and failure reason.
Never synthesize an exit-zero record or successful coverage on restart.

Write output atomically; refuse to overwrite an existing run directory. A resume
has a new attempt ID and links `resume_of` to the previous attempt; validate input,
implementation and evidence hashes before reusing a checkpoint. Maintain the
original failure record. Logs on stderr and result JSON must be separate.

## Evidence, reproducibility and hashes

The response envelope embeds the precise request claim, bounds, outcome,
coverage, and provenance. `math_status` describes only that claim and is
`PROVED`, `DISPROVED` or `INCOMPLETE`. `state` is producer lifecycle
`PREPARED/RUNNING/CANDIDATE/INCOMPLETE/BLOCKED`; the producer schema deliberately
cannot emit `VERIFIED`. Independent review is a separate attestation binding the
frozen implementation commit, raw request hash, certificate hash and checker.

Hash bytes using SHA-256. `input_hash` hashes the original request file bytes,
including any newline; a valid semantic reserialization receives a new hash.
The immutable `certificate.json` evidence file contains `schema_version`, input
hash, full request, claim, exact result, feasibility witnesses, interval cells,
event/polynomial references and their hashes, and arithmetic/rounding evidence.
Its raw byte hash is `provenance.certificate_hash`. There is no self-referential
hash: the outer response points to the certificate file, whose contents do not
contain their own hash. Every auxiliary artifact has a raw-byte SHA-256 digest.
Relative artifact paths must resolve inside the specified artifacts directory,
including after resolving symlinks; reject traversal and absolute paths.

A consumer recomputes hashes, checks the certificate's input/claim/result binding,
and checks evidence before accepting. A matching hash alone is not a proof.
Record exact implementation commit and dirty flag, interpreter and all relevant
dependency versions, platform without host/user identifiers, logical argv as a
JSON array, actual exit code, elapsed milliseconds, peak-memory value or null,
precision schedule, cells, and exact arithmetic method. The public command uses
bundle-relative filenames and no private connection parameters or credentials.
If local launch paths are private, retain the full launch record locally and
publish only the equivalent reproducible argv with that redaction disclosed.
Illustrations must use null hashes and versions rather than fabricated values.

## Coverage accounting

Counters describe unique request IDs with an immutable planned manifest hash.
For a one-request invocation, `planned=1`. `started` means execution actually
began; `completed` means the requested claim or its negation was strictly resolved
within contract; `failed` means a terminal non-completion, including refusal,
budget exhaustion and cancellation. `certified` counts completed requests with
full strict evidence, even if their requested predicate was disproved. It does
not count independently reviewed artifacts. Strict partial bounds alone count 0.

Enforce `0<=certified<=completed<=started<=planned` and
`completed+failed<=started`. Thus pending/running is `started-completed-failed`;
never include failures in completed. Attempts are separate ledger rows with IDs,
command, input hash, status, exit code, certificate hash and failure reasons.
Aggregate retries by request ID and latest designated attempt, while retaining
all earlier attempts. Report attempt totals separately; never sum retries as
additional planned objects. A response has one attempt; a sweep aggregator must
create the planned manifest before executing, not infer it from successes.
For a singleton request the request file itself is the planned manifest, so its
raw-byte hash supplies `planned_manifest_hash`. A multi-request manifest must
explicitly list unique request IDs and their raw input hashes. Parsing/validation
counts as starting the request, even if it immediately refuses malformed input.

Also record full `events_planned=2^n`, explicit `events_completed`, and
`events_represented` (the union of explicitly evaluated and implicitly covered
events via checked structural compression); these are not request
counts. Feasibility-only work can have zero completed event evaluations.
`cells_planned`, `cells_completed`, `cells_unresolved` refer to current leaf cells,
not all split ancestors. Record exact rational endpoints, coverage intervals and
endpoint conventions in evidence. A uniform certificate requires leaves covering
the entire requested domain with no gaps and zero unresolved leaves. Shared
endpoints may overlap; count each leaf once. A point claim requires just its point.
For a strictly resolved entropy request, `events_represented=events_planned`.
If `include_events=true`, `events_completed=events_planned` is also required;
the event artifact must contain every full event. This does not apply to an
early disproof of feasibility, which may stop at its first exact witness.

## Minimal fixture and integration acceptance

The supplied scalar example has `K=[1/4]`, `D=[1/2]`, path `[0,1]`, and asks
`H''(1/2)<=0`. The expected exact event polynomials are `p_empty=3/4-t/2`
and `p_{0}=1/4+t/2`; at `t=1/2` the jets are `(1/2,-1/2,0)` and
`(1/2,1/2,0)`. Hand substitution gives `H''=-1`. The response is an illustration
with `evidence.strict=false`, null execution fields and `certified=0`.

Before integration, main should run strict core/reference acceptance on at least:

- The scalar fixture; require a real endpoint feasibility witness and exact
  `[-1/1,-1/1]` curvature certificate, then independent review.
- Coupled `K=[[1/2,1/4],[1/4,1/2]]`, `D=0`, path `[0,1]`: exact configuration
  masses in mask order are `3/16,5/16,5/16,3/16`, not the inclusion minors
  `1,1/2,1/2,3/16`. This catches confusing the two distributions.
- `K=diag(0,1/2), D=0`: identically zero events are allowed and entropy is finite.
- `K=[0], D=[1]`, path `[0,1]`: chord weight `1/2` has gap `log(2)` using endpoint
  limits; path curvature is refused under the v0.1 boundary policy.
- Near-zero rational masses and tiny unresolved gaps: no epsilon and no automatic
  positive sign. Malformed input, budget exhaustion and interruption must retain
  their explicit failure records and zero completed/certified request counts.

These are proposed acceptance cases, not execution coverage claimed by this change.
