# Smooth response to every finite order

Status: **PROVED AS AN AUTHOR COROLLARY / PENDING REVIEW.**

The local concavity theorem needs only four derivatives. The complete-event loop argument in fact gives every finite derivative order under the same unweighted small-Wiener hypothesis.

## Corollary

Under the hypotheses of the main theorem, choose `tau>0` with

\[
R=r_c+\tau r_g<\delta:=\min\{\mu,1-\mu\}.
\]

Then the true stationary DPP configuration Shannon entropy rate

\[
t\longmapsto h(c+t g)
\]

belongs to `C^infinity((-tau,tau))`. For each fixed integer `r>=0`, the derivatives of normalized finite-volume entropies converge locally uniformly through order `r` to the corresponding derivative of the entropy rate.

No claim of complex analyticity or a uniform-in-`r` radius is made.

## 1. Complete-event differentiation at arbitrary fixed order

For a complete word on a distinct support `J`, write

\[
M_{J,x}(t)=T_J(c+t g)-I_{Z_x},
\qquad G_J=T_J(g).
\]

The real interval has the common coercive inverse bound

\[
\|M_{J,x}(t)^{-1}\|_{2\to2}
\le\delta_*^{-1},
\qquad
\delta_*=\delta-R>0.
\tag{1.1}
\]

For every `j>=1`, the `j`-th logarithmic determinant derivative is a constant multiple of

\[
\operatorname{Tr}(M^{-1}G_J)^j,
\]

and therefore has absolute value at most

\[
(j-1)!\,|J|(r_g/\delta_*)^j.
\tag{1.2}
\]

For an arbitrary but fixed `r`, the complete Bell polynomial formula consequently gives

\[
\boxed{
|\partial_t^r p_{J,t}(x)|
\le p_{J,t}(x)K_r|J|^rC_*^r,}
\tag{1.3}
\]

where `K_r<infinity` depends on `r` but not on `J,x,t`. Positivity of the real complete atom is used only to retain the factor `p_{J,t}(x)` under absolute values.

For every bounded local observable `F` on `J`, summation over the full complete law yields

\[
|\partial_t^rE_tF|
\le K_r|J|^rC_*^r\|F\|_\infty.
\tag{1.4}
\]

Thus the rare-atom cancellation used at orders zero through four persists at every fixed finite order.

## 2. Arbitrary-order closed-walk majorant

For a length-`m` trace walk, split the `r` derivatives between the affine edge product and the local spin expectation. If `ell` derivatives hit edges, then `ell<=min(r,m)` and the number of assignments is at most `m^ell` times a constant depending only on `r`. The anchored absolute edge sum is

\[
r_g^\ell R^{m-\ell}.
\tag{2.1}
\]

The remaining `r-ell` derivatives of the local spin expectation are bounded by (1.4), with support size at most `m` and observable norm at most `delta^{-m}`. Therefore, for every fixed `r`, the normalized length-`m` coefficient obeys

\[
\sup_{\Lambda,|t|\le\tau'}
|\partial_t^r C_{m,\Lambda}(t)|
\le B_r m^{2r}\rho^{m-r},
\qquad
\rho=R/\delta<1,
\tag{2.2}
\]

on every closed subinterval `[-tau',tau'] subset (-tau,tau)`. Finitely many indices `m<r` are absorbed into `B_r`.

For each fixed `r`,

\[
\sum_{m\ge2}\frac1m
B_rm^{2r}\rho^{m-r}<\infty.
\tag{2.3}
\]

## 3. Thermodynamic passage

At fixed walk length `m`, derivative order `r`, and displacement tuple, DPP restriction consistency identifies the local complete-event expectation with the infinite stationary marginal. The allowed-anchor proportion tends to one. Equation (2.2) provides a displacement-summable and then length-summable majorant.

Dominated convergence first in the spatial displacement tuple and then in `m` gives local uniform convergence of the normalized KL derivatives at order `r`. Repeating this for all orders up to a fixed `r` and using the standard finite-order differentiation theorem proves

\[
h\in C^r((-\tau,\tau)).
\]

Since `r` was arbitrary,

\[
\boxed{h\in C^\infty((-\tau,\tau)).}
\tag{3.1}
\]

## 4. Why analyticity is not asserted

The constants in (1.3) contain Bell-polynomial/factorial growth, while summing `m^{2r}\rho^m` can introduce additional factorial growth in `r`. The present estimates are sufficient for every fixed derivative order but do not provide a bound of the form

\[
\|h^{(r)}\|\le C R_0^{-r}r!
\]

with one positive `R_0`. Therefore this corollary states smoothness, not real or complex analyticity.

This distinction is material: the theorem bypasses the invalid Dobrushin analytic-pressure import and does not silently recreate it under a weaker hypothesis.