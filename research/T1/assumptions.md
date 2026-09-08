# Assumptions and interface

- n is any positive integer; K is real symmetric and 0<K<I.
- A is real skew-symmetric and D=iA. The real parameter t is local around 0.
- Every active edge of A is an existing bridge of the support graph of K.
- Entropy is the finite full-event Shannon entropy in nats, not entropy rate.
- The input is deterministic. There are no sampling or probabilistic success claims.
- The implementation accepts only integer or rational-string matrices. Floating
  inputs are rejected; exact zero support decisions must not use tolerances.
- Strict positivity of K and I-K is checked by exact LDL pivots. The mathematical
  theorem allows real entries, while this implementation covers rational entries.
- Rejection of a theorem hypothesis is not a curvature sign judgment.
- Zero direction has zero curvature. Boundary kernels are outside this checker.
- The proof author and verifier may not alter the frozen hypotheses.
