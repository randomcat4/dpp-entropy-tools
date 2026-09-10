# I05-30 sources, method comparison, and failure ledger

Status labels in this file distinguish author proof from prior accepted premises and from independent review. Novelty is not assessed.

## Accepted repository premises consulted

1. `docs/verification_round3_20260909/accepted_pr54.md`: accepted near-decoupling theorem and the previously scoped **simple** legal spectral-endpoint theorem. Its endpoint result assumes a one-dimensional kernel on one active spectral side. I05-30 does not treat that assumption as already removed.
2. `docs/verification_round4_20260909/accepted_pr58.md`: accepted complete rank-two likelihood `q=1-sa+s^2 b`, full Fisher/acceleration curvature identity, conditional/additive sufficient bounds, and the two finite correlated witnesses. General dense correlated whole-chord curvature remained open there.
3. PR94 `research/I05-29-channel-lift-20260910/CHANNEL_LIFT.md`: author proof, not an accepted premise. It gives an exact actual-coordinate local-channel lift of the accepted m-by-2 theorem. Its own structural limitation is used only for comparison: a three-coordinate group expanded from two base coordinates forces a proportional pair among the corresponding observed cross-block columns (and symmetrically rows).
4. PR95 `research/I05-29-maximal-rank2-chord-20260910/ADDENDUM_MOVING_ENDPOINT_STABILITY.md`: author proof under review, not an accepted premise. Its moving-endpoint theorem assumes a simple one-sided active spectral endpoint. I05-30 supplies a separate proof for multiple/simultaneous endpoints and does not edit PR95.

## Primary-source check

Hough, Krishnapur, Peres and Virag, *Determinantal Processes and Independence*, arXiv:math/0503110, proves the standard Bernoulli-eigenvalue description of the total number of points of a finite DPP. I05-30 does not import this as a black-box bridge: `RESULT.md` directly derives

`E[z^|X|]=det(I-K+zK)=product_j(1-lambda_j+z lambda_j)`

from the determinant, and uses the product only to estimate the **true observed cardinality probability**. No rotated configuration entropy is evaluated.

For the pointwise atom identity in the two-scale addendum, Kulesza and Taskar, *Determinantal Point Processes for Machine Learning*, Foundations and Trends in Machine Learning 5 (2012), arXiv:1207.6083, is background for the L-ensemble identity. The addendum again supplies the bridge from the actual K at each strict interior point. `L=K(I-K)^(-1)` is never made affine in the physical parameter.

## Two structurally different mechanisms compared

### A. Exact local-channel decomposition (PR94)

PR94 proves an equality expressing an expanded-coordinate entropy as an affine marginal correction plus a fixed positive mixture of truly K-affine lower-dimensional DPP entropies. When its grouped-coordinate factorization applies, whole-chord concavity descends from the accepted m-by-2 theorem without an endpoint asymptotic estimate.

Both I05-30 3+3 fixtures lie outside the particular three-from-two grouped shape: every pair of their three cross-block columns is nonproportional and every pair of rows is nonproportional, with exact nonzero 2x2 witnesses committed in the checkers. This is a noncoverage statement for that construction, not a universal no-channel theorem.

### B. Complete-event/cardinality Fisher grouping (I05-30)

I05-30 stays in the original observed complete law. At a multiple endpoint it groups true complete events by vanishing order or by true cardinality. A dangerous double atom is retained with its adverse acceleration logarithm; a simple-order cardinality group supplies the stronger Fisher singularity. The two-scale addendum uses the full/empty atom together with the adjacent cardinality group when a repeated endpoint splits.

The simultaneous-endpoint fixture makes this visible on both sides at once: empty and full events are double zeros, while the true `|X|=1` and `|X|=5` groups are simple and their grouped Fisher terms dominate the complete logarithmic acceleration budget.

Thus the two routes discard different information and neither is a relabeling of the other.

## Failure ledger

1. **Pure-double endpoint idea — analytically impossible for a true affine DPP.** An abstract rank-two quadratic likelihood can have only double zeros; each such atom has bounded Fisher and an adverse `-const*log(1/delta)` contribution to `-H''`. The cardinality determinant proves that a strict-interior affine DPP boundary always has at least one simple complete atom. This is a realizability obstruction, not an entropy counterexample.
2. **Single-atom uniform perturbation around a repeated endpoint — insufficient.** When a double endpoint splits by scale `eta`, the full-event Fisher behaves like `(eta+delta)/delta`; its coefficient can vanish with `eta`. Uniform endpoint stability cannot be obtained by simply reusing PR95's fixed simple-root constant. The repair is the adjacent cardinality Fisher `1/(eta+delta)`; their sum is uniformly at least `C/sqrt(delta)`.
3. **Common likelihood window to the boundary — loses the endpoint mechanism.** Double and simple zero atoms force the common lower likelihood to zero. Bounding every logarithm by one worst window makes the acceleration budget diverge without retaining the cardinality Fisher singularity. I05-30 separates the final band and keeps the true Fisher group.
4. **Author checker development failure for the first fixture.** The first local attempt at `verify_double_endpoint_fixture.py` used in-place diagonal modification on a SymPy immutable matrix and terminated before mathematical checks. It was changed to copy the matrix with `sp.Matrix(K)` before modification. A subsequent full author execution passed. One subprocess invocation emitted unrelated environment warm-up stderr from a spreadsheet package before the script output; a clean same-interpreter replay produced the retained stdout. Neither execution is independent evidence.
5. **Simultaneous fixture evidence is still author-side.** The exact development calculation reconstructed all 64 complete laws, checked the Mobius definition for all 64 events at `t=1/2` and `t=1`, checked the rational compact bounds and rational atanh logarithm enclosures, and matched the 13 type/cardinality formulas. `output/verify_simultaneous_endpoint_fixture.stdout.txt` is deliberately labelled an author-side summary rather than an external raw S2/Codex certificate.
6. **No heavy computation.** Both exact 64-event fixture checks are short symbolic/rational work. No >60-minute computation was launched or requested, and no existing independent PR95 evidence budget was reused.

## Evidence boundary

`code/verify_double_endpoint_fixture.py`, `input/fixture.json`, and its output are author-side evidence for the first fixture. `code/verify_simultaneous_endpoint_fixture.py`, `input/simultaneous_fixture.json`, and its output are author-side evidence for the simultaneous fixture. The checkers reconstruct complete events in the actual observed basis and prove continuum polynomial inequalities by exact endpoints/vertices rather than a time grid.

A future independent arithmetic review must reimplement the finite objects rather than merely rerun the author scripts. Mathematical review, finite/source binding, and novelty remain separate dispositions.
