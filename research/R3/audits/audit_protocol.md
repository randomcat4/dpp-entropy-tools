# R3 independent audit protocol

Verdict for any current R3 real-domain candidate: **INCOMPLETE** until a frozen
candidate, exact certificate bundle, and fresh-context verification are supplied.
Verdict for a candidate that uses inclusion minors as exact atom probabilities,
uses the T3 positive-gap sign without conversion, or relies on ordinary floating
arithmetic for the final sign: **CRITICAL_GAPS**.

This protocol is for finite real symmetric strict positive contractions. It does
not certify a universal statement over the full real domain. It certifies only a
named finite chord or a named structure theorem whose hypotheses are proved.

## 1. Frozen object contract

The author must freeze a single object before certification:

- an integer `n >= 1`;
- rational real symmetric matrices `M,D in R^{n x n}`;
- chord endpoints `K_- = M - D`, `K_+ = M + D`;
- midpoint `M = (K_- + K_+)/2`;
- entropy convention

```text
H(K) = - sum_{S subset [n]} p_K(S) log p_K(S),
p_K(S) = sum_{T: S subset T subset [n]} (-1)^(|T|-|S|) det K_T,
det K_empty = 1,
0 log 0 = 0.
```

The R3 target sign is

```text
Delta = (H(K_-) + H(K_+))/2 - H(M) > 0.
```

If a tool defines `Gap = H(M) - (H(K_-)+H(K_+))/2`, then the R3 quantity is
`Delta = -Gap`. A positive T3-style `Gap` is evidence against the R3 sign, not
for it.

## 2. Spectral and feasibility certificate

The certificate must prove a strict contraction margin, not just display
approximate eigenvalues:

```text
delta I <= K_- <= (1-delta) I,
delta I <= K_+ <= (1-delta) I
```

for an explicit rational `delta > 0`. This implies the whole chord is feasible
by convexity, including `M`, but the certificate should still record the same
margin for all three evaluation points.

Acceptable witnesses:

- exact rational LDL or Cholesky-type witnesses for `K_r - delta I >= 0` and
  `I - K_r - delta I >= 0`, with permutations and zero pivots handled;
- exact all-principal-minor signs for small `n`;
- a rigorously outward-rounded interval eigenvalue proof with a separately
  checked residual bound.

Unacceptable witnesses:

- double precision eigenvalues or Cholesky success;
- Gershgorin rejection interpreted as infeasibility;
- endpoint feasibility inferred from small entries without a norm or Schur
  complement proof;
- clipping negative probabilities or eigenvalues to zero.

## 3. Exact probability certificate

For each of `K_-`, `M`, `K_+`, the certificate must prove:

```text
p_K(S) >= 0 for every S subset [n],
sum_S p_K(S) = 1.
```

The primary formula must be Mobius inversion from inclusion minors. A separate
reference implementation should cross-check with the mixed-row determinant
formula:

```text
p_K(S) = (-1)^{|S^c|} det A_S,
where row i of A_S is row i of K for i in S,
and row i of A_S is row i of K-I for i notin S.
```

This second formula is equivalent to extracting the exact atom from
`det(I-K+KZ)` and deliberately avoids sharing the Mobius implementation.

If grouping or symmetry is used, the certificate must include:

- the exact orbit partition of all `2^n` subsets;
- proof that every event in an orbit has the same atom probability for all
  three chord points;
- orbit sizes summing to `2^n`;
- group entropy contribution `- |O| p_O log p_O`;
- a full-event denominator stating both represented and explicitly enumerated
  counts.

No grouped certificate may aggregate inclusion minors and call the result exact
atom entropy.

## 4. Entropy and gap lower bound

For rational positive atoms, logarithms must be enclosed with a rigorous method,
for example range reduction plus the positive atanh series with an explicit tail.
For exact zero atoms, use only the mathematical limit `0 log 0 = 0`. A nonzero
atom whose interval crosses zero must trigger refinement or refusal.

Each entropy must be an interval:

```text
H_-(lo,hi), H_0(lo,hi), H_+(lo,hi).
```

The R3 lower certificate is

```text
Delta_lo = (H_-^lo + H_+^lo)/2 - H_0^hi.
```

Certification requires `Delta_lo > 0`, with the rational lower margin reported.
The output must also record target width, actual width, precision schedule,
all rounding directions, and whether the logarithm backend is exact rational,
directed interval, certified ball arithmetic, or another audited method.

## 5. Optional T2 finite-block transfer

T2 may be used only as an error-control lemma after its hypotheses are
explicitly checked for the same frozen chord and a fixed coordinate partition
`Pi`. It never creates a seed gap.

Let `B_r = blockdiag_Pi(K_r)`, `L_r = H(B_r)-H(K_r) >= 0`, and
`J_r = H(M)-[H(K_-)+H(K_+)]/2 = -Delta`. T2's Jensen identity gives

```text
Delta(K) = Delta(B) + L_M - (L_- + L_+)/2.
```

Therefore a sufficient R3 lower certificate from blocks is

```text
Delta(B)^lo - (C_-^hi + C_+^hi)/2 > 0,
```

where `C_r >= L_r` are independently certified T2 loss bounds. The midpoint loss
`L_M` helps the R3 sign and need not be upper-bounded for this one-sided lower
bound, though recording it is still useful for the full interval.

For T2 Claim B bounds, the certificate must prove:

```text
eta I <= B_r <= (1-eta) I,
C_r = tr(E_r^2 [B_r(I-B_r)]^{-1})
```

or a rigorously larger computable bound such as

```text
C_r <= ||E_r||_F^2 / (eta(1-eta)).
```

The buffer is on `B_r`, eta must be positive, and the Frobenius energy counts
all off-block entries. A universal unbuffered quadratic constant is not allowed.

## 6. Reproducibility and run ledger

Every strict run must record:

- frozen statement hash and implementation commit;
- dirty flag;
- command as an argv array;
- interpreter and dependency versions;
- platform without private host/user details;
- actual exit code and elapsed time;
- thread and memory caps;
- all random seeds, or `random_draws=0`;
- rational denominator policy and maximum numerator/denominator bit lengths;
- planned, started, completed, failed, certified request counts;
- `events_planned`, `events_completed`, `events_represented`;
- certificate SHA-256 and all auxiliary artifact hashes.

Failures, refusals, interruptions and precision exhaustion must remain as
immutable records. A resumed attempt receives a new attempt ID and links to the
old one; it may reuse checkpoints only after verifying input, code and evidence
hashes.

## 7. Fresh-context verification protocol

The original author cannot certify their own candidate. A verifier receives only:

- the frozen statement;
- the exact input file;
- the implementation commit or archived source;
- the certificate bundle;
- this audit protocol.

The verifier must not receive author commentary saying the expected sign, except
for the formal predicate in the request. The verifier works in a separate
checkout or read-only source tree and writes a separate report.

Minimum verifier checks:

1. Recompute the input and certificate hashes.
2. Parse exact rationals without binary floats, duplicate keys or unknown fields.
3. Reprove symmetry and strict contraction margins.
4. Recompute exact event probabilities by an independent formula.
5. Check nonnegativity and normalization exactly or with directed intervals.
6. Recompute entropy intervals and `Delta_lo`.
7. Check that reported coverage denominators match the actual event set.
8. Run adversarial fixtures: two-site inclusion-vs-event case, zero-probability
   boundary case, repeated eigenvalue case, tiny-gap float false positive,
   nonsymmetric input, malformed rationals, and interrupted/resumed run ledger.
9. Issue exactly one of:

```text
STATUS: CORRECT
STATUS: CRITICAL_GAPS
STATUS: INCOMPLETE
```

`CORRECT` means the named finite certificate proves `Delta > 0`. It does not
mean a structure family covers the full real domain. `CRITICAL_GAPS` is required
for a wrong event law, wrong sign, unproved feasibility, invalid rounding, wrong
coverage denominator, hash mismatch, or self-verification. `INCOMPLETE` is used
for missing but not yet contradicted evidence, unresolved precision, unsupported
feature, or a T2 transfer whose error inequality does not close.

## 8. Public-source anchors checked

- T2 Draft PR #5:
  https://github.com/randomcat4/dpp-entropy-tools/pull/5
- T2 frozen theorem:
  https://github.com/randomcat4/dpp-entropy-tools/blob/research/T2-local-entropy-tool/research/T2/frozen_theorem_v1.md
- T2 proof:
  https://github.com/randomcat4/dpp-entropy-tools/blob/research/T2-local-entropy-tool/research/T2/proofs/construction_v1.md
- T2 fresh verification:
  https://github.com/randomcat4/dpp-entropy-tools/blob/research/T2-local-entropy-tool/research/T2/verifications/fresh_v1.md
- T3 Draft PR #6, candidate only:
  https://github.com/randomcat4/dpp-entropy-tools/pull/6

The local `git clone` attempt from GitHub failed because the configured proxy
could not connect. This audit therefore used the existing read-only local mirror
under `math/i05-real-20260908/R3/repo` and web-visible GitHub pages. No remote
compute job was started.
