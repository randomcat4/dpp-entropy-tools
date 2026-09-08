# D10-M3 hazards

Author status: open-risk ledger for later fresh review.

1. **Spectral entropy is not output entropy.**  The latent spectral subset
   \(Z_t\) has entropy \(\sum_i h(\theta_i(t))\), but the observed DPP
   configuration \(Y_t\) is the output of a nontrivial channel.  Replacing
   \(H(Y_t)\) by \(H(Z_t)\), \(H(|Z_t|)\), or spectral Bernoulli entropy is
   invalid except in explicitly closed subcases.

2. **Doubly stochastic blocks are not curvature certificates.**  Each
   cardinality block of the projection-DPP channel is doubly stochastic, so it
   increases entropy pointwise.  Pointwise entropy increase does not imply that
   \(t\mapsto H(T\nu_t)\) is concave.

3. **The posterior term cannot be dropped.**  In
   \(H(Y)=H(Z)+\mathbb E H(Y\mid Z)-H(Z\mid Y)\), the term
   \(\mathbb E H(Y\mid Z)\) may curve under heterogeneous spectral rates.
   The safe unresolved object is the combined correction
   \(\mathbb E H(Y\mid Z)-H(Z\mid Y)\), equivalently \(H(Y\mid |Y|)\).

4. **Same-sign rates matter for the sufficient condition.**  The discrete
   concavity argument for \(\mathbb E c_{N_t}\) uses \(v_iv_j\ge0\).  It covers
   PSD rates \(v_i\ge0\) and NSD rates \(v_i\le0\), not mixed-sign spectral
   directions.

5. **Strict interior is required.**  The score formulas use
   \(\theta_i(t)^{-1}\), \((1-\theta_i(t))^{-1}\), and positive atom logs.
   Boundary eigenvalues \(0\) or \(1\) are excluded.

6. **Repeated eigenvalues do not give permission to rotate.**  If eigenvalues
   collide, the spectral basis is not unique.  The frozen route fixes \(Q\) and
   affine eigenvalue coordinates; changing \(Q\) with \(t\) is a different path.

7. **Cardinality-uniform channels are very restrictive.**  The condition that
   all same-size squared minors equal \(\binom nk^{-1}\) is a sufficient
   hypothesis, not a generic property of orthogonal matrices.  No classification
   or high-dimensional existence theorem is claimed here.

8. **2D blocks do not imply coupled high-dimensional control.**  The closed
   arbitrary-rotation \(2\times2\) block proof survives direct sums, but direct
   sums add independent components.  It does not control genuinely coupled
   cardinality blocks for a dense \(Q\).

9. **Small exact sanity is not theorem evidence.**  The rational checks only
   validate formulas and derivative bookkeeping in small dimensions.

10. **Positive candidate gate remains strict.**  A true counterexample would
   need a strictly feasible chord and a certified positive gap
   \(\Delta=[H(K_-)+H(K_+)]/2-H(M)>0\).  This work found no such candidate.
