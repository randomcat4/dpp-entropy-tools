# Primary sources, route comparison, and failure ledger

Status: **AUTHOR SOURCE MAP / PENDING REVIEW**.

## 1. Norm-controlled inversion

Primary source: the Comptes Rendus Mathématique article *Norm-controlled inversion of Banach algebras of infinite matrices*, DOI `10.5802/crmath.54`, public article/PDF at

`https://comptes-rendus.academie-sciences.fr/mathematique/item/10.5802/crmath.54.pdf`.

The load-bearing imported statement is the article's theorem for the convolution-dominated classes `C^{p,r}` on relatively separated subsets of `R^d`: under

\[
r>d(1-1/p),
\]

an element invertible on `ell^2` has its inverse in the same matrix algebra, with norm control in terms of the algebra norm, inverse operator norm, and geometric separation data.

Exact map used here:

- ambient set: the packed `Lambda subset Z subset R`, so `d=1` and relative separation is one;
- matrix exponent: `p_mtx=2`;
- weight exponent: `r=1`, satisfying `1>1/2`;
- algebra input: the diagonal envelopes of the event direct sum and the direction direct sum are the `H^1_F` Fourier coefficient sequences;
- operator input: the complete-event coercivity gives one direct-sum inverse bound `delta^{-1}` on `ell^2(Lambda)`;
- conclusion used: the inverse direct sum has one `h^1` diagonal envelope.

Nothing is inferred from a theorem for one fixed event matrix. The theorem is applied once to a single matrix containing the complete countable event family.

The subsequent common complex disk is proved by an explicit algebra Neumann series and a summed convolution envelope. It is not obtained by taking a pointwise supremum over a family of separately bounded algebra norms.

## 2. Coupling and loss of memory

Primary source: X. Bressaud, R. Fernandez, and A. Galves, *Decay of correlations for non Holderian dynamics. A coupling approach*, Electronic Journal of Probability 4 (1999). Public journal PDF:

`https://www.math.univ-toulouse.fr/~bressaud/Papiers/decayyyyy.pdf`

and arXiv record `math/9806132`.

The exact imported pieces are:

- ratio condition (4.1), which permits any valid decreasing majorant `gamma_m`, not only the smallest canonical one;
- Proposition 1 and the matched-suffix coupling construction;
- comparison with the age chain that increments from `m` to `m+1` with probability `1-gamma_m` and resets to zero with probability `gamma_m`;
- equations (5.4)--(5.5), which bound an arbitrary observable by its variation sequence before the paper specializes to its displayed observable norm;
- the first-return formula in equations (5.7)--(5.11).

The present proof then performs its own nonnegative summations in the moment spaces `V_1` and `V_0`. No BFG theorem is quoted as a ready-made second-order parameter response result.

Independent comparison source: R. Fernandez and G. Maillard, *Chains with complete connections: general theory, uniqueness, loss of memory and mixing properties*, arXiv `math/0305026`.

That paper's one-sided specification/sensitivity framework supplies alternative uniqueness and loss-of-memory criteria. Our first-moment continuity majorant lies well inside the summable continuity regime relevant to those criteria. However, the paper does not state the two-level parameter response lemma needed here. In particular, uniqueness or loss of memory is not silently upgraded to `C^2` response. The exact difference-quotient and two-Poisson argument remains part of the present proof.

## 3. Comparison of structurally different routes

### Route A: weighted-Wiener complete-event localization

PR82 uses weighted Fourier `ell^1` and obtains a common inverse envelope in a weighted Schur algebra. The two-leg square turns a `p`-moment on each leg into a `2p`-moment influence. A first moment of the variation tail then appears automatically at `p>=1` in the later PR106 author route.

### Route B: Fourier-Sobolev localization — selected here

The present theorem packs finite events in one spatial dimension and uses `C^{2,1}` inverse closedness. A conditional leg is in weighted `ell^2_1`; squaring it gives directly

\[
\sum_j(1+j)^2\beta_j<\infty.
\]

This proves the same response moment without requiring weighted Fourier `ell^1_1`. It is therefore not just a renamed `A_1` assumption.

### Route C: direct conditional relative entropy

For any sufficiently continuous conditional family,

\[
D(s)=E_{\nu_s}
\left[
D_{\rm KL}(G_s(\cdot|X_1^\infty)
\|G_0(\cdot|X_1^\infty))
\right].
\]

This identity can give the centered quartic coefficient from uniform conditional Taylor expansion and weak convergence under weaker moments. It does not by itself give the sign of the second derivative at every nearby nonzero parameter. A value expansion or positive Fisher coefficient at the center is therefore not substituted for local concavity.

### Route D: Fernandez--Maillard sensitivity matrices

This route is useful for uniqueness and quantitative forgetting. Without an additional parameter-dependent resolvent or differentiated coupling estimate, it does not close the entropy curvature. It remains a comparison, not the load-bearing bridge.

## 4. Relation to Tanaka's high-order operator theory

Tanaka, arXiv `2205.12561`, is not invoked as a theorem input. Its same-space reduced-resolvent hypotheses are stronger than the two-level moment bounds proved here. Encoding `V_1 -> V_0 -> C` into recursive graph domains would reproduce the direct difference-quotient work rather than remove it.

## 5. Dobrushin 1974 remains excluded

The source-bound defect in PR66 remains unchanged:

- A1 has exponential support-cardinality summability;
- A2 requires a controlled null-state potential.

The present proof constructs no Dobrushin interaction and uses no pressure analyticity. Ordinary first moment is not relabeled as an A1/A2 hypothesis.

## 6. Exact nonclaims and preserved failures

1. The theorem does not cover every `A_p` symbol for any `p<1`; it covers the structurally different `H^1_F` class.
2. It does not prove sharpness of the `H^1` derivative count. The second moment of the two-leg influence is sufficient, not asserted necessary for entropy concavity.
3. Sparse Fourier examples can make this second influence moment diverge below the corresponding weighted regularity, but such examples obstruct this response mechanism only. They are not DPP entropy counterexamples.
4. The theorem is local about `t=0`; no whole-legal-interval curvature sign is claimed.
5. No finite-window sign is extrapolated. Finite cutoffs occur only inside absolutely controlled coupling/Poisson sums.
6. Full classical `C^4` regularity of `t -> h(c+t g)` at every nearby parameter is not needed or claimed. The proof establishes `C^2` response in `s=t^2`, which is sufficient for the displayed curvature expansion.
7. No numerical computation or machine certificate is used.
8. Novelty relative to the external literature is NOT_ASSESSED.