# D10-S4 hazards

Author status: **HAZARD_LEDGER**.

1. **Exact events, not principal minors.**  The proof uses Möbius inversion from
   inclusion determinants.  It never identifies \(\det K[S,S]\) with the exact
   atom \(p_S\).

2. **Off-diagonal acceleration does not vanish atomwise.**  For zero-diagonal
   off-diagonal directions, \(p_S'(0)=0\) but \(p_S''(0)\) can be nonzero.  The
   entropy contribution vanishes only after summing against
   \(\log p_S(0)\).

3. **The scalar version was not maximal.**  The same cancellation works for any
   diagonal \(K_0=\operatorname{diag}(x_i)\).  The current frozen claim is the
   diagonal-box version; \(xI\) is only a special case.

4. **The formula is not a global concavity theorem.**  It is the Hessian at a
   diagonal kernel.  The neighborhood conclusion covers only PSD/NSD directions
   and only near a compact diagonal box.

5. **Indefinite directions can be flat.**  If \(D\) has zero diagonal, then
   \(H''_{K_0}[D,D]=0\).  This blocks any claim of a uniform negative bound over
   all nonzero symmetric directions.

6. **PSD/NSD strictness uses semidefinite structure.**  A nonzero PSD matrix
   cannot have all diagonal entries zero; the same holds for NSD by sign
   reversal.  This is exactly why semidefinite directions are strictly negative
   even though indefinite zero-diagonal directions are flat.

7. **The neighborhood radius is existential.**  The proof uses compactness and
   continuity of the exact-event entropy Hessian.  It does not provide a
   computable numerical radius.

8. **Compact diagonal box is necessary for uniformity.**  As any \(x_i\to0\) or
   \(x_i\to1\), the expression \(1/[x_i(1-x_i)]\) and atom logarithms become
   singular.  Uniform statements must keep all \(x_i\) in
   \(0<a\le x_i\le b<1\).

9. **Strict feasibility is local.**  For arbitrary symmetric \(D\), the affine
   path \(K_0+tD\) is strict only for sufficiently small \(t\).  The Hessian
   statement is local at \(t=0\).

10. **Author-side proof only.**  This directory should go to a fresh
    non-author verifier before being used as a certified lemma.
