# NS-3 hazards and audit notes

STATUS: PROVED_CANDIDATE, with fresh-verification still required

## What this lemma does not cover

- It is local at a two-block decoupling face \(A\oplus B\). It does not prove entropy concavity on the full real DPP domain.
- It does not certify or refute any frozen real counterexample away from the decoupling face.
- It does not cover arbitrary block-exchangeable parameter families except when their local tangent is exactly a cross-block perturbation with both diagonal blocks fixed.
- It does not convert finite numerical non-hits into a universal theorem.

## Exact-event hazards

- The atom \(P(Y=S)\) must be computed by Möbius inversion from inclusion probabilities, or equivalently by a valid exact-event determinant formula. A principal minor \(\det K_S\) is only an inclusion probability.
- The coefficient \(r_{I,J}\) is an exact-atom coefficient. The simpler trace formula first gives the inclusion-probability coefficient \(q^{(2)}_{U,V}\); one must still apply Möbius inversion.
- Empty subsets require conventions: if \(U=\varnothing\) or \(V=\varnothing\), the cross-block second coefficient is zero. No inverse of an empty matrix should be silently used except as a formal convention yielding the same zero contribution.

## Analytic and boundary hazards

- Strictness matters. If \(K_\varepsilon\) reaches \(0\) or \(I\), exact atoms may hit zero and the entropy Taylor expansion with \(\log p\) can fail.
- The proof only asserts existence of a small feasible interval in \(\varepsilon\). A rigorous numerical exclusion on a finite interval would need an explicit remainder bound, not just the leading coefficient.
- Near the spectral boundary, atom probabilities can be tiny; the denominator \(p_A(I)p_B(J)\) in \(c_4\) can make arithmetic ill-conditioned even though the formula is mathematically valid.

## Sign hazards

- The R3 gap is
  \[
  \Delta=\frac{H(K_-)+H(K_+)}2-H(M).
  \]
  Around \(M=K_0=A\oplus B\) with \(K_\pm=K_{\pm\varepsilon}\), the lemma gives
  \[
  \Delta=-c_4\varepsilon^4+O(\varepsilon^6).
  \]
  A positive \(c_4\) is therefore evidence for negative R3 gap, not a counterexample.
- The law is even in \(\varepsilon\) by sign conjugacy. Any apparent odd term in an implementation is a bug or a comparison of non-conjugate paths.

## Floating-point hazards

The prior `noise_followup` material identified exactly the failure mode this lemma explains:

- entropy differences near a decoupling direction can be order \(\varepsilon^4\), so subtracting three large float64 entropy values can flip signs at the ULP scale;
- Hessian eigenvalues along nearly decoupled cross-block coordinates can be numerically reported as tiny positives even when finite-step gaps are negative;
- alternating Möbius sums can lose significant digits, especially when exact atoms are small;
- logdet formulas can hide sign mistakes if implementations take absolute values before separately certifying nonnegative exact probabilities;
- normalization checks are necessary but not sufficient: a nearly normalized event vector can still have wrong local coefficients.

## Multiple-parameter hazards

For \(X(\theta)=\sum_\alpha \theta_\alpha X_\alpha\), \(c_4(\theta)\) is quartic in \(\theta\). Equality means the aggregate cross block \(X(\theta)\) is zero. If the chosen parameter basis has a kernel, that is a parameterization degeneracy, not a nonzero entropy-flat coupling.

## Coverage boundary

This structure is valuable as a local audit lens:

- it explains why decoupled or nearly decoupled block directions should produce negative small-step midpoint gaps;
- it supplies an explicit coefficient that can be used to test implementations;
- it warns against treating ULP-level positive gaps near decoupling as evidence.

But it does not cover:

- repeated-row or group-count reductions away from a decoupling face;
- low-rank updates with moving diagonal blocks;
- paths where \(A\), \(B\), and \(X\) all vary together;
- direct sums used to fabricate new seeds;
- any global real-domain concavity claim.
