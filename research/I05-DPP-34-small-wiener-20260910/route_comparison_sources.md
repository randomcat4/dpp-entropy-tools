# Route comparison, source map, and preserved failures

Status: **AUTHOR SOURCE/LOGIC AUDIT / PENDING REVIEW**.

## 1. Selected route: exact complete-event determinant loops

The proof used in this packet is finite-volume and algebraic.

For every complete word it factors the exact DPP atom relative to a product Bernoulli atom and expands

\[
\log\det(I+B_xA_t)
\]

under the explicit contraction `||B_xA_t||<1`. The expectation remains under the full complete-event DPP law. The thermodynamic limit is taken only after expansion into anchored closed walks with an absolute `ell^1` majorant.

The sole non-elementary inputs are standard finite-dimensional determinant differentiation and the already accepted PR53 matching inequality. The complete-event singular gap and full-atom determinant formula are reproved in the packet where used.

This route proves `C^4` of the true entropy rate directly. It neither constructs a Gibbs potential nor identifies a pressure derivative.

## 2. BFG / Fernandez--Maillard response route

Primary sources checked:

- X. Bressaud, R. Fernandez, A. Galves, *Decay of correlations for non Holderian dynamics. A coupling approach*, EJP 4 (1999), public PDF `https://www.math.univ-toulouse.fr/~bressaud/Papiers/decayyyyy.pdf`, arXiv `math/9806132`.
- R. Fernandez, G. Maillard, *Chains with complete connections: general theory, uniqueness, loss of memory and mixing properties*, arXiv `math/0305026`.

BFG gives an explicit ratio coupling, matched-suffix process, and renewal control. Fernandez--Maillard gives a general sensitivity-matrix framework for uniqueness and loss of memory. These are appropriate for proving finite-order response when differentiated conditionals have suitable summable **moments**.

For a generic polynomial-memory family, two Poisson response orders consume two levels of memory unless additional structure is proved. Neither primary source states that mere summable variation automatically gives the `C^2` parameter response in `s=t^2` needed for local entropy curvature.

For the present `A_0` example the coordinate influence is summable, but it need not have any positive spatial moment. Therefore the moment-Poisson route does not close uniformly. The determinant-loop route is genuinely different: small amplitude supplies a geometric expansion in walk **length**, so it does not ask for a spatial moment of the Fourier tail.

## 3. Dobrushin 1974 A1/A2 route remains excluded

The PR66 source-bound defect is unchanged.

- A1 includes an exponential support-cardinality factor together with its spatial decay condition.
- A2 removes that factor only under a controlled null-state representation.

The old polynomial interval telescope proves neither condition. This packet does not relabel ordinary finite first moment as sufficient and does not cite Dobrushin's theorem.

Small Wiener norm does make an alternative determinant closed-walk expansion geometrically summable in walk length. One could try to convert it into a high-temperature interaction theorem, but that conversion is unnecessary here and is not claimed.

## 4. Relation to PR39

At `mu=1/2`, the hypothesis

\[
\sum_{m\ne0}|\widehat c(m)|<\min\{\mu,1-\mu\}
\]

becomes

\[
2\|c-1/2\|_W<1,
\]

which is the accepted PR39 center condition. The quartic coefficient also specializes to

\[
\alpha_k=\frac23|\widehat g(k)|^4.
\]

PR39 is accepted only in its stated mean-one-half setting. The present proof obtains the arbitrary-mean result from the product-Bernoulli complete-atom factorization, not by asserting that the PR39 response theorem already covers other means.

## 5. Relation to the `H^1_F` successor

The `H^1_F` proof uses one-dimensional complete-event packing, norm-controlled inverse localization, and two moment-space Poisson inverses. It handles arbitrary strict-margin centers in that Sobolev class, with no small-correlation assumption.

The present theorem trades that global center range for much lower Fourier regularity:

- center must satisfy the explicit small off-diagonal Wiener norm;
- no positive weighted Fourier moment is required;
- entropy regularity comes from a length-geometric complete-event loop series.

Neither theorem subsumes the other.

## 6. Why the parity/normalization observation alone is insufficient

At the center, fixed parity marginals and conditional normalization eliminate the linear entropy-deficit response. Under weak regularity one can often obtain a centered quartic value expansion from this cancellation.

A value expansion alone does not imply a common local concavity interval: uniformly convergent analytic approximants can have shrinking curvature intervals. The present theorem closes this gap by proving a volume-uniform `C^4` bound for the **true entropy rate**, not merely by identifying its coefficient at zero.

## 7. Exact nonclaims

1. No conclusion is made for an arbitrary `A_0` center with off-diagonal norm at or above `min(mu,1-mu)`.
2. The norm condition is sufficient and not claimed sharp.
3. No whole-legal-interval sign is proved.
4. No arbitrary measurable or merely square-integrable symbol is covered.
5. The logarithmic-tail example is a positive theorem family, not an entropy counterexample.
6. No external novelty claim is made.
7. No numerical computation or finite-window sign search is used.
8. The full Fisher and atom-acceleration terms are retained through the exact complete-event KL; the proof does not establish their signs separately.