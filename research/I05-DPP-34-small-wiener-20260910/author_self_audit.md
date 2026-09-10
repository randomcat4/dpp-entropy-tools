# Reverse author audit of the complete-event loop proof

Status: **AUTHOR SELF-AUDIT / NOT AN INDEPENDENT REVIEW.**

This note checks the proof backwards from the curvature conclusion to the finite complete-event input. It adds explicit justifications at the three places most likely to hide an invalid interchange. It does not change the theorem statement or inherit any external verdict.

## 1. From local concavity back to `C^4`

The final argument uses only the following facts about

\[
J(t)=h(c)-h(c+t g):
\]

1. `J` is even and `C^4` on a real neighborhood of zero;
2. `J(0)=0` and `J(t)>=0`;
3. the accepted matching inequality gives `J(t)>=C_k t^4+O(t^6)`.

If `J''(0)>0`, continuity of `J''` proves the corrected curvature immediately. If `J''(0)=0`, even `C^4` Taylor expansion gives

\[
J(t)=\frac{J^{(4)}(0)}{24}t^4+o(t^4)
\]

and

\[
J''(t)=\frac{J^{(4)}(0)}2t^2+o(t^2).
\]

Thus no sixth derivative, analytic pressure, or finite-volume curvature limit is used.

## 2. Entropy/KL identity uses the full law

For every interval `Lambda_n`, the product reference `q_mu` has the same one-site marginals as the DPP. Therefore

\[
D(p_{n,t}\|q_{\mu,n})
=-H(p_{n,t})
-n\{\mu\log\mu+(1-\mu)\log(1-\mu)\}.
\]

This is an identity after summing every complete atom. The limit

\[
h(t)=h_{Ber}(\mu)-\lim_n n^{-1}D(p_{n,t}\|q_{\mu,n})
\]

is consequently the classical configuration entropy rate. The proof never replaces this KL by a spectral integral or by a selected-event statistic.

## 3. The nonnormal trace-log step

For a complete word `x`, put `X=B_xA_{Lambda,t}`. The matrix need not be normal. The required contraction follows from both absolute row and column sums:

\[
\|X\|_\infty\le R/\delta,
\qquad
\|X\|_1\le R/\delta.
\]

Hence

\[
\|X\|_{2\to2}
\le\sqrt{\|X\|_1\|X\|_\infty}
\le R/\delta=\rho<1.
\tag{3.1}
\]

Thus the operator-norm series

\[
\log(I+X)=\sum_{m\ge1}\frac{(-1)^{m+1}}mX^m
\]

converges even though `X` is nonnormal. Since the exact ratio

\[
\det(I+X)=p_{Lambda,t}(x)/q_{\mu,Lambda}(x)
\]

is positive for real `t`, the continued branch has real trace equal to the ordinary real logarithm of the likelihood ratio. The `m=1` trace is zero because `A_{Lambda,t}` has zero diagonal and `B_x` is diagonal.

## 4. Complete-event derivatives retain rare atoms

For the complete event on a distinct support `J`,

\[
p_{J,t}(x)=(-1)^{|Z_x|}\det M_{J,x}(t).
\]

The complete-event coercivity gives `||M^{-1}||<=delta_*^{-1}`. Jacobi/Bell differentiation has the exact form

\[
\partial_t^r p_{J,t}(x)
=p_{J,t}(x)\,\mathcal B_r(s_1,\ldots,s_r),
\]

up to the fixed complete-event sign already absorbed in `p`, where each trace variable satisfies `|s_j|<=C_j|J|`. Hence

\[
|\partial_t^r p_{J,t}(x)|
\le p_{J,t}(x)K_r|J|^r.
\]

The factor `p_{J,t}(x)`, rather than a uniform atom bound, is essential. For a bounded observable `F`, summing gives

\[
|\partial_t^r E_tF|
\le K_r|J|^r\sum_xp_{J,t}(x)|F(x)|
\le K_r|J|^r\|F\|_\infty.
\]

Thus arbitrarily rare complete events remain present and no factor `2^{|J|}` appears.

## 5. Repeated vertices in a trace walk

For a length-`m` closed walk `w=(i_1,\ldots,i_m)`, let `J(w)` be the set of distinct visited coordinates. The spin observable is

\[
F_w(X_{J(w)})
=\prod_{\ell=1}^m b_{X_{i_\ell}}.
\]

Repeated visits produce repeated powers of the same binary variable, but do not enlarge the support. Precisely,

\[
|J(w)|\le m,
\qquad
\|F_w\|_\infty\le\delta^{-m}.
\]

The complete-event derivative estimate is applied to the marginal law on the **distinct** set `J(w)`, with `F_w` as a fixed bounded function. Therefore the bound is

\[
|\partial_t^rE_tF_w|
\le K_r m^r\delta^{-m},
\]

including repeated vertices. No assumption that all walk vertices are distinct enters the proof.

Adjacent repeated vertices cause no separate term: `A_t(i,i)=0`, and `g_hat(0)=0`, so every edge factor and every derivative of such a zero-displacement edge vanishes.

## 6. Marked-edge summation

If exactly `ell` parameter derivatives hit the affine edge factors of a length-`m` walk, each marked edge contributes `|g_hat|` and each unmarked edge contributes `|a_t|`. After fixing the first vertex, extending the finite-volume sum to all integer displacements gives

\[
\sum_{i_2,\ldots,i_m}
\prod_{e\text{ marked}}|\widehat g(d_e)|
\prod_{e\text{ unmarked}}|a_t(d_e)|
\le r_g^{\ell}R^{m-\ell}.
\tag{6.1}
\]

This is the zero coefficient of a convolution and is bounded by the product of the `ell^1` norms. Assigning `ell` derivatives to distinct affine factors costs at most `m^ell` times a constant depending only on derivative order. Combining (6.1) with Section 5 gives the summable geometric majorant

\[
C_r m^{2r}\rho^{m-r},
\qquad \rho=R/\delta<1.
\]

## 7. Order of the thermodynamic and walk-length limits

For each fixed `m` and each fixed derivative order `r<=4`:

1. anchor `i_1`;
2. fix a displacement tuple;
3. use stationarity of the infinite DPP marginal to identify the local expectation independently of the anchor;
4. let the interval length tend to infinity, so the allowed-anchor fraction tends to one;
5. apply dominated convergence to the displacement sum using (6.1) and the local derivative bound.

Only after this fixed-`m` limit is obtained is the sum over `m` taken. The uniform majorant

\[
\sum_{m\ge2}m^{-1}C_rm^{2r}\rho^{m-r}<\infty
\]

permits the final interchange and proves uniform convergence through derivative order four. This order avoids an unjustified simultaneous boundary/walk-length limit.

## 8. Earliest-failure search

The reverse audit tested the following possible failure points:

- nonnormality of `B_xA_t`;
- complete-word sign in the Bernoulli factorization;
- loss of rare atoms under differentiation;
- repeated walk vertices;
- derivatives hitting the moving edge product;
- boundary anchors in the thermodynamic limit;
- an implicit sixth-order remainder.

No load-bearing failure was found. The theorem remains an author proof pending the independent review contract. The most sensitive independent audit units are the complete-event Bell bound and the fixed-`m` differentiated boundary limit.