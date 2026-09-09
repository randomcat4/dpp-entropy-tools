# C3 PR29 independent verification verdict

Covered frozen commit: `648f1906468e3e548410f98a6b1a53a978f2ea11`.

Reviewer role: non-author C3 cross-check. I did not merge, open a PR, alter PR29 sources, or use PR30 author self-acceptance as evidence.

## Scope A: radial theorem

Verdict: `ACCEPTED_SCOPED`.

The proof in `sources/pr29/proof.md` proves the two frozen statements in `sources/pr29/frozen_statement_v2.md`: finite entropy concavity on every feasible radial interval through an interior diagonal kernel, and scalar stationary true entropy-rate concavity on every legal line through a constant symbol.

Core reasons:

- The product replacement channel is identified exactly with the finite DPP family `B+t(K-B)` by inclusion moments and determinant expansion (`proof.md:83-105`).
- The bidirectional KL contraction step gives entrywise nonnegative mixed derivatives, and the proof uses it only for the simultaneous all-ones retention path, not as a PSD Hessian claim (`proof.md:44-69`, `proof.md:173-176`).
- Positive and negative half-rays are joined at the interior product point using equality of one-sided derivatives and the three-point concavity criterion (`proof.md:116-141`).
- Diagonal changes, noncommuting `A`, complex Toeplitz finite compressions, and boundary symbols are covered (`proof.md:83-112`, `proof.md:145-157`).
- The true entropy-rate conclusion passes through pointwise finite-block entropy inequalities and subadditive limits, with no derivative/limit interchange (`proof.md:159-169`).

Scope limits: no full Lyons-Steif conjecture, no arbitrary scalar chord, no arbitrary finite affine direction away from an interior diagonal base, and no novelty certification.

## Scope B: fixed C3-M1 rate certificate

Verdict: `ACCEPTED_SCOPED`.

The fixed C3-M1 certificate proves a strictly negative true entropy-rate pair gap:

```text
(h(f_-)+h(f_+))/2 - h(f_0) < 0.
```

The replay in `children/c3/compute_replay/` used Python `3.12.3`, numpy `2.1.2`, mpmath `1.3.0`, sympy `1.13.3`, one CPU thread, no GPU, and the frozen `M=64`, `bits=160`, `n=4` parameters only.

Core replay outcomes:

- Boundary replay: 6 cases, 66 residual rows per case, all operator errors below `1/200`.
- Rate replay: 288 exact determinants, `NEGATIVE_PAIR_GAP`.
- Supplied audit replay: `CORRECT_SELF_AUDIT`.
- Reviewer exact checker: `REVIEWER_CHECK_PASS`, including separate permutation determinant recomputation of all 288 event determinants.
- Exact negative upper endpoint:

```text
-299855012916397501897282364769067397783
/356811923176489970264571492362373784095686656 < 0
```

Non-blocking documentation issue: `rate/candidate.json:6` says the negated `b/db` input gives conjugate-transpose Toeplitz kernels. Under the declared script convention `c_k=(a_k-i*b_k)/2` and `K(i,j)=c_(i-j)`, the negated values instead give the true coefficients `(a_k+i*b_true_k)/2` at all three `t` values. `rate_analysis.md:130` already states the correct interpretation. This should be clarified if the artifact text is edited, but it does not affect the certificate.

Scope limits: fixed C3-M1 only; no family theorem, no larger-window claim, no long-range-symbol certificate, no positive counterexample, and no novelty certification.
