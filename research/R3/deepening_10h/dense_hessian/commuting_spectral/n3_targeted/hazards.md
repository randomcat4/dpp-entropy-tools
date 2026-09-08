# D10-M5 hazards

1. **Finite search is only scout.**  The `202000` evaluated directions found no
   positive candidate, but this is not a proof for all \(Q,\theta,v\).

2. **Singleton/pair layers are not separately concave.**  Raw singleton
   second derivatives \(r_i''\) and pair second derivatives \(s_i''\) can be
   positive under \(v\ge0\).  Any proof must use cancellation or a sharper
   invariant.

3. **Doubly stochastic is too weak.**  \(P=q^2\) is doubly stochastic, but
   entropy increase under a doubly stochastic map is pointwise, not a curvature
   bound along the special paths \(r(t),s(t)\).

4. **Orthostochastic constraints were not fully exploited.**  The search samples
   \(P\) through random orthogonal \(Q\), but the failed proof attempts did not
   derive a complete inequality from the special \(3\times3\) orthostochastic
   algebra.

5. **Near-boundary negatives can be huge.**  Several layerwise-positive extrema
   occurred near very small atoms and had large negative opposite-layer terms.
   This is not evidence for a positive candidate unless a strict chord and
   high-precision gap are also supplied.

6. **PSD is spectral here.**  \(v_i\ge0\) implies
   \(D=Q\operatorname{diag}(v_i)Q^\top\succeq0\).  Mixed-sign \(v\) is outside
   this targeted task.

7. **Exact event semantics.**  All atoms are exact configuration probabilities
   from the spectral-channel formula, equivalent to Möbius/signed determinant
   atoms.  Inclusion probabilities alone are not entropy atoms.

8. **Author result.**  This directory is an author attempt.  It must not be
   labeled `CORRECT` without a fresh non-author verification pass.
