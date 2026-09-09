# Strict Hessian Box Certificate Method

Status: method used for the accepted scoped server certificate.

## Scope

This run certifies finite coordinate boxes only. It does not prove the entropy Hessian sign on the full spectral domain `1/4 I <= A <= 3/4 I`.

The official accepted server unit is:

- Center: `R12_boundary_mid`.
- Center matrix:

```text
[[ 41/100, -3/25, 0 ],
 [ -3/25, 17/50, 0 ],
 [ 0,      0,     3/4 ]]
```

- Coordinate order: `[a11,a22,a33,a12,a13,a23]`.
- Coordinate radius: `1/2048`.
- Whole-box spectral envelope certified by Frobenius perturbation: `[509/2048, 1539/2048]`.
- Thus the whole certified box is inside `0 < A < I`.
- The whole box is not claimed to lie inside `1/4 I <= A <= 3/4 I`; the center itself lies in that target band, so the certified box has a nonempty intersection with the target band.

For every real symmetric direction `V`, the interval certificate proves that the entropy Hessian matrix on this box is negative definite, hence `H''_A[V,V] < 0` for every nonzero `V` and every `A` in the certified coordinate box.

## Probability Reconstruction

The script constructs all exact probability polynomials independently from `inputs.json`.

For the fixed rational `U`, it uses the 26 nonzero events:

- empty event: `p0 = det(I-A)`;
- singleton events: `p_i = r_i^T [A^2 + (1-tr A)A + det(A)I] r_i`;
- pair events: `p_ij = w_ij^T [adj(A) - det(A)I] w_ij`;
- triple events: `p_ijk = det(A) det(U_ijk)^2`;
- six events of size 4 or 5 are identically zero.

The script differentiates these degree-at-most-3 polynomials exactly in the six symmetric coordinates and checks that the event probabilities sum to 1 as a polynomial.

Main-instance independent reconstruction checked the final 12 centers by 5x5 principal-subset inclusion-exclusion: `12 x 32 x 28 = 10752` rational values for probability, six first derivatives, and 21 second derivatives matched exactly.

## Hessian Interval

For a coordinate box, every coordinate is replaced by a rational interval. All polynomial values, gradients, and second derivatives are evaluated by rational interval arithmetic.

For each positive event,

```text
H_ab = - sum p_a p_b / p - sum p_ab log(p)
```

is enclosed entrywise as a rational interval. The six constant-zero events contribute zero derivatives and are recorded separately.

Logarithms are enclosed by the rational atanh series:

```text
log y = 2 * sum_{j=0}^{N-1} z^(2j+1)/(2j+1) + R_N,
z = (y-1)/(y+1),  1 <= y < 2,
0 <= R_N <= 2 z^(2N+1)/((2N+1)(1-z^2)).
```

For the official server unit, `N=96`. Powers of 2 are handled by the same rational interval for `log 2` with sign-correct multiplication for negative exponents.

## Sign Certificate

The script forms an interval matrix for `-H(A)` over the whole box. Floating point is used only to select a Cholesky-based preconditioner at the center. The preconditioner is rationalized before the proof step.

For the accepted box, the script computes the interval matrix

```text
P(A) = S^T (-H(A)) S
```

with rational interval arithmetic. It then proves strict positive definiteness by Gershgorin:

```text
P_ii.lower > sum_{j != i} max(|P_ij.lower|, |P_ij.upper|)
```

for all six rows. Since `S` is square and the strict Gershgorin test makes `P` positive definite, `-H(A)` is positive definite throughout the box.

The accepted server checkpoint records:

- the rationalized preconditioner `S`;
- decimal outward displays of the entropy Hessian and preconditioned matrix intervals;
- per-row Gershgorin margins, each computed and checked as an exact rational comparison;
- all event probability bounds, including rare-event lower bounds;
- the six identically-zero events.

## Persistence

Accepted boxes are checkpointed immediately as `accepted_box_attempt_*.json` before final aggregation. This prevents a connection interruption from losing a passed box.

The official run exited normally with code 0 and wrote `certificate.json`, `RESULT.md`, `attempts.jsonl`, `center_event_jets.json`, `run_environment.json`, and the accepted-box checkpoint.

## Budget Ledger

Integration audit of the retained logs corrects the author's initial count of 85. The local debug logs contain 78 status rows for 65 distinct per-run attempt numbers. Some early attempts logged ACCEPTED before a later serialization exception, producing a second status row for the same attempt. None of those debugging statuses is an official certificate.

The server logs contain 9 status rows for 8 distinct attempts: 2 in the initial interrupted run, 3 in the compact interrupted run, 1 in a further interrupted checkpoint run, 1 failed checkpoint attempt (two status rows), and 1 final successful attempt. The failed checkpoint used an undefined filename variable; it is preserved as INCOMPLETE.

Thus there are 73 distinct recorded attempts in total. Charging every status row conservatively gives 87 against the frozen 128-attempt ceiling. The authoritative per-run counts are in `attempt_accounting.json` and the retained logs. Independent reviewer smoke/replay checks have their own bounded review budget and are not new search candidates.

No positive Hessian direction was found in the certified server unit. No finite-box certificate here is a global spectral-domain proof.
