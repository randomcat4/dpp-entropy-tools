# Source scope and failure audit for the arbitrary-`A_0` route

Status: **AUTHOR SOURCE/LOGIC AUDIT / PENDING INDEPENDENT DELTA REVIEW.**

This file separates external inverse-algebra facts, repository inputs, and the new proof. No external source is promoted to a complete-event entropy-response theorem.

## 1. What inverse-closedness does and does not supply here

A tempting route is:

1. place every complete-event matrix for an arbitrary `A_0` center in an unweighted convolution-dominated/Baskakov--Gohberg--Sjöstrand algebra;
2. use inverse-closedness or norm-controlled inversion;
3. infer one event-uniform summable diagonal envelope for the whole complete-event family;
4. differentiate complete-event conditionals under that envelope.

The logical point needed by PR117 is only that Step 3 is **not established in this packet merely from Step 2**. A theorem controlling an inverse algebra norm still has to be mapped to the exact complete-event family, with the correct uniform family norm, geometry, and event/volume quantifiers, before it becomes the differentiated common envelope required by Step 4.

### Correction of the first source audit

The earlier version of this file and the initial README overstated the literature by saying that the unweighted `p=1` BGS endpoint in `B(ell^2)` does not admit norm-controlled inversion from the algebra norm and operator inverse norm. That statement is withdrawn.

Fang--Shin, *Norm-Controlled Inversion of Banach algebras of infinite matrices* (Comptes Rendus Mathématique 358 (2020), DOI `10.5802/crmath.54`), explicitly recalls earlier Baskakov results giving norm-controlled inversion for the `p=1` BGS algebra in `B(ell^2)`. Fang--Shin's own more general asymmetric theorem has additional weight restrictions, but those restrictions cannot be used to infer failure of the classical unweighted `p=1`, `ell^2` case.

This correction is **non-load-bearing** for the PR117 theorem. The final proof does not require either a positive or a negative theorem about BGS norm control. It instead freezes one finite-range reference and proves directly the exact operator and localization estimates used below.

The accurate source boundary is therefore:

> PR117 neither needs nor establishes a BGS norm-control theorem for the complete-event inverse family. The initial common-envelope route was not proved in this manuscript and is not a step of the final proof. No claim is made that the inverse-algebra literature rules such a route out.

Samei--Shepelska (arXiv:1809.04097) remains comparison/background only. It is not used as a black-box complete-event response theorem.

## 2. First PR117 checkpoint route that is superseded

The initial `README.md` checkpoint proposed choosing a finite-range reference `c^(L)` and then requiring an `ell^1` inverse-envelope norm `||u||_1` to satisfy

`||u||_1 ||c-c^(L)+t g||_W < 1`.

That requirement was not proved to be available with the needed uniform truncation/event quantifiers. In particular, from the argument as written one could not simply conclude that the product tends to zero from Wiener-tail convergence alone while allowing the envelope constant to depend on the truncation.

This route is **withdrawn as a required step**. Its historical checkpoint remains visible for auditability. The withdrawal is a proof-design correction, not a theorem that no suitable inverse-envelope theorem can ever exist.

The replacement in `arbitrary_A0_C4_proof.md`, made explicit in `operator_vs_absolute_sum_audit.md`, separates the two jobs:

- trace-log existence uses the complete-event operator bound `||R_x^0||<=delta_0^{-1}` and the small Wiener norm of the perturbation relative to one frozen finite-range reference;
- configuration locality uses exponential operator-norm approximation of that same fixed finite-range reference inverse.

After localization, absolute displacement summation uses only the Fourier `ell^1` norm of the perturbation, while the inverse factors pay the common **operator** bound `B<=delta_0^{-1}+1`. No common inverse `ell^1` envelope is used.

The quantifier order is also fixed: first choose and freeze `c^0` so the center tail itself satisfies `B||c-c^0||_W<1/4`; only afterward shrink `t` so `B|t|||g||_W<1/4`. Shrinking `t` is never used to repair the frozen center tail.

## 3. External facts actually used in the new proof

The new proof needs only elementary/standard finite-dimensional facts, all reproved or reduced explicitly in the packet:

1. complete-event determinant formula and the coercive inverse bound for `M_x=K-I_Z` under a strict spectral margin;
2. for a finite-band Hermitian `M_x` with a uniform singular gap, the geometric identity

   `M_x^{-1}=M_x sum_{q>=0}(I-M_x^2)^q`

   and the resulting exponential off-diagonal decay;
3. finite-dimensional resolvent identities and local block comparison;
4. Jacobi/Bell determinant differentiation of every complete atom;
5. dominated convergence under the explicit localization-shell, Wiener-displacement, and walk-length majorants.

No Gibbs uniqueness theorem, Ruelle parameter-response theorem, Dobrushin theorem, BFG response theorem, HMM analyticity theorem, or BGS norm-controlled inversion theorem is load-bearing.

## 4. Repository theorem input

The final curvature step imports only the already accepted **regularity-free parity matching floor** from PR53:

`h(c)-h(c+t g) >= (1/2) d_Ber(mu^2-|g_hat(k)|^2 t^2 || mu^2)`.

PR117 does not import PR53's exponential-response theorem. It independently supplies the missing `C^4` response for arbitrary strict `A_0` centers.

PR82, PR106, PR110 and PR113 are predecessor/comparison results, not premises of the new `C^4` proof.

## 5. Failure ledger

The following statements are explicitly not inferred:

- inverse-closedness or an abstract norm-control theorem => the exact common differentiated complete-event envelope needed here, without checking its family quantifiers;
- an eventwise inverse bound => a differentiated thermodynamic envelope;
- finite-window entropy curvature => entropy-rate curvature;
- a selected-event or Gaussian log-determinant identity => complete configuration Shannon entropy;
- failure or non-use of a sufficient inverse/response route => entropy nonconcavity;
- inability of this proof to use a route => impossibility of that route in the literature.

The final proof instead starts from every complete atom, factors it relative to one frozen finite-range reference DPP, and keeps the score/Fisher and acceleration terms inside exact atom differentiation before any thermodynamic passage.

## 6. Current evidence class

- arbitrary-`A_0` `C^4` bridge: **author proof; S3 fresh SECOND says CORRECT_WITHIN_SCOPE at frozen head `7a960926...`; later source delta pending**;
- local corrected-concavity theorem: same mathematical status;
- operator-vs-absolute-sum audit and support-cardinality correction: included in that frozen SECOND mathematical audit;
- this BGS source wording correction: **author correction after the frozen SECOND; requires delta review**;
- S1 FIRST: separately claimed/frozen and must be cross-compared only after its independent report is public;
- computation: none;
- novelty: not assessed.

No earlier review automatically covers this corrected file blob.