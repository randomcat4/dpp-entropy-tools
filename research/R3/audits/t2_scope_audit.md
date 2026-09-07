# T2 scope audit for R3

Conclusion: **CORRECT as a finite-block error-control route under its stated
hypotheses; INCOMPLETE for certifying any R3 real-domain candidate by itself.**
Misusing T2 as a seed generator, a full-real-domain theorem, an unbuffered
quadratic bound, or a sign-free transfer is a **CRITICAL_GAP**.

## 1. Exact public statement checked

The public T2 Draft PR #5 is
https://github.com/randomcat4/dpp-entropy-tools/pull/5. It is still a GitHub
Draft PR, but its public comment and branch include a finite theorem, proof,
boundary families, an exact helper, and a fresh verification report for the T2
finite tool. No Lean verification is claimed.

The checked branch is `research/T2-local-entropy-tool`, with visible commits:

```text
31143e0925f95e1c05b2165a71c0d541a20be3ef  frozen candidate snapshot
27dda692856da210e23ae74ce267b813d3221822  evidence/status metadata
```

The frozen theorem states the following finite result. For a finite complex
Hermitian marginal DPP kernel `0 <= K <= I`, a fixed coordinate partition `Pi`,
pinching `B = P_Pi(K)`, and off-block part `E = K-B`, define

```text
L_Pi(K) = H(B)-H(K),
Q_Pi(K) = tr h(B)-tr h(K),
h(x) = -x log x - (1-x) log(1-x).
```

Here `H(K)` is full-subset Shannon entropy of the DPP law, not `tr h(K)`.

Claim A:

```text
0 <= L_Pi(K) <= Q_Pi(K)
```

for all finite contractions, including singular `K`.

Claim B:

```text
if eta I <= B <= (1-eta) I with 0 < eta <= 1/2,
then Q_Pi(K) <= tr(E^2 [B(I-B)]^{-1})
              <= ||E||_F^2/[eta(1-eta)].
```

The buffer is on `B`, not on `K`; `K` may be singular. Eta zero is excluded, and
there is no dimension-free operator-norm continuity claim.

Claim C:

For a shared partition and `K_t=(1-t)K_0+tK_1`,

```text
J_K = H(K_t)-(1-t)H(K_0)-tH(K_1),
J_B = H(B_t)-(1-t)H(B_0)-tH(B_1),
J_B-C_t <= J_K <= J_B+(1-t)C_0+t C_1
```

whenever `C_r >= L_Pi(K_r)` at `r=0,1,t`.

The public helper `block_transfer.py` is narrower than the theorem: exact
rational real-symmetric inputs, sufficient Gershgorin feasibility/buffer tests,
block sizes at most eight for exact block entropy enumeration, and rational log
enclosures. Its rejection is often inconclusive.

## 2. Can T2 strictly control R3 error?

Yes, for a fixed finite chord, if all hypotheses below are certified.

Let R3 use midpoint sign

```text
Delta(K) = (H(K_-)+H(K_+))/2 - H(M).
```

Since T2's `J` sign is the opposite,

```text
J_K = -Delta(K),  J_B = -Delta(B).
```

Using T2's exact loss identity at midpoint:

```text
Delta(K) = Delta(B) + L(M) - (L(K_-)+L(K_+))/2.
```

Thus a strict finite R3 transfer certificate can use

```text
Delta(B)^lo - (C_-^hi+C_+^hi)/2 > 0.
```

This is the useful one-sided bound for R3: the midpoint loss has the favorable
sign. If the author instead uses T2's symmetric absolute interval, it must still
prove an upper bound on T3-style `J_K` below zero.

Required T2 inputs for such a transfer:

- one fixed coordinate partition `Pi` used for `K_-`, `M`, and `K_+`;
- exact/proved real symmetric strict contractions for all three kernels;
- exact block DPP entropies proving `Delta(B)^lo`;
- independently valid upper loss bounds `C_-`, `C_+`;
- for Claim B, an explicit block buffer `eta > 0` for `B_-` and `B_+`;
- a strict positive lower margin after subtracting endpoint errors.

T2 does not require full-system enumeration when blocks are small, but every
block atom still uses exact event probabilities, not inclusion minors.

## 3. What T2 cannot do for R3

T2 cannot create an R3 seed. If `Delta(B) <= 0`, the loss bound cannot turn that
into a certified positive `Delta(K)` unless the favorable midpoint loss `L(M)`
is itself lower-bounded strongly enough by a separate argument.

T2's published application has positive `J` in its own sign convention. That is
a positive concavity gap, hence negative R3 `Delta`; it is not an R3
concavity-violation seed.

T2 cannot remove the real-kernel obligation. It includes real symmetric kernels
as a subclass of complex Hermitian kernels, but a complex seed or realification
argument does not automatically transfer a full-subset entropy gap to the
original real finite set.

T2 cannot support an unbuffered quadratic error estimate. Its own boundary
family B2 shows that a universal constant in

```text
H(B)-H(K) <= C ||K-B||_F^2
```

fails without a fixed block buffer.

T2 cannot turn a direct sum into a new seed. A direct sum only adds already
present finite gaps. After normalization, an `O(1)` gap can vanish, and a
block-valued periodic construction is not automatically a scalar stationary
DPP.

T2 cannot claim coverage of the full real domain. Its theorem is a conditional
finite error transfer, not a structural classification of all real symmetric
strict contractions.

## 4. Boundary examples and their meaning

The public T2 boundary file proves two useful warnings:

- B1: operator-norm proximity alone gives no dimension-free total-entropy
  modulus, even with spectra bounded away from 0 and 1.
- B2: a fixed block buffer is necessary for a universal Frobenius-quadratic
  constant; pointwise strict interiority without a uniform margin is not enough.

These are boundary limitations. They do not disprove global DPP concavity, do
not certify a real R3 counterexample, and do not justify replacing exact entropy
with spectral entropy.

## 5. R3 decision rule for T2 use

Return **CORRECT** for a T2-assisted R3 candidate only if:

```text
all T2 hypotheses are proved,
Delta(B)^lo is computed from exact block atom entropies,
C_- and C_+ are rigorous upper bounds for endpoint losses,
Delta(B)^lo - (C_-^hi+C_+^hi)/2 > 0,
and an independent verifier reproduces the inequality from the frozen bundle.
```

Return **CRITICAL_GAPS** if any of these occurs:

- no block buffer but Claim B is used;
- `tr h(K)` is substituted for DPP Shannon entropy;
- inclusion minors are treated as exact atoms;
- the T2 `J` sign is reported as R3 `Delta` without negation;
- a positive T2 application is advertised as an R3 violation;
- T2 is used to cover all real symmetric kernels;
- public `CANDIDATE` or Draft status is treated as verified without fresh
  bounded reproduction.

Return **INCOMPLETE** when the T2 theorem is relevant but the frozen R3 seed gap,
block buffer, exact block entropy, loss constants or independent reproduction
are missing.

## 6. Public-source anchors checked

- T2 PR #5:
  https://github.com/randomcat4/dpp-entropy-tools/pull/5
- T2 frozen theorem:
  https://github.com/randomcat4/dpp-entropy-tools/blob/research/T2-local-entropy-tool/research/T2/frozen_theorem_v1.md
- T2 proof:
  https://github.com/randomcat4/dpp-entropy-tools/blob/research/T2-local-entropy-tool/research/T2/proofs/construction_v1.md
- T2 fresh verifier:
  https://github.com/randomcat4/dpp-entropy-tools/blob/research/T2-local-entropy-tool/research/T2/verifications/fresh_v1.md
- T2 boundary families:
  https://github.com/randomcat4/dpp-entropy-tools/blob/research/T2-local-entropy-tool/research/T2/boundaries/boundary_families.md
