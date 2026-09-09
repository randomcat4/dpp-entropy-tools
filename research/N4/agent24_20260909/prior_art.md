# Prior-art and route separation

**Status: literature/scope audit, not a novelty certificate.**

The work unit compared two structurally different mechanisms before deepening
one of them.

## Route A: moving low-rank physical frames

The repository's accepted R2 boundary results freeze the physical high/low
frames and the leading data.  The A2 result treats one explicit moving
rank-two physical frame near a projection boundary, with a negative leading
entropy gap, but explicitly leaves faster rotations and changing degeneracy
scales.  The theorem in `moving_rank1_theorem.md` attacks a different frozen
quantifier set: both endpoints may have unrelated rank-one physical directions
and unrelated nonzero eigenvalues, and the object is their true arithmetic
midpoint.

The bridge is the complete-law mass transfer

\[
q={p_{K_-}+p_{K_+}\over2}=p_0
\longrightarrow p_{K_0}=p_m,
\]

where empty/singleton mass is transferred to all rank-two pair events.  The
exact derivative is

\[
{d\over dr}H(p_r)=\sum_{i<j}b_{ij}
\log {p_i(r)p_j(r)\over p_\varnothing(r)r b_{ij}}.
\]

This route was deepened to a complete theorem and an explicit strict interior
lift.

## Route B: strong internal blocks and multi-ring interaction

The second route keeps two correlated `3x3` blocks and turns on a dense
rank-two cross coupling:

\[
K(t)=\begin{pmatrix}A&tB\\tB^{\mathsf T}&C\end{pmatrix}.
\]

For complete left/right configurations `S,T`, the exact bridge is

\[
p_t(S,T)=p_A(S)p_C(T)
\det\bigl(I_2-t^2G_A(S)G_C(T)\bigr),              \tag{1}
\]

where

\[
G_A(S)=U^{\mathsf T}(A-E_{S^c})^{-1}U,
\qquad
G_C(T)=V^{\mathsf T}(C-E_{T^c})^{-1}V,
\qquad B=UV^{\mathsf T}.
\]

Thus every one of the 64 atoms is the exact quartic polynomial

\[
p_t(S,T)=\mu_{S,T}(1+t^2u_{S,T}+t^4v_{S,T}).      \tag{2}
\]

This is structurally different from Route A: no endpoint is rank one, both
marginal blocks remain strongly correlated, and the unresolved object is
curvature in the compact middle of a radial chord.  A motivated rational
fixture and a precise interval-certification handoff are recorded in
`multiring_fixture.md`; no finite diagnostic is promoted to a theorem.

## Primary sources checked

1. J. B. Hough, M. Krishnapur, Y. Peres, and B. Virag,
   *Determinantal Processes and Independence*, Probability Surveys 3 (2006),
   arXiv:math/0503110.  Relevant background: the Bernoulli-eigenvalue mixture
   and projection-DPP decomposition.
2. R. Lyons, *Determinantal probability measures*, Publications
   Mathematiques de l'IHES 98 (2003), arXiv:math/0204325.  Relevant background:
   finite determinantal measures and negative dependence.
3. E. Hillion and O. Johnson, *A proof of the Shepp--Olkin entropy concavity
   conjecture*, Bernoulli 23(4B) (2017), arXiv:1503.01570.  This controls the
   entropy of the Bernoulli eigenvalue count, not configuration entropy after a
   rotating physical frame; it therefore does not prove Theorem 1.
4. K. M. R. Audenaert, *A sharp continuity estimate for the von Neumann
   entropy*, Journal of Physics A 40 (2007), arXiv:quant-ph/0610146.  Its
   classical finite-alphabet specialization supplies the explicit strict-lift
   entropy error bound.

The rank-one midpoint monotonicity proof itself is elementary and
self-contained.  The source audit separates correctness from any novelty
claim.
