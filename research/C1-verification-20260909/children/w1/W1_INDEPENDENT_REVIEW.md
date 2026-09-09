# W1 independent review

Status: `ACCEPTED_SCOPED` for PR32 first-round Theorem T.

Second-round status: `INCOMPLETE`; no author manuscript was available in this W1 packet. The comments below on the `m x 2` and "two nonzero coordinate columns" extensions are checks against the transcribed target only, not a verification of a supplied proof.

## Scope

I reviewed the frozen PR32 first-round package at commit `7c6e40bb3ba6dd0537f3c49bba83c718f86462fb`, restricted to `result/frozen_statement.md`, `result/proof.md`, `result/code/`, `result/inputs/`, and `result/data/`. I did not read the older PR32 review directory, old PR30 material, or any `INDEPENDENT_REVIEW.md` opinion before this judgment.

The accepted claim is exactly the rank-one cross-block scalar path in `frozen_statement.md:28-48`: fixed Hermitian strict contractions `A,C`, fixed vectors `u,v`, and

```text
K(t) = [[A, t u v*], [t v u*, C]].
```

The acceptance covers whole-configuration Shannon entropy for all events, not cardinality entropy or spectral entropy. It does not cover the original unrestricted target R in `frozen_statement.md:16`, the stationary entropy-rate target in `frozen_statement.md:103-112`, or any rank-two/general-cross-block theorem.

## PR32 first-round theorem

I find the proof of Theorem T complete in the stated scope.

The event determinant formula `p_K(S)=(-1)^|S^c| det(K-E_{S^c})` is correctly derived from inclusion-exclusion in `proof.md:10-26`. The strict-interior positivity and invertibility needed for logs, Schur complements, and derivatives are covered in `proof.md:28-39`; the boundary passage is by value continuity, not differentiating at singular endpoints, in `proof.md:219-235`.

The rank-one Schur step in `proof.md:53-96` has the right signs for every full event `(S,T)`. For `X=A-E_{S^c}` and `Y=C-E_{T^c}`, Schur plus the rank-one determinant lemma gives exactly

```text
p_t(S,T) = a_S c_T - t^2 alpha_S gamma_T.
```

This is a full event identity, not a layerwise or projected identity. The proof's fixed-marginal step in `proof.md:41-50` and the zero-marginal compensation in `proof.md:146-166` then justify the relative-entropy identity.

The curvature formula in `proof.md:169-198` follows from `P_s=P_0+sR`, zero total mass, and fixed product marginals. The strictness statement is also correctly phrased: `proof.md:200-203` gives `H''(0)=0` and `H''(t)<0` only at strict interior points with `t != 0`; strict concavity is Jensen strictness on every nondegenerate interval, not pointwise negativity of the second derivative at every point. This matches `frozen_statement.md:36-38`.

The proof does not secretly reduce by an entropy-changing basis rotation. `proof.md:270-278` explicitly warns that unitary/orthogonal rotations are not coordinate relabelings for full-configuration entropy.

## Independent compute evidence

I wrote the scope and compute plan before running checks:

- `children/w1/frozen_scope.md`
- `children/w1/COMPUTE_PLAN.md`

I then ran `children/w1/w1_independent_check.py` in W1's isolated compute directory with one numerical thread. The returned records are:

- `children/w1/job_record.txt`: Python 3.12.3, SymPy 1.13.3, NumPy 2.1.2, mpmath 1.3.0, PID 167055, exit code 0.
- `children/w1/stdout.txt`: complete JSON output.
- `children/w1/stderr.txt`: empty.
- `children/w1/compute_outputs/w1_independent_check_results.json`: structured result.

Key independent checks:

- Rank-one author example: all 16 full-event identities passed, inclusion-exclusion passed, both block marginals stayed fixed, `rank(D)=2`, and the direct `H''` at `t=1/4` matched the relative-entropy/Fisher formula to about `6.5e-82`.
- Two-coordinate-column diagnostic: all 32 event Schur conditional identities passed for an exact dense `3 x 2` cross block, but every right-event conditional direction had rank 2 and all 32 event probabilities had `t^4` terms.
- Rank-two diagnostics with `A=C=I/2`: `H''(0)=0` exactly for nonzero rank-two `B`; sampled strict-interior values in three deterministic examples were negative, but these samples are diagnostic only.
- Rotation check: two kernels with eigenvalues `1/10, 9/10` had full-configuration entropies `0.650165946782896...` and `1.164540667370039...`; this confirms that orthogonal rotation is not a coordinate relabeling for this entropy.

## Second-round m x 2 / coordinate-column extension

No second-round author proof is present, so I cannot accept the extension.

The transcribed `m x 2` claim is materially stronger than PR32. PR32 itself identifies the obstruction: once `rank(B)>=2`, full-event probabilities are generally quadratic in `s=t^2`, not affine; see `frozen_statement.md:97-99` and `proof.md:282-320`. The PR32 proof cannot be integrated as evidence for the rank-two theorem without a new argument controlling the `Q` term in `proof.md:303-320`.

The "at most two nonzero coordinate columns" version must be kept separate from the condition `rank(B)<=2`. If the two columns are actual coordinate columns, one can partition the two affected coordinates as the right block and derive, event by event,

```text
p_t(S,T) = c_T p_{A - t^2 B (C-E_{T^c})^{-1} B^T}(S).
```

My exact 32-event check confirms this conditional Schur identity. It does not prove entropy concavity, because the four conditional directions can all have rank 2. A rank condition obtained after an arbitrary orthogonal rotation is weaker and is not valid for coordinate-event entropy.

Any second-round proof must also state strictness carefully. For these block-scaling paths, `p_t` is even in `t` and the two block marginals are fixed, so `H''(0)=0` under the same product-marginal compensation mechanism. Therefore a claim of `H''(t)<0` at every strict interior point would be false at `t=0`; only strict Jensen concavity can be plausible across intervals containing zero.

## Verdict

`ACCEPTED_SCOPED`: PR32 first-round Theorem T is ready to archive or integrate as an independently checked scoped result. The accepted scope is the fixed rank-one cross-block scalar path and its stated nonstrict closed-boundary extension.

`INCOMPLETE`: the later `m x 2` / two-coordinate-column extension remains unverified until a concrete author manuscript is supplied and checked against its actual text.
