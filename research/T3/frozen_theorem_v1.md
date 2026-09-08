# Frozen Theorem v1

Status: frozen by the T3 main instance. Proof, implementation, and verification
agents may not modify, weaken, or reinterpret the assumptions.

## Objects And Definitions

Let `E = {0, ..., n-1}` be a finite ground set. Let `K0` and `D` be symmetric
`n x n` matrices with rational entries, and let

```text
K(t) = K0 + t D
```

for rational `t`.

For each subset `S subset E`, define the exact event mass of the finite DPP with
marginal kernel `K(t)` by Mobius inversion from inclusion minors:

```text
q_t(S) = sum_{T: S subset T subset E} (-1)^(|T|-|S|) det(K(t)_T),
```

with `det(K_empty) = 1`. This is the probability of the exact event `X = S`,
not the inclusion event `S subset X`.

For a feasible `t`, define Shannon entropy

```text
H(t) = - sum_{S subset E} q_t(S) log(q_t(S)),
```

using natural logarithms and the mathematical convention `0 log 0 = 0`.

Given rational `t0 < t1` and rational `alpha in [0,1]`, define

```text
tm = (1-alpha) t0 + alpha t1
Gap(t0, tm, t1)
  = H(tm) - ((1-alpha) H(t0) + alpha H(t1)).
```

## Intent Contract And Semantic Source

- Source: public T3 issue and route prompt, 2026-09-07.
- Intended meaning: certify a concrete finite entropy calculation using exact
  all-subsets probabilities and rigorous numerical enclosures.
- Forbidden trivial readings: inclusion-minor entropy, finite-window entropy
  rate claims, real-symmetric universal counterexample claims, or random scan
  non-hits.
- Semantic auditor: T3 main instance, with independent verification required
  before `VERIFIED`.

## Assumptions

For v1, a certificate may cover either:

1. the three chord points `t0`, `tm`, and `t1`; or
2. an explicitly stated rational subinterval if the implementation supplies a
   valid interval proof for every required probability or principal constraint.

The first closed-loop certificate only needs mode 1.

At every covered `t`, the implementation must prove:

- `K(t)` is symmetric over the rationals;
- all exact event masses `q_t(S)` are real and satisfy `q_t(S) >= 0`;
- `sum_S q_t(S) = 1`;
- every logarithm enclosure used for `q log q` has an outward rounding or exact
  analytic justification, including the case `q = 0`.

## Information Interface

Allowed information:

- rational entries of `K0`, `D`, `t0`, `tm`, `t1`, and `alpha`;
- requested certificate type;
- declared precision and rounding policy;
- dependency versions and command metadata;
- deterministic finite enumeration over subsets of `E`.

Forbidden information:

- hidden empirical samples or random-search outcomes as proof;
- private historical repository contents;
- long-lived credentials or server connection details in public artifacts;
- any unstated smoothness, genericity, strict positivity, or eigenvalue
  separation assumptions.

## Boundary And Randomness Conventions

- `q log q` at `q = 0` is evaluated by the limit `lim_{q downarrow 0} q log q =
  0`.
- Repeated eigenvalues, zero probabilities, endpoint kernels, and tiny gaps are
  in scope.
- If a path-interval claim is requested but only pointwise chord evidence is
  available, the certificate must mark interval coverage as `not_covered`.
- All computations are deterministic unless a future diagnostic explicitly
  records its seed. Random diagnostics cannot certify.

## Claim

If the v1 verifier returns `CERTIFIED_STRICT_POSITIVE_CHORD_GAP` for an input
instance and covered chord points, then the exact finite all-subsets DPP masses
at those covered points define valid probability distributions and

```text
Gap(t0, tm, t1) > 0
```

for the exact Shannon entropy defined above.

If the verifier returns `REFUSED`, no sign conclusion is claimed.

## Success Criteria

- A fresh context can reproduce the certificate from public files and recorded
  commands.
- At least one non-trivial rational example is certified or refused with an
  exact reason.
- At least one floating-point-looking false positive is rejected or labeled
  diagnostic-only.
- Coverage fields distinguish planned, started, completed, failed, and
  certified checks.

## Non-Claims

- No global concavity or non-concavity theorem.
- No entropy-rate theorem for stationary processes.
- No claim for all real symmetric kernels.
- No path-interval feasibility claim unless explicitly certified.
- No correctness claim for any certificate not independently verified.
