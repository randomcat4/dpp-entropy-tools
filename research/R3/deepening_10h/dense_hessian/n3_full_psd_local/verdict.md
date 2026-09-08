# D10-S5 author verdict

STATUS: **CORRECT_AFTER_FRESH_REVIEW_AND_REVISION_RECHECK** for the full
Hessian theorem and local-neighborhood consequence; finite PSD optimization
remains `SCOUT`.

The fixed-\(Q\) M7 result can be genuinely enlarged at the specific rational
base \(K_*\) of equation (19).  In fact, the exact-event entropy Hessian at
\(K_*\) is negative definite on the full six-dimensional real symmetric
direction space:

\[
H''_{K_*}[D,D]<0
\qquad(D=D^\top,\ D\ne0).
\]

This covers arbitrary PSD and NSD directions, including noncommuting
observation-coordinate directions.  The proof is not a finite non-hit: it uses
exact-event Möbius atom jets, rational intervals for the logarithms of rational
base atoms, and a strict Gershgorin diagonal-dominance certificate for the
matrix of \(-H''\).  The minimum certified row margin is approximately

\[
1.7200075505>0.
\]

Consequences:

1. On the Frobenius-unit PSD cone, the maximum of \(H''_{K_*}\) is strictly
   negative.  A certified upper bound follows from the Gershgorin margin:
   \[
   H''_{K_*}[D,D]\le -m\|x(D)\|_2^2
   \le -\frac m2\|D\|_F^2
   \]
   for the exact \(m>0\) recorded in `hessian_scout.json`.
2. By continuity, there is an open neighborhood of \(K_*\) on which the full
   Hessian remains negative definite.  No explicit radius is claimed.
3. The exact PSD-cone optimizer was not solved symbolically. Numerical attack
   suggests the Frobenius-unit PSD maximum is near \(-2.2851\) and rank one,
   but that value remains scout evidence only.

Boundary:

- This is a local theorem around one rational \(n=3\) base point, not a global
  R3 concavity theorem.
- It does not classify all \(n=3\) kernels or all fixed-diagonal fibers.
- A fresh non-author verifier rebuilt the multivariate exact atoms, Hessian and
  rational log/Gershgorin certificate, obtaining the explicit uniform bound
  `H''<=-(43/50)||D||_F^2`. Its first pass found an off-diagonal factor error
  only in the optional projected scout; that update was fixed, fully replayed,
  and passed a revision recheck without changing the saved best point.
