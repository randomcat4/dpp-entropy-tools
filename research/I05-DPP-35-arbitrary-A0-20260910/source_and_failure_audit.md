# Source scope and failure audit for the arbitrary-`A_0` route

Status: **AUTHOR SOURCE/LOGIC AUDIT / PENDING INDEPENDENT REVIEW.**

This file separates external inverse-algebra facts, repository inputs, and the new proof. No external source is promoted to a complete-event entropy-response theorem.

## 1. Why bare inverse-closedness is not the proof

A tempting route is:

1. place every complete-event matrix for an arbitrary `A_0` center in the unweighted convolution-dominated/Baskakov--Gohberg--Sjöstrand algebra;
2. use inverse-closedness in `B(ell^2)`;
3. conclude one event-uniform summable diagonal envelope for all inverses;
4. differentiate complete-event conditionals under that envelope.

Step 3 does not follow from Step 2.

The relevant norm-controlled-inversion literature distinguishes spectral inverse-closedness from a quantitative bound of the inverse algebra norm in terms of the original algebra norm and the operator inverse norm. In the BGS matrix setting the standard norm-control hypotheses require a positive weight exponent at the endpoint corresponding to `p=1,d=1`; bare unweighted `C_{1,0}` is precisely the endpoint not supplied by those quantitative theorems.

The Samei--Shepelska weighted-convolution work (arXiv:1809.04097) is therefore treated only as comparison/background on norm-controlled inversion. It is not cited as a theorem yielding a common envelope for the nonnormal complete-event family.

Likewise Fang--Shin's norm-controlled inversion theorem for infinite matrix algebras is used only to locate the quantitative endpoint obstruction. PR117 does not apply it.

This is a **method obstruction**, not a DPP entropy counterexample.

## 2. First PR117 checkpoint route that is superseded

The initial `README.md` checkpoint proposed choosing a finite-range reference `c^(L)` and then requiring an `ell^1` inverse-envelope norm `||u||_1` to satisfy

`||u||_1 ||c-c^(L)+t g||_W < 1`.

That requirement is stronger than what arbitrary `A_0` convergence guarantees. The inverse-envelope norm may deteriorate as the truncation range grows, so the product need not tend to zero merely because the Wiener tail does.

This route is **withdrawn as a required step**. The first checkpoint remains in history for auditability.

The replacement in `arbitrary_A0_C4_proof.md` separates the two jobs:

- trace-log convergence uses only the operator bound `||R_x^0||<=delta_0^{-1}` and the small Wiener tail;
- configuration locality uses exponential approximation of the **fixed finite-range** reference inverse in operator norm.

No product of a growing `ell^1` inverse norm with the truncation tail is used.

## 3. External facts actually used in the new proof

The new proof needs only elementary/standard finite-dimensional facts, all reproved or reduced explicitly in the packet:

1. complete-event determinant formula and the coercive inverse bound for `M_x=K-I_Z` under a strict spectral margin;
2. for a finite-band Hermitian `M_x` with a uniform singular gap, the geometric identity

   `M_x^{-1}=M_x sum_{q>=0}(I-M_x^2)^q`

   and the resulting exponential off-diagonal decay;
3. the finite-dimensional resolvent identity;
4. Jacobi/Bell determinant differentiation;
5. dominated convergence under the explicit shell/displacement/walk-length majorants.

No Gibbs uniqueness theorem, Ruelle parameter-response theorem, Dobrushin theorem, BFG response theorem, or norm-controlled BGS inversion theorem is load-bearing.

## 4. Repository theorem input

The final curvature step imports only the already accepted **regularity-free parity matching floor** from PR53:

`h(c)-h(c+t g) >= (1/2) d_Ber(mu^2-|g_hat(k)|^2 t^2 || mu^2)`.

PR117 does not import PR53's exponential-response theorem. It independently supplies the missing `C^4` response for arbitrary strict `A_0` centers.

PR82, PR106, PR110 and PR113 are predecessor/comparison results, not premises of the new `C^4` proof.

## 5. Failure ledger

The following statements are explicitly not inferred:

- inverse-closedness => a common family envelope;
- an eventwise inverse bound => a differentiated thermodynamic envelope;
- finite-window entropy curvature => entropy-rate curvature;
- a selected-event or Gaussian log-determinant identity => complete configuration Shannon entropy;
- failure of a sufficient inverse/response method => entropy nonconcavity.

The new proof instead starts from every complete atom, factors it relative to a finite-range reference DPP, and keeps the score/Fisher and acceleration terms inside exact atom differentiation before any thermodynamic passage.

## 6. Current evidence class

- arbitrary-`A_0` `C^4` bridge: **author proof, pending review**;
- local corrected-concavity theorem: **author proof, pending review**;
- support-cardinality correction: **author correction, pending review**;
- external source map: **author audit, pending review**;
- computation: none;
- independent review: none claimed;
- novelty: not assessed.