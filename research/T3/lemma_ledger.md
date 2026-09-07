# Lemma Ledger

## LEMMA-1: Finite Exact Event Mass From Inclusion Minors

- Statement: For a finite DPP with marginal kernel `K`, the exact event
  probability `P(X=S)` equals
  `sum_{T: S subset T subset E} (-1)^(|T|-|S|) det(K_T)`.
- Status: KNOWN.
- Relative to original problem: STRICTLY_WEAKER.
- Source or proof file: standard finite inclusion-exclusion identity; used as a
  definition in `frozen_theorem_v1.md` until a formal reference is added.
- Used by: all T3 implementations.
- Dependencies: finite inclusion probabilities `P(T subset X)=det(K_T)`.
- External theorem condition check: finite ground set.
- Counterexamples or gaps: using `det(K_S)` alone fails for diagonal Bernoulli
  kernels unless all complement probabilities equal 1.

## LEMMA-2: Zero Entropy Term Limit

- Statement: `lim_{p downarrow 0} -p log p = 0`.
- Status: KNOWN.
- Relative to original problem: STRICTLY_WEAKER.
- Source or proof file: elementary calculus; encoded as convention in
  `frozen_theorem_v1.md`.
- Used by: strict entropy bounds and reference enumerator.
- Dependencies: natural logarithm on positive reals.
- External theorem condition check: one-sided positive limit.
- Counterexamples or gaps: replacing zero by arbitrary epsilon changes strict
  gap claims and is excluded.

## LEMMA-3: Outward-Rounded Entropy Interval Soundness

- Statement: If every exact event mass is enclosed and every `-p log p` term is
  enclosed with outward rounding, then interval addition gives an enclosure for
  entropy and therefore for the chord gap.
- Status: OPEN for implementation until a concrete arithmetic method is
  supplied and independently checked.
- Relative to original problem: STRICTLY_WEAKER.
- Source or proof file: pending child A/core implementation and later
  verification.
- Used by: v1 certificate.
- Dependencies: monotone/critical-point handling of `-p log p`.
- External theorem condition check: pending.
- Counterexamples or gaps: ordinary float intervals without directed rounding
  are insufficient.

## LEMMA-4: Pointwise Feasibility From Exact Masses

- Statement: For the finite certificate's covered point `t`, nonnegative exact
  masses `q_t(S)` with sum 1 define a probability distribution on all subsets.
- Status: KNOWN.
- Relative to original problem: STRICTLY_WEAKER.
- Source or proof file: finite probability definition.
- Used by: v1 pointwise chord certificate.
- Dependencies: all subsets enumerated exactly.
- External theorem condition check: finite set.
- Counterexamples or gaps: does not certify unlisted points on a path interval.
