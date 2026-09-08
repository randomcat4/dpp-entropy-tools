# D10-U10j non-author minimal audit: boundary noncompact scales

STATUS: PROOF_CANDIDATE_NO_BLOCKER_FOUND

This is the requested final 5-minute audit.  I only checked the quantifier logic and the load-bearing non-circular use of the \(R^6\) estimate in `proof_candidate.md`; I did not perform a full algebraic replay of every constant, cofactor bound, or normal-form reduction.  Therefore this is not a `CORRECT` certification.

## Inputs frozen

- `proof_candidate.md`, author status: proof candidate pending independent audit.
- `sanity.json`, author status: exponent sanity only, not Hessian replay.
- Prior dependency used as a conditional black-box for this minimal audit: the already-audited exponential boundary wedge where \(\sigma>0\) implies full Sym(3) Hessian negativity for the symmetric path reduction.

The author-side `sanity.json` records the input hash

```text
proof_candidate.md SHA256 a18cefffa00ccc891d5d8d21f77715d0d43aa36a13e94f628f9cbdd167cb36cc
```

## Quantifier check

The central claimed estimate is

\[
|\sigma(x,s)-\phi(\beta)|\le C\sqrt{x}\,R^6,\qquad
R=2+\beta+\beta^{-1},
\]

under \(xR^6\le c\) and \(s=\exp(-\beta/x)\le x^2\).

For any fixed \(0<\theta<1/12\) and
\[
x^\theta\le \beta\le x^{-\theta},
\]
we have, for small \(x\),

\[
R \le 4x^{-\theta},\qquad
xR^6\le 4^6x^{1-6\theta}\to0,
\]

so the hypothesis \(xR^6\le c\) is eventually satisfied.  Also

\[
\sqrt{x}R^6\le 4^6x^{1/2-6\theta}\to0
\]

exactly when \(\theta<1/12\).  Finally the worst case for
\(s=\exp(-\beta/x)\) is \(\beta=x^\theta\), giving
\(\exp(-x^{\theta-1})\), which is eventually at most \(x^2\).  Thus, conditional on the positive lower bound for \(\phi(\beta)\) from the prior wedge analysis, the stated exponent range is logically sufficient for \(\sigma>0\) for all sufficiently small \(x\).

This part passes.

## Non-circularity check for the \(R^6\) mechanism

I checked the proof skeleton for the specific circularity risk: whether the final \(O(\sqrt{x}R^6)\) conclusion is used to prove the estimates that feed into it.

The chain in `proof_candidate.md` appears non-circular:

- \(R\ge 2\), so \(xR^6\le c\) controls \(xR\), \(xR^3\), \(xR^4\), and \(\sqrt{x}R^3=\sqrt{xR^6}\).
- The provisional bound \(\|z_{\min}\|=O(R^2)\) is obtained before the sharper comparison.
- The singleton/full-atom coercive constraints then give \(\|z_{\min}-z_0\|=O(\sqrt{x}R^4)\).
- Since \(\sqrt{x}R^3\) is small, this improves \(\|z_{\min}\|=O(R)\) without assuming the final energy estimate.
- With coefficient/cofactor size \(O(R)\), the quadratic-energy comparison gives
  \(O(R\cdot R\cdot \sqrt{x}R^4)=O(\sqrt{x}R^6)\).
- The trial-side error term \(xR^7\) is also absorbed by \(\sqrt{x}R^6\) once \(\sqrt{x}R\le1\), which follows from the same smallness regime.

I did not find a quantifier loop in this argument.  The use of a single smallness condition \(xR^6\le c\) is strong enough to dominate all listed local smallness requirements.

## Remaining blockers / not certified here

- I did not independently rederive the exact constants in the normalized atom expansion, the \(N_0\) eigenvalue lower bound, the cofactor norm \(O(R)\), or the \(3\times3\) linear solve used to extract \(\|z_{\min}-z_0\|\).
- I did not replay the full Hessian-to-\(\sigma\) equivalence in this short audit; the conclusion is conditional on the prior audited reduction.
- The result remains explicitly local in the noncompact wedge.  It does not cover \(\theta\ge1/12\), algebraic scales \(s=x^p\), \(\beta=O(x)\), or faster corner regimes.

## Verdict

The two requested stress points pass: the \(\theta<1/12\) quantifier implication is sound, and the \(R^6\) estimate is strong enough to support the stated non-circular proof skeleton.  Because the full algebraic constant audit was out of scope and not completed, the correct frozen status is:

```text
STATUS: PROOF_CANDIDATE_NO_BLOCKER_FOUND
```
