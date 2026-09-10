# I05-DPP-34 — arbitrary-mean small-Wiener local entropy-rate concavity

## Status

**PROVED AS AN AUTHOR THEOREM / PENDING INDEPENDENT REVIEW.**

This is a new successor theorem. It starts from `main`, does not modify PR82, PR106, or the `H^1_F` successor, and inherits no review verdict from those branches.

The theorem uses the true affine kernel

\[
K_t=T(c)+tT(g)
\]

and the classical stationary DPP configuration Shannon entropy rate. Every complete event is retained. No spectral or fermionic entropy, observation-basis rotation, `L`-affine path, finite-window curvature extrapolation, or Dobrushin A1/A2 import is used.

## Theorem

Let

\[
\mathcal A_0
=\left\{u:\sum_{m\in\mathbb Z}|\widehat u(m)|<\infty\right\}.
\]

Let real `c,g in A_0` satisfy

\[
c(\theta+1/2)=c(\theta),
\qquad
g(\theta+1/2)=-g(\theta),
\qquad g\ne0.
\]

Put

\[
\mu=\widehat c(0),
\qquad
\delta_\mu=\min\{\mu,1-\mu\},
\qquad
r_c=\sum_{m\ne0}|\widehat c(m)|.
\]

Assume

\[
0<\mu<1,
\qquad
\boxed{r_c<\delta_\mu.}
\tag{T.1}
\]

For every odd `k` with `\widehat g(k)\ne0`, define

\[
\alpha_k
=\frac{|\widehat g(k)|^4}
{8\mu^2(1-\mu^2)}.
\]

Then there exists `epsilon>0` such that `c+t g` is legal and

\[
t\longmapsto h(c+t g)+\alpha_k t^4
\]

is concave on `[-epsilon,epsilon]`. After shrinking `epsilon`, its second derivative is strictly negative for every `0<|t|<=epsilon`.

The theorem includes real non-even symbols and the resulting complex Hermitian Toeplitz kernels.

## Why this crosses every positive weighted-Wiener threshold

Condition (T.1) uses only the unweighted Wiener norm. The packet gives explicit nonconstant mean-`1/3` symbols with Fourier tails

\[
\frac1{n(\log(n+2))^2}
\]

on the required parity subsequences. After multiplying by a sufficiently small amplitude they satisfy (T.1), but they lie in no `A_p` with `p>0`. Thus the conclusion supplies a true local corrected-entropy theorem for symbols below every positive polynomial Fourier moment.

At `mu=1/2`, condition (T.1) is the same numerical small-center condition `2||c-1/2||_W<1` appearing in the accepted PR39 scope. The present theorem extends the conclusion to every mean `0<mu<1`; the proof is different and does not import PR39's mean-one-half response bridge.

## Proof idea

For a finite coordinate set `Lambda`, write

\[
K_{t,\Lambda}=\mu I+A_{t,\Lambda},
\]

where `A_t` has zero diagonal. For a complete word `x`, let

\[
D_x=\operatorname{diag}
\bigl(\mu\mathbf1_{x_i=1}+(\mu-1)\mathbf1_{x_i=0}\bigr),
\qquad B_x=D_x^{-1}.
\]

The exact complete-event probability factors as

\[
p_{\Lambda,t}(x)
=q_{\mu,\Lambda}(x)
\det(I+B_xA_{t,\Lambda}),
\]

where `q_mu` is the product Bernoulli law. On a common real parameter interval,

\[
\|B_xA_{t,\Lambda}\|\le\rho<1
\]

uniformly in `Lambda` and every complete word. Hence

\[
\log\frac{p_{\Lambda,t}(x)}{q_{\mu,\Lambda}(x)}
=\sum_{m\ge2}\frac{(-1)^{m+1}}m
\operatorname{Tr}(B_xA_{t,\Lambda})^m
\]

with a volume- and event-uniform geometric bound.

Since the one-site marginals are all `mu`,

\[
\frac1{|\Lambda|}H(p_{\Lambda,t})
=h_{\rm Ber}(\mu)
-\frac1{|\Lambda|}D(p_{\Lambda,t}\|q_{\mu,\Lambda}).
\]

Expanding each trace into closed walks, keeping the expectation over every complete atom, gives a thermodynamic-limit series. Complete-event coercivity bounds derivatives of every finite local expectation. Through order four the differentiated walk sums have a uniform majorant

\[
C_r m^{2r}\rho^{m-r},
\qquad 0\le r\le4,
\]

so the true entropy rate is `C^4` in `t` on a nonempty interval.

The half-period symmetry fixes the two parity marginals and makes them independent at `t=0`. Therefore

\[
h(c)-h(c+t g)
\]

is the mutual-information rate between the parity processes and is nonnegative and even. If its quadratic coefficient is positive, ordinary `C^2` continuity already gives local strict concavity. If the quadratic coefficient vanishes, the accepted regularity-free PR53 matching inequality forces the quartic coefficient to be at least `2 alpha_k`. In either case the displayed corrected entropy is locally concave.

## Files

- `complete_event_loop_C4.md`: exact atom factorization, trace-log expansion, derivative bounds, closed-walk thermodynamic limit, and `C^4` entropy-rate conclusion.
- `parity_matching_concavity.md`: mutual-information identity and the two-case curvature proof.
- `explicit_zero_positive_moment_family.md`: an `A_0` family lying in no `A_p`, `p>0`.
- `route_comparison_sources.md`: comparison with BFG/Fernandez--Maillard, Dobrushin, PR39, and the `H^1_F` route.
- `review_contract.md`: independent audit units and stop conditions.

## Evidence separation

- new theorem and lemmas: author proof in this branch;
- PR39 mean-one-half theorem and PR53 matching bound: separate accepted scoped inputs, used only where stated;
- PR82/PR106/`H^1_F` successors: not theorem premises;
- numerical or machine evidence: none;
- novelty: NOT_ASSESSED;
- independent review: PENDING_REVIEW until an issue is explicitly claimed.

No claim is made for arbitrary `A_0` centers violating (T.1), for a whole legal interval, for arbitrary measurable symbols, or for an entropy counterexample.