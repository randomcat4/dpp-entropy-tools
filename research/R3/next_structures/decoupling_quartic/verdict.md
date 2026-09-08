# NS-3 verdict

STATUS: PROVED_CANDIDATE

I found a closed local proof candidate for the two-block decoupling quartic lemma.

## Scope of the verdict

This verdict certifies only the algebraic candidate statement:

\[
K_\varepsilon=
\begin{pmatrix}
A&\varepsilon X\\
\varepsilon X^T&B
\end{pmatrix},
\qquad 0<A<I,\quad 0<B<I,
\]

with \(K_\varepsilon\) restricted to the sufficiently small interval where it remains a strict positive contraction.

It does not certify:

- a real R3 counterexample;
- concavity or non-concavity on the full real domain;
- the block-exchangeable search family as globally concave;
- any finite numerical candidate from another route.

## Result

The exact joint event probabilities satisfy

\[
P_\varepsilon(I,J)
=p_A(I)p_B(J)+\varepsilon^2r_{I,J}(X)+\varepsilon^4s_{I,J}(X)+O(\varepsilon^6).
\]

The entropy has no \(\varepsilon^2\) term because both marginals are fixed:

\[
H(K_\varepsilon)
=H(K_0)-c_4(X)\varepsilon^4+O(\varepsilon^6),
\]

where

\[
c_4(X)=
\frac12\sum_{I,J}\frac{r_{I,J}(X)^2}{p_A(I)p_B(J)}.
\]

This coefficient is nonnegative and is zero if and only if \(X=0\). Therefore every nonzero cross-block coupling direction has strictly negative R3 midpoint gap for sufficiently small nonzero \(\varepsilon\):

\[
\frac{H(K_{-\varepsilon})+H(K_\varepsilon)}2-H(K_0)
=-c_4(X)\varepsilon^4+O(\varepsilon^6)<0.
\]

## Most load-bearing steps

1. Exact atoms are obtained by Möbius inversion from inclusion probabilities. No principal minor is used as an exact event probability.
2. Inclusion minors of \(K_\varepsilon\) are even in \(\varepsilon\), and their second coefficient is the Schur-complement trace term.
3. The block marginals are fixed for all \(\varepsilon\), so the linear entropy variation in the variable \(\varepsilon^2\) cancels.
4. The fourth-order entropy coefficient is the negative one-half chi-square quadratic form
   \[
   -\frac12\sum_{I,J}r_{I,J}^2/(p_A(I)p_B(J)).
   \]
5. Equality is strict: if the coefficient vanishes, all exact-atom second coefficients vanish; summing them back to singleton cross-block inclusion events gives \(-X_{ij}^2=0\), hence \(X=0\).

## Audit context read

The route was checked against:

- `repo/AGENTS.md`;
- `research/R3/problem.md`;
- `research/R3/noise_followup/README.md`;
- `research/R3/noise_followup/completed_search_summary.json`;
- `research/R3/structure/research_note.md`;
- `research/R3/structure/summary.json`;
- `research/R3/structure/validation.json`;
- `research/R3/structure/run_log.md`.

The prior noise follow-up is consistent with this result: tiny positive float64 Hessian or midpoint signs near cross-block decoupling are expected numerical hazards, not local positive-gap evidence.

No remote computation was used, no new numerical search was launched, and no files outside `research/R3/next_structures/decoupling_quartic/` were modified.

## Fresh-verification status

This is a proved candidate from this context, not a final project-level theorem. A new independent verifier should still check:

- the Möbius sign convention in the displayed \(r_{I,J}\) formula;
- the Schur-complement trace coefficient;
- the entropy Taylor cancellation under fixed marginals;
- the equality step using singleton cross-block inclusion probabilities.
