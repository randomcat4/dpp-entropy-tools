# PR102 general multiple-boundary analytic FIRST

## Status

`ACCEPTED_SCOPED` at frozen author head `16a25c3810977d67207a95f935990df0a807bff9`.

No critical mathematical gap was identified in the included analytic unit.

## 1. General affine boundary geometry

Let

\[
K(t)=K(T)+(t-T)D,
\qquad \varepsilon=T-t>0,
\]

be strict for `t<T` and legal at `T`.  On `ker K(T)`, strict interior legality implies `-P_0DP_0>0`; on `ker(I-K(T))`, it implies `P_1DP_1>0`.  The kernel blocks are therefore `epsilon` times positive-definite compressions, the off-diagonal blocks are `O(epsilon)`, and the complementary endpoint blocks have fixed gaps.  Schur complementation gives linear comparability for every eigenvalue born from zero and every deficit born from one, with no simplicity assumption.

## 2. A simple-order complete-event group is forced

The exact cardinality generating determinant is

\[
\mathbf E[z^{|X|}]
=\det(I-K+zK)
=\prod_j(1-\lambda_j+z\lambda_j).
\]

If `r_0=dim ker K(T)>0`, the forbidden endpoint cardinality `N-r_0+1` has probability `Theta(epsilon)`: a lower bound selects exactly one small eigenmode and all endpoint-nonzero modes, while an upper bound uses the requirement that at least one small eigenmode be occupied.  The complementary argument for `r_1=dim ker(I-K(T))>0` gives `Theta(epsilon)` mass at cardinality `r_1-1`.

These are probabilities of true observed cardinality groups.  Each is a finite sum of nonnegative complete-event polynomials vanishing at the endpoint.  Therefore at least one complete event has a first-order zero, and the sum of the corresponding leading coefficients is positive.  Spectral coordinates are used only to evaluate the cardinality law; no rotated configuration entropy is introduced.

## 3. Complete Fisher dominance at arbitrary multiplicity

For every complete event with endpoint expansion

\[
p_E(T-\varepsilon)
=c_E\varepsilon^{k_E}+O(\varepsilon^{k_E+1}),
\qquad c_E>0,
\]

the exact identity is

\[
-H''(t)=\sum_E\frac{(p_E')^2}{p_E}
+\sum_Ep_E''\log p_E.
\]

For `k_E=1`, the Fisher term is `c_E/epsilon+O(1)` and the acceleration term is only logarithmic.  Double zeros have bounded Fisher information and logarithmic acceleration; higher-order zeros are smaller, and endpoint-positive atoms are bounded.  The forced simple-order group consequently gives

\[
-H''(T-\varepsilon)
=\frac{A_1}{\varepsilon}+O(\log(1/\varepsilon))
\longrightarrow+\infty.
\]

This includes repeated `K` zeros, repeated complement zeros, and simultaneous activity.  All complete events and both curvature terms remain present.

## 4. Rank-two double-root obstruction

For a rank-two radial cross-block path, every likelihood ratio has

\[
q_E(s)=1-a_Es+b_Es^2,
\qquad s=t^2.
\]

A double boundary zero at `s_*` necessarily has

\[
q_E(s)=(1-s/s_*)^2.
\]

Its Fisher term tends to `16mu_E/s_*`, while its acceleration contribution to `-H''` is

\[
-\frac{16\mu_E}{s_*}\log(1/\Delta)+O(1),
\qquad \Delta=s_*-s.
\]

This adverse behavior is real, but the general cardinality theorem forces a simple-order complete-event group with a `1/Delta` Fisher pole.  Hence an abstract pure-double quadratic likelihood pattern is not realizable by a strict-interior affine DPP.  This is a realizability obstruction, not an entropy counterexample.

## 5. The rank-two split scale

For an active `K` side, let the two positive generalized endpoint eigenvalues satisfy `rho_1>=rho_2` and put

\[
\delta=1-s\rho_1,
\qquad
\eta=1-\rho_2/\rho_1.
\]

The full-event likelihood is exactly

\[
q_{\rm full}=\delta[\eta+(1-\eta)\delta].
\]

At a double seed endpoint, the true neighboring cardinality probability `G=P(|X|=N-1)` has a simple zero.  Coefficient continuity supplies a uniform positive `partial_delta G` near the seed.  At a split endpoint, the second small eigenvalue is `O(eta)`, so the exact cardinality formula gives `G(0)=O(eta)` and hence

\[
G(\delta)\le C(\eta+\delta).
\]

Weighted Cauchy over all complete events in this cardinality class yields

\[
F_{N-1}\ge \frac{c_1}{\eta+\delta}.
\]

The full event supplies

\[
F_{\rm full}\ge c_2\frac{\eta+\delta}{\delta}.
\]

AM--GM then gives the uniform two-scale lower bound

\[
F_{\rm full}+F_{N-1}
\ge 2\sqrt{c_1c_2}\,\delta^{-1/2}.
\]

Complementation exchanges full/empty and size `N-1`/size one.  Taking the minimum over the finitely many seed-active clusters correctly covers simultaneous `K` and `I-K` activity.

## 6. Complete acceleration budget

Writing `r=t/T`, affine interpolation from the uniformly strict center gives

\[
K(rT),\ I-K(rT)\ge c\delta I,
\qquad \delta=1-r^2.
\]

At each strict interior point, the exact pointwise L-ensemble identity

\[
p_E=\det(I-K)\det L_E,
\qquad L=K(I-K)^{-1},
\]

and `L>=K` imply `p_E>=c_0delta^{2N}` for every complete event.  Thus all logarithms are `O(log(1/delta))`.  Finite-dimensional polynomial dependence gives a uniform bound on `sum_E|p_E''|`, so the entire acceleration loss is only logarithmic.  The `delta^(-1/2)` Fisher bound therefore dominates uniformly.

This use of `L` is pointwise.  The physical path remains affine in `K`.

## 7. Moving maximal-chord stability

Assume a rank-two seed already has

\[
\Gamma_0(t^2)=-H_0''(t)/t^2\ge g>0
\]

through its strict maximal chord, with the continuous value at zero.  The uniform endpoint estimate gives `Gamma>=g/2` on a common normalized endpoint strip for nearby paths, regardless of endpoint splitting or simultaneous activity.  On the complementary normalized compact interval, every event likelihood stays positive and the exact full-law rank-two formula is jointly continuous in the finite parameters and the moving normalized coordinate.  Compactness transfers the same lower bound after shrinking the parameter neighborhood.

Consequently every nearby path satisfies

\[
H''(t)\le-(g/2)t^2
\]

on its own strict maximal chord, and `H(t)+(g/24)t^4` is concave on the closed chord by continuity.  The theorem assumes the seed's compact-interior margin; it does not prove that margin universally.

## 8. Source and premise checks

The Hough--Krishnapur--Peres--Virag Bernoulli-eigenvalue description agrees with the cardinality generating determinant used here.  Kulesza--Taskar gives the finite L-ensemble atom identity and `L=K(I-K)^{-1}` for strict `K`; PR102 uses it only pointwise.

The compact-interior formula retains the full rank-two likelihood `q=1-sa+s^2b`, Fisher term, and acceleration term, in the accepted PR58 scope.  No PR95 simple-endpoint theorem is imported into the new multiple-endpoint proof.

## Final disposition

The general finite endpoint theorem, the rank-two pure-double realizability obstruction, and the rank-two two-scale moving-endpoint stability theorem are accepted within the frozen analytic scope.  No explicit fixture, arithmetic certificate, seed whole-chord bound, universal interior sign, higher-rank hierarchy, entropy-rate claim, or novelty claim is accepted here.
