# Complete-event loop expansion and `C^4` entropy rate

Status: **AUTHOR PROOF / PENDING REVIEW**.

This file proves parameter regularity of the true stationary DPP configuration entropy rate under the unweighted small-Wiener condition. The proof is finite-volume first, keeps the full complete-event law, and passes to the thermodynamic limit with a differentiated closed-walk majorant.

## 1. Uniform smallness interval and spectral margin

Let

\[
\mu=\widehat c(0),
\qquad
\delta=\min\{\mu,1-\mu\},
\qquad
r_c=\sum_{m\ne0}|\widehat c(m)|<\delta.
\]

Since `g` is half-period odd, `\widehat g(0)=0`. Put

\[
r_g=\sum_m|\widehat g(m)|.
\]

Choose `tau>0` so that

\[
R:=r_c+\tau r_g<\delta.
\tag{1.1}
\]

For `|t|<=tau`, write

\[
f_t=c+t g,
\qquad
a_t(0)=0,
\qquad
a_t(m)=\widehat f_t(m)\quad(m\ne0).
\tag{1.2}
\]

Then

\[
\|a_t\|_{\ell^1}\le R
\tag{1.3}
\]

and pointwise

\[
\mu-R\le f_t(\theta)\le\mu+R.
\]

Thus every real kernel has the strict spectral margin

\[
\delta_*:=\delta-R>0,
\qquad
\delta_*I\le T_\Lambda(f_t)
\le(1-\delta_*)I
\tag{1.4}
\]

for every finite coordinate set `Lambda`.

## 2. Exact factorization of every complete atom

Fix a finite nonempty `Lambda subset Z` and a complete word `x in {0,1}^Lambda`. Let

\[
S_x=\{i:x_i=1\},
\qquad
Z_x=\Lambda\setminus S_x.
\]

The full atom probability is

\[
p_{\Lambda,t}(x)
=(-1)^{|Z_x|}
\det\bigl(T_\Lambda(f_t)-I_{Z_x}\bigr).
\tag{2.1}
\]

Set

\[
A_{\Lambda,t}=T_\Lambda(f_t)-\mu I,
\tag{2.2}
\]

and define the diagonal matrices

\[
D_x(i,i)=
\begin{cases}
\mu,&x_i=1,\\
\mu-1,&x_i=0,
\end{cases}
\qquad
B_x=D_x^{-1}.
\tag{2.3}
\]

Since `A_{Lambda,t}` has zero diagonal,

\[
T_\Lambda(f_t)-I_{Z_x}=D_x+A_{\Lambda,t}.
\]

Moreover

\[
(-1)^{|Z_x|}\det D_x
=\mu^{|S_x|}(1-\mu)^{|Z_x|}
=:q_{\mu,\Lambda}(x),
\tag{2.4}
\]

the complete atom of the product Bernoulli law of mean `mu`. Therefore

\[
\boxed{
p_{\Lambda,t}(x)
=q_{\mu,\Lambda}(x)
\det(I+B_xA_{\Lambda,t}).}
\tag{2.5}
\]

This identity includes every occupied/vacant pattern. It is not an inclusion-probability formula.

The absolute row and column sums of `A_{Lambda,t}` are at most `R`, while `||B_x||<=delta^{-1}`. Consequently

\[
\|B_xA_{\Lambda,t}\|_{2\to2}
\le\|B_xA_{\Lambda,t}\|_{\rm Schur}
\le\rho:=R/\delta<1
\tag{2.6}
\]

uniformly in `Lambda`, `x`, and real `|t|<=tau`.

## 3. Uniform trace-log expansion

The path `z -> I+zB_xA_{Lambda,t}`, `0<=z<=1`, stays invertible by (2.6). The logarithm branch continuing from the identity therefore gives

\[
\log\det(I+B_xA_{\Lambda,t})
=\sum_{m\ge1}\frac{(-1)^{m+1}}m
\operatorname{Tr}(B_xA_{\Lambda,t})^m.
\tag{3.1}
\]

The first term vanishes because `A_{Lambda,t}` has zero diagonal:

\[
\operatorname{Tr}(B_xA_{\Lambda,t})=0.
\tag{3.2}
\]

Also

\[
\left|\operatorname{Tr}(B_xA_{\Lambda,t})^m\right|
\le|\Lambda|\rho^m.
\tag{3.3}
\]

Thus the series in (3.1), beginning at `m=2`, converges absolutely with one bound independent of every complete word and of the volume.

Let

\[
D_\Lambda(t)
=D\bigl(p_{\Lambda,t}\|q_{\mu,\Lambda}\bigr).
\]

Using (2.5) and Tonelli/dominated convergence,

\[
\frac{D_\Lambda(t)}{|\Lambda|}
=\sum_{m\ge2}\frac{(-1)^{m+1}}m
C_{m,\Lambda}(t),
\tag{3.4}
\]

where

\[
C_{m,\Lambda}(t)
:=\frac1{|\Lambda|}
\mathbf E_t
\operatorname{Tr}(B_XA_{\Lambda,t})^m.
\tag{3.5}
\]

Here `E_t` is expectation under the full complete-event law (2.1). No event or acceleration term has been removed.

## 4. Derivatives of finite complete-event expectations

The differentiated thermodynamic limit needs a bound that does not pay `2^{|J|}` for a local support `J`.

Let `J` be a finite coordinate set of size `d`, and let `F:{0,1}^J -> C` be bounded and independent of `t`. Put

\[
M_{J,x}(t)=T_J(f_t)-I_{Z_x},
\qquad
G_J=T_J(g).
\]

The complete-event coercivity argument gives

\[
\|M_{J,x}(t)^{-1}\|_{2\to2}
\le\delta_*^{-1}
\tag{4.1}
\]

for every real `|t|<=tau`, every `J`, and every word `x`.

For `j>=1`, define

\[
s_j(t)=(-1)^{j-1}(j-1)!
\operatorname{Tr}(M_{J,x}(t)^{-1}G_J)^j.
\tag{4.2}
\]

Jacobi's formula and its iterates give

\[
\partial_t^r\det M_{J,x}(t)
=\det M_{J,x}(t)
\mathcal B_r(s_1,\ldots,s_r),
\tag{4.3}
\]

where `B_r` is the complete exponential Bell polynomial. Since

\[
\|G_J\|_{2\to2}
\le\|g\|_\infty\le r_g,
\]

one has

\[
|s_j(t)|
\le(j-1)!\,d\,(r_g/\delta_*)^j.
\tag{4.4}
\]

For each fixed `r<=4`, every monomial in `B_r` contains at most `r` trace factors and total derivative weight `r`. Hence

\[
\left|\partial_t^r p_{J,t}(x)\right|
\le p_{J,t}(x)
K_r d^r(1+r_g/\delta_*)^r,
\tag{4.5}
\]

with a constant `K_r` independent of `J,x,t`. The sign in the atom determinant is constant and disappears under absolute values.

Summing (4.5) against `|F(x)|` uses `sum_x p_{J,t}(x)=1`, not a count of words. Therefore

\[
\boxed{
\left|\partial_t^r\mathbf E_tF(X_J)\right|
\le K_r d^r(1+r_g/\delta_*)^r
\|F\|_\infty,
\qquad0\le r\le4.}
\tag{4.6}
\]

This is the key complete-event derivative bound. The probability factor in (4.5) retains the full Fisher/score contribution of rare atoms while preventing an artificial exponential support loss.

## 5. Closed-walk expansion and differentiated majorant

Expand the trace in (3.5):

\[
\operatorname{Tr}(B_XA_t)^m
=\sum_{i_1,\ldots,i_m\in\Lambda}
\left(\prod_{\ell=1}^m
b_{X_{i_\ell}}\right)
\left(\prod_{\ell=1}^m
 a_t(i_\ell-i_{\ell+1})\right),
\tag{5.1}
\]

with `i_{m+1}=i_1` and

\[
b_1=1/\mu,
\qquad
b_0=-1/(1-\mu).
\tag{5.2}
\]

For each walk `w=(i_1,...,i_m)`, its spin observable

\[
F_w(X)=\prod_{\ell=1}^m b_{X_{i_\ell}}
\tag{5.3}
\]

depends only on the set `J(w)` of visited vertices, whose size is at most `m`, and

\[
\|F_w\|_\infty\le\delta^{-m}.
\tag{5.4}
\]

Differentiate (5.1) `r<=4` times. If `ell` derivatives fall on the affine edge product, there are at most `m^ell` assignments, and the anchored absolute walk sum is bounded by

\[
r_g^\ell R^{m-\ell}.
\tag{5.5}
\]

Indeed it is the value at zero of a convolution of `ell` copies of `|\widehat g|` and `m-ell` copies of `|a_t|`, and this is at most the product of their `ell^1` norms.

The remaining `r-ell` derivatives fall on the local expectation of `F_w`. Equations (4.6) and (5.4), with `d<=m`, bound them by

\[
K_{r-\ell}m^{r-\ell}
(1+r_g/\delta_*)^{r-\ell}\delta^{-m}.
\tag{5.6}
\]

Leibniz' rule, (5.5), and (5.6) therefore give, for each fixed `0<=r<=4`,

\[
\sup_{\Lambda,|t|\le\tau}
|\partial_t^r C_{m,\Lambda}(t)|
\le A_r m^{2r}
\sum_{\ell=0}^{\min(r,m)}
 r_g^\ell R^{m-\ell}\delta^{-m}.
\tag{5.7}
\]

Since `rho=R/delta<1`, the right side is bounded by

\[
\boxed{
B_r m^{2r}\rho^{m-r}}
\tag{5.8}
\]

with a finite constant depending on `r,delta,delta_*,R,r_g` but not on `m,Lambda,t`. Finitely many indices `m<r` are absorbed into `B_r`.

Thus

\[
\sum_{m\ge2}\frac1m
\sup_{\Lambda,|t|\le\tau}
|\partial_t^r C_{m,\Lambda}(t)|<\infty,
\qquad0\le r\le4.
\tag{5.9}
\]

## 6. Thermodynamic limit of each differentiated walk coefficient

Take `Lambda_n={1,...,n}`. The DPP on `Lambda_n` is the restriction of the infinite stationary DPP, so the expectation associated with any fixed translated finite walk support is exactly the corresponding infinite-process expectation.

Anchor `i_1` in (5.1) and record the displacement tuple

\[
(i_2-i_1,\ldots,i_m-i_1).
\]

For every fixed tuple, the fraction of anchors for which all visited sites remain in `Lambda_n` tends to one. Each parameter derivative of its local expectation is translation invariant. The absolute anchored sums are dominated by (5.7). Dominated convergence therefore yields, uniformly in `|t|<=tau`, limits

\[
C_m^{(r)}(t)
:=\lim_{n\to\infty}
\partial_t^r C_{m,\Lambda_n}(t),
\qquad0\le r\le4.
\tag{6.1}
\]

The usual finite-order uniform-convergence theorem then shows that `C_m` is `C^4` and that the displayed limits are its derivatives.

Now (5.9) permits summation in `m`. Define

\[
d(t)=
\sum_{m\ge2}\frac{(-1)^{m+1}}m C_m(t).
\tag{6.2}
\]

Then

\[
\lim_{n\to\infty}
\frac1nD_{\Lambda_n}(t)=d(t)
\tag{6.3}
\]

uniformly, and

\[
\boxed{d\in C^4([ -\tau,\tau]).}
\tag{6.4}
\]

All four derivatives are the limits of the full finite-volume derivatives; the Fisher square and atom-acceleration terms are not separately discarded.

## 7. Identification with the true entropy rate

Every one-site marginal of the stationary DPP has mean `mu`. Hence

\[
\begin{aligned}
D_{\Lambda_n}(t)
&=\sum_xp_{\Lambda_n,t}(x)
\log\frac{p_{\Lambda_n,t}(x)}{q_{\mu,\Lambda_n}(x)}\\
&=-H_{\Lambda_n}(t)
+n\bigl[-\mu\log\mu-(1-\mu)\log(1-\mu)\bigr].
\end{aligned}
\tag{7.1}
\]

Therefore

\[
\frac1nH_{\Lambda_n}(t)
=h_{\rm Ber}(\mu)-\frac1nD_{\Lambda_n}(t).
\tag{7.2}
\]

The left side converges to the stationary configuration Shannon entropy rate, while (6.3) identifies the right limit. Thus

\[
\boxed{
h(c+t g)=h_{\rm Ber}(\mu)-d(t),
\qquad h\in C^4([-\tau,\tau]).}
\tag{7.3}
\]

This is a true classical configuration-entropy identity for the physical affine kernel. It is not the scalar spectral entropy integral.