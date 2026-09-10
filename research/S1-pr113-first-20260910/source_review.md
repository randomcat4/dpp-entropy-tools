# Primary-source and imported-dependency audit

## Original problem

Russell Lyons and Jeffrey E. Steif, *Stationary Determinantal Processes: Phase Multiplicity, Bernoullicity, Entropy, and Domination*, arXiv:math/0204324, Section 9, Conjecture 9.2:

https://arxiv.org/pdf/math/0204324

The source asks concavity of the stationary configuration entropy under scalar-symbol midpoint interpolation.  PR113 proves only the stated local, half-period, small-Wiener subfamily and does not claim to settle the conjecture globally.

## Complete-event and negative-association input

Russell Lyons, *Determinantal Probability Measures*, Publications Mathematiques de l'IHES 98 (2003), Theorem 8.1 and Remark 8.4:

https://numdam.org/item/10.1007/s10240-003-0016-0.pdf

The source supplies conditional negative association for positive-contraction DPPs and an explicit occupied/vacant cylinder determinant formula.  The accepted PR53 matching proof uses negative association only for nonnegative decreasing functions on disjoint matched edges, followed by the entropy variational inequality.  Its exact coefficient and direction agree with the PR113 import.

## Comparison sources that do not supply response regularity

Xavier Bressaud, Roberto Fernandez, and Antonio Galves, *Decay of correlations for non Holderian dynamics. A coupling approach*, arXiv:math/9806132:

https://arxiv.org/pdf/math/9806132

Theorem 1 controls correlations for a fixed normalized function with summable variations via an explicit coupling/renewal sequence.  The paper does not state fourth-order differentiability of invariant measures or entropy with respect to an external parameter.  Its discussion of nonnormalized functions also exhibits additional moment losses.

Roberto Fernandez and Gregory Maillard, *Chains with complete connections: general theory, uniqueness, loss of memory and mixing properties*, arXiv:math/0305026:

https://arxiv.org/pdf/math/0305026

The relevant results concern uniqueness, hereditary uniqueness, loss of memory, mixing, and Dobrushin sensitivity matrices.  They do not supply the `C^4` or `C^infinity` entropy response asserted by PR113 under a Fourier tail with no positive spatial moment.

Accordingly, the author packet's non-application statement is correct: the new determinant-loop proof, not either comparison source, carries the thermodynamic parameter differentiation.

## Accepted repository dependency

The PR53 matching floor is accepted and version-bound in:

- `docs/verification_round3_20260909/accepted_pr53.md`, blob `92746613904ec719685f4839dd580f2f1fcfca77`;
- `research/I05-DPP-21-20260909/finite_range_local_theorem.md`, blob `e1c014d654d71a89c700dbd12e44fdab95cd2a9d` at author head `ebecc412467939591e018a295a18c49a0a341ce9`.

Only the finite matching inequality is imported.  PR113 supplies its own entropy regularity and does not inherit PR53's analytic-response proof.
